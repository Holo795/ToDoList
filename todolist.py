"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

import secrets
from datetime import timedelta

# Librairie(s) utilisée(s)
from flask import *

from bdd.bdd import Database
from modules import accounts_manager
from modules.tasks_utils import TasksUtils

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = secrets.token_urlsafe(16)

# Initialisation du gestionnaire de comptes
accounts_manager = accounts_manager.AccountsManager()


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("index"))


@app.before_request
def check_login():
    """Vérifie si l'utilisateur est connecté"""
    if request.endpoint not in ["index", "logout", "login", "register", "static", None] and \
            accounts_manager.get_account(session["username"]) is None:
        return redirect(url_for("index"))


@app.route("/")
def index():
    """Page d'accueil"""
    user = accounts_manager.get_account(session.get("username"))
    tasks = user.get_tasks() if user else []
    print(tasks)

    return render_template("accueil.html", user=user, tasks=tasks)


@app.route("/login", methods=["post"])
def login():
    return accounts_manager.login(request)


@app.route("/logout")
def logout():
    return accounts_manager.logout()


@app.route("/register", methods=["post"])
def register():
    return accounts_manager.register(request)


@app.route("/add_task", methods=["post"])
def add_task() -> list:
    """Ajoute une tâche"""
    name_task = session.get("nom")
    description = session.get("description")
    echeance = session.get("echeance")
    print(name_task)
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)
