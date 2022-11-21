"""Mini-projet ToDoList - squelette de départ

Ce mini-projet en terminale NSI consiste à créer une application web dynamique
gérant une liste de tâches à faire
"""

# Librairie(s) utilisée(s)
from flask import *
import sqlite3
import secrets


# Création des objets Flask et Bdd
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Les routes associées aux fonctions
@app.route("/", methods=["POST", "GET"])
def accueillir():
    """Gère l'accueil des utilisateurs"""
   
    # Rendu de la vue
    return render_template("accueil.html")


# Migrer des lignes dans bdd.py pour rendre le code vla carré
@app.route("/connexion", methods=["POST"])
def connexion():
    # getting input with name = fname in HTML form
    username = request.form.get("username")
    print(username)
    bdd = sqlite3.connect('bdd/todo.sqlite').cursor()
    taches = bdd.execute("SELECT * FROM Taches INNER JOIN Comptes ON Comptes.idCompte = Taches.compte WHERE Comptes.username = ?;", (username, )).fetchall()
    try:
        taches = taches[0] # juste pour tester
        taches = f"Utilisateur : {taches[-1]}\nNom : {taches[1]}\nType : {taches[2]}\nDate : {taches[3]}\nHeure : {taches[4]}\n"
        flash(taches)
    except:
        flash("Cet utilisateur n'existe pas ou n'a aucune tâche")
    finally:
    # Rendu de la vue
        return render_template("accueil.html")


    
       
# TODO : ajoutez de nouvelles routes associées à des fonctions "contrôleur" Python


# Lancement du serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)