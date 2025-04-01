import random
from datetime import datetime, timezone
from crewai.tools import BaseTool
import json

class MarketingDataCollectorTool(BaseTool):
    name: str = "Marketing Data Collector Tool"
    description: str = (
        "Collects simulated marketing campaign metrics. "
        "Returns a JSON string containing timestamp, CPC, CTR, conversions, and spend."
    )

    def _run(self) -> str:
        """Simulates fetching marketing data."""
        print("\n--- Executing MarketingDataCollectorTool ---")
        metrics = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'cpc': round(random.uniform(0.5, 1.8), 2),
            'ctr': round(random.uniform(1.0, 4.5), 2),
            'conversions': random.randint(5, 50),
            'spend': round(random.uniform(100.0, 600.0), 2)
        }
        print(f"--- Collected Metrics: {metrics} ---")
        # Return as a JSON string, as LLMs often handle strings better for inter-task data
        return json.dumps(metrics)