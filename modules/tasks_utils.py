from modules.date_format import DateMillis


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
            "date": DateMillis(task[4]).get_date_text(),
            "done": DateMillis(task[5]).get_date_text(),
            "time_left": DateMillis(task[4]).get_difference_text(),
            "type": task[6],
            "priority": task[7],
            "category": task[8]
        }
