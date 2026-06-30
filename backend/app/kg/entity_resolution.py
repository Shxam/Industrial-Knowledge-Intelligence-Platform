"""
Entity resolution and deduplication
Handles fuzzy matching and canonicalization of entities
"""
from typing import List, Dict, Any, Tuple, Set
from difflib import SequenceMatcher
import re

from app.core.logging import logger


class EntityResolver:
    """
    Resolve and deduplicate entities
    
    Handles:
    - Fuzzy matching (P-101 = Pump 101 = P101)
    - Canonicalization (standardize format)
    - Deduplication
    - Entity merging
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize entity resolver
        
        Args:
            similarity_threshold: Minimum similarity for matching (0.0-1.0)
        """
        self.similarity_threshold = similarity_threshold
        self.canonical_forms = {}  # Maps variants to canonical form
    
    def normalize_equipment_tag(self, text: str) -> str:
        """
        Normalize equipment tag to standard format
        
        Examples:
        - "P-101" -> "P-101"
        - "Pump 101" -> "P-101"
        - "P101" -> "P-101"
        - "pump-101" -> "P-101"
        """
        text = text.strip().upper()
        
        # Handle "Equipment Name NNN" format
        equipment_types = {
            'PUMP': 'P',
            'TANK': 'TK',
            'VALVE': 'V',
            'COMPRESSOR': 'C',
            'MOTOR': 'M',
            'HEAT EXCHANGER': 'HX',
            'HX': 'HX',
            'REACTOR': 'R',
            'VESSEL': 'V'
        }
        
        for full_name, abbrev in equipment_types.items():
            pattern = rf'\b{full_name}\s+(\d{{2,4}}[A-Z]?)\b'
            match = re.search(pattern, text)
            if match:
                return f"{abbrev}-{match.group(1)}"
        
        # Handle "X-NNN" or "XNNN" format
        match = re.match(r'([A-Z]{1,4})-?(\d{2,4}[A-Z]?)', text)
        if match:
            prefix, number = match.groups()
            return f"{prefix}-{number}"
        
        # Return as-is if no pattern matched
        return text
    
    def normalize_parameter(self, text: str) -> str:
        """
        Normalize parameter names
        
        Examples:
        - "Temperature" -> "temperature"
        - "temp" -> "temperature"
        - "Flow Rate" -> "flow_rate"
        """
        text = text.lower().strip()
        
        # Map common abbreviations to full names
        abbreviations = {
            'temp': 'temperature',
            'pres': 'pressure',
            'ph': 'ph',
            'rpm': 'rpm'
        }
        
        if text in abbreviations:
            return abbreviations[text]
        
        # Replace spaces with underscores
        return text.replace(' ', '_')
    
    def normalize_regulation(self, text: str) -> str:
        """
        Normalize regulation references
        
        Examples:
        - "OISD STD 105" -> "OISD-STD-105"
        - "oisd-105" -> "OISD-STD-105"
        - "IS 2825" -> "IS-2825"
        """
        text = text.upper().strip()
        
        # OISD standards
        match = re.match(r'OISD[\s-]*(STD)?[\s-]*(\d+)', text)
        if match:
            number = match.group(2)
            return f"OISD-STD-{number}"
        
        # IS/ISO standards
        match = re.match(r'(IS|ISO)[\s-]*(\d+)', text)
        if match:
            standard, number = match.groups()
            return f"{standard}-{number}"
        
        return text
    
    def normalize_entity(self, text: str, entity_type: str) -> str:
        """
        Normalize entity based on type
        
        Args:
            text: Entity text
            entity_type: Entity type
        
        Returns:
            Normalized text
        """
        if entity_type == 'EQUIPMENT':
            return self.normalize_equipment_tag(text)
        elif entity_type == 'PARAMETER':
            return self.normalize_parameter(text)
        elif entity_type == 'REGULATION':
            return self.normalize_regulation(text)
        else:
            # Default: lowercase and strip
            return text.lower().strip()
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two strings
        
        Uses SequenceMatcher for fuzzy matching
        
        Returns:
            Similarity score (0.0-1.0)
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def find_canonical_form(
        self,
        entity: Dict[str, Any],
        existing_entities: List[Dict[str, Any]]
    ) -> Tuple[str, float]:
        """
        Find canonical form of entity from existing entities
        
        Args:
            entity: Entity to resolve
            existing_entities: List of existing entities to match against
        
        Returns:
            Tuple of (canonical_id, confidence)
        """
        entity_text = entity['text']
        entity_type = entity['type']
        
        # Normalize the entity
        normalized = self.normalize_entity(entity_text, entity_type)
        
        # Find best match in existing entities
        best_match = None
        best_score = 0.0
        
        for existing in existing_entities:
            if existing['type'] != entity_type:
                continue
            
            existing_normalized = self.normalize_entity(
                existing['text'],
                existing['type']
            )
            
            # Exact match after normalization
            if normalized == existing_normalized:
                return existing['entity_id'], 1.0
            
            # Fuzzy match
            score = self.calculate_similarity(normalized, existing_normalized)
            if score > best_score:
                best_score = score
                best_match = existing
        
        # Return match if above threshold
        if best_match and best_score >= self.similarity_threshold:
            return best_match['entity_id'], best_score
        
        # No match found - this is a new entity
        return None, 0.0
    
    def resolve_entities(
        self,
        entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Resolve entities within a single document/chunk
        
        Handles deduplication within the same context
        
        Args:
            entities: List of extracted entities
        
        Returns:
            Deduplicated list with canonical forms
        """
        if not entities:
            return []
        
        logger.info(f"Resolving {len(entities)} entities")
        
        resolved = []
        seen = {}  # Maps normalized text to first occurrence
        
        for entity in entities:
            entity_type = entity['type']
            text = entity['text']
            
            # Normalize
            normalized = self.normalize_entity(text, entity_type)
            key = (entity_type, normalized)
            
            if key in seen:
                # Duplicate - update the canonical form
                canonical = seen[key]
                entity['canonical_text'] = canonical['canonical_text']
                entity['is_duplicate'] = True
                entity['canonical_id'] = canonical['entity_id']
            else:
                # First occurrence
                entity['canonical_text'] = normalized
                entity['is_duplicate'] = False
                seen[key] = entity
                resolved.append(entity)
        
        logger.info(f"Resolved to {len(resolved)} unique entities")
        return resolved
    
    def merge_entities(
        self,
        entity1: Dict[str, Any],
        entity2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge two entities that refer to the same thing
        
        Keeps the most complete information
        """
        merged = entity1.copy()
        
        # Use the canonical text (usually the more standard form)
        if 'canonical_text' in entity2:
            merged['canonical_text'] = entity2['canonical_text']
        
        # Merge metadata
        if 'metadata' in entity2:
            merged_metadata = merged.get('metadata', {})
            merged_metadata.update(entity2['metadata'])
            merged['metadata'] = merged_metadata
        
        # Keep highest confidence
        merged['confidence'] = max(
            entity1.get('confidence', 0),
            entity2.get('confidence', 0)
        )
        
        # Track merge history
        aliases = merged.get('aliases', [])
        aliases.append(entity2['text'])
        if 'aliases' in entity2:
            aliases.extend(entity2['aliases'])
        merged['aliases'] = list(set(aliases))
        
        return merged
    
    def build_equivalence_classes(
        self,
        entities: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """
        Build equivalence classes of entities
        
        Groups entities that refer to the same real-world object
        
        Returns:
            Dict mapping canonical_id to list of variant ids
        """
        equivalence = {}
        
        for entity in entities:
            canonical_id = entity.get('canonical_id', entity['entity_id'])
            entity_id = entity['entity_id']
            
            if canonical_id not in equivalence:
                equivalence[canonical_id] = []
            
            if entity_id != canonical_id:
                equivalence[canonical_id].append(entity_id)
        
        return equivalence
    
    def create_resolution_report(
        self,
        original_count: int,
        resolved_count: int,
        equivalence_classes: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Create a report of entity resolution
        
        Useful for debugging and validation
        """
        return {
            'original_count': original_count,
            'resolved_count': resolved_count,
            'deduplication_rate': 1 - (resolved_count / original_count) if original_count > 0 else 0,
            'equivalence_classes': len(equivalence_classes),
            'largest_class_size': max(
                [len(v) for v in equivalence_classes.values()],
                default=0
            )
        }


# Global entity resolver
entity_resolver = EntityResolver()
