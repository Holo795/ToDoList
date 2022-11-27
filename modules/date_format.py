from datetime import datetime, timedelta


class DateFormat:
    """Classe permettant de formater les dates"""
    def __init__(self, date_text: str):
        self.date_text = date_text

        self.date = datetime.strptime(date_text, "%Y-%m-%dT%H:%M")

    def get_date(self) -> datetime:
        """Renvoie la date"""
        return self.date

    def get_date_text(self) -> str:
        """Renvoie la date sous forme de texte"""
        return self.date_text

    def get_difference(self, date=datetime.now()) -> timedelta:
        """Renvoie la différence entre deux dates"""
        return self.date - date


class DateMillis:
    """Classe permettant de formater les dates en millisecondes"""
    def __init__(self, mills: int):
        self.mills = mills
        self.date = datetime.fromtimestamp(mills / 1000)

    def get_date(self) -> datetime:
        """Renvoie la date"""
        return self.date

    def get_date_text(self) -> str:
        """Renvoie la date sous forme de texte"""
        return self.date.strftime("%A %d %B %Y %Hh%M")

    def get_difference(self, date=None) -> timedelta:
        """Renvoie la différence entre deux dates"""
        if date is None:
            date = datetime.now()
        return self.date - date

    def get_difference_text(self, date=None) -> str:
        """Renvoie la différence entre deux dates sous forme de texte"""
        if date is None:
            date = datetime.now()
        difference = self.get_difference(date)
        text = "" + ("Il y a " if self.date.microsecond < date.microsecond else "Dans ")
        difference = abs(difference)
        if difference.days > 0:
            text += f"{difference.days} jour(s) "
        if difference.seconds > 0:
            text += f"{difference.seconds // 3600} heure(s) "
            text += f"{(difference.seconds // 60) % 60} minute(s) "

        return text
