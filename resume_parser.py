import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Where is api key?")

client = Groq(api_key=my_api_key)

model= "llama-3.3-70b-versatile"
# role="user"

from pydantic import BaseModel
class Description(BaseModel):
    job_title:str
    required_skils: list[str]
    preffered_skills: list[str]
    experience:int | None = None
    education:str | None = None

schema = Description.model_json_schema()
response_format={
    "type":"json_object"
}
system_prompt=f"""
return the output in json format strictly following this schema
{schema}
"""
message_system = {
    "role":"system",
    "content":system_prompt
}
job_description = """
Job Title: AI Engineer

Company: Amazon

Location: Bengaluru, India

Job Type: Full-Time

Job Description:

Amazon is looking for a talented AI Engineer to design, develop, and deploy scalable artificial intelligence solutions that improve customer experience and optimize business operations. You will collaborate with software engineers, data scientists, and product managers to build production-ready machine learning and generative AI applications.

Key Responsibilities:

- Design and develop AI-powered applications using Large Language Models (LLMs).
- Build and optimize machine learning models for production.
- Develop REST APIs for AI services.
- Integrate AI models with cloud-based applications.
- Work with cross-functional teams to understand business requirements.
- Optimize model performance, latency, and scalability.
- Write clean, maintainable, and well-documented code.
- Participate in code reviews and technical discussions.

Required Qualifications:

- Bachelor's or Master's degree in Computer Science, Artificial Intelligence, Data Science, or a related field.
- 2+ years of software development experience.
- Strong programming skills in Python.
- Experience with machine learning concepts.
- Experience working with Large Language Models (LLMs).
- Knowledge of Prompt Engineering techniques.
- Experience with FastAPI or Flask.
- Strong understanding of REST APIs.
- Experience with SQL and relational databases.
- Familiarity with Git and GitHub.
- Strong problem-solving and debugging skills.
- Excellent communication and teamwork skills.

Preferred Qualifications:

- Experience with LangChain or LlamaIndex.
- Experience deploying AI applications on AWS.
- Knowledge of Docker and Kubernetes.
- Experience with vector databases such as Pinecone, ChromaDB, or FAISS.
- Familiarity with Retrieval-Augmented Generation (RAG).
- Experience with CI/CD pipelines.
- Knowledge of cloud-native architectures.

Technical Skills:

Programming Languages:
- Python
- SQL

Frameworks:
- FastAPI
- Flask
- LangChain

Cloud:
- AWS

Databases:
- PostgreSQL
- MySQL

Tools:
- Git
- Docker
- Kubernetes

AI/ML:
- Machine Learning
- Deep Learning
- LLMs
- Prompt Engineering
- RAG
- Vector Databases

Benefits:

- Competitive salary
- Health insurance
- Performance bonus
- Employee stock options
- Learning and development programs
- Flexible work environment
"""
prompt = f"""
Extract the following information from the job description:

- Job title
- Required skills (return as a list of individual skills)
- Preferred skills (return as a list)
- Required experience (return only the number of years if mentioned)
- Education (return a short phrase)

Do not merge multiple skills into one sentence.
{job_description}
"""
message = {
    "role":"user",
    "content":prompt
}
messages = [message_system,message]
response = client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer = response.choices[0].message.content
# print(answer)

import json
raw_json = answer
job_data = json.loads(raw_json)
job = Description(**job_data)


print(job.job_title)
# print(job.required_skils)
# print(job.preffered_skills)

# for skills in job.required_skils:
#     print(skills)

# for skills in job.preffered_skills:
#     print(skills)


class MatchDetails(BaseModel):
    matching_skills : list[str] = []
    missing_skills : list[str] = []
    experience_requirement_met : bool
    verdict : str

class MatchResult(BaseModel):
    score: float
    details: MatchDetails

class Experience(BaseModel):
    company:str | None = None
    role:str | None = None
    duration:str | None = None
    description:str | None = None
    skills_used : list[str] = []

class Resume(BaseModel):
    name:str | None = None
    email:str | None = None
    phone: str | None = None
    skills:list[str] = []
    education : list[str] = []
    projects : list[str] = []
    certifications : list[str] = []
    experiences:list[Experience] = []

resume_schema = Resume.model_json_schema()

def final_result(job, resume):
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume.model_dump_json(indent=2)}
    Return JSON matching this schema:

    {match_schema}

    Give me:

    1. Candidate name
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage from 0 to 100
    6. A short final verdict

    Keep the response concise and easy to read.
    """
    message = {
        "role":"user",
        "content":prompt
    }
    messages=[message]
    response_format={
        "type":"json_object"
    }
    response = client.chat.completions.create(model=model,messages=messages,response_format=response_format)
    raw_data = response.choices[0].message.content
    data = json.loads(raw_data)
    return MatchResult(**data)

def parse_resume(resume_text):
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    message_system = {
        "role" : "system",
        "content" : system_prompt
    }

    prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message = {
        "role" : "user",
        "content" : prompt
    }

    messages = [message_system,message]
    response_format = {
        "type" : "json_object"
    }

    response = client.chat.completions.create(model=model,messages=messages,response_format=response_format)
    answer = response.choices[0].message.content
    raw_output = answer
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume



from pypdf import PdfReader
from docx import Document

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text();

        if page_text:
            text+=page_text + "\n"

    return text

def read_docx(file_path):
    document = Document(file_path)
    text = ""
    
    for paragraph in document.paragraphs:
        # paragraph_text = paragraphs.extract_text();
        if paragraph.text.strip():
            text+=paragraph.text + "\n"

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"

    return text

def read_resume(file_path):
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        return read_docx(file_path)
    else:
        return None
    

resume_folder = Path("resumes")
all_results = []
for file_path in resume_folder.iterdir():
    if file_path.suffix.lower() not in [".pdf" , ".docx"]:
        continue
    print("\nProcessing:", file_path.name)
    resume_text = read_resume(file_path)
    parsed_resume = parse_resume(resume_text)
    time.sleep(5)
    result = final_result(job,parsed_resume)
    time.sleep(5)
    print("Score:" ,result.score)
    all_results.append({
        "name":parsed_resume.name,
        "score":result.score,
        "details":result.details
    })

all_results.sort(
    key=lambda candidate: candidate["score"],
    reverse=True
)
top_2 = all_results[:2]
worst_2 = all_results[-2:]

print("TOP 2 CANDIDATES")
for candidate in top_2:

    print(
        candidate["name"],
        "-",
        candidate["score"],
        "%"
    )

    print(candidate["details"])

print("LOWEST 2 CANDIDATES")
for candidate in worst_2:

    print(
        candidate["name"],
        "-",
        candidate["score"],
        "%"
    )
    print(candidate["details"])





