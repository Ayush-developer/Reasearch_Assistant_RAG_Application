import subprocess
import sys

def run_script(script_path, *args):
    """
    Run a Python script located at script_path with optional arguments.
    """
    # Use the absolute path for the scripts
    result = subprocess.run([sys.executable, script_path] + list(args), capture_output=True, text=True)

def run_ai_script(query):
    """
    Run ai.py code after preprocessing step, passing the query.
    """
    try:
        from ai import main as ai_main
        ai_main(query)  # Pass query as an argument to main()
    except Exception as e:
        print(f"Error in executing ai.py: {e}")

if __name__ == "__main__":
    # Get query from command-line argument
    query = sys.argv[1] if len(sys.argv) > 1 else "default query"

    # Absolute paths to the scripts
    fetch_script = '/Users/ayushdeb/Desktop/pg/scripts/fetches.py'
    preprocess_script = '/Users/ayushdeb/Desktop/pg/scripts/preprocess.py'

    # Run fetches.py with query
    run_script(fetch_script, query)

    # Run preprocess.py
    run_script(preprocess_script)

    # Run the AI logic in ai.py
    run_ai_script(query)  # Pass the query to ai.py

