from crewai import Task

# Will take care of the strategy optimization task 

def strategy_optimization_task(agent, context_task):
    """Creates the task for optimizing campaign strategy."""
    return Task(
        description=(
            "1. Take the JSON string output from the data collection task as input.\n"
            "2. Pass this JSON string directly to the 'Bid Adjustment Tool'.\n"
            "3. Report the JSON output provided by the 'Bid Adjustment Tool', which includes "
            "the original metrics, the calculated adjustment_factor, and the reason."
        ),
        expected_output=(
            "A JSON string containing the analysis result from the 'Bid Adjustment Tool', "
            "including 'input_metrics', 'adjustment_factor', and 'reason'."
        ),
        agent=agent,
        context=[context_task], # Depends on the data collection task
        output_file="output/strategy_adjustment.json" # Save strategy tool output
    )