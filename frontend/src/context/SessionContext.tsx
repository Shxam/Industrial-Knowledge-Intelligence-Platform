import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Array<{
    text: string;
    source: string;
    score: number;
  }>;
  timestamp: number;
}

interface Session {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
}

interface SessionContextType {
  sessions: Session[];
  currentSession: Session | null;
  createSession: (title?: string) => Session;
  switchSession: (sessionId: string) => void;
  deleteSession: (sessionId: string) => void;
  addMessage: (message: Message) => void;
  updateSessionTitle: (sessionId: string, title: string) => void;
  clearCurrentSession: () => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

const STORAGE_KEY = 'ikip_sessions';
const CURRENT_SESSION_KEY = 'ikip_current_session';

export function SessionProvider({ children }: { children: ReactNode }) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);

  // Load sessions from localStorage on mount
  useEffect(() => {
    const savedSessions = localStorage.getItem(STORAGE_KEY);
    const savedCurrentSessionId = localStorage.getItem(CURRENT_SESSION_KEY);
    
    if (savedSessions) {
      const parsedSessions = JSON.parse(savedSessions);
      setSessions(parsedSessions);
      
      if (savedCurrentSessionId) {
        const current = parsedSessions.find((s: Session) => s.id === savedCurrentSessionId);
        if (current) {
          setCurrentSession(current);
        } else if (parsedSessions.length > 0) {
          setCurrentSession(parsedSessions[0]);
        }
      } else if (parsedSessions.length > 0) {
        setCurrentSession(parsedSessions[0]);
      }
    } else {
      // Create initial session
      const initialSession = createInitialSession();
      setSessions([initialSession]);
      setCurrentSession(initialSession);
    }
  }, []);

  // Save sessions to localStorage whenever they change
  useEffect(() => {
    if (sessions.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
    }
  }, [sessions]);

  // Save current session ID
  useEffect(() => {
    if (currentSession) {
      localStorage.setItem(CURRENT_SESSION_KEY, currentSession.id);
    }
  }, [currentSession]);

  const createInitialSession = (): Session => {
    return {
      id: generateId(),
      title: 'New Chat',
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
  };

  const generateId = () => {
    return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  const createSession = (title?: string): Session => {
    const newSession: Session = {
      id: generateId(),
      title: title || 'New Chat',
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    
    setSessions((prev) => [newSession, ...prev]);
    setCurrentSession(newSession);
    return newSession;
  };

  const switchSession = (sessionId: string) => {
    const session = sessions.find((s) => s.id === sessionId);
    if (session) {
      setCurrentSession(session);
    }
  };

  const deleteSession = (sessionId: string) => {
    setSessions((prev) => {
      const filtered = prev.filter((s) => s.id !== sessionId);
      
      // If we deleted the current session, switch to another or create new
      if (currentSession?.id === sessionId) {
        if (filtered.length > 0) {
          setCurrentSession(filtered[0]);
        } else {
          const newSession = createInitialSession();
          return [newSession];
        }
      }
      
      return filtered;
    });
  };

  const addMessage = (message: Message) => {
    if (!currentSession) return;

    setSessions((prev) =>
      prev.map((session) =>
        session.id === currentSession.id
          ? {
              ...session,
              messages: [...session.messages, message],
              updatedAt: Date.now(),
              // Auto-generate title from first user message
              title:
                session.messages.length === 0 && message.role === 'user'
                  ? message.content.slice(0, 50) + (message.content.length > 50 ? '...' : '')
                  : session.title,
            }
          : session
      )
    );

    setCurrentSession((prev) =>
      prev
        ? {
            ...prev,
            messages: [...prev.messages, message],
            updatedAt: Date.now(),
            title:
              prev.messages.length === 0 && message.role === 'user'
                ? message.content.slice(0, 50) + (message.content.length > 50 ? '...' : '')
                : prev.title,
          }
        : null
    );
  };

  const updateSessionTitle = (sessionId: string, title: string) => {
    setSessions((prev) =>
      prev.map((session) =>
        session.id === sessionId
          ? { ...session, title, updatedAt: Date.now() }
          : session
      )
    );

    if (currentSession?.id === sessionId) {
      setCurrentSession((prev) => (prev ? { ...prev, title, updatedAt: Date.now() } : null));
    }
  };

  const clearCurrentSession = () => {
    if (!currentSession) return;

    setSessions((prev) =>
      prev.map((session) =>
        session.id === currentSession.id
          ? { ...session, messages: [], updatedAt: Date.now() }
          : session
      )
    );

    setCurrentSession((prev) => (prev ? { ...prev, messages: [], updatedAt: Date.now() } : null));
  };

  return (
    <SessionContext.Provider
      value={{
        sessions,
        currentSession,
        createSession,
        switchSession,
        deleteSession,
        addMessage,
        updateSessionTitle,
        clearCurrentSession,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export function useSession() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
}
