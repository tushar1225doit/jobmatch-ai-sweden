import sqlite3
from datetime import datetime
import os

# Folder and database file name
DB_FOLDER = "data"
DB_NAME = "jobs.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)


def create_database():
    """
    Create the data folder and jobs table if they do not already exist.
    This function runs when the Streamlit app starts.
    """

    # Create data folder if it does not exist
    os.makedirs(DB_FOLDER, exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            job_link TEXT,
            location TEXT,
            source TEXT,
            deadline TEXT,
            job_description TEXT,
            status TEXT,
            match_score INTEGER,
            applied_date TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_missing_columns():
    # Add new columns to jobs table if they do not already exist

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Read existing columns from jobs table
    cursor.execute("PRAGMA table_info(jobs)")
    columns = cursor.fetchall()

    existing_columns = []

    for column in columns:
        existing_columns.append(column[1])

    # Add matching_skills column if missing
    if "matching_skills" not in existing_columns:
        cursor.execute("ALTER TABLE jobs ADD COLUMN matching_skills TEXT DEFAULT ''")

    # Add missing_skills column if missing
    if "missing_skills" not in existing_columns:
        cursor.execute("ALTER TABLE jobs ADD COLUMN missing_skills TEXT DEFAULT ''")

    conn.commit()
    conn.close()

def add_job(position_name, company_name, job_link, location, source, deadline, job_description):
    """
    Insert a new job into the jobs table.
    This function is used when user clicks Save Job in the Add Job page.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs (
            position_name,
            company_name,
            job_link,
            location,
            source,
            deadline,
            job_description,
            status,
            match_score,
            applied_date,
            notes,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        position_name,
        company_name,
        job_link,
        location,
        source,
        str(deadline),
        job_description,
        "Found",
        0,
        "",
        "",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_jobs():
    """
    Fetch all saved jobs from the database.

    This function returns 13 fields.
    So the DataFrame in app.py must also have 13 column names.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            position_name,
            company_name,
            location,
            source,
            deadline,
            status,
            match_score,
            matching_skills,
            missing_skills,
            applied_date,
            job_link,
            created_at
        FROM jobs
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
           


def count_jobs():
    """
    Count total jobs saved in the database.
    This is used in Dashboard.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total = cursor.fetchone()[0]

    conn.close()

    return total


def count_applied_jobs():
    """
    Count jobs where status is Applied.
    This is used in Dashboard.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Applied'")
    total = cursor.fetchone()[0]

    conn.close()

    return total


def update_job_status(job_id, new_status, applied_date=None):
    """
    Update job application status.

    If status is Applied, save the selected applied date.
    If status is not Applied, only update the status.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if new_status == "Applied":
        cursor.execute("""
            UPDATE jobs
            SET status = ?, applied_date = ?
            WHERE id = ?
        """, (new_status, str(applied_date), job_id))

    else:
        cursor.execute("""
            UPDATE jobs
            SET status = ?
            WHERE id = ?
        """, (new_status, job_id))

    conn.commit()
    conn.close()


def get_job_by_id(job_id):
    """
    Fetch one job from database using job ID.

    In the Match CV page, user selects a saved job.
    Then we fetch that job's description from database.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            position_name,
            company_name,
            location,
            source,
            deadline,
            status,
            match_score,
            job_description,
            job_link
        FROM jobs
        WHERE id = ?
    """, (job_id,))

    job = cursor.fetchone()

    conn.close()

    return job


def update_match_score(job_id, match_score, matching_skills="", missing_skills=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET match_score = ?, matching_skills = ?, missing_skills = ?
        WHERE id = ?
    """, (match_score, matching_skills, missing_skills, job_id))

    conn.commit()
    conn.close()

  
def get_all_missing_skills():
    # Fetch missing_skills column from all jobs.
    # This function is used in the Skill Gap Report page.
    # Example value in database:
    # "Intune, Swedish Language, Networking"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT missing_skills
        FROM jobs
        WHERE missing_skills IS NOT NULL
        AND missing_skills != ''
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def job_exists_by_link(job_link):
    # Check whether a job with the same job_link already exists in database.
    # Returns True if job exists, otherwise False.

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM jobs
        WHERE job_link = ?
    """, (job_link,))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0