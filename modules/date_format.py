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

    def get_difference(self, date: datetime) -> timedelta:
        """Renvoie la différence entre deux dates"""
        return self.date - date
