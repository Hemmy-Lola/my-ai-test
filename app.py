import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv 
from dropbox_utils import upload_to_dropbox, download_from_dropbox
from PyPDF2 import PdfReader
import docx

load_dotenv()

app = Flask(__name__)

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)

def extract_text_from_file(file_path):
    """Extraire le texte d'un fichier PDF, DOCX ou TXT."""
    text = ""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    return text

@app.route('/embed', methods=['POST'])
def route_embed():
    """Route pour télécharger et intégrer un fichier."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    local_path = os.path.join(TEMP_FOLDER, file.filename)
    file.save(local_path)

    dropbox_path = f"/{file.filename}"
    upload_to_dropbox(local_path, dropbox_path)

    text = extract_text_from_file(local_path)

    os.remove(local_path)

    if text:
        return jsonify({"message": "File embedded successfully", "text_preview": text[:200]}), 200
    return jsonify({"error": "File embedding unsuccessful"}), 400

@app.route('/query', methods=['POST'])
def route_query():
    """Route pour interroger les fichiers intégrés."""
    data = request.get_json()
    prompt = data.get('query')

    if prompt:
        response = f"Mock response for query: {prompt}"
        return jsonify({"message": response}), 200
    return jsonify({"error": "No query provided"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)