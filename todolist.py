"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

# Librairie(s) utilisée(s)
from flask import *
import secrets
import bdd.bdd as bdd


class ToDoList:

    def __init__(self):
        """Constructeur"""
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.app.secret_key = secrets.token_urlsafe(16)

        # Initialisation de la base de données
        self.bdd_path = "bdd/todo.sqlite"

        self.accounts = bdd.Accounts(self.bdd_path)
        self.tasks = bdd.Tasks(self.bdd_path)
        self.types = bdd.Types(self.bdd_path)
        self.priorities = bdd.Priorities(self.bdd_path)
        self.states = bdd.States(self.bdd_path)

    def run(self):
        """Lance le serveur web"""
        self.app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)



