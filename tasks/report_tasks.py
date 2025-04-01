from crewai import Task

# this will take care of the performance_report_task

def performance_report_task(agent, context_task):
    """Creates the task for generating the performance report."""
    return Task(
        description=(
            "1. Review the JSON string output from the strategy optimization task (provided as context).\n"
            "2. Extract the key information: original metrics (CPC, CTR), the bid adjustment factor, and the reason.\n"
            "3. Generate a concise summary report in Markdown format. Include:\n"
            "    - A title (e.g., 'Campaign Performance Update')\n"
            "    - Timestamp from the original data (if available in context)\n"
            "    - Key Metrics Observed (CPC, CTR)\n"
            "    - Recommended Bid Adjustment Factor\n"
            "    - Reasoning for the adjustment."
        ),
        expected_output=(
            "A well-formatted Markdown report summarizing the campaign performance "
            "and the strategic bid adjustment applied."
        ),
        agent=agent,
        context=[context_task], # Depends on the strategy optimization task
        output_file="output/performance_report.md" # Save report as Markdown
    )