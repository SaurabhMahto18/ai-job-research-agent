import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from .state import AgentState
from .tools import search_jobs


load_dotenv()


# -----------------------------------
# Groq LLM
# -----------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# -----------------------------------
# 1. Analyze User Query
# -----------------------------------

def analyze_query(state: AgentState):

    prompt = f"""
You are an AI job research assistant.

Analyze this job search request:

{state["user_query"]}

Identify:

- Target job role
- Job type
- Important skills
- Experience level
- Location preference
- Remote or on-site preference
- Other useful filters

Return a concise structured analysis.
"""

    response = llm.invoke(prompt)

    return {
        "query_analysis": response.content
    }


# -----------------------------------
# 2. Create Short Search Query
# -----------------------------------

def create_search_query(state: AgentState):

    prompt = f"""
Create a short web search query for finding current job listings.

User request:
{state["user_query"]}

Query analysis:
{state["query_analysis"]}

Rules:

- Keep the query under 300 characters.
- Include the job role.
- Include job type.
- Include the most important skills only.
- Include location.
- Focus on actual job or internship listings.
- Do not explain anything.
- Return ONLY the search query.
"""

    response = llm.invoke(prompt)

    search_query = response.content.strip()

    # Extra safety for Tavily
    search_query = " ".join(search_query.split())[:1400]

    return {
        "search_query": search_query
    }


# -----------------------------------
# 3. Search Jobs using Tavily
# -----------------------------------

def search_job_node(state: AgentState):

    query = state["search_query"]

    results = search_jobs(query)

    return {
        "search_results": results
    }


# -----------------------------------
# 4. Analyze Search Results
# -----------------------------------

def analyze_jobs(state: AgentState):

    jobs = state["search_results"]

    jobs_text = ""

    for i, job in enumerate(jobs, start=1):

        jobs_text += f"""
JOB {i}

Title:
{job.get("title", "Not specified")}

URL:
{job.get("url", "Not specified")}

Content:
{job.get("content", "Not specified")}

-------------------------
"""


    prompt = f"""
You are an expert AI job research assistant.

USER REQUEST:
{state["user_query"]}

QUERY ANALYSIS:
{state["query_analysis"]}

SEARCH RESULTS:
{jobs_text}

Find the most relevant jobs for the user.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "jobs": [
        {{
            "title": "Job title",
            "company": "Company name",
            "location": "Job location",
            "experience": "Required experience",
            "salary": "Salary or stipend",
            "skills": [
                "skill1",
                "skill2"
            ],
            "match_score": 85,
            "reason": "Why this job matches",
            "url": "Original URL"
        }}
    ]
}}

Rules:

1. Return ONLY JSON.
2. Do NOT use Markdown.
3. Do NOT use ```json.
4. Do NOT add any explanation outside JSON.
5. Do NOT invent information.
6. If information is unavailable, use "Not specified".
7. match_score must be an integer between 0 and 100.
8. Use ONLY URLs that appear in the search results.
9. Ignore irrelevant results.
10. Return maximum 10 jobs.
11. Match score should consider:
    - Job role
    - Job type
    - Experience level
    - Candidate skills
    - Location
"""


    # Ask Groq for JSON instead of tool-based structured output
    json_llm = llm.bind(
        response_format={
            "type": "json_object"
        }
    )


    response = json_llm.invoke(prompt)


    try:

        data = json.loads(response.content)

        jobs = data.get("jobs", [])

        # Basic validation
        valid_jobs = []

        for job in jobs:

            if not isinstance(job, dict):
                continue

            job.setdefault("title", "Not specified")
            job.setdefault("company", "Not specified")
            job.setdefault("location", "Not specified")
            job.setdefault("experience", "Not specified")
            job.setdefault("salary", "Not specified")
            job.setdefault("skills", [])
            job.setdefault("match_score", 0)
            job.setdefault("reason", "Not specified")
            job.setdefault("url", "Not specified")

            # Keep score between 0 and 100
            try:
                job["match_score"] = max(
                    0,
                    min(
                        100,
                        int(job["match_score"])
                    )
                )
            except (ValueError, TypeError):
                job["match_score"] = 0

            valid_jobs.append(job)


        return {
            "analyzed_jobs": valid_jobs
        }


    except json.JSONDecodeError:

        return {
            "analyzed_jobs": []
        }