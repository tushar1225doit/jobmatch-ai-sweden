# JobMatch AI Sweden

JobMatch AI Sweden is a Streamlit-based job search assistant built for IT Support, Junior Cloud, and IAM job applications in Sweden. The goal of this project is to help job seekers manage job applications, compare their CV with job descriptions, track application progress, and later use AI to suggest CV and cover letter improvements.

This project is being developed step by step as a practical portfolio project using Python, Streamlit, SQLite, and later Azure services.

---

## Project Purpose

As a job seeker, I wanted to build a tool that can support my job search process in a structured way. Instead of tracking jobs manually in Excel, this application allows me to save job details, view applications in a dashboard, and prepare the foundation for AI-based CV matching and skill gap analysis.

The long-term goal is to create an AI-powered assistant that can:

* Find jobs similar to my profile
* Compare my CV with job descriptions
* Calculate a match score
* Identify missing technical and soft skills
* Suggest CV improvements
* Generate tailored cover letter drafts
* Track jobs I have applied for
* Create weekly job search reports

---

## Current Features

### Phase 1.1 - Streamlit App Structure

The first version of the application includes a basic Streamlit interface with the following pages:

* Dashboard
* Add Job
* Match CV with Job
* Application Tracker
* Skill Gap Report

### Phase 1.2 - SQLite Database Integration

The application is now connected with a local SQLite database.

Current database features:

* Creates a local `data/jobs.db` database automatically
* Saves job details from the Add Job form
* Stores position name, company name, job link, location, source, deadline, job description, status, match score, applied date, notes, and created date
* Displays saved jobs in the Application Tracker page
* Shows real job count on the Dashboard

---

## Tech Stack

* Python
* Streamlit
* SQLite
* Pandas

Planned Azure services:

* Azure App Service
* Azure SQL Database
* Azure Blob Storage
* Azure Key Vault
* Microsoft Entra ID
* Azure Monitor / Application Insights

---

## Project Structure

```text
jobmatch-ai-sweden/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
│
├── data/
│   └── jobs.db
│
└── .venv/
```

---

## Database Design

The current version uses one SQLite table called `jobs`.

### jobs table

| Field           | Description                                        |
| --------------- | -------------------------------------------------- |
| id              | Unique job ID                                      |
| position_name   | Job position title                                 |
| company_name    | Company name                                       |
| job_link        | Link to job advertisement                          |
| location        | Job location                                       |
| source          | Job source, such as LinkedIn or Arbetsförmedlingen |
| deadline        | Application deadline                               |
| job_description | Full job description                               |
| status          | Current application status                         |
| match_score     | CV-job match score                                 |
| applied_date    | Date when application was submitted                |
| notes           | Additional notes                                   |
| created_at      | Date and time when job was saved                   |

---

## Application Pages

### Dashboard

The dashboard currently shows:

* Total jobs found
* Total jobs applied
* Interviews
* Average match score

At this stage, total jobs and applied jobs are connected to the SQLite database.

### Add Job

This page allows the user to add a new job manually by entering:

* Position name
* Company name
* Job link
* Location
* Source
* Application deadline
* Job description

When the user clicks `Save Job`, the job is stored in the SQLite database.

### Application Tracker

This page displays all saved jobs from the database in a table.

### Match CV with Job

This page is currently a placeholder. In the next phase, it will compare CV text with a job description and calculate a match score.

### Skill Gap Report

This page is currently a placeholder. In future phases, it will show the most common missing skills found across saved job descriptions.

---

## How to Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/jobmatch-ai-sweden.git
cd jobmatch-ai-sweden
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

For Git Bash on Windows:

```bash
source .venv/Scripts/activate
```

For PowerShell on Windows:

```bash
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

---

## Current Development Status

Completed:

* Basic Streamlit application layout
* Sidebar navigation
* Add Job page
* SQLite database connection
* Save job details into database
* Display saved jobs in Application Tracker
* Dashboard job count from database

In progress:

* Application status update
* Basic CV-job keyword matching
* Match score calculation

Planned:

* AI-based CV matching
* Skill gap analysis
* Cover letter generation
* Job search API integration
* Azure deployment
* Authentication using Microsoft Entra ID

---

## Learning Outcomes

This project demonstrates practical skills in:

* Python application development
* Streamlit dashboard development
* SQLite database integration
* Data entry forms
* Application tracking workflows
* Modular code structure
* GitHub portfolio documentation
* Future Azure cloud deployment planning

---

## Future Improvements

Planned improvements include:

* Add edit and update status option for each job
* Add delete/archive job feature
* Add CV upload functionality
* Add AI-based match score calculation
* Add missing skills report
* Add cover letter generator
* Connect Arbetsförmedlingen JobSearch API
* Deploy the application on Azure App Service
* Move from SQLite to Azure SQL Database
* Store CV files in Azure Blob Storage
* Secure API keys using Azure Key Vault

---

Added editable application status tracking and applied date management. When a job status is updated to Applied, the user can select the actual applied date, which is stored in SQLite and displayed in the Application Tracker.


## Project Goal

The final goal is to build a complete AI-powered job search assistant that supports job seekers with structured application tracking, CV matching, skill gap analysis, and personalized job application preparation.


## Latest Completed Features

### CV-Job Matching

The application can now compare a pasted CV with a saved job description. It calculates a basic keyword-based match score using predefined IT support and cloud-related skills such as Microsoft 365, Active Directory, Azure, Windows Support, Ticketing, Customer Support, Intune, Networking, MFA, IAM, and Documentation.

The match result includes:

- Match score
- Skills found in the CV
- Skills required in the job description
- Matching skills
- Missing skills
- Simple recommendation based on match percentage

### Match Result Storage

The calculated match score, matching skills, and missing skills are saved into the SQLite database. These values are displayed in the Application Tracker.

### Application Status Tracking

The user can update the application status for each job. Supported statuses include:

- Found
- Shortlisted
- CV Tailored
- Cover Letter Ready
- Applied
- Interview
- Rejected
- Offer
- Archived

When the status is changed to Applied, the app shows an editable Applied Date field. The selected applied date is saved into the database.

### Skill Gap Report

The Skill Gap Report reads missing skills from all saved job records and counts the most frequently missing skills. This helps the user identify which skills should be prioritized for learning and portfolio development.

The report shows:

- Most common missing skills
- Count of each missing skill
- Top priority missing skill
- Learning recommendation based on the top missing skill