# JobMatch AI Sweden

**JobMatch AI Sweden** is an AI-powered job search assistant built with Python, Streamlit, SQLite, Gemini AI API, and Arbetsförmedlingen / JobTech JobSearch API.

The application helps job seekers find relevant jobs, save job opportunities, compare their CV with job descriptions, identify missing skills, generate AI-based CV/job analysis, and track application progress in one dashboard.

This project was built as a practical portfolio project for **IT Support, Junior Cloud, IAM, and Azure-focused roles in Sweden**.

---

## Project Summary

Job searching is often managed manually using Excel sheets, browser bookmarks, and separate documents for CV and cover letters. This project solves that problem by creating a structured job search assistant where a user can:

* Search real job ads from Arbetsförmedlingen / JobTech API
* Save selected jobs into a local database
* Compare CV text with job descriptions
* Calculate a keyword-based match score
* Identify matching and missing skills
* Generate AI-based CV-job analysis using Gemini API
* Track application status and applied dates
* View a skill gap report to guide learning priorities

The project combines practical job-search workflow automation with AI, database management, API integration, and dashboard development.

---

## Key Features

### 1. Job Search API Integration

The app includes a **Find Jobs** page that connects to the Arbetsförmedlingen / JobTech JobSearch API.

Users can search jobs by:

* Keyword
* Location
* Number of results

Example searches:

* IT support in Malmö
* Azure in Lund
* Service desk in Skåne

The app displays job results in a table and allows users to select individual jobs for more details.

---

### 2. Save Jobs to Database

From the job search results, users can select a job and save it directly into the SQLite database.

Saved job details include:

* Position name
* Company name
* Job link
* Location
* Source
* Deadline
* Full job description

This creates a complete workflow:

```text
Find Jobs → Select Job → Save Job → Match CV → AI Analysis → Track Application
```

---

### 3. Manual Job Entry

In addition to API-based job search, the app also allows manual job entry.

This is useful for jobs found from:

* LinkedIn
* Company websites
* Recruiter messages
* EURES
* Other job portals

---

### 4. Application Tracker

The **Application Tracker** page displays all saved jobs from the database.

It shows:

* Position
* Company
* Location
* Source
* Deadline
* Application status
* Match score
* Matching skills
* Missing skills
* Applied date
* Job link
* Created date

Supported application statuses:

* Found
* Shortlisted
* CV Tailored
* Cover Letter Ready
* Applied
* Interview
* Rejected
* Offer
* Archived

When the status is changed to **Applied**, the app shows an editable **Applied Date** field. This is useful when recording applications for job search activity reports.

---

### 5. Keyword-Based CV Matching

The app compares a pasted CV with a saved job description using a predefined IT and cloud skill dictionary.

The current keyword matcher checks for skills such as:

* Microsoft 365
* Active Directory
* Microsoft Entra ID
* Azure
* Windows Support
* Ticketing System
* Customer Support
* Remote Support
* Troubleshooting
* Networking
* Intune
* IAM
* RBAC
* MFA
* Cybersecurity Basics
* Documentation
* Swedish Language
* English Language

The result includes:

* Match score
* Skills found in the CV
* Skills required in the job description
* Matching skills
* Missing skills
* Simple application recommendation

---

### 6. Match Result Storage

The calculated match score, matching skills, and missing skills are saved into SQLite.

This allows the user to return to the Application Tracker and quickly compare which jobs are stronger or weaker matches.

---

### 7. Skill Gap Report

The **Skill Gap Report** page reads missing skills from all saved jobs and counts which skills appear most often.

The report shows:

* Most common missing skills
* Count of each missing skill
* Top priority missing skill
* Learning recommendation based on the top missing skill

Example:

| Missing Skill        | Count |
| -------------------- | ----: |
| Swedish Language     |     3 |
| Intune               |     2 |
| Networking           |     2 |
| Cybersecurity Basics |     1 |

