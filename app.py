import streamlit as st
import pandas as pd
from datetime import date
from database import create_database, add_missing_columns, add_job, get_all_jobs, count_jobs, count_applied_jobs, update_job_status, get_job_by_id, update_match_score, get_all_missing_skills
from matcher import calculate_match


st.set_page_config(
    page_title="JobMatch AI Sweden",
    page_icon="💼",
    layout="wide"
)

create_database()

# Add new columns to existing old database if missing
add_missing_columns()

st.title("💼 JobMatch AI Sweden")
st.write("AI-powered job search assistant for IT Support and Junior Cloud roles in Sweden.")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Job",
        "Match CV with Job",
        "Application Tracker",
        "Skill Gap Report"
    ]
)

if menu == "Dashboard":
    st.header("Dashboard")

    total_jobs = count_jobs()
    applied_jobs = count_applied_jobs()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jobs Found", total_jobs)
    col2.metric("Jobs Applied", applied_jobs)
    col3.metric("Interviews", 0)
    col4.metric("Average Match", "0%")

    st.info("This dashboard now reads job counts from your SQLite database.")

elif menu == "Add Job":
    st.header("Add New Job")

    with st.form("add_job_form"):
        position_name = st.text_input("Position Name")
        company_name = st.text_input("Company Name")
        job_link = st.text_input("Job Link")
        location = st.text_input("Location", value="Lund / Malmö")

        source = st.selectbox(
            "Source",
            [
                "LinkedIn",
                "Arbetsförmedlingen",
                "EURES",
                "Company Website",
                "Other"
            ]
        )

        deadline = st.date_input("Application Deadline")
        job_description = st.text_area("Paste Job Description", height=250)

        submitted = st.form_submit_button("Save Job")

        if submitted:
            if position_name.strip() == "" or company_name.strip() == "":
                st.error("Please enter both Position Name and Company Name.")
            else:
                add_job(
                    position_name,
                    company_name,
                    job_link,
                    location,
                    source,
                    deadline,
                    job_description
                )
                st.success("Job saved successfully in SQLite database.")

elif menu == "Match CV with Job":
    st.header("Match CV with Saved Job")

    st.write(
        "Select a saved job from your database, paste your CV text, calculate the match score, and save it."
    )

    # Fetch all saved jobs from database
    jobs = get_all_jobs()

    # If no jobs are saved, ask user to add a job first
    if len(jobs) == 0:
        st.warning("No saved jobs found. Please add a job first from the Add Job page.")

    else:
        # Create a simple list for dropdown.
        # Each option will show Job ID, Position, and Company.
        job_options = {}

        for job in jobs:
            job_id = job[0]
            position = job[1]
            company = job[2]

            label = f"{job_id} - {position} at {company}"
            job_options[label] = job_id

        # User selects one saved job
        selected_label = st.selectbox(
            "Select Saved Job",
            list(job_options.keys())
        )

        selected_job_id = job_options[selected_label]

        # Fetch selected job details from database
        selected_job = get_job_by_id(selected_job_id)

        if selected_job:
            job_id = selected_job[0]
            position_name = selected_job[1]
            company_name = selected_job[2]
            location = selected_job[3]
            source = selected_job[4]
            deadline = selected_job[5]
            status = selected_job[6]
            old_match_score = selected_job[7]
            job_description = selected_job[8]
            job_link = selected_job[9]

            # Show selected job summary
            st.subheader("Selected Job Details")

            col1, col2, col3 = st.columns(3)
            col1.write(f"**Position:** {position_name}")
            col2.write(f"**Company:** {company_name}")
            col3.write(f"**Location:** {location}")

            col4, col5, col6 = st.columns(3)
            col4.write(f"**Source:** {source}")
            col5.write(f"**Status:** {status}")
            col6.write(f"**Current Match Score:** {old_match_score}%")

            # Show job description from database
            with st.expander("View Saved Job Description"):
                st.write(job_description)

            # User pastes CV text
            cv_text = st.text_area("Paste your CV text", height=250)

            # Button to calculate match score
            if st.button("Calculate and Save Match Score"):

                if cv_text.strip() == "":
                    st.error("Please paste your CV text.")

                elif job_description.strip() == "":
                    st.error("This saved job does not have a job description.")

                else:
                    # Calculate match result using matcher.py
                    result = calculate_match(cv_text, job_description)

                    # Get match score from result
                    score = result["match_score"]

                    # Convert matching skills list into comma-separated text
                    matching_skills_text = ", ".join(result["matching_skills"])

                    # Convert missing skills list into comma-separated text
                    missing_skills_text = ", ".join(result["missing_skills"])

                    # Save match score, matching skills, and missing skills into database
                    update_match_score(
                        job_id,
                        score,
                        matching_skills_text,
                        missing_skills_text
                    )

                    st.subheader("Match Result")

                    # Show score level
                    if score >= 80:
                        st.success(f"Strong Match: {score}%")
                    elif score >= 60:
                        st.warning(f"Moderate Match: {score}%")
                   
                    else:
                        st.error(f"Low Match: {score}%")

                    # Show metric cards
                    m1, m2, m3 = st.columns(3)

                    m1.metric("CV Skills Found", len(result["cv_skills"]))
                    m2.metric("Job Skills Found", len(result["job_skills"]))
                    m3.metric("Matching Skills", len(result["matching_skills"]))

                    # Show matched skills
                    st.subheader("Matching Skills")
                    if result["matching_skills"]:
                        st.success(", ".join(result["matching_skills"]))
                    else:
                        st.warning("No matching skills found.")

                    # Show missing skills
                    st.subheader("Missing Skills")
                    if result["missing_skills"]:
                        st.error(", ".join(result["missing_skills"]))
                    else:
                        st.success("No missing skills detected from the current keyword list.")

                    # Recommendation
                    st.subheader("Recommendation")

                    if score >= 80:
                        st.write(
                            "This job is a strong match. You should apply with a tailored CV and cover letter."
                        )
                    elif score >= 60:
                        st.write(
                            "This job is a moderate match. You should apply after adding stronger examples related to the missing skills."
                        )
                    else:
                        st.write(
                            "This job is a weak match based on current keywords. Apply only if the role is important or if you can quickly improve the missing skills."
                        )

                    st.info("Match score has been saved into the database. Check Application Tracker.")

