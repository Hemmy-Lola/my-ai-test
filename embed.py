import os
from datetime import datetime
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from get_vector_db import get_vector_db
import docx

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

def save_file(file):
    ct = datetime.now()
    ts = ct.timestamp()
    filename = str(ts) + "_" + secure_filename(file.filename)
    file_path = os.path.join(TEMP_FOLDER, filename)
    file.save(file_path)

    return file_path

def extract_text_from_file(file_path):
    """Extraire le texte d'un fichier PDF, DOCX ou TXT."""
    text = ""
    if file_path.endswith('.pdf'):
        loader = UnstructuredPDFLoader(file_path=file_path)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
        chunks = text_splitter.split_documents(data)
        text = "\n".join([chunk["text"] for chunk in chunks])
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    return text

def embed(file):
    if file.filename != '' and file and allowed_file(file.filename):
        file_path = save_file(file)
        text = extract_text_from_file(file_path)
        
        if text:
            db = get_vector_db()
            chunks = text.split("\n")  
            db.add_documents(chunks)
            db.persist()
            os.remove(file_path)

            return True

    return False
