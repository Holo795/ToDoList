from datetime import datetime

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
        if len(password) < 3:
            flash("Le mot de passe doit faire au moins 3 caractères", "error")
        elif len(username) > 20:
            flash("Le nom d'utilisateur ne doit pas depasser 20 caractères", "error")
        elif self.accounts_table.get_account(username):
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

        account.send_notification(f"Vous êtes connecté ! {account.get_username()}")

        account.notify_late_tasks()

        if self.get_account(username):
            self.accounts.remove(self.get_account(username))

        self.accounts.append(account)

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

        self.filter_type = -1
        self.filter_priority = -1

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

    def send_notification(self, msg):
        print(f"Notification envoyée à {self.username}: {msg}")
        flash(msg, f"notifier-{self.username}")

    def notify_late_tasks(self):
        for task in self.tasks:
            if task[4] < datetime.now().timestamp() and task[7] == 1:
                self.send_notification(f"La tâche {task[2]} est en retard !")

    def add_task(self, name: str, description: str, deadline_date: str, idType: int, idPriority: int, idState: int):
        """Ajoute une tâche à l'utilisateur"""
        tasks_table = Database().tasks
        tasks_table.add_task(self.user_id, name, description, deadline_date, idType, idPriority, idState)

        self.tasks = tasks_table.get_tasks(self.user_id)

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
        tasks_table.edit_task(idTask=idTask, name=name, description=description, deadline_date=deadline_date,
                              idType=idType, idPriority=idPriority, idState=idState)

        self.tasks = tasks_table.get_tasks(self.user_id)

    def validate_task(self, idTask: int, validate: bool):
        """Valide une tâche"""
        tasks_table = Database().tasks
        tasks_table.edit_task(idTask=idTask, success_date=datetime.now().timestamp() if validate else None,
                              idState=2 if validate else 1)

        self.tasks = tasks_table.get_tasks(self.user_id)

    def get_html_tasks(self) -> list:
        """Renvoie la liste des tâches formattées de l'utilisateur"""
        print(TasksUtils(self.get_tasks()).get_formatted_tasks())
        return TasksUtils(self.get_tasks()).get_formatted_tasks()

    def get_tasks(self) -> list:
        """Renvoie la liste des tâches de l'utilisateur triées par date d'échéance croissante"""
        if self.filter_type == -1 and self.filter_priority == -1:
            return sorted(self.tasks, key=lambda task: task[3], reverse=True)
        elif self.filter_type == -1:
            return sorted([task for task in self.tasks if task[7] == self.filter_priority], key=lambda task: task[3],
                          reverse=True)
        elif self.filter_priority == -1:
            return sorted([task for task in self.tasks if task[6] == self.filter_type], key=lambda task: task[3],
                          reverse=True)
        else:
            return sorted([task for task in self.tasks if task[6] == self.filter_type and task[7] ==
                           self.filter_priority], key=lambda task: task[3], reverse=True)

    def get_types(self) -> list:
        """Renvoie la liste des types de l'utilisateur"""
        return self.types

    def add_type(self, name: str):
        """Ajoute un type à l'utilisateur"""
        types_table = Database().types
        types_table.add_type(name, self.user_id)

        self.types = types_table.get_all_types(self.user_id)

    def remove_type(self, idType: int):
        """Supprime un type de l'utilisateur"""
        types_table = Database().types
        types_table.delete_type(idType)

        self.types = types_table.get_all_types(self.user_id)

    def set_filter_type(self, filter: int):
        """Définit le filtre"""
        self.filter_type = filter

    def get_filter_type(self) -> int:
        """Renvoie le filtre actuel"""
        return self.filter_type

    def set_filter_priority(self, filter: int):
        """Définit le filtre"""
        self.filter_priority = filter

    def get_priorities(self) -> list:
        """Renvoie la liste des priorités"""
        priorities_table = Database().priorities
        return priorities_table.get_all_priorities()

    def get_filter_priority(self) -> int:
        """Renvoie le filtre actuel"""
        return self.filter_priority

    def get_username(self) -> str:
        """Renvoie le nom d'utilisateur"""
        return self.username

    def get_user_id(self) -> int:
        """Renvoie l'identifiant de l'utilisateur"""
        return self.user_id

    def set_user_id(self, id: int):
        """Définit l'identifiant de l'utilisateur"""
        self.user_id = id
