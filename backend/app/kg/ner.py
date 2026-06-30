"""
Named Entity Recognition for industrial documents
Extracts equipment tags, parameters, regulations, personnel, dates, failure modes
"""
import spacy
import re
from typing import List, Dict, Any, Tuple
from datetime import datetime

from app.core.logging import logger


class Entity:
    """Represents an extracted entity"""
    def __init__(
        self,
        text: str,
        entity_type: str,
        start: int,
        end: int,
        confidence: float = 1.0,
        metadata: Dict[str, Any] = None
    ):
        self.text = text
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.confidence = confidence
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'type': self.entity_type,
            'start': self.start,
            'end': self.end,
            'confidence': self.confidence,
            'metadata': self.metadata
        }


class IndustrialNER:
    """
    NER for industrial documents
    
    Entity types:
    - EQUIPMENT: Equipment tags (P-101, TK-205, V-301)
    - PARAMETER: Process parameters (temperature, pressure, flow)
    - REGULATION: Regulations (OISD, PESO, Factory Act)
    - FAILURE_MODE: Failure modes (seal leak, bearing failure)
    - PERSON: Personnel names
    - DATE: Dates and timestamps
    - MEASUREMENT: Values with units (45 Nm, 100°C)
    """
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize NER with spaCy model"""
        self.model_name = model_name
        self.nlp = None
        self._load_model()
    
    def _load_model(self):
        """Load spaCy model"""
        try:
            logger.info(f"Loading spaCy model: {self.model_name}")
            self.nlp = spacy.load(self.model_name)
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning(f"Model {self.model_name} not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", self.model_name])
            self.nlp = spacy.load(self.model_name)
    
    def extract_equipment_tags(self, text: str) -> List[Entity]:
        """
        Extract equipment tags using patterns
        
        Patterns:
        - P-101, TK-205, V-301 (letter + dash + numbers)
        - Pump 101, Tank 205, Valve 301
        - HX-201A (with suffix)
        """
        entities = []
        
        # Pattern 1: TAG-NNN format (P-101, TK-205, V-301)
        pattern1 = r'\b([A-Z]{1,4})-(\d{2,4}[A-Z]?)\b'
        for match in re.finditer(pattern1, text):
            entities.append(Entity(
                text=match.group(0),
                entity_type='EQUIPMENT',
                start=match.start(),
                end=match.end(),
                confidence=0.95,
                metadata={'tag_format': 'standard'}
            ))
        
        # Pattern 2: Equipment Name + Number (Pump 101, Tank 205)
        pattern2 = r'\b(Pump|Tank|Valve|Compressor|Motor|Heat Exchanger|HX|Reactor)\s+(\d{2,4}[A-Z]?)\b'
        for match in re.finditer(pattern2, text, re.IGNORECASE):
            entities.append(Entity(
                text=match.group(0),
                entity_type='EQUIPMENT',
                start=match.start(),
                end=match.end(),
                confidence=0.85,
                metadata={'tag_format': 'named'}
            ))
        
        return entities
    
    def extract_parameters(self, text: str) -> List[Entity]:
        """
        Extract process parameters
        
        Examples: temperature, pressure, flow rate, level
        """
        entities = []
        
        # Common process parameters
        parameters = [
            'temperature', 'temp', 'pressure', 'flow', 'flow rate',
            'level', 'ph', 'conductivity', 'viscosity', 'density',
            'rpm', 'speed', 'torque', 'voltage', 'current', 'power'
        ]
        
        for param in parameters:
            pattern = rf'\b({param})\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append(Entity(
                    text=match.group(0),
                    entity_type='PARAMETER',
                    start=match.start(),
                    end=match.end(),
                    confidence=0.90,
                    metadata={'parameter_name': param.lower()}
                ))
        
        return entities
    
    def extract_measurements(self, text: str) -> List[Entity]:
        """
        Extract measurements with units
        
        Examples: 45 Nm, 100°C, 15 bar, 500 rpm
        """
        entities = []
        
        # Pattern: number + optional space + unit
        pattern = r'\b(\d+(?:\.\d+)?)\s*(°C|°F|K|bar|psi|MPa|kPa|Pa|Nm|kg|g|L|mL|rpm|Hz|V|A|W|m|mm|cm)\b'
        
        for match in re.finditer(pattern, text):
            entities.append(Entity(
                text=match.group(0),
                entity_type='MEASUREMENT',
                start=match.start(),
                end=match.end(),
                confidence=0.95,
                metadata={
                    'value': match.group(1),
                    'unit': match.group(2)
                }
            ))
        
        return entities
    
    def extract_regulations(self, text: str) -> List[Entity]:
        """
        Extract regulatory references
        
        Examples: OISD-STD-105, PESO, Factory Act, IS 2825
        """
        entities = []
        
        # Pattern 1: OISD standards
        pattern1 = r'\b(OISD)[\s-]*(STD)?[\s-]*(\d+)\b'
        for match in re.finditer(pattern1, text, re.IGNORECASE):
            entities.append(Entity(
                text=match.group(0),
                entity_type='REGULATION',
                start=match.start(),
                end=match.end(),
                confidence=0.95,
                metadata={'source': 'OISD'}
            ))
        
        # Pattern 2: Common regulations
        regulations = ['PESO', 'Factory Act', 'Explosives Act', 'Environment Protection Act']
        for reg in regulations:
            pattern = rf'\b({re.escape(reg)})\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append(Entity(
                    text=match.group(0),
                    entity_type='REGULATION',
                    start=match.start(),
                    end=match.end(),
                    confidence=0.90,
                    metadata={'source': reg}
                ))
        
        # Pattern 3: IS/ISO standards
        pattern3 = r'\b(IS|ISO)\s+(\d+)'
        for match in re.finditer(pattern3, text):
            entities.append(Entity(
                text=match.group(0),
                entity_type='REGULATION',
                start=match.start(),
                end=match.end(),
                confidence=0.85,
                metadata={'source': match.group(1)}
            ))
        
        return entities
    
    def extract_failure_modes(self, text: str) -> List[Entity]:
        """
        Extract failure modes
        
        Examples: seal leak, bearing failure, corrosion, erosion
        """
        entities = []
        
        failure_patterns = [
            'leak', 'leakage', 'failure', 'breakdown', 'fault',
            'corrosion', 'erosion', 'wear', 'crack', 'rupture',
            'blockage', 'clog', 'seizure', 'vibration',
            'overheating', 'contamination', 'degradation'
        ]
        
        for pattern in failure_patterns:
            regex = rf'\b(\w+\s+)?({pattern})\b'
            for match in re.finditer(regex, text, re.IGNORECASE):
                entities.append(Entity(
                    text=match.group(0).strip(),
                    entity_type='FAILURE_MODE',
                    start=match.start(),
                    end=match.end(),
                    confidence=0.75,
                    metadata={'failure_type': pattern}
                ))
        
        return entities
    
    def extract_with_spacy(self, text: str) -> List[Entity]:
        """
        Extract entities using spaCy's built-in NER
        
        Extracts: PERSON, ORG, DATE, TIME, etc.
        """
        entities = []
        doc = self.nlp(text)
        
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'DATE', 'TIME', 'ORG']:
                entities.append(Entity(
                    text=ent.text,
                    entity_type=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.80,
                    metadata={'spacy_label': ent.label_}
                ))
        
        return entities
    
    def extract_all(self, text: str) -> List[Entity]:
        """
        Extract all entity types from text
        
        Returns list of Entity objects sorted by position
        """
        logger.info("Extracting entities from text")
        
        all_entities = []
        
        # Extract each type
        all_entities.extend(self.extract_equipment_tags(text))
        all_entities.extend(self.extract_parameters(text))
        all_entities.extend(self.extract_measurements(text))
        all_entities.extend(self.extract_regulations(text))
        all_entities.extend(self.extract_failure_modes(text))
        all_entities.extend(self.extract_with_spacy(text))
        
        # Remove overlapping entities (keep highest confidence)
        filtered = self._remove_overlaps(all_entities)
        
        # Sort by position
        filtered.sort(key=lambda x: x.start)
        
        logger.info(f"Extracted {len(filtered)} entities")
        return filtered
    
    def _remove_overlaps(self, entities: List[Entity]) -> List[Entity]:
        """
        Remove overlapping entities, keeping the one with highest confidence
        """
        if not entities:
            return []
        
        # Sort by start position, then by confidence (descending)
        sorted_entities = sorted(entities, key=lambda x: (x.start, -x.confidence))
        
        filtered = []
        last_end = -1
        
        for entity in sorted_entities:
            if entity.start >= last_end:
                filtered.append(entity)
                last_end = entity.end
        
        return filtered
    
    def extract_with_context(
        self,
        text: str,
        document_id: str,
        chunk_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        Extract entities with document context for knowledge graph
        
        Returns list of entity dicts ready for graph ingestion
        """
        entities = self.extract_all(text)
        
        result = []
        for i, entity in enumerate(entities):
            result.append({
                'entity_id': f"{document_id}_ent_{i}",
                'text': entity.text,
                'type': entity.entity_type,
                'confidence': entity.confidence,
                'metadata': entity.metadata,
                'provenance': {
                    'document_id': document_id,
                    'chunk_id': chunk_id,
                    'char_start': entity.start,
                    'char_end': entity.end
                }
            })
        
        return result


# Global NER instance
ner = IndustrialNER()
