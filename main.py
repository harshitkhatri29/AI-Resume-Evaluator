from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from pathlib import Path
import shutil
import uuid

from resume_parser import analyze_resume

app = FastAPI()

@app.get("/")
def home():
    return {
        "Resume Parser Api is running!"
    }

@app.post("/analyze")
