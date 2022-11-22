from flask import flash  # for flash messages

from bdd.bdd import Accounts  # Accounts database gestion
import bcrypt  # for password hashing


class AccountsManager:
    """Classe pour gérer les comptes"""
    def __init__(self, flask):
        """Constructeur"""
        self.flask = flask
        self.accounts = Accounts("../bdd/todo.sqlite")

    def login(self, request):
        """Connecte un utilisateur"""
        username = request.form.get("username")
        password = request.form.get("password")
        if account := self.accounts.get_account(username):
            account = account[0]
            if bcrypt.checkpw(password.encode('utf8'), account[2].encode('utf8')):
                self.flask.session["username"] = username
                return self.flask.redirect(self.flask.url_for("accueil"))
            else:
                flash("Mot de passe incorrect", "error")
        else:
            flash("Cet utilisateur n'existe pas", "error")
        return self.flask.redirect(self.flask.url_for("accueil"))

    def logout(self):
        """Déconnecte un utilisateur"""
        self.flask.session.pop("username", None)
        return self.flask.redirect(self.flask.url_for("accueil"))

    def register(self, request):
        """Enregistre un utilisateur"""
        username = request.form.get("username")
        password = request.form.get("password")
        if self.accounts.get_account(username):
            flash("Cet utilisateur existe déjà", "error")
        else:
            self.accounts.add_account(username, bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8'))
            flash("Compte créé", "success")
        return self.flask.redirect(self.flask.url_for("accueil"))
