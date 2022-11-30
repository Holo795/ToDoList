from flask import *  # for flash messages

from bdd.bdd import Database  # Accounts database gestion
import bcrypt  # for password hashing

from modules.tasks_utils import TasksUtils


class AccountsManager:
    """Classe pour gérer les comptes"""

    def __init__(self):
        """Constructeur"""
        self.accounts_table = Database().accounts
        self.accounts = []

    def login(self, request: Request) -> Response:
        """Connecte un utilisateur"""
        username = request.form.get("username")
        password = request.form.get("password")
        if account_bdd := self.accounts_table.get_account(username):
            account_bdd = account_bdd[0]
            if bcrypt.checkpw(password.encode('utf8'), account_bdd[2].encode('utf8')):
                self.add_user(username)
                return redirect(url_for("index"))
            else:
                flash("Mot de passe et/ou identifiant incorrect", "error")
        else:
            flash("Mot de passe et/ou identifiant incorrect", "error")
        return redirect(url_for("index"))

    def logout(self) -> Response:
        """Déconnecte un utilisateur"""
        self.remove_user(session["username"])
        session.pop("username", None)
        return redirect(url_for("index"))

    def register(self, request: Request) -> Response:
        """Enregistre un utilisateur"""
        username = request.form.get("username")
        password = request.form.get("password")
        if self.accounts_table.get_account(username):
            flash("Cet utilisateur existe déjà", "error")
        else:
            self.accounts_table.add_account(username,
                                            bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8'))
            self.add_user(username)
        return redirect(url_for("index"))

    def add_user(self, username: str):
        session["username"] = username

        account = Account(username)
        account.refresh()

        if self.get_account(username):
            self.accounts.remove(self.get_account(username))

        self.accounts.append(account)
        flash("Vous êtes connecté", "success")

    def remove_user(self, username: str):
        self.accounts.remove(self.get_account(username))

    def get_account(self, username: str):
        return next((account for account in self.accounts if account.username == username), False)


class Account:
    """Classe pour un compte utilisateur"""

    def __init__(self, username: str):
        """Constructeur"""
        self.username = username
        self.user_id = None

        self.tasks = []
        self.types = []

        self.filter = -1

    def refresh(self):
        """Rafraîchit les données de l'utilisateur"""
        accounts_table = Database().accounts
        tasks_table = Database().tasks
        types_table = Database().types

        self.set_user_id(accounts_table.get_account(self.username)[0][0])

        self.tasks.clear()
        self.tasks = tasks_table.get_tasks(self.user_id)

        self.types.clear()
        self.types = types_table.get_all_types(self.user_id)

    def remove_task(self, id: int):
        """Supprime une tâche de l'utilisateur"""
        for task in self.tasks:
            if task[0] == id:
                self.tasks.remove(task)
                break

    def update_task(self, idTask: int, name: str, description: str, deadline_date: str, idType: int, idPriority: int,
                    idState: int):
        """Met à jour une tâche"""
        tasks_table = Database().tasks
        tasks_table.edit_task(idTask, name, description, deadline_date, idType, idPriority, idState)

        self.tasks = tasks_table.get_tasks(self.user_id)

    def get_html_tasks(self) -> list:
        """Renvoie la liste des tâches formattées de l'utilisateur"""
        return TasksUtils(self.get_tasks()).get_formatted_tasks()

    def get_tasks(self) -> list:
        """Renvoie la liste des tâches de l'utilisateur"""
        if self.filter == -1:
            print(self.tasks)
            return self.tasks
        elif self.filter in [type[0] for type in self.types]:
            return [task for task in self.tasks if task[6] == self.filter]
        else:
            return []

    def get_types(self) -> list:
        """Renvoie la liste des types de l'utilisateur"""
        return self.types

    def set_filter(self, filter: int):
        """Définit le filtre"""
        self.filter = filter
        
    def get_filter(self) -> int:
        """Renvoie le filtre actuel"""
        return self.filter

    def get_username(self) -> str:
        """Renvoie le nom d'utilisateur"""
        return self.username

    def get_user_id(self) -> int:
        """Renvoie l'identifiant de l'utilisateur"""
        return self.user_id

    def set_user_id(self, id: int):
        """Définit l'identifiant de l'utilisateur"""
        self.user_id = id
