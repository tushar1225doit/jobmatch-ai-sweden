# Import regular expression module.
# We use this to search words/phrases inside CV text and job description.
import re


# This dictionary contains the skills we want to detect.
# Each main skill has different possible words/phrases that may appear in a CV or job description.
# Example:
# "Microsoft 365" can appear as "microsoft 365", "m365", "office 365", or "o365".
SKILLS_KEYWORDS = {
    "Microsoft 365": ["microsoft 365", "m365", "office 365", "o365"],
    "Active Directory": ["active directory", "ad", "windows ad"],
    "Microsoft Entra ID": ["entra id", "azure ad", "microsoft entra"],
    "Azure": ["azure", "microsoft azure"],

    "Windows Support": ["windows", "windows 10", "windows 11", "windows support"],
    "Ticketing System": ["ticketing", "ticket system", "incident management", "service request"],
    "Customer Support": ["customer support", "user support", "end user support", "helpdesk", "service desk"],
    "Remote Support": ["remote support", "remote troubleshooting", "remote assistance"],
    "On-site Support": ["onsite support", "on-site support", "field support"],

    "Troubleshooting": ["troubleshooting", "diagnose", "problem solving", "resolve issues"],
    "Networking": ["networking", "tcp/ip", "dns", "dhcp", "vpn", "router", "switch"],
    "Intune": ["intune", "microsoft intune", "endpoint manager"],

    "Hardware Support": ["hardware", "printer", "laptop", "desktop", "peripherals"],
    "Software Installation": ["software installation", "install software", "application support"],

    "IAM": ["iam", "identity and access management", "access management", "user access"],
    "RBAC": ["rbac", "role based access control", "role-based access control"],
    "MFA": ["mfa", "multi factor authentication", "multi-factor authentication"],

    "Cybersecurity Basics": ["security", "cybersecurity", "defender", "endpoint security"],

    "Communication": ["communication", "communicate", "stakeholder", "collaboration"],
    "Documentation": ["documentation", "document", "knowledge base", "kb article"],

    "Swedish Language": ["swedish", "svenska"],
    "English Language": ["english"],

    "Driving License": ["driving license", "driver license", "b-körkort", "körkort"]
}


def clean_text(text):
    """
    This function cleans the text before matching.

    Why we need this:
    - CV and job description may have uppercase/lowercase differences.
    - There may be extra spaces or line breaks.
    - To compare properly, we convert everything to lowercase.

    Example:
    "Microsoft 365 Support" becomes "microsoft 365 support"
    """

    # If text is empty, return empty string
    if not text:
        return ""

    # Convert text to lowercase
    text = text.lower()

    # Replace multiple spaces/new lines with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove extra spaces from beginning and end
    return text.strip()


def find_skills(text):
    """
    This function finds skills from the given text.

    Input:
    - CV text or job description text

    Output:
    - A list of skills found in the text

    Example:
    If text contains "Microsoft 365 and Active Directory",
    output will be:
    ["Active Directory", "Microsoft 365"]
    """

    # First clean the text
    text = clean_text(text)

    # Empty list to store detected skills
    found_skills = []

    # Go through each skill and its related keywords
    for skill, keywords in SKILLS_KEYWORDS.items():

        # Check each keyword for this skill
        for keyword in keywords:

            # Create a search pattern.
            # \b means word boundary.
            # It helps avoid false matches inside bigger words.
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"

            # If keyword is found in the text
            if re.search(pattern, text):

                # Add the main skill name to found_skills
                found_skills.append(skill)

                # Stop checking more keywords for this skill
                # Example: if "m365" is found, no need to check "office 365"
                break

    # Return skills in alphabetical order
    return sorted(found_skills)


def calculate_match(cv_text, job_description):
    """
    This is the main matching function.

    It compares:
    - Skills found in your CV
    - Skills required in the job description

    Then it calculates the match score.

    Formula:
    match_score = matching skills / job required skills * 100

    Example:
    Job needs 10 skills.
    Your CV has 7 of those skills.
    Match score = 7 / 10 * 100 = 70%
    """

    # Find skills from CV text
    cv_skills = find_skills(cv_text)

    # Find skills from job description
    job_skills = find_skills(job_description)

    # If no known skill is found in job description,
    # then we cannot calculate a useful match score.
    if len(job_skills) == 0:
        return {
            "match_score": 0,
            "cv_skills": cv_skills,
            "job_skills": job_skills,
            "matching_skills": [],
            "missing_skills": [],
            "message": "No known skills found in the job description."
        }

    # Skills that are present in both CV and job description
    matching_skills = sorted(list(set(cv_skills) & set(job_skills)))

    # Skills required in job description but missing from CV
    missing_skills = sorted(list(set(job_skills) - set(cv_skills)))

    # Calculate match score percentage
    match_score = round((len(matching_skills) / len(job_skills)) * 100)

    # Return all results in dictionary format
    # This makes it easy to use in app.py
    return {
        "match_score": match_score,
        "cv_skills": cv_skills,
        "job_skills": job_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "message": "Match score calculated successfully."
    }