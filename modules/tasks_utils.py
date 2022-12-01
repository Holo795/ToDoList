import locale
from datetime import datetime

from bdd.bdd import Database


class TasksUtils:
    def __init__(self, tasks: list):
        self.tasks = tasks

    def get_formatted_tasks(self) -> list:
        return [self.format_task(task) for task in self.tasks]

    def format_task(self, task: tuple) -> dict:
        return {
            "id": task[0],
            "title": task[2],
            "description": task[3],
            "date": TasksTimeUtils(task[4]).get_date_text(),
            "done": TasksTimeUtils(task[5]).get_date_text() if task[5] else False,
            "time_left": TasksTimeUtils(task[4]).get_difference_text(),
            "type": self.get_type(task[6]),
            "priority": self.get_priority(task[7]),
            "stats": self.get_state(task[8]),
        }

    def get_type(self, type_id: int) -> tuple:
        type_table = Database().types
        return type_id, type_table.get_type(type_id)[0][1]

    def get_priority(self, priority_id: int) -> tuple:
        priorities_table = Database().priorities
        return priority_id, priorities_table.get_priority(priority_id)[0][1]

    def get_state(self, state_id: int) -> tuple:
        states_table = Database().states
        return state_id, states_table.get_state(state_id)[0][1]


class TasksTimeUtils:
    """Cette classe permet de convertir tout type de date en format datetime"""

    def __init__(self, date):
        """Constructeur"""

        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")  # Permet d'avoir les jours et les mois en français

        if type(date) == str:
            self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        elif type(date) in [int, float]:
            self.date = datetime.fromtimestamp(int(date))
        elif type(date) == datetime:
            self.date = date
        else:
            raise TypeError("Type de date non reconnu")

    def get_date(self) -> datetime:
        return self.date

    def get_date_text(self) -> str:
        return self.date.strftime("%A %d %B %Y %Hh%M").capitalize()

    def get_difference(self, date=None) -> datetime:
        if date is None:
            date = datetime.now()
        return self.date - date

    def get_difference_text(self, date=None) -> str:
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

    def get_microseconds(self) -> int:
        return int(self.date.timestamp())
