from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from transcript_manager.core.models import Base

class Database:
    def __init__(self, db_url="sqlite:///transcript_manager/data/transcripts.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()