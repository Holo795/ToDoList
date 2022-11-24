"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

import secrets

# Librairie(s) utilisée(s)
from flask import *

from bdd.bdd import Database
from modules import accounts_manager

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = secrets.token_urlsafe(16)

# Initialisation de la base de données
bdd_path = "bdd/todo.sqlite"
bdd = Database(bdd_path)


@app.route("/")
def accueil():
    """Page d'accueil"""
    return render_template("accueil.html", login=session.get("USERNAME") is not None)


@app.route("/login", methods=["post"])
def login():
    user = accounts_manager.AccountsManager(path=bdd_path)
    return user.login(request)





def show_task():
    """Affiche les tâches dans le tableau"""
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)
