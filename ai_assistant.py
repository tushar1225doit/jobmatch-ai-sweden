import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()

# Read Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_ai_cv_analysis(cv_text, job_description, position_name, company_name):
    # Check whether API key exists
    if GEMINI_API_KEY is None or GEMINI_API_KEY.strip() == "":
        return "Error: GEMINI_API_KEY is missing. Please add it to your .env file."

    # Configure Gemini API
    genai.configure(api_key=GEMINI_API_KEY)

    # Use Gemini Flash model
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Prompt for AI analysis
    prompt = f"""
You are an AI career assistant helping a job seeker in Sweden.

Analyze the candidate CV against the job description.

Position: {position_name}
Company: {company_name}

Candidate CV:
{cv_text}

Job Description:
{job_description}

Return the analysis in this format:

Overall Match:
Strong Matching Points:
Missing Technical Skills:
Missing Soft Skills:
CV Improvement Suggestions:
Cover Letter Direction:
Application Decision:

Rules:
- Do not invent experience.
- Only suggest improvements based on the CV.
- Keep the language simple and professional.
- Focus on IT Support, Junior Cloud, IAM, Microsoft 365, Active Directory, Azure, Windows support, ticketing, and customer support.
"""

    response = model.generate_content(prompt)

    return response.text