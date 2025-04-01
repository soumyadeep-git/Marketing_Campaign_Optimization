from crewai import Agent
from langchain_ollama import ChatOllama # Use ChatOllama
from tools.data_tools import MarketingDataCollectorTool

def create_data_agent(llm: ChatOllama):
    """Creates the Marketing Data Collector Agent."""
    return Agent(
        role="Marketing Data Analyst",
        goal=(
            "Retrieve the latest marketing campaign performance metrics "
            "using the provided Marketing Data Collector Tool."
        ),
        backstory=(
            "You are an analyst responsible for fetching raw performance data. "
            "You rely solely on your specialized tool to get this information."
        ),
        llm=llm,
        tools=[MarketingDataCollectorTool()], # Provide an instance of the tool
        allow_delegation=False,
        verbose=True,
        max_iter=3 # Limit iterations in case of issues
    )