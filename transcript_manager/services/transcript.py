import json
from sqlalchemy.orm import Session
from transcript_manager.core.models import Transcript
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class RawTranscriptSegment:
    start: float
    end: float
    text: str
    speaker: str
    language: Optional[str] = None
    
    def to_dict(self):
        return {
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "speaker": self.speaker,
            "language": self.language
        }

@dataclass
class RawTranscript:
    segments: List[RawTranscriptSegment]
    language: str
    num_speakers: int
    
    def to_dict(self):
        return {
            "language": self.language,
            "num_speakers": self.num_speakers,
            "segments": [segment.to_dict() for segment in self.segments]
        }

class TranscriptService:
    def __init__(self, session: Session):
        self.session = session
    
    def validate_transcript(self, content: dict) -> bool:
        try:
            raw_transcript = RawTranscript(
                segments=[RawTranscriptSegment(**segment) for segment in content['segments']],
                language=content['language'],
                num_speakers=content['num_speakers']
            )
            return True
        except (KeyError, TypeError, ValueError):
            return False
    
    def add_transcript(self, project_id: int, filename: str, content: dict) -> Transcript:
        if not self.validate_transcript(content):
            raise ValueError("Invalid transcript schema")
        
        transcript = Transcript(
            project_id=project_id,
            filename=filename,
            content=content
        )
        self.session.add(transcript)
        self.session.commit()
        return transcript
    
    def get_transcript(self, transcript_id: int) -> Transcript:
        return self.session.query(Transcript).filter(Transcript.id == transcript_id).first()
    
    def list_project_transcripts(self, project_id: int):
        return self.session.query(Transcript).filter(Transcript.project_id == project_id).all()
    
    def delete_transcript(self, transcript_id: int) -> bool:
        transcript = self.session.query(Transcript).filter(Transcript.id == transcript_id).first()
        if transcript:
            self.session.delete(transcript)
            self.session.commit()
            return True
        return False
    
    def get_transcript_json(self, transcript_id: int) -> str:
        transcript = self.get_transcript(transcript_id)
        if transcript:
            return json.dumps(transcript.content)
        return None