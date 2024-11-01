from sqlalchemy.orm import Session
from transcript_manager.core.models import Project
from typing import List

class ProjectService:
    def __init__(self, session: Session):
        self.session = session

    def create_project(self, name: str, description: str) -> Project:
        if self.session.query(Project).filter(Project.name == name).first():
            raise ValueError("Project with this name already exists")
        
        project = Project(name=name, description=description)
        self.session.add(project)
        self.session.commit()
        return project

    def get_project(self, project_id: int) -> Project:
        return self.session.query(Project).filter(Project.id == project_id).first()

    def list_projects(self) -> List[Project]:
        return self.session.query(Project).all()

    def delete_project(self, project_id: int) -> bool:
        project = self.session.query(Project).filter(Project.id == project_id).first()
        if project:
            self.session.delete(project)
            self.session.commit()
            return True
        return False