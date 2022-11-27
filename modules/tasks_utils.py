from modules.date_format import DateMicros


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
            "date": DateMicros(task[4]).get_date_text(),
            "done": DateMicros(task[5]).get_date_text() if task[5] else None,
            "time_left": DateMicros(task[4]).get_difference_text(),
            "type": task[6],
            "priority": task[7],
            "category": task[8]
        }
