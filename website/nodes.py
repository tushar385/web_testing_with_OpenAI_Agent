from flask import Flask, request, jsonify, render_template
import openai, os, json, datetime, pytz, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.models.model import get_completion
from config.logs.logger import *

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'config', 'templates'))
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found in environment variables")


@app.route("/")

def home():
    return render_template('home.html') 



@app.route("/happy_path", methods=["GET", "POST"])
def happy_path():
    if request.method == "POST":
        clear_logs()  
        data = request.json
        url = data.get("url")
        prompt = data.get("prompt")
        if not url or not prompt:
            return jsonify({"error": "URL and prompt are required"}), 400
        
        full_prompt = f"Navigate to the following URL: {url}\n\n{prompt}"
        generated_text, cost_info = get_completion(full_prompt)
        try:
            generated_text = json.loads(generated_text)
        except json.JSONDecodeError:
            generated_text = generated_text

        timestamp = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
        logs = read_logs()
        response_json = {
            "generated_text": generated_text,
            "cost_info": cost_info,
            "timestamp": timestamp,
            "logs": logs
        }
        return jsonify(response_json)
    
    return render_template("happy_path.html")




if __name__ == '__main__':
    app.run(debug=True, port=5001)  # or any other available port