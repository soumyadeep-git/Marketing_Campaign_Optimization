from crewai import Agent
from langchain_ollama import ChatOllama # Use ChatOllama
from tools.strategy_tools import BidAdjustmentTool

def create_strategy_agent(llm: ChatOllama):
    """Creates the Campaign Strategy Optimization Agent."""
    return Agent(
        role="Campaign Optimization Strategist",
        goal=(
            "Analyze incoming campaign performance data (passed as context). "
            "Use the Bid Adjustment Tool to calculate a necessary bid adjustment factor. "
            "Formulate a concise recommendation based on the tool's output."
        ),
        backstory=(
            "You are a data-driven strategist focused on ROI. You receive performance data, "
            "use a specific tool to calculate bid adjustments, and then report the "
            "tool's findings along with its reasoning."
        ),
        llm=llm,
        tools=[BidAdjustmentTool()], # Provide an instance of the tool
        allow_delegation=False,
        verbose=True,
        max_iter=3 # Limit iterations
    )