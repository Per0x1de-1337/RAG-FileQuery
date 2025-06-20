from flask import Flask, render_template, request, flash
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY environment variable is not set.")

RAG_API_URL = os.getenv('RAG_API_URL')
if not RAG_API_URL:
    raise RuntimeError("RAG_API_URL environment variable is not set.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form.get('question')
    if not question:
        flash('Please enter a question.')
        return render_template('index.html')

    question_endpoint = f"{RAG_API_URL}/v1/pw_ai_answer"
    answer = None
    try:
        response = requests.post(
            question_endpoint,
            json={"prompt": question},
            timeout=120
        )
        response.raise_for_status()
        answer_data = response.json()
        answer = answer_data.get("response", "No 'response' key found in the API answer.")

    except requests.exceptions.RequestException as e:
        flash(f"Error connecting to the RAG API: {e}")
        print(f"Error making request to {question_endpoint}: {e}")
    except Exception as e:
        flash(f"An unexpected error occurred: {e}")
        print(f"An unexpected error in ask_question: {e}")

    return render_template('index.html', question=question, answer=answer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)