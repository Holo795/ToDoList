from datetime import datetime

import bcrypt  # for password hashing
from flask import *  # for flash messages

from bdd.bdd import Database  # Accounts database gestion
from modules.tasks_utils import TasksUtils  # for tasks gestion


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
            if bcrypt.checkpw(password.encode('utf8'), account_bdd[2].encode('utf8')):  # Check password
                self.add_user(username)
                return redirect(url_for("index"))
            else:
                flash("Mot de passe et/ou identifiant incorrect", "error")
        else:
            flash("Mot de passe et/ou identifiant incorrect", "error")
        return redirect(url_for("index"))

    def logout(self) -> Response:
        """Déconnecte un utilisateur"""
        self.remove_user(session["username"])  # Remove user from accounts list
        session.pop("username", None)  # remove the username from the session
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
            self.add_user(username)  # Connect user

            # Add default categories
            self.get_account(username).add_type("Maison")
            self.get_account(username).add_type("Travail")

        return redirect(url_for("index"))

    def add_user(self, username: str):
        """Add user to accounts list"""
        session["username"] = username

        account = Account(username)  # Create account
        account.refresh()  # Refresh tasks, categories, etc...

        account.send_notification(f"Vous êtes connecté ! {account.get_username()}")

        account.notify_late_tasks()

        if self.get_account(username):  # If user already exists
            self.accounts.remove(self.get_account(username))  # Remove old account

        self.accounts.append(account)

    def remove_user(self, username: str):
        """Remove user from accounts list"""
        self.accounts.remove(self.get_account(username))

    def get_account(self, username: str):
        """Return account from username"""
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

    def update_username(self, new_username):
        """Change l'username de l'utilisateur"""
        account_table = Database().accounts
        account_table.edit_account(self.user_id, username=new_username)
        self.username = new_username
        session["username"] = self.username

    def update_password(self, new_password):
        """Change le mot de passe de l'utilisateur"""
        account_table = Database().accounts
        password_crypt = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')

        account_table.edit_account(self.user_id, password=password_crypt)

    def send_notification(self, msg):
        """Envoie une notification a l'utilisateur"""
        flash(msg, f"notifier-{self.username}")

    def notify_late_tasks(self):
        """Notifie des taches en retard"""
        late_tasks = sum(task[4] < datetime.now().timestamp() and task[8] == 1 for task in self.tasks)
        if late_tasks > 0:
            self.send_notification(f"Vous avez {late_tasks} " + ("taches" if late_tasks != 1 else "tache") + " en "
                                                                                                             "retard")

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
        tasks_table.edit_task(idTask=idTask, success_date=int(datetime.now().timestamp()) if validate else None,
                              idState=2 if validate else 1)

        self.tasks = tasks_table.get_tasks(self.user_id)

    def archive_task(self, idTask: int):
        """Archive une tâche"""
        task = self.get_task(idTask)

        tasks_table = Database().tasks
        if task[8] == 2:
            tasks_table.edit_task(idTask=idTask, idState=3)
        else:
            tasks_table.edit_task(idTask=idTask, idState=3, success_date=int(datetime.now().timestamp()))

        self.tasks = tasks_table.get_tasks(self.user_id)

    def get_html_tasks(self) -> list:
        """Renvoie la liste des tâches formattées de l'utilisateur"""
        return TasksUtils(self.get_tasks()).get_formatted_tasks()

    def get_tasks(self) -> list:
        """Renvoie la liste des tâches de l'utilisateur filtrées"""
        if self.filter_type == -1 and self.filter_priority == -1:
            return self.tasks
        elif self.filter_type == -1:
            return [task for task in self.tasks if task[7] == self.filter_priority]
        elif self.filter_priority == -1:
            return [task for task in self.tasks if task[6] == self.filter_type]
        else:
            return [task for task in self.tasks if task[6] == self.filter_type and task[7] == self.filter_priority]

    def get_task(self, idTask: int) -> list:
        """Renvoie la tâche correspondant à l'id"""
        return [task for task in self.tasks if task[0] == idTask][0]

    def get_types(self) -> list:
        """Renvoie la liste des types de l'utilisateur"""
        return self.types

    def get_used_types(self) -> list:
        """Renvoie la liste des types utilisés par l'utilisateur"""
        return [task[6] for task in self.tasks]

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


class UserStats:
    """Classe permettant de gérer les statistiques d'un utilisateur"""

    def __init__(self, user: Account):
        self.user = user
        self.tasks = user.get_tasks()

    def get_user(self) -> Account:
        """Renvoie l'utilisateur"""
        return self.user

    def get_tasks_done_count(self, idType=None) -> int:
        """Renvoie le nombre de tâches terminées par catégorie"""
        if idType is None:
            return len([task for task in self.tasks if task[8] == 2])
        return len([task for task in self.tasks if task[8] == 2 and task[6] == idType])

    def get_tasks_in_progress_count(self, idType=None) -> int:
        """Renvoie le nombre de tâches en cours par catégorie"""
        if idType is None:
            return len([task for task in self.tasks if task[8] == 1])
        return len([task for task in self.tasks if task[8] == 1 and task[6] == idType])

    def get_tasks_done_on_time_count(self, idType=None) -> int:
        """Renvoie le nombre de tâches terminées à temps par catégorie"""
        if idType is None:
            return len([task for task in self.tasks if task[8] == 2 and task[4] >= task[5]])
        return len([task for task in self.tasks if task[8] == 2 and task[4] >= task[5] and task[6] == idType])

    def get_json_radar_chart(self) -> dict:
        """Renvoie les données pour le graphique radar"""
        types = self.user.get_types()

        tasks_done = [self.get_tasks_done_count(idType=type[0]) for type in types]
        tasks_in_progress = [self.get_tasks_in_progress_count(idType=type[0]) for type in types]
        tasks_done_on_time = [self.get_tasks_done_on_time_count(idType=type[0]) for type in types]

        return {
            "labels": [type[1] for type in types],
            "datasets": [
                {
                    "label": "Tâches terminées",
                    "data": tasks_done,
                    "backgroundColor": "rgba(255, 99, 132, 0.2)",
                    "borderColor": "rgba(255, 99, 132, 1)",
                    "borderWidth": 2
                },
                {
                    "label": "Tâches en cours",
                    "data": tasks_in_progress,
                    "backgroundColor": "rgba(54, 162, 235, 0.2)",
                    "borderColor": "rgba(54, 162, 235, 1)",
                    "borderWidth": 2
                },
                {
                    "label": "Tâches terminées à temps",
                    "data": tasks_done_on_time,
                    "backgroundColor": "rgba(75, 192, 192, 0.2)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "borderWidth": 2
                }
            ]
        }
