from crewai import Agent
from langchain_ollama import ChatOllama # Use ChatOllama

def create_report_agent(llm: ChatOllama):
    """Creates the Performance Reporting Agent."""
    return Agent(
        role="Marketing Performance Reporter",
        goal=(
            "Receive the analysis and bid adjustment recommendation from the Strategy Agent (passed as context). "
            "Generate a clear, concise performance summary report in Markdown format, "
            "highlighting the key metrics observed, the adjustment made, and the reason."
        ),
        backstory=(
            "You specialize in translating marketing data and strategy adjustments "
            "into easy-to-understand reports for stakeholders. You focus on clarity and actionability."
        ),
        llm=llm,
        tools=[], # This agent only synthesizes information, no tools needed here
        allow_delegation=False,
        verbose=True,
        max_iter=3 # Limit iterations
    )