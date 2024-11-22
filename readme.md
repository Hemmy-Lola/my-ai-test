# My AI Test Application

Ce projet est une application Flask permettant de télécharger des fichiers, de les envoyer à Dropbox et d'en extraire du texte pour un traitement ultérieur.

## Prérequis

Avant de démarrer l'application, assurez-vous que les éléments suivants sont installés sur votre machine :

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- Un compte Dropbox avec un [token d'accès Dropbox](https://www.dropbox.com/developers/apps/create)
- **ChromaDB** pour la gestion des embeddings
- **Ollama** pour le traitement des modèles de langage (par exemple, le modèle Mistral)
- **Flask** pour créer l'API web

### Installation des dépendances

Clonez ce dépôt et installez les dépendances requises en utilisant `pip`.

```bash
git clone https://github.com/yourusername/my-ai-test.git
cd my-ai-test
python -m venv venv  # Créer un environnement virtuel
source venv/bin/activate  # Pour Linux/MacOS
venv\Scripts\activate  # Pour Windows
pip install -r requirements.txt
