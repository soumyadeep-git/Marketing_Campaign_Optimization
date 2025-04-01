from crewai import Task

# this will take care of the collection of the data

def data_collection_task(agent):
    """Creates the task for collecting marketing data."""
    return Task(
        description=(
            "Access and execute the 'Marketing Data Collector Tool' to fetch the most recent "
            "campaign performance metrics. Ensure the output is the direct result from the tool."
        ),
        expected_output=(
            "A JSON string containing the latest campaign metrics "
            "(timestamp, cpc, ctr, conversions, spend), exactly as provided by the tool."
        ),
        agent=agent,
        output_file="output/campaign_metrics.json" # Save raw tool output
    )