import dropbox
import os
from dotenv import load_dotenv
from dropbox.exceptions import ApiError

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer le token d'accès Dropbox depuis le fichier .env
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')

# Vérifier que le token est bien chargé
if not DROPBOX_ACCESS_TOKEN:
    raise ValueError("Le token d'accès Dropbox n'est pas défini dans le fichier .env")

# Connexion à Dropbox
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def upload_to_dropbox(local_file_path, dropbox_path):
    """
    Upload un fichier vers Dropbox.
    Si l'upload échoue, retourne un message d'erreur.
    """
    try:
        # Lecture du fichier local
        with open(local_file_path, "rb") as f:
            # Envoi du fichier à Dropbox
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
        print(f"Fichier téléchargé : {local_file_path} vers {dropbox_path}")
        return f"Fichier téléchargé : {local_file_path} vers {dropbox_path}"
    except ApiError as e:
        # Si un problème d'API survient, affiche l'erreur
        if e.error.is_path_conflict():
            print(f"Conflit de chemin : {e}")
            return f"Erreur : Conflit de chemin lors du téléchargement du fichier"
        elif e.user_message_text:
            print(f"Erreur d'API : {e.user_message_text}")
            return f"Erreur d'API : {e.user_message_text}"
        else:
            print(f"Erreur Dropbox inconnue : {e}")
            return f"Erreur Dropbox inconnue : {e}"

def download_from_dropbox(dropbox_path, local_file_path):
    """
    Télécharge un fichier depuis Dropbox vers un chemin local.
    """
    try:
        # Téléchargement du fichier de Dropbox
        metadata, res = dbx.files_download(dropbox_path)
        with open(local_file_path, "wb") as f:
            f.write(res.content)
        print(f"Fichier téléchargé depuis Dropbox : {dropbox_path} vers {local_file_path}")
        return f"Fichier téléchargé depuis Dropbox : {dropbox_path} vers {local_file_path}"
    except ApiError as e:
        # Si un problème d'API survient, affiche l'erreur
        print(f"Erreur API lors du téléchargement : {e}")
        return f"Erreur API lors du téléchargement : {e}"

def list_files_in_dropbox(folder_path):
    """
    Liste les fichiers dans un dossier Dropbox.
    """
    try:
        # Liste des fichiers dans le dossier
        result = dbx.files_list_folder(folder_path)
        files = result.entries
        file_names = [file.name for file in files]
        print(f"Fichiers dans {folder_path} : {file_names}")
        return file_names
    except ApiError as e:
        print(f"Erreur API lors de la liste des fichiers : {e}")
        return f"Erreur API lors de la liste des fichiers : {e}"

