from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pathlib import Path
import shutil
import uuid

from resume_parser import analyze_resume

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Resume Matcher API is running!"
    }


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Only allow PDF and DOCX files
    allowed_extensions = [".pdf", ".docx"]

    file_extension = Path(resume.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    # Create a unique temporary filename
    temp_file_path = Path(
        f"temp_{uuid.uuid4()}{file_extension}"
    )

    try:
        # Save uploaded resume temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        # Call your existing resume analysis logic
        result = analyze_resume(
            temp_file_path,
            job_description
        )

        return result

    finally:
        # Delete temporary file after processing
        if temp_file_path.exists():
            temp_file_path.unlink()