This helps the user decide what to study next and what portfolio labs to build.

---

### 8. AI CV Analysis with Gemini API

The app includes an **AI CV Analysis** page powered by Gemini API.

The user selects a saved job, pastes CV text, and generates an AI-based analysis.

The AI output includes:

* Overall match summary
* Strong matching points
* Missing technical skills
* Missing soft skills
* CV improvement suggestions
* Cover letter direction
* Application decision

The AI prompt is designed to avoid fake experience and only suggest improvements based on the provided CV.

For privacy, users are advised not to paste sensitive personal data such as personal identity numbers, passport details, full address, or private information.

---

## Application Workflow

```text
1. Search jobs using Arbetsförmedlingen / JobTech API
2. Select a job from the search result
3. Save the job into SQLite database
4. Open Match CV with Job page
5. Paste CV text and calculate match score
6. Save matching and missing skills
7. Open AI CV Analysis page
8. Generate AI-based analysis
9. Track application status in Application Tracker
10. Review Skill Gap Report for learning priorities
```

---

## Tech Stack

| Area                  | Technology                                 |
| --------------------- | ------------------------------------------ |
| Programming Language  | Python                                     |
| Web App Framework     | Streamlit                                  |
| Database              | SQLite                                     |
| Data Handling         | Pandas                                     |
| Job Search API        | Arbetsförmedlingen / JobTech JobSearch API |
| AI Layer              | Gemini API                                 |
| Environment Variables | python-dotenv                              |
| HTTP Requests         | requests                                   |
| Version Control       | Git and GitHub                             |

---

## Project Architecture

```text
jobmatch-ai-sweden/
│
├── app.py              # Main Streamlit application
├── database.py         # SQLite database functions
├── matcher.py          # Keyword-based CV-job matching logic
├── ai_assistant.py     # Gemini AI analysis functions
├── job_api.py          # Arbetsförmedlingen JobSearch API integration
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Files excluded from Git
│
├── data/
│   └── jobs.db         # Local SQLite database, ignored by Git
│
└── .env                # API keys, ignored by Git
```

---

## Module Overview

### `app.py`

Main Streamlit application. It contains the user interface and page navigation.

Current pages:

* Dashboard
* Find Jobs
* Add Job
* Match CV with Job
* AI CV Analysis
* Application Tracker
* Skill Gap Report

---

### `database.py`

Handles SQLite database operations.

Main functions:

* Create database
* Add missing columns safely
* Add jobs
* Fetch saved jobs
* Update job status
* Update applied date
* Update match score
* Store matching and missing skills
* Fetch missing skills for report

---

### `matcher.py`

Contains rule-based CV-job matching logic.

It compares CV text and job description text using a predefined skill dictionary and returns:

* CV skills
* Job skills
* Matching skills
* Missing skills
* Match score

---

### `ai_assistant.py`

Contains Gemini API integration.

It generates AI-based career analysis for a selected job and pasted CV text.

---

### `job_api.py`

Connects to Arbetsförmedlingen / JobTech JobSearch API and returns job ads in a clean format for the Streamlit app.

---

## Database Design

The project currently uses one SQLite table called `jobs`.

### jobs table

| Field           | Description                                 |
| --------------- | ------------------------------------------- |
| id              | Unique job ID                               |
| position_name   | Job position title                          |
| company_name    | Company name                                |
| job_link        | Link to job advertisement                   |
| location        | Job location                                |
| source          | Job source                                  |
| deadline        | Application deadline                        |
| job_description | Full job description                        |
| status          | Current application status                  |
| match_score     | CV-job match score                          |
| matching_skills | Skills found in both CV and job description |
| missing_skills  | Skills required in job but missing from CV  |
| applied_date    | Date when application was submitted         |
| notes           | Additional notes                            |
| created_at      | Date and time when job was saved            |

---

## Screenshots

Add screenshots here after saving images in a `screenshots/` folder.

