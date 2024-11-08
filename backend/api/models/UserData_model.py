from .Todo_Model import Todo
from .Task_Model import Task
from .models import FrequentTask
from datetime import datetime, timedelta

class UserData:
    def __init__(self, user_id) -> None:
        """
        User ID
        """
        self.__user_id = user_id

        """
        key: date (str)
        value: dictionary {
            key: item_id (str)
            value: Todo object
        }
        """
        self.__todos: dict[str, dict[str, Todo]] = {}

        """
        key: frequency (str)
        value: dictionary that holds all tasks in that frequency (dict[str, FrequentTask])
        """
        self.__frequentTasks: dict[str, dict[str, FrequentTask]] = {
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

        """
        key: date (str)
        value: dictionary {
            key: item_id (str)
            value: Task object
        }
        """
        self.__tasks: dict[str, dict[str, Task]] = {
        }

    """
        ALL TODOS METHODS
    """

    def add_todo(self, todo: Todo) -> bool:
        # if it already exists in our dictionary, means that we are trying to add an existing element
        if todo.date not in self.__todos:
            self.__todos[todo.date] = {}

        self.__todos[todo.date][todo.item_id] = todo
        return True
    

    def get_todos(self, date) -> dict:
        if date not in self.__todos:
            return []
        todos = [todo.to_dict() for todo in self.__todos[date].values()]
        return todos
    
    def getAllTodos(self) -> dict:
        return [todo.to_dict() for todos in self.__todos.values() for todo in todos.values()]

    def getTodo(self, item_id, date) -> Todo:
        return self.__todos[date][item_id]

    def delete_todo(self, item_id) -> bool:
        for date in self.__todos:
            if item_id in self.__todos[date]:
                del self.__todos[date][item_id]
                return True
            
        return False


    def update_todo(self, item_id, isCompleted=None, content=None) -> None:
        for date in self.__todos:
            if item_id in self.__todos[date]:
                self.__todos[date][item_id].update(isCompleted=isCompleted, content=content)
                return True
        return False

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
        print("WE ARE ADDING A TASK")
        if task.date in self.__tasks and task.item_id in self.__tasks[task.date]:
            return False

        if fromDB:
            if task.date not in self.__tasks:
                self.__tasks[task.date] = {}
            self.__tasks[task.date][task.item_id] = task
            return True

        # what we do to add tasks from user input
        if task.date not in self.__tasks:
            self.__tasks[task.date] = {}
            self.__tasks[task.date][task.item_id] = task
            return True

        self.__tasks[task.date][task.item_id] = task
        return True

    def delete_task(self, item_id) -> bool:
        for dic in self.__tasks.values():
            if item_id in dic:
                # if dic[item_id].parent is not None:
                #     pass # handle what happens to parent             
                del dic[item_id]
        return True
    
    """
    Updates a task with the given item_id.
    
    Args:
        item_id (str): The item_id of the task to be updated.
        isCompleted (bool, optional): Whether the task is completed. Defaults to None.
        title (str, optional): The title of the task. Defaults to None.
        content (str, optional): The content of the task. Defaults to None.
        timeFrame (list, optional): The time frame of the task. Defaults to None.
        date (str, optional): The date of the task. Defaults to None.
    
    Returns:
        bool: True if the task was found and updated, False otherwise.
    """
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
    
    """
    Gets a week of tasks for the user given a date.

    :param date: Date string in MM-DD-YYYY format.
    :return: A dictionary where the keys are day names and the values are dictionaries of tasks.
    """
    def getWeek(self, date) -> dict:
        week = {}
        START_DAY = datetime.strptime(date, "%m-%d-%Y").date()

        for i in range(0, 5):
            dayName = str((START_DAY + timedelta(days=i)).strftime("%A"))
            fullDay = (
                dayName + ", " + str((START_DAY + timedelta(days=i)).strftime("%B %d"))
            )  # full Day name for the day
            d = str((START_DAY + timedelta(days=i)).strftime("%m-%d-%Y"))

            if dayName not in week:
                week[fullDay] = {}

            userTasks = self.get_tasks()
            if d in userTasks:
                week[fullDay] = userTasks[d]
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
    

    def getAllData(self) -> tuple[list[Todo], dict[str, dict[str, Task]]]:
        return self.getAllTodos(), self.get_tasks()
    


