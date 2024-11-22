# My AI Test Application

Ce projet est une application Flask permettant de télécharger des fichiers, de les envoyer à Dropbox, d'extraire du texte et de répondre à des questions en utilisant les techniques de **RAG (Retrieval-Augmented Generation)**. 

## Prérequis

Avant de démarrer l'application, assurez-vous que les éléments suivants sont installés sur votre machine :

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- Un compte Dropbox avec un [token d'accès Dropbox](https://www.dropbox.com/developers/apps/create)
- **ChromaDB** pour la gestion des embeddings
- **Ollama** pour le traitement des modèles de langage (par exemple, le modèle Mistral)
- **Flask** pour créer l'API web
- **PyPDF2**, **python-docx** et **Unstructured** pour manipuler les fichiers PDF, DOCX et TXT

---

## Installation des dépendances

Clonez ce dépôt et installez les dépendances requises en utilisant `pip`.

```bash
git clone https://github.com/yourusername/my-ai-test.git
cd my-ai-test
python -m venv venv  # Créer un environnement virtuel
source venv/bin/activate  # Pour Linux/MacOS
venv\Scripts\activate  # Pour Windows
pip install -r requirements.txt
```

Créez un fichier .env pour y stocker les variables d'environnement nécessaires :

```bash
plaintext
Copier le code
TEMP_FOLDER=./_temp
CHROMA_PATH=chroma
COLLECTION_NAME=local-rag
LLM_MODEL=mistral
TEXT_EMBEDDING_MODEL=nomic-embed-text
DROPBOX_ACCESS_TOKEN=Votre_Token_Dropbox
```

## Utilisation
### Démarrage de l'application
Lancez le serveur Flask avec la commande suivante :

```bash
Copier le code
python app.py
Le serveur sera accessible à l'adresse : http://127.0.0.1:8080.
```
## API Endpoints
1. Ajouter un fichier (/embed)

Méthode : POST
URL : http://127.0.0.1:8080/embed
Body (form-data) :
Clé : file (type fichier)
Exemple de réponse :

json
Copier le code
{
  "message": "File embedded successfully."
}
2. Poser une question (/query)

Méthode : POST
URL : http://127.0.0.1:8080/query
Body (raw, JSON) :

```bash
{
  "query": "Quels sont les dangers auxquels font face les coraux ?",
  "temperature": 0.7
}
```
Réponse :
```bash
{
  "response": "Les coraux font face à des dangers comme le réchauffement climatique, la pollution et la surpêche."
}
```

## Exemple de Test avec et sans RAG
### Document importé :
Le documentaire La beauté du monde sauvage explore les paysages naturels les plus impressionnants de la planète... [Voir contenu complet dans les fichiers].

### Question posée :
Quels sont les dangers auxquels les écosystèmes naturels font face ?
Réponses obtenues :
- Sans RAG :

Les écosystèmes naturels sont menacés par le réchauffement climatique, la pollution et la déforestation.

- Avec RAG :

Selon le documentaire, les écosystèmes naturels, tels que les forêts d'Amazonie et la Grande Barrière de Corail, sont menacés par des dangers tels que la déforestation, le réchauffement climatique et la pollution des océans. Un exemple poignant est le blanchiment des coraux causé par le changement climatique.

## Structure du projet
Voici un aperçu des fichiers principaux dans ce projet :

```bash
Copier le code
my-ai-test/
│
├── app.py                # Serveur Flask principal
├── embed.py              # Gestion de l'intégration des fichiers
├── query.py              # Gestion des requêtes RAG
├── get_vector_db.py      # Initialisation de la base de données vectorielle
├── dropbox_utils.py      # Fonctions pour interagir avec Dropbox
├── requirements.txt      # Liste des dépendances Python
├── .env                  # Variables d'environnement (non inclus dans Git)
├── README.md             # Documentation
└── _temp/                # Dossier temporaire pour les fichiers
```