import os
import time
import traceback

# --- Environment Variables (ADD THESE AT THE VERY TOP) ---
# Use the OpenAI standard names as LiteLLM often looks for these for compatible endpoints
# Use the 'ollama/<model>' format for clarity with LiteLLM
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1" # Use the v1 endpoint for OpenAI compatibility
os.environ["OPENAI_MODEL_NAME"] = "ollama/llama3"        # Explicitly mention ollama provider and model
os.environ["OPENAI_API_KEY"] = "NA"                       # Required by LiteLLM, value doesn't matter for Ollama
print("--- Set OPENAI_API_BASE, OPENAI_MODEL_NAME, OPENAI_API_KEY environment variables ---")
# --- End Environment Variables ---

# --- LiteLLM Verbose Logging ---
try:
    import litellm
    litellm.set_verbose = True
    print("--- Enabled LiteLLM verbose logging ---")
except ImportError:
    print("--- LiteLLM not found, cannot enable verbose logging ---")
    litellm = None
except Exception as e:
    print(f"--- Error enabling LiteLLM verbose logging: {e} ---")
# --- End Logging ---

from crewai import Crew, Process
from langchain_ollama import ChatOllama

# Import agent and task creation functions
from agents.data_agent import create_data_agent
from agents.strategy_agent import create_strategy_agent
from agents.report_agent import create_report_agent
from tasks.data_tasks import data_collection_task
from tasks.strategy_tasks import strategy_optimization_task
from tasks.report_tasks import performance_report_task

# --- Configuration ---
# Ensure this model name MATCHES the one in OPENAI_MODEL_NAME if using that format
OLLAMA_MODEL = 'ollama/llama3' # Use the same name as in the env var for consistency
# OLLAMA_MODEL = 'llama3' # Alternatively, try using just the base name and rely on base_url

OLLAMA_BASE_URL = "http://localhost:11434" # Keep this for ChatOllama direct init

# Create output directory if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")

def get_llm():
    """Initializes the ChatOllama LLM."""
    # Use the model name defined in CONFIGURATION above
    model_to_init = OLLAMA_MODEL
    print(f"--- Initializing LLM: {model_to_init} ---")
    try:
        llm = ChatOllama(
            model=model_to_init, # Use the consistent model name
            base_url=OLLAMA_BASE_URL,
            temperature=0.1
        )
        # Optional: Test connection
        from langchain_core.messages import HumanMessage
        test_message = [HumanMessage(content="Respond with 'Connected'")]
        try:
            response = llm.invoke(test_message).content.strip()
            print(f"--- LLM Connection Test Response: '{response}' ---")
        except Exception as invoke_err:
            print(f"--- WARNING: LLM Connection Test FAILED for {model_to_init}: {invoke_err} ---")
            # Don't raise here, maybe the main execution will still work

        print(f"--- Successfully initialized {model_to_init} ---")
        return llm
    except Exception as e:
        print(f"--- FATAL: Failed to initialize LLM ({model_to_init}) ---")
        print(f"Error: {e}")
        print("Troubleshooting:")
        print("1. Ensure Ollama is running ('ollama serve').")
        print(f"2. Ensure the model for '{OLLAMA_MODEL}' is installed ('ollama list').")
        print(f"3. Check Ollama base URL: {OLLAMA_BASE_URL}")
        print(f"4. Check environment variables at the top of main.py")
        raise

def run_crew():
    """Sets up and runs the CrewAI crew."""
    llm = get_llm()

    data_collector = create_data_agent(llm)
    strategist = create_strategy_agent(llm)
    reporter = create_report_agent(llm)

    task1 = data_collection_task(data_collector)
    task2 = strategy_optimization_task(strategist, context_task=task1)
    task3 = performance_report_task(reporter, context_task=task2)

    marketing_crew = Crew(
        agents=[data_collector, strategist, reporter],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        llm=llm,  # Explicitly pass the configured LLM instance
        verbose=True # Keep boolean verbose setting
    )

    print("\n---Starting Marketing Optimization Crew ---")
    start_time = time.time()
    results = marketing_crew.kickoff()
    end_time = time.time()
    print(f"\n--- Crew Execution Finished ---")
    print(f"Execution Time: {end_time - start_time:.2f} seconds")
    return results

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Marketing Campaign Optimization System")
    print("="*50 + "\n")

    final_report_content = None
    try:
        final_report_content = run_crew()
        print("\n" + "="*50)
        print("Final Performance Report Content:")
        print("="*50 + "\n")
        print(final_report_content)
        print("\n" + "="*50)
        print("Report saved to: output/performance_report.md")
        print("Raw data saved to: output/campaign_metrics.json")
        print("Strategy output saved to: output/strategy_adjustment.json")
        print("="*50 + "\n")

    except Exception as e:
        print("\n" + "❌" * 25)
        print("SYSTEM FAILURE DURING CREW EXECUTION")
        print("❌" * 25 + "\n")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        print("\n--- Traceback ---")
        traceback.print_exc()
        print("--- End Traceback ---")
        print("\n--- Review LiteLLM verbose logs above for clues ---")