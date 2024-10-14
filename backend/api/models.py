"""
frequency: MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY

EVERYDAY, BIWEEKLEY, MONTHLY, YEARLY
"""

from datetime import datetime, timedelta


# For todo list
class Todo:
    __ITEM_TYPE = "TODO"

    def __init__(self, item_id, content, completed) -> None:
        self.item_id = item_id
        self.content: str = content
        self.completed: bool = completed

    def getItemType(self) -> str:
        return self.__ITEM_TYPE

    def to_dict(self) -> dict:
        # Convert the object to a dictionary
        return {
            "item_id": self.item_id,
            "content": self.content,
            "completed": self.completed,
            "item_type": self.__ITEM_TYPE,  # Include item type if needed
        }

    def update(self, isCompleted, content=None) -> bool:
        self.content = content if content is not None else self.content
        self.completed = isCompleted if isCompleted is not None else self.completed

        return True


class Task:
    __ITEM_TYPE = "TASK"

    def __init__(self, item_id, title, content, completed, timeFrame, date) -> None:
        self.item_id = item_id
        self.title: str = title
        self.content: str = content
        self.completed: bool = completed
        self.timeFrame: tuple = timeFrame
        self.date: str = date

    def getItemType(self) -> str:
        return self.__ITEM_TYPE

    def setCompleted(self, stat: bool):
        self.completed = stat

    def toDict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "completed": self.completed,
            "item_type": self.getItemType(),  # Include item type if needed
            "timeFrame": self.timeFrame,
            "date": self.date,
            "item_id": self.item_id,
        }

    def update(self, isCompleted, title, content, timeFrame, date):
        self.title = title if title is not None else self.title
        self.content = content if content is not None else self.content
        self.timeFrame = timeFrame if timeFrame is not None else self.timeFrame
        self.date = date if date is not None else self.date
        self.completed = isCompleted if isCompleted is not None else self.completed


class FrequentTask:
    __ITEM_TYPE = "FREQUENT"

    def __init__(
        self, item_id, title, content, frequency, completed, timeFrame
    ) -> None:
        self.item_id = item_id
        self.title: str = title
        self.content: str = content
        self.frequency: list = frequency
        self.completed: bool = completed
        self.timeFrame: tuple = timeFrame
        # self.endFrequency: str = endFrequency

    def getItemType(self) -> str:
        return self.__ITEM_TYPE

    def toDict(self) -> dict:
        # Convert the object to a dictionary
        return {
            "title": self.title,
            "content": self.content,
            "frequency": self.frequency,
            "completed": self.completed,
            "item_type": self.getItemType(),  # Include item type if needed
            "timeFrame": self.timeFrame,
        }

    def generate(self, date) -> Task:
        return Task(
            title=self.title,
            content=self.content,
            completed=False,
            timeFrame=self.timeFrame,
            date=date,
        )


class Goal:
    ITEM_TYPE = "GOAL"

    def __init__(
        self, title, content, completed, started, completedBy, tasksMap
    ) -> None:
        self.title: str = title
        self.content: str = content
        self.completed: bool = completed
        self.started: str = started
        self.completedBy: str = completedBy
        self.taskMap: dict = tasksMap

    def getItemType(self) -> str:
        return self.__ITEM_TYPE

    def toDict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "completed": self.completed,
            "started": self.started,
            "completedBy": self.completedBy,
            "taskMap": self.tasksMap,
            "item_type": self.getItemType(),
        }


class UserData:
    def __init__(self, user_id):
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

        self.__tasks = {}

    """
        ALL TODOS METHODS
    """

    def add_todo(self, todo: Todo, addingToDB: bool = False) -> bool:
        # if it already exists in our dictionary, means that we are trying to add an existing element
        if todo.item_id in self.__todos:
            return False

        if addingToDB:
            pass
        # We will be insert to the database here if its newData

        self.__todos[todo.item_id] = todo
        return True

    def getTodos(self) -> dict:
        todos = [todo.to_dict() for todo in self.__todos.values()]
        return todos

    def getTodo(self, item_id):
        return self.__todos[item_id]

    def delete_todo(self, item_id) -> bool:
        if item_id not in self.__todos:
            return False

        del self.__todos[item_id]

        return True

    def update_todo(self, item_id, isCompleted):
        if item_id not in self.__todos:
            return False

        self.__todos[item_id].update(isCompleted)

    """
        ALL FREQUENT TASK METHODS
    """

    def add_frequentTask(self, freqTask: FrequentTask) -> bool:

        # if it already exists in our dictionary, means that we are trying to add an existing element
        if freqTask.title in self.__frequentTasks[freqTask.frequency.upper()]:
            return False

        self.__frequentTasks[freqTask.frequency.upper()][freqTask.title] = freqTask
        return True

    """
        ALL TASKS METHODS
    """

    def add_task(self, task: Task) -> bool:
        if task.date in self.__tasks and task.item_id in self.__tasks[task.date]:
            return False

        if task.date not in self.__tasks:
            self.__tasks[task.date] = {}
            self.__tasks[task.date][task.item_id] = task
        else:
            self.__tasks[task.date][task.item_id] = task

        return True
    
    def create(self, task: Task) -> bool:
        if task.date in self.__tasks and task.item_id in self.__tasks[task.date]:
            return False

        if task.date not in self.__tasks:
            self.__tasks[task.date] = {}
            self.__tasks[task.date][task.item_id] = task
            return True
        

        for event in self.__tasks[task.date]:
            if self.time_frame_overlap(event, task):
                return False
            
        self.__tasks[task.date][task.item_id] = task
        return True
    

    def delete_task(self, item_id) -> bool:
        for dic in self.__tasks.values():
            if item_id in dic:
                del dic[item_id]
                return True

        return False

    def update_task(
        self,
        item_id,
        isCompleted=None,
        title=None,
        content=None,
        timeFrame=None,
        date=None,
    ) -> bool:
        for dic in self.__tasks.values():
            if item_id in dic:
                dic[item_id].update(isCompleted, title, content, timeFrame, date)
                return True

        return False

    """
    USER STUFF
    """

    def get_user_id(self):
        return self.__user_id

    def getWeek(self, date) -> dict:
        week = {}

        START_DAY = datetime.strptime(date, "%m-%d-%Y").date()

        for i in range(1, 7):
            dayName = str((START_DAY + timedelta(days=i)).strftime("%A"))
            fullDay = (
                dayName + ", " + str((START_DAY + timedelta(days=i)).strftime("%B %d"))
            )  # full Day name for the day
            d = str((START_DAY + timedelta(days=i)).strftime("%m-%d-%Y"))

            if dayName not in week:
                week[fullDay] = {}

            # for task in self.__frequentTasks[dayName.upper()].values():
            #     self.__frequentTasks.generate()

            # for freq in self.__frequentTasks:
            if d in self.__tasks:
                for item_id, task in self.__tasks[d].items():
                    week[fullDay][item_id] = task.toDict()
        return week

    def getToday(self, date) -> dict:
        today = {}

        return today
    
    """
    Check if two tasks overlap based on their time frames.

    :param task1: First task (FrequentTask or Task)
    :param task2: Second task (FrequentTask or Task)
    :return: True if the time frames overlap, False otherwise
    """

    def time_frame_overlap(task1, task2) -> bool:

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

        # Check for overlap
        return not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes)

