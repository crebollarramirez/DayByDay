from .Todo_Model import Todo
from .Task_Model import Task
from .models import FrequentTask
from datetime import datetime

class UserData:
    def __init__(self, user_id) -> None:
        self.__user_id = user_id

        """
        key: title of todo
        value: object todo
        """

        self.__todos = {}

        """
        key: frequency
        value: dictionary that holds all tasks in that frequency {
            key: title
            value: frequent task object
        }
        
        """

        self.__frequentTasks = {
            "MONDAY": {},
            "TUESDAY": {},
            "WEDNESDAY": {},
            "THURSDAY": {},
            "FRIDAY": {},
            "SATURDAY": {},
            "SUNDAY": {},
            "EVERYDAY": {},
            "BIWEEKLY": {},
            "MONTHLY": {},
            "YEARLY": {},
        }
        # self.__allFrequentTasks = {}

        self.__tasks: dict[str, Task] = {
        }
        # self.__allTasks = {}

    """
        ALL TODOS METHODS
    """

    def add_todo(self, todo: Todo) -> bool:
        # if it already exists in our dictionary, means that we are trying to add an existing element
        if todo.item_id in self.__todos:
            return False

        # We will be insert to the database here if its newData

        self.__todos[todo.item_id] = todo
        return True

    def getTodos(self) -> dict:
        todos = [todo.to_dict() for todo in self.__todos.values()]
        return todos

    def getTodo(self, item_id) -> Todo:
        return self.__todos[item_id]

    def delete_todo(self, item_id) -> bool:
        if item_id not in self.__todos:
            return False

        del self.__todos[item_id]

        return True

    def update_todo(self, item_id, isCompleted=None, content=None) -> None:
        if item_id not in self.__todos:
            return False

        self.__todos[item_id].update(isCompleted=isCompleted, content=content)

    """
        ALL FREQUENT TASK METHODS
    """

    def add_frequentTask(self, freqTask: FrequentTask) -> bool:
        # checking if the item already exists
        for freq in freqTask.frequency:
            if freqTask.item_id in self.__frequentTasks[freq.upper()]:
                return False
                         
        for freq in freqTask.frequency:
            self.__frequentTasks[freq.upper()][freqTask.item_id] = freqTask

        # self.__allFrequentTasks[freqTask.item_id] = freqTask
        return True

    def delete_frequentTask(self, item_id) -> bool:
        for day in self.__frequentTasks:
            if item_id in day:
                del day[item_id]
                return True

        # del self.__allFrequentTasks[item_id]
        return False

    def update_frequentTask(
        self,
        item_id,
        title=None,
        content=None,
        frequency=None,
        timeFrame=None,
        endFrequency=None,
    ) -> None:
        for freqTasks in self.__frequentTasks.values():
            if item_id in freqTasks:
               freqTasks[item_id].update(self.__allTasks,
            title=title,
            content=content,
            timeFrame=timeFrame,
            frequency=frequency,
            endFrequency=endFrequency,
        )
               
    def get_frequentTasks(self) -> dict:
        return self.__frequentTasks

    """
        ALL TASKS METHODS
    """

    def add_task(self, task: Task, fromDB=False) -> bool:
        if task.date in self.__tasks and task.item_id in self.__tasks[task.date]:
            return False

        if fromDB:
            if task.date not in self.__tasks:
                self.__tasks[task.date] = {}
            self.__tasks[task.date][task.item_id] = task
            return True

        print(task.toDict())
        # what we do to add tasks from user input
        if task.date not in self.__tasks:
            self.__tasks[task.date] = {}
            self.__tasks[task.date][task.item_id] = task
            return True

        print("THIS IS BEFORE THE COMPARE")
        print(task.toDict())
        for event in self.__tasks[task.date].values():
            
            
            if self.time_frame_overlap(event, task):
                return False

        self.__tasks[task.date][task.item_id] = task
        return True

    def delete_task(self, item_id) -> bool:
        for dic in self.__tasks.values():
            if item_id in dic:
                if dic[item_id].parent is not None:
                    pass # handle what happens to parent             
                del dic[item_id]
        return True

    def update_task(
        self,
        item_id,
        isCompleted=None,
        title=None,
        content=None,
        timeFrame=None,
        date=None,
    ) -> bool:
        
        for d in self.__tasks.values():
            if item_id in d:
                d[item_id].update(isCompleted=isCompleted, title=title, content=content, timeFrame=timeFrame, date=date)
                return True
        return False
    
    def get_tasks(self) -> dict:
        organizedTasks = {}
        
        for day, tasks in self.__tasks.items():
            organizedTasks[day] = {}
            for task in tasks.values():
               organizedTasks[day][task.item_id] = task.toDict()

        return organizedTasks            

    """
    USER STUFF
    """

    def get_user_id(self) -> str:
        return self.__user_id

    def checkIfDuplicate(self, newTask, d) -> bool:
        for task in self.__tasks[d].values():
            if task.parent is not None and newTask.parent == task.parent:
                return True
        return False

    def getWeek(self, date) -> dict:
        week = {}
        return week

    def getToday(self, date) -> dict:
        today = {}

        date = datetime.strptime(date, "%m-%d-%Y").date()
        dayName = date.strftime("%A").upper()
        date = date.strftime("%m-%d-%Y")

        if str(date) in self.__tasks:
            for title, task in self.__tasks[date].items():
                today[title] = task.toDict()

        return today

    """
    Check if two tasks overlap based on their time frames.

    :param task1: First task (FrequentTask or Task)
    :param task2: Second task (FrequentTask or Task)
    :return: True if the time frames overlap, False otherwise
    """

    def time_frame_overlap(self, task1, task2) -> bool:
        start1, end1 = task1.timeFrame
        start2, end2 = task2.timeFrame

        # Convert military time to minutes since midnight for comparison
        def military_to_minutes(military_time):
            hours, minutes = map(int, military_time.split(":"))
            return hours * 60 + minutes

        start1_minutes = military_to_minutes(start1)
        end1_minutes = military_to_minutes(end1)
        start2_minutes = military_to_minutes(start2)
        end2_minutes = military_to_minutes(end2)


        if not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes):
            print("task1 time:")
            print(task1.toDict())
            print("task2 time:")
            print(task2.toDict())
        # Check for overlap
        return not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes)
