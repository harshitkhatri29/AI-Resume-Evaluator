# AI Resume Evaluator

An AI-powered Resume Evaluator built with Python that analyzes PDF and DOCX resumes using the Groq API and returns structured feedback.

## Features

- Parse PDF and DOCX resumes
- AI-powered resume analysis
- Structured feedback on:
  - Skills
  - Experience
  - Education
  - Strengths
  - Areas for improvement
- JSON output using Pydantic

## Tech Stack

- Python
- Google Gemini API
- Pydantic
- python-dotenv
- PyPDF2
- python-docx

## Project Structure

```
AI-Resume-Evaluator/
│
├── resume_parser.py
├── pyproject.toml
├── uv.lock
├── .gitignore
├── README.md
└── resumes/
    └── README.md
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/harshitkhatri29/AI-Resume-Evaluator.git
```

2. Move into the project

```bash
cd AI-Resume-Evaluator
```

3. Install dependencies

```bash
uv sync
```

4. Create a `.env` file

```
GEMINI_API_KEY=your_api_key_here
```

5. Add your resume(s) inside the `resumes/` folder.

6. Run the project

```bash
uv run resume_parser.py
```

## Example Output

The project analyzes resumes and returns structured feedback including:

- Skills assessment
- Experience evaluation
- Education review
- Overall strengths
- Suggestions for improvement

## Future Improvements

- Resume scoring
- ATS compatibility analysis
- Streamlit web interface
- Multi-resume comparison

## License

This project is for learning and educational purposes.