elif menu == "Application Tracker":
    st.header("Application Tracker")

    jobs = get_all_jobs()

    if len(jobs) == 0:
        st.warning("No jobs saved yet. Go to 'Add Job' and save your first job.")

    else:
        df = pd.DataFrame(
            jobs,
             columns=[
                "ID",
                "Position",
                "Company",
                "Location",
                "Source",
                "Deadline",
                "Status",
                "Match Score",
                "Matching Skills",
                "Missing Skills",
                "Applied Date",
                "Job Link",
                "Created At"
            ]
        )

        st.subheader("Saved Jobs")
        st.dataframe(df, use_container_width=True)

        st.subheader("Update Application Status")

        selected_job_id = st.selectbox(
            "Select Job ID",
            df["ID"].tolist()
        )

        new_status = st.selectbox(
            "Select New Status",
            [
                "Found",
                "Shortlisted",
                "CV Tailored",
                "Cover Letter Ready",
                "Applied",
                "Interview",
                "Rejected",
                "Offer",
                "Archived"
            ]
        )

        # Important:
        # This date field appears only when Applied is selected.
        selected_applied_date = None

        if new_status == "Applied":
            selected_applied_date = st.date_input(
                "Applied Date",
                value=date.today()
            )

        if st.button("Update Status"):

            if new_status == "Applied":
                update_job_status(
                    selected_job_id,
                    new_status,
                    selected_applied_date
                )

                st.success(
                    f"Job ID {selected_job_id} updated to Applied with applied date {selected_applied_date}."
                )

            else:
                update_job_status(
                    selected_job_id,
                    new_status
                )

                st.success(
                    f"Job ID {selected_job_id} updated to {new_status}."
                )

            st.rerun()

elif menu == "Skill Gap Report":
    st.header("Skill Gap Report")

    st.write(
        "This report shows the most common missing skills across all saved jobs."
    )

    # Fetch missing skills from database
    missing_skill_rows = get_all_missing_skills()

    if len(missing_skill_rows) == 0:
        st.warning(
            "No missing skills found yet. First calculate match score for saved jobs."
        )

    else:
        # Empty dictionary to count skills
        skill_count = {}

        # Each row looks like: ('Intune, Networking, Swedish Language',)
        for row in missing_skill_rows:
            missing_skills_text = row[0]

            # Skip empty values
            if missing_skills_text is None or missing_skills_text.strip() == "":
                continue

            # Split comma-separated skills into a list
            skills = missing_skills_text.split(",")

            for skill in skills:
                clean_skill = skill.strip()

                if clean_skill == "":
                    continue

                # Count skill frequency
                if clean_skill in skill_count:
                    skill_count[clean_skill] += 1
                else:
                    skill_count[clean_skill] = 1

        if len(skill_count) == 0:
            st.warning("No valid missing skills found.")

        else:
            # Convert dictionary into DataFrame
            skill_gap_df = pd.DataFrame(
                list(skill_count.items()),
                columns=["Missing Skill", "Count"]
            )

            # Sort by count, highest first
            skill_gap_df = skill_gap_df.sort_values(
                by="Count",
                ascending=False
            )

            st.subheader("Most Common Missing Skills")

            st.dataframe(
                skill_gap_df,
                use_container_width=True
            )

            st.subheader("Top Priority Skill")

            top_skill = skill_gap_df.iloc[0]["Missing Skill"]
            top_count = skill_gap_df.iloc[0]["Count"]

            st.success(
                f"Your top missing skill is: {top_skill} — found in {top_count} job(s)."
            )

            st.subheader("Learning Recommendation")

            if top_skill == "Intune":
                st.write(
                    "Recommendation: Create a small Microsoft Intune learning lab and document it on GitHub."
                )

            elif top_skill == "Networking":
                st.write(
                    "Recommendation: Revise DNS, DHCP, VPN, TCP/IP and basic troubleshooting commands."
                )

            elif top_skill == "Swedish Language":
                st.write(
                    "Recommendation: Practice Swedish IT support phrases for helpdesk and workplace communication."
                )

            elif top_skill == "Cybersecurity Basics":
                st.write(
                    "Recommendation: Learn Microsoft Defender, MFA, endpoint protection and basic security concepts."
                )

            elif top_skill == "Hardware Support":
                st.write(
                    "Recommendation: Add examples of laptop, printer, desktop and peripheral troubleshooting in your CV."
                )

            else:
                st.write(
                    "Recommendation: Add this skill to your learning plan and create one small portfolio task around it."
                )