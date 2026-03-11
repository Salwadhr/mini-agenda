from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret123"  # clé pour sessions

# Expiration automatique de session après 5 minutes
app.permanent_session_lifetime = timedelta(minutes=5)

DB_NAME = "agenda.db"

# --- Initialisation de la base ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS evenements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_evenement DATE NOT NULL,
            heure_evenement TIME NOT NULL,
            titre TEXT NOT NULL,
            description TEXT,
            auteur TEXT NOT NULL,
            type_event TEXT NOT NULL,
            notification_envoyee BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # utilisateur simple
        if username == "admin" and password == "motdepasse":
            session.permanent = True  # session limitée à app.permanent_session_lifetime
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template("login.html", erreur="Utilisateur ou mot de passe incorrect")
    return render_template("login.html", erreur=None)

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()  # supprime toutes les infos de session
    return redirect(url_for('login'))

# --- Vérification session ---
def check_auth():
    return 'user' in session

# --- Page principale ---
@app.route('/')
def index():
    if not check_auth():
        return redirect(url_for('login'))
    return render_template("index.html")

# --- Routes événements ---
@app.route('/evenements', methods=['GET'])
def get_evenements():
    if not check_auth():
        return jsonify({"erreur": "Non autorisé"}), 401
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM evenements")
    rows = c.fetchall()
    conn.close()
    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "date_evenement": row[1],
            "heure_evenement": row[2],
            "titre": row[3],
            "description": row[4],
            "auteur": row[5],
            "type_event": row[6],
            "notification_envoyee": row[7]
        })
    return jsonify(events)

@app.route('/evenements/ajouter', methods=['POST'])
def ajouter_evenement():
    if not check_auth():
        return jsonify({"erreur": "Non autorisé"}), 401
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO evenements (date_evenement, heure_evenement, titre, description, auteur, type_event)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['date_evenement'],
        data['heure_evenement'],
        data['titre'],
        data.get('description', ''),
        data['auteur'],
        data['type_event']
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Événement ajouté avec succès"}), 201

@app.route('/evenements/supprimer/<int:id>', methods=['DELETE'])
def supprimer_evenement(id):
    if not check_auth():
        return jsonify({"erreur": "Non autorisé"}), 401
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM evenements WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Événement supprimé"}), 200

@app.route('/evenements/modifier/<int:id>', methods=['PUT'])
def modifier_evenement(id):
    if not check_auth():
        return jsonify({"erreur": "Non autorisé"}), 401
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE evenements SET
        date_evenement = ?, heure_evenement = ?, titre = ?,
        description = ?, auteur = ?, type_event = ?
        WHERE id = ?
    ''', (
        data['date_evenement'],
        data['heure_evenement'],
        data['titre'],
        data.get('description', ''),
        data['auteur'],
        data['type_event'],
        id
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Événement modifié"}), 200

if __name__ == '__main__':
    app.run(debug=True)