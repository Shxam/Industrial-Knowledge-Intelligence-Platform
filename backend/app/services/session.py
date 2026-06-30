"""
Session management for conversation memory
Uses Redis for persistence
"""
import redis
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.logging import logger


class Message:
    """Conversation message"""
    def __init__(
        self,
        role: str,
        content: str,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            role=data['role'],
            content=data['content'],
            timestamp=data.get('timestamp'),
            metadata=data.get('metadata', {})
        )


class ConversationSession:
    """
    Manage conversation history with context window
    
    Features:
    - Redis-based persistence
    - Context window management
    - Message history
    - Session metadata
    """
    
    def __init__(
        self,
        session_id: Optional[str] = None,
        max_history: int = 10,
        ttl_hours: int = 24
    ):
        """
        Initialize conversation session
        
        Args:
            session_id: Session ID (creates new if None)
            max_history: Maximum messages to keep in context
            ttl_hours: Session expiration time in hours
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.max_history = max_history
        self.ttl_seconds = ttl_hours * 3600
        
        # Initialize Redis client
        try:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            logger.info(f"Connected to Redis for session {self.session_id}")
        except Exception as e:
            logger.warning(f"Redis unavailable, using in-memory storage: {e}")
            self.redis_client = None
            self._memory_storage = []
    
    def _get_key(self, suffix: str = "") -> str:
        """Get Redis key for session"""
        key = f"session:{self.session_id}"
        if suffix:
            key += f":{suffix}"
        return key
    
    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add message to conversation history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata (citations, scores, etc.)
        """
        message = Message(role, content, metadata=metadata)
        
        if self.redis_client:
            # Store in Redis
            try:
                messages_key = self._get_key("messages")
                
                # Get current messages
                messages_data = self.redis_client.get(messages_key)
                if messages_data:
                    messages = json.loads(messages_data)
                else:
                    messages = []
                
                # Add new message
                messages.append(message.to_dict())
                
                # Trim to max history
                if len(messages) > self.max_history * 2:  # 2x because user+assistant pairs
                    messages = messages[-(self.max_history * 2):]
                
                # Save back
                self.redis_client.setex(
                    messages_key,
                    self.ttl_seconds,
                    json.dumps(messages)
                )
                
                # Update last activity
                self._update_last_activity()
                
                logger.debug(f"Added {role} message to session {self.session_id}")
                
            except Exception as e:
                logger.error(f"Error storing message in Redis: {e}")
        else:
            # In-memory fallback
            self._memory_storage.append(message.to_dict())
            if len(self._memory_storage) > self.max_history * 2:
                self._memory_storage = self._memory_storage[-(self.max_history * 2):]
    
    def get_history(
        self,
        limit: Optional[int] = None
    ) -> List[Message]:
        """
        Get conversation history
        
        Args:
            limit: Number of recent messages to return (None = all)
        
        Returns:
            List of Message objects
        """
        if self.redis_client:
            try:
                messages_key = self._get_key("messages")
                messages_data = self.redis_client.get(messages_key)
                
                if messages_data:
                    messages_dicts = json.loads(messages_data)
                    messages = [Message.from_dict(m) for m in messages_dicts]
                else:
                    messages = []
                
            except Exception as e:
                logger.error(f"Error retrieving history from Redis: {e}")
                messages = []
        else:
            # In-memory fallback
            messages = [Message.from_dict(m) for m in self._memory_storage]
        
        # Apply limit
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def get_context_for_llm(
        self,
        include_system_prompt: bool = True
    ) -> List[Dict[str, str]]:
        """
        Get conversation history formatted for LLM
        
        Returns list of message dicts with 'role' and 'content'
        """
        messages = []
        
        if include_system_prompt:
            messages.append({
                'role': 'system',
                'content': 'You are a helpful AI assistant for industrial documentation.'
            })
        
        history = self.get_history()
        for msg in history:
            messages.append({
                'role': msg.role,
                'content': msg.content
            })
        
        return messages
    
    def clear_history(self):
        """Clear conversation history"""
        if self.redis_client:
            try:
                messages_key = self._get_key("messages")
                self.redis_client.delete(messages_key)
                logger.info(f"Cleared history for session {self.session_id}")
            except Exception as e:
                logger.error(f"Error clearing history: {e}")
        else:
            self._memory_storage = []
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get session metadata"""
        if self.redis_client:
            try:
                meta_key = self._get_key("metadata")
                meta_data = self.redis_client.get(meta_key)
                if meta_data:
                    return json.loads(meta_data)
            except Exception as e:
                logger.error(f"Error getting metadata: {e}")
        
        return {
            'session_id': self.session_id,
            'message_count': len(self.get_history()),
            'created_at': None,
            'last_activity': None
        }
    
    def set_metadata(self, metadata: Dict[str, Any]):
        """Set session metadata"""
        if self.redis_client:
            try:
                meta_key = self._get_key("metadata")
                self.redis_client.setex(
                    meta_key,
                    self.ttl_seconds,
                    json.dumps(metadata)
                )
            except Exception as e:
                logger.error(f"Error setting metadata: {e}")
    
    def _update_last_activity(self):
        """Update last activity timestamp"""
        metadata = self.get_metadata()
        if not metadata.get('created_at'):
            metadata['created_at'] = datetime.utcnow().isoformat()
        metadata['last_activity'] = datetime.utcnow().isoformat()
        self.set_metadata(metadata)
    
    def is_expired(self) -> bool:
        """Check if session has expired"""
        metadata = self.get_metadata()
        if not metadata.get('last_activity'):
            return False
        
        last_activity = datetime.fromisoformat(metadata['last_activity'])
        age = datetime.utcnow() - last_activity
        return age.total_seconds() > self.ttl_seconds
    
    def extend_ttl(self):
        """Extend session TTL"""
        if self.redis_client:
            try:
                for suffix in ['messages', 'metadata']:
                    key = self._get_key(suffix)
                    self.redis_client.expire(key, self.ttl_seconds)
                logger.debug(f"Extended TTL for session {self.session_id}")
            except Exception as e:
                logger.error(f"Error extending TTL: {e}")


class SessionManager:
    """Manage multiple conversation sessions"""
    
    def __init__(self):
        self.sessions = {}  # In-memory cache
    
    def create_session(
        self,
        user_id: Optional[str] = None,
        max_history: int = 10
    ) -> ConversationSession:
        """Create new conversation session"""
        session = ConversationSession(max_history=max_history)
        self.sessions[session.session_id] = session
        
        if user_id:
            metadata = session.get_metadata()
            metadata['user_id'] = user_id
            session.set_metadata(metadata)
        
        logger.info(f"Created session {session.session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Get existing session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
        else:
            # Try to load from Redis
            session = ConversationSession(session_id=session_id)
            if not session.is_expired():
                self.sessions[session_id] = session
            else:
                return None
        
        return session
    
    def delete_session(self, session_id: str):
        """Delete session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.clear_history()
            del self.sessions[session_id]
            logger.info(f"Deleted session {session_id}")


# Global session manager
session_manager = SessionManager()
