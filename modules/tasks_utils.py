import locale
from datetime import datetime


class TasksUtils:
    def __init__(self, tasks):
        self.tasks = tasks

    def get_formatted_tasks(self):
        return [self.format_task(task) for task in self.tasks]

    def format_task(self, task):
        return {
            "id": task[0],
            "title": task[2],
            "description": task[3],
            "date": TasksTimeUtils(task[4]).get_date_text(),
            "done": TasksTimeUtils(task[5]).get_date_text() if task[5] else None,
            "time_left": TasksTimeUtils(task[4]).get_difference_text(),
            "type": task[6],
            "priority": task[7],
            "category": task[8]
        }


class TasksTimeUtils:
    """Cette classe permet de convertir tout type de date en format datetime"""
    def __init__(self, date):
        """Constructeur"""

        locale.setlocale(locale.LC_TIME, "fr_FR")  # Permet d'avoir les jours et les mois en français

        if type(date) == str:
            self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        elif type(date) in [int, float]:
            self.date = datetime.fromtimestamp(int(date))
        elif type(date) == datetime:
            self.date = date
        else:
            raise TypeError("Type de date non reconnu")

    def get_date(self):
        return self.date

    def get_date_text(self):
        return self.date.strftime("%A %d %B %Y %Hh%M").capitalize()

    def get_difference(self, date=None):
        if date is None:
            date = datetime.now()
        return self.date - date

    def get_difference_text(self, date=None):
        if date is None:
            date = datetime.now()
        difference = self.get_difference(date)
        text = "" + ("Il y a " if self.date.timestamp() <= date.timestamp() else "Dans ")
        difference = abs(difference)
        if difference.days > 0:
            text += f"{difference.days} jour(s) "
        if difference.seconds > 3600:
            text += f"{difference.seconds // 3600} heure(s) "
        if difference.seconds > 60:
            text += f"{difference.seconds % 3600 // 60} minute(s) "
        if difference.seconds > 0:
            text += f"{difference.seconds % 60} seconde(s)"
        return text

    def get_microseconds(self):
        return int(self.date.timestamp())



