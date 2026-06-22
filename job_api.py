import requests


# Base URL for Arbetsförmedlingen / JobTech JobSearch API
JOBSEARCH_API_URL = "https://jobsearch.api.jobtechdev.se/search"


def search_jobs(keyword="it support", location="", limit=10):
    # Search jobs from Arbetsförmedlingen JobSearch API.
    #
    # keyword: job search keyword, for example "IT support"
    # location: optional location text, for example "Malmö" or "Lund"
    # limit: number of jobs to return

    params = {
        "q": keyword,
        "limit": limit
    }

    # If user enters a location, add it to query text.
    # Simple first version: combine keyword and location in search query.
    if location.strip() != "":
        params["q"] = f"{keyword} {location}"

    try:
        response = requests.get(
            JOBSEARCH_API_URL,
            params=params,
            timeout=15
        )

        # Raise error if API request failed
        response.raise_for_status()

        data = response.json()

        # JobSearch API usually returns job ads inside "hits"
        jobs = data.get("hits", [])

        job_list = []

        for job in jobs:
            title = job.get("headline", "")
            employer = job.get("employer", {}).get("name", "")
            workplace = job.get("workplace_address", {})

            municipality = workplace.get("municipality", "")
            region = workplace.get("region", "")
            description = job.get("description", {}).get("text", "")

            # Some ads contain web page URL in webpage_url
            job_link = job.get("webpage_url", "")

            # If webpage_url is missing, use source_url if available
            if job_link == "":
                job_link = job.get("source_url", "")

            publication_date = job.get("publication_date", "")
            application_deadline = job.get("application_deadline", "")

            job_list.append({
                "Position": title,
                "Company": employer,
                "Location": municipality if municipality else region,
                "Region": region,
                "Publication Date": publication_date,
                "Deadline": application_deadline,
                "Job Link": job_link,
                "Job Description": description
            })

        return job_list

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }