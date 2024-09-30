from flask import Flask, render_template, request, redirect, flash
import subprocess
import os
import requests
app = Flask(__name__)
app.secret_key = 'your_secret_key'

process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_config', methods=['POST'])
def upload_config():
    file = request.files['config_file']
    if file.filename == '':
        flash('No file selected!')
        return redirect(request.url)

    # Create the /data directory if it doesn't exist
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Save the file in the /data directory
    file_path = os.path.join(data_dir, 'config.yaml')
    file.save(file_path)

    flash('Configuration uploaded successfully!')
    return redirect('/')


@app.route('/start_server')
def start_server():
    global process
    if process is None:
        process = subprocess.Popen(["python3", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        flash('Server started successfully!')
    else:
        flash('Server is already running.')
    return redirect('/')

@app.route('/stop_server')
def stop_server():
    global process
    if process:
        process.terminate()
        process = None
        flash('Server stopped.')
    else:
        flash('No server is running.')
    return redirect('/')
@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.form['question']
    question_url = "http://0.0.0.0:9000/v1/pw_ai_answer"  # Make sure this points to the correct port
    data_prompt = {
        "prompt": question
    }
    r=requests.post(question_url,data=data_prompt)
    response=r.text
    return render_template('index.html', answer=response)


if __name__ == '__main__':
    app.run(debug=True)
