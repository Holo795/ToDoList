import sqlite3
import time

# abc library for abstract base classes
from abc import abstractmethod


class Database:
    """Classe principal de la gestion de la bdd"""

    def __init__(self):
        """Constructeur"""

        self.path = "bdd/todo.sqlite"

        self.accounts = Accounts_Table(self.path)
        self.tasks = Tasks_Table(self.path)
        self.types = Types_Table(self.path)
        self.priorities = Priorities_Table(self.path)
        self.states = States_Table(self.path)


class BddManager:
    """Classe pour faire le lien entre la base de données SQLite et le programme"""

    def __init__(self, path):
        """Constructeur"""
        self.path = path
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.create_table()

    def execute(self, request, parameters=None):
        """Exécute une requête SQL"""
        if parameters is None:
            self.cursor.execute(request)
        else:
            self.cursor.execute(request, parameters)
        self.connection.commit()
        return self.cursor.fetchall()

    @abstractmethod
    def create_table(self):
        """Méthode abstraite"""
        raise NotImplementedError("Méthode abstraite create_table non implémentée !")


class Tasks_Table(BddManager):
    """Classe pour gérer les tâches"""

    def __init__(self, path):
        """Constructeur"""
        super().__init__(path)

    def create_table(self):
        """Crée la table Taches"""
        self.execute("CREATE TABLE IF NOT EXISTS Tasks (idTask INTEGER NOT NULL UNIQUE, "
                     "idAccount INTEGER NOT NULL, "
                     "name TEXT NOT NULL, "
                     "description TEXT NOT NULL, "
                     "deadline_date	INTEGER NOT NULL, "
                     "success_date INTEGER NOT NULL, "
                     "idType INTEGER NOT NULL, "
                     "idPriority INTEGER NOT NULL, "
                     "idState INTEGER NOT NULL, "
                     "PRIMARY KEY(idTask AUTOINCREMENT), "
                     "FOREIGN KEY(idPriority) REFERENCES Priorities(idPriority), "
                     "FOREIGN KEY(idAccount) REFERENCES Accounts(idAccount), "
                     "FOREIGN KEY(idType) REFERENCES Types(idType), "
                     "FOREIGN KEY(idState) REFERENCES States(idState));")

    def get_tasks(self, idAccount):
        """Récupère les tâches d'un utilisateur"""
        return self.execute("SELECT * FROM Tasks WHERE idAccount = ?;", (idAccount,))

    def add_task(self, idAccount, name, description, deadline_date, success_date, idType, idPriority, idState):
        """Ajoute une tâche à un utilisateur"""
        return self.execute("INSERT INTO Tasks (idAccount, name, description, deadline_date, success_date, idType, "
                            "idPriority, idState) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                            (idAccount, name, description, deadline_date, success_date, idType, idPriority, idState))

    def edit_task(self, idTask, **kwargs):
        """Modifie une tâche d'un utilisateur"""
        request = "UPDATE Tasks SET "
        parameters = []
        for key, value in kwargs.items():
            request += f"{key} = ?, "
            parameters.append(value)
        request = f"{request[:-2]} WHERE idTask = ?;"
        parameters.append(idTask)
        return self.execute(request, tuple(parameters))


class Accounts_Table(BddManager):
    """Classe pour gérer les comptes dans la base de données"""

    def __init__(self, path):
        """Constructeur"""
        super().__init__(path)

    def create_table(self):
        """Crée la table Comptes"""
        self.execute("CREATE TABLE IF NOT EXISTS Accounts (idAccount INTEGER NOT NULL UNIQUE, "
                     "username TEXT NOT NULL CHECK(length(username) <= 20 AND length(username) > 3) UNIQUE, "
                     "password	TEXT NOT NULL CHECK(length(password) > 3 AND length(password) <= 16), "
                     "PRIMARY KEY(idAccount AUTOINCREMENT));")

    def add_account(self, username, password):
        """Ajoute un compte"""
        return self.execute("INSERT INTO Accounts (username, password) VALUES (?, ?);", (username, password))

    def get_account(self, username):
        """Récupère un compte"""
        return self.execute("SELECT * FROM Accounts WHERE username = ?;", (username,))

    def get_all_accounts(self):
        """Récupère tous les comptes"""
        return self.execute("SELECT * FROM Accounts;")

    def edit_account(self, username, password):
        """Modifie un compte"""
        return self.execute("UPDATE Accounts SET password = ? WHERE username = ?;", (password, username))

    def delete_account(self, username):
        """Supprime un compte"""
        return self.execute("DELETE FROM Accounts WHERE username = ?;", (username,))


class Types_Table(BddManager):
    """Classe pour gérer les types de tâches"""

    def __init__(self, path):
        """Constructeur"""
        super().__init__(path)

    def create_table(self):
        """Crée la table Types"""
        self.execute("CREATE TABLE IF NOT EXISTS Types (idType INTEGER NOT NULL UNIQUE, "
                     "name TEXT NOT NULL, "
                     "idAccount INTEGER NOT NULL, "
                     "PRIMARY KEY(idType AUTOINCREMENT));")

    def add_type(self, name):
        """Ajoute un type de tâche"""
        return self.execute("INSERT INTO Types (name) VALUES (?);", (name,))

    def get_type(self, name):
        """Récupère un type de tâche"""
        return self.execute("SELECT * FROM Types WHERE name = ?;", (name,))

    def get_all_types(self):
        """Récupère tous les types de tâche"""
        return self.execute("SELECT * FROM Types;")

    def edit_type(self, name, new_name):
        """Modifie un type de tâche"""
        return self.execute("UPDATE Types SET name = ? WHERE name = ?;", (new_name, name))

    def delete_type(self, name):
        """Supprime un type de tâche"""
        return self.execute("DELETE FROM Types WHERE name = ?;", (name,))


class Priorities_Table(BddManager):
    """Classe pour gérer les priorités de tâches"""

    def __init__(self, path):
        """Constructeur"""
        super().__init__(path)

    def create_table(self):
        """Crée la table Priorités"""
        self.execute("CREATE TABLE IF NOT EXISTS Priorities (idPriority INTEGER NOT NULL UNIQUE, "
                     "name TEXT NOT NULL UNIQUE, "
                     "PRIMARY KEY(idPriority AUTOINCREMENT));")

    def add_priority(self, name):
        """Ajoute une priorité de tâche"""
        return self.execute("INSERT INTO Priorities (name) VALUES (?);", (name,))

    def get_priority(self, name):
        """Récupère une priorité de tâche"""
        return self.execute("SELECT * FROM Priorities WHERE name = ?;", (name,))

    def get_all_priorities(self):
        """Récupère toutes les priorités de tâche"""
        return self.execute("SELECT * FROM Priorities;")

    def edit_priority(self, name, new_name):
        """Modifie une priorité de tâche"""
        return self.execute("UPDATE Priorities SET name = ? WHERE name = ?;", (new_name, name))

    def delete_priority(self, name):
        """Supprime une priorité de tâche"""
        return self.execute("DELETE FROM Priorities WHERE name = ?;", (name,))


class States_Table(BddManager):
    """Classe pour gérer les états de tâches"""

    def __init__(self, path):
        """Constructeur"""
        super().__init__(path)

    def create_table(self):
        """Crée la table États"""
        self.execute("CREATE TABLE IF NOT EXISTS States (idState INTEGER NOT NULL UNIQUE, "
                     "name TEXT NOT NULL UNIQUE, "
                     "PRIMARY KEY(idState AUTOINCREMENT));")

    def add_state(self, name):
        """Ajoute un état de tâche"""
        return self.execute("INSERT INTO States (name) VALUES (?);", (name,))

    def get_state(self, name):
        """Récupère un état de tâche"""
        return self.execute("SELECT * FROM States WHERE name = ?;", (name,))

    def get_all_states(self):
        """Récupère tous les états de tâche"""
        return self.execute("SELECT * FROM States;")

    def edit_state(self, name, new_name):
        """Modifie un état de tâche"""
        return self.execute("UPDATE States SET name = ? WHERE name = ?;", (new_name, name))

    def delete_state(self, name):
        """Supprime un état de tâche"""
        return self.execute("DELETE FROM States WHERE name = ?;", (name,))


if __name__ == "__main__":
    actual_milli_time = round(time.time() * 1000)

    tache = Tasks_Table("todo.sqlite")
    print(tache.get_user_all_tasks("Test1"))
