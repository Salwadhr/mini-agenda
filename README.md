# mini-agenda

Une petite application Flask pour gérer des événements avec authentification et sessions temporisées.

---


- Python 3.10+ installé
- Modules Python :
```bash
pip install flask flask-login
Lancer l'application

Cloner le projet :

git clone https://github.com/ton-nom-utilisateur/mini-agenda-urel.git
cd mini-agenda-urel

Installer les dépendances si ce n’est pas fait :

pip install -r requirements.txt

Lancer le serveur Flask :

python python.py

Ouvrir votre navigateur à l’adresse :

http://127.0.0.1:5000
🔑 Authentification

Utilisateur : admin

Mot de passe : motdepasse

La session expire automatiquement après 5 minutes d’inactivité.

✨ Fonctionnalités

Ajouter, modifier, supprimer des événements

Affichage de la liste des événements

Authentification et session automatique

Gestion simple de la base SQLite

📂 Structure du projet
mini-agenda-urel/
│
├─ python.py           # Script principal Flask
├─ agenda.db           # Base de données SQLite
├─ templates/          # Templates HTML
│   ├─ index.html
│   └─ login.html
├─ static/             # CSS, JS, images (optionnel)
└─ README.md
⚡ Astuce pour l’usage quotidien

Pour lancer l’app sans tout reconfigurer à chaque fois, il suffit de :

python python.py

Puis ouvrir le navigateur à http://127.0.0.1:5000 et se connecter.
