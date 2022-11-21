import sqlite3
import time


# La classe
class Bdd:
    """Classe pour faire le lien entre la base de données SQLite et le programme"""

    def __init__(self, path):
        """Constructeur"""
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def execute(self, request, parameters=None):
        """Exécute une requête SQL"""
        if parameters is None:
            self.cursor.execute(request)
        else:
            self.cursor.execute(request, parameters)
        self.connection.commit()
        return self.cursor.fetchall()


class Tasks(Bdd):
    """Classe pour gérer les tâches"""

    def __init__(self, path):
        """Constructeur"""
        super().__init__(path)

    def get_user_all_tasks(self, username):
        """Récupère les tâches d'un utilisateur"""
        return self.execute("SELECT * FROM Taches INNER JOIN Comptes ON Comptes.idCompte = Taches.idCompte WHERE "
                            "Comptes.username = ?;", (username,))

    def add_user_tasks(self, username, name, echeance_date, succes_date, idPriority, idState, idType):
        """Ajoute une tâche à un utilisateur"""
        return self.execute("INSERT INTO Taches (nom, echeance_date, succes_date, idPriority, idState, "
                            "idType, idCompte) "
                            " VALUES (?, ?, ?, ?, ?, ?, (SELECT idCompte FROM Comptes WHERE username = ?));", 
                            (name, echeance_date, succes_date, idPriority, idState, idType, username))
    

if __name__ == "__main__":

    actual_milli_time = round(time.time() * 1000)

    tache = Tasks("todo.sqlite")
    print(tache.get_user_all_tasks("Test1"))
    tache.add_user_tasks("Test1", "Test_task", actual_milli_time, 1, 1, 1, 1)
