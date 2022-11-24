"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

# Librairie(s) utilisée(s)
from flask import *
import secrets

from bdd.bdd import Database

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = secrets.token_urlsafe(16)

# Initialisation de la base de données
bdd_path = "bdd/todo.sqlite"
bdd = Database(bdd_path)


@app.route("/")
def accueil():
    """Page d'accueil"""
    return render_template("accueil.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)



