from crewai.tools import BaseTool
import json

class BidAdjustmentTool(BaseTool):
    name: str = "Bid Adjustment Tool"
    description: str = (
        "Analyzes marketing metrics (CPC, CTR) from a JSON string input "
        "and suggests a bid adjustment factor (e.g., 1.1 for +10%, 0.9 for -10%)."
        "Input must be a JSON string containing at least 'cpc' and 'ctr'."
    )

    def _run(self, metrics_json: str) -> str:
        """Calculates a bid adjustment based on metrics."""
        print(f"\n--- Executing BidAdjustmentTool with input: {metrics_json} ---")
        try:
            metrics = json.loads(metrics_json)
        except json.JSONDecodeError:
            print("--- Error: Invalid JSON input received by BidAdjustmentTool ---")
            return json.dumps({"error": "Invalid JSON input", "adjustment_factor": 1.0})
        except TypeError:
             print("--- Error: Input was not a string for JSON decoding ---")
             return json.dumps({"error": "Invalid input type, expected JSON string", "adjustment_factor": 1.0})


        if not isinstance(metrics, dict) or 'cpc' not in metrics or 'ctr' not in metrics:
            print("--- Error: Missing 'cpc' or 'ctr' in parsed metrics ---")
            return json.dumps({"error": "Missing required keys 'cpc' or 'ctr'", "adjustment_factor": 1.0})

        try:
            cpc = float(metrics['cpc'])
            ctr = float(metrics['ctr'])
        except (ValueError, TypeError):
             print("--- Error: Non-numeric values for 'cpc' or 'ctr' ---")
             return json.dumps({"error": "Non-numeric metric values", "adjustment_factor": 1.0})


        adjustment_factor = 1.0 # Default: no change
        reason = "Metrics within acceptable range."

        if ctr < 1.5: # If Click-Through Rate is low
            adjustment_factor = 1.15 # Increase bid significantly
            reason = f"Low CTR ({ctr} < 1.5), increasing bid factor."
        elif cpc > 1.5: # If Cost Per Click is high
            adjustment_factor = 0.90 # Decrease bid
            reason = f"High CPC ({cpc} > 1.5), decreasing bid factor."
        elif ctr > 4.0: # If CTR is very high (good performance)
             adjustment_factor = 1.05 # Slight increase maybe
             reason = f"High CTR ({ctr} > 4.0), slight bid factor increase considered."


        result = {
            "input_metrics": metrics,
            "adjustment_factor": round(adjustment_factor, 2),
            "reason": reason
        }
        print(f"--- Bid Adjustment Result: {result} ---")
        # Return results as a JSON string
        return json.dumps(result)