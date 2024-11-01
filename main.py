

# Example usage:
if __name__ == "__main__":
    db = Database()
    session = next(db.get_session())
    
    # Create project service
    project_service = ProjectService(session)
    transcript_service = TranscriptService(session)
    
    # Create a new project
    project = project_service.create_project("Interview Analysis 2024", "Customer interview transcripts")
    
    # Add a transcript to the project
    with open("sample_transcript.json", "r") as f:
        transcript_content = json.load(f)
    
    transcript = transcript_service.add_transcript(
        project_id=project.id,
        filename="interview_1.json",
        content=transcript_content
    )
    
    # List all transcripts in the project
    project_transcripts = transcript_service.list_project_transcripts(project.id)
    for t in project_transcripts:
        print(f"Transcript: {t.filename}")