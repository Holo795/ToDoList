from bdd.bdd import Accounts
import bcrypt


class AccountsManager:
    def __init__(self, flask):
        self.flask = flask
        self.accounts = Accounts("bdd/todo.sqlite")

    def login(self, request):
        username = request.form.get("username")
        password = request.form.get("password")

        if account := self.accounts.get_account(username):
            account = account[0]
            if bcrypt.checkpw(password.encode('utf8'), account[2].encode('utf8')):
                self.flask.session["username"] = username
                return self.flask.redirect(self.flask.url_for("accueil"))
            else:
                self.flask.flash("Mot de passe incorrect")
        else:
            self.flask.flash("Cet utilisateur n'existe pas")
        return self.flask.redirect(self.flask.url_for("accueil"))

    def logout(self):
        self.flask.session.pop("username", None)
        return self.flask.redirect(self.flask.url_for("accueil"))

    def register(self, request):
        username = request.form.get("username")
        password = request.form.get("password")
        password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        if self.accounts.get_account(username):
            self.flask.flash("Cet utilisateur existe déjà")
        else:
            self.accounts.add_account(username, password.decode('utf8'))
            self.flask.flash("Compte créé")
        return self.flask.redirect(self.flask.url_for("accueil"))
