from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes import (
    analyze_query,
    create_search_query,
    search_job_node,
    analyze_jobs
)


builder = StateGraph(AgentState)

builder.add_node(
    "analyze_query",
    analyze_query
)

builder.add_node(
    "create_search_query",
    create_search_query
)

builder.add_node(
    "search_jobs",
    search_job_node
)

builder.add_node(
    "analyze_jobs",
    analyze_jobs
)


builder.add_edge(
    START,
    "analyze_query"
)

builder.add_edge(
    "analyze_query",
    "create_search_query"
)

builder.add_edge(
    "create_search_query",
    "search_jobs"
)

builder.add_edge(
    "search_jobs",
    "analyze_jobs"
)

builder.add_edge(
    "analyze_jobs",
    END
)


graph = builder.compile()