Recommended screenshots:

```text
screenshots/dashboard.png
screenshots/find-jobs.png
screenshots/application-tracker.png
screenshots/match-cv.png
screenshots/skill-gap-report.png
screenshots/ai-analysis.png
```

Example Markdown:

```markdown
![Dashboard](screenshots/dashboard.png)
![Find Jobs](screenshots/find-jobs.png)
![Application Tracker](screenshots/application-tracker.png)
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/jobmatch-ai-sweden.git
cd jobmatch-ai-sweden
```

Replace `YOUR_USERNAME` with your GitHub username.

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

---

### 3. Activate the virtual environment

For Git Bash on Windows:

```bash
source .venv/Scripts/activate
```

For PowerShell on Windows:

```bash
.venv\Scripts\Activate.ps1
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Create `.env` file

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit this file to GitHub.

---

### 6. Run the app

```bash
streamlit run app.py
```

---

## Environment Variables

The app uses environment variables for API keys.

| Variable       | Purpose                        |
| -------------- | ------------------------------ |
| GEMINI_API_KEY | API key for Gemini AI analysis |

The `.env` file is ignored by Git for security.

---

## Security and Privacy Notes

* `.env` is excluded from Git using `.gitignore`
* Local database file `data/jobs.db` is excluded from Git
* Users should avoid pasting sensitive personal details into AI analysis
* The application does not automatically apply to jobs
* The user remains in control of final application submission

---

## Current Status

Completed:

* Streamlit app structure
* SQLite database integration
* Manual job entry
* Application tracker
* Editable application status
* Editable applied date
* Keyword-based CV-job matching
* Match score storage
* Matching skills storage
* Missing skills storage
* Skill Gap Report
* Gemini AI CV analysis
* Arbetsförmedlingen / JobTech job search integration
* Save selected API job to database
* Streamlit session state handling for stable job search results
* Git and GitHub version control

In progress:

* Duplicate job prevention
* Dashboard improvement
* Better filtering of job search results

Planned:

* Avoid saving duplicate jobs
* Improve dashboard with charts and KPIs
* Save AI analysis results into database
* Generate tailored cover letter draft
* Export weekly job search report
* Add CV file upload
* Add recruiter/contact tracker
* Add job search filters for language, remote/hybrid, and location
* Deploy on Azure App Service
* Move from SQLite to Azure SQL Database
* Store uploaded CVs in Azure Blob Storage
* Secure API keys using Azure Key Vault
* Add Microsoft Entra ID authentication

---

## Learning Outcomes

This project demonstrates practical skills in:

* Python development
* Streamlit application development
* SQLite database design
* CRUD-style application workflow
* REST API integration
* AI API integration
* Environment variable management
* Git and GitHub version control
* Modular project structure
* Basic data analysis using Pandas
* Job-search workflow automation
* AI-assisted career support
* Future Azure deployment planning

---

## Portfolio Value

This project is relevant for roles such as:

* IT Support Technician
* Service Desk Analyst
* Junior Cloud Administrator
* IAM / Access Management Assistant
* Junior Azure Administrator
* Technical Support Specialist

It demonstrates a practical combination of:

* IT support domain understanding
* Cloud upskilling direction
* Python automation
* API integration
* Database handling
* AI-assisted workflow design
* Documentation and version control

---

## Future Azure Architecture

Planned cloud version:

```text
Streamlit App
    ↓
Azure App Service
    ↓
Azure SQL Database
    ↓
Azure Blob Storage
    ↓
Azure Key Vault
    ↓
Azure Monitor / Application Insights
    ↓
Microsoft Entra ID Authentication
```

This will convert the local MVP into a cloud-hosted Azure portfolio project.

---

## Project Goal

The final goal is to build a complete AI-powered job search assistant that supports job seekers with structured application tracking, CV matching, skill gap analysis, AI-based application preparation, and job search workflow management.
