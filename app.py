import os
import subprocess
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langchain.embeddings import OpenAIEmbeddings
from PyPDF2 import PdfReader 
import docx 

load_dotenv()

app = Flask(__name__)

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)

def query_ollama(model, prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", model, "-p", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() 
    except Exception as e:
        print(f"Error running Ollama: {e}")
        return None

def extract_text_from_file(file):
    file_path = os.path.join(TEMP_FOLDER, file.filename)
    file.save(file_path)

    text = ""
    if file.filename.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif file.filename.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    elif file.filename.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

    return text

def embed(file):
    text = extract_text_from_file(file)

    if text:
        embedding_model = OpenAIEmbeddings()

        embedded_text = embedding_model.embed(text)

        return embedded_text
    else:
        return None

@app.route('/embed', methods=['POST'])
def route_embed():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    embedded = embed(file)
    if embedded:
        return jsonify({"message": "File embedded successfully"}), 200

    return jsonify({"error": "File embedding unsuccessful"}), 400

@app.route('/query', methods=['POST'])
def route_query():
    data = request.get_json()
    prompt = data.get('query')

    if prompt:
        response = query_ollama("mistral", prompt)
        if response:
            return jsonify({"message": response}), 200
        return jsonify({"error": "Error processing the query"}), 400
    return jsonify({"error": "No query provided"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
