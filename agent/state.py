from typing import TypedDict


class AgentState(TypedDict):
    user_query: str
    query_analysis: str
    search_query: str
    search_results: list
    analyzed_jobs: list
    final_answer: str