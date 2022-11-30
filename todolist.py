"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

import secrets

# Librairie(s) utilisée(s)
from flask import *

from modules import accounts_manager
from modules.tasks_utils import *

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
    if request.endpoint not in ["index", "static", None] and \
            request.method != "POST" and \
            not accounts_manager.get_account(session.get("username")):
        return redirect(url_for("index"))


@app.route("/")
def index():
    """Page d'accueil"""
    user = accounts_manager.get_account(session.get("username"))
    return render_template("accueil.html", user=user)


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
def add_task():
    """Ajoute une tâche"""
    user = accounts_manager.get_account(session.get("username"))

    name_task = request.form["nom"]
    description = request.form["description"]
    deadline = request.form["echeance"]
    type_tache = request.form["type_tache"]

    deadline_micro = TasksTimeUtils(deadline).get_microseconds()

    tasks_table = Database().tasks
    tasks_table.add_task(user.get_user_id(), name_task, description, deadline_micro, type_tache, 1, 1)

    user.refresh()

    return redirect(url_for("index"))


@app.route("/delete_task", methods=["get"])
def delete_task():
    """Supprime une tâche"""
    user = accounts_manager.get_account(session.get("username"))

    task_id = int(request.args.get("id"))

    tasks_table = Database().tasks
    tasks_table.delete_task(task_id)

    user.remove_task(task_id)

    return redirect(url_for("index"))


@app.route("/edit_task", methods=["post"])
def edit_task():
    """Modifie une tâche"""
    user = accounts_manager.get_account(session.get("username"))

    task_id = request.form["task_id"]
    name_task = request.form["nom"]
    description = request.form["description"]
    deadline = request.form["echeance"]
    type_tache = request.form["type_tache"]

    deadline_micro = TasksTimeUtils(deadline).get_microseconds()

    user.update_task(task_id, name_task, description, deadline_micro, type_tache, 1, 1)

    return redirect(url_for("index"))


@app.route("/show_tasks", methods=["get"])
def show_tasks():
    """Affiche les tâches"""
    user = accounts_manager.get_account(session.get("username"))
    filter_id = request.args.get("filter")
    user.set_filter(int(filter_id))

    return redirect(url_for("index"))


@app.route("/add_type", methods=["post"])
def add_type():
    """Ajoute un type de tâche"""
    user = accounts_manager.get_account(session.get("username"))

    type_name = request.form["type_name"]

    types_table = Database().types
    types_table.add_type(type_name, user.get_user_id())

    user.refresh()

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)
