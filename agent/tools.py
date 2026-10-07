import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_jobs(query: str):

    results = tavily.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    return results["results"]