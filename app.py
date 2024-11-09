from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Use the absolute path to run_pipeline.py
    result = subprocess.run(
        ['/Users/ayushdeb/opt/anaconda3/bin/python', '/Users/ayushdeb/Desktop/pg/scripts/run_pipeline.py', user_query],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    # Return the output of the pipeline as a response
    return jsonify({"response": result.stdout.strip()})


if __name__ == '__main__':
    app.run(debug=True)
