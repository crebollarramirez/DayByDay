from datetime import datetime, timedelta
import uuid

"""
Represents a to-do list item with attributes for content and completion status.

Attributes:
    item_id (str): A unique identifier for the to-do item.
    content (str): The content or description of the to-do item.
    completed (bool): A flag indicating whether the to-do item is completed.
"""


class Todo:

    __ITEM_TYPE = "TODO"

    """
    Initializes a Todo object.

    Args:
        item_id (str): A unique identifier for the to-do item.
        content (str): The content or description of the to-do item.
        completed (bool): Indicates whether the to-do item is completed.
    """

    def __init__(self, item_id, content, completed) -> None:

        self.item_id = item_id
        self.content = content
        self.completed = completed

    """
    Returns the type of the to-do item.
    
    Returns:
        str: The item type (always "TODO").
    """

    def getItemType(self) -> str:

        return self.__ITEM_TYPE

    """
    Converts the Todo object into a dictionary.
    
    Returns:
        dict: A dictionary representation of the Todo object.
    """

    def to_dict(self) -> dict:

        return {
            "item_id": self.item_id,
            "content": self.content,
            "completed": self.completed,
            "item_type": self.__ITEM_TYPE,
        }

    """
    Updates the content and/or completed status of the to-do item.
    
    Args:
        isCompleted (bool, optional): New completion status of the to-do item.
        content (str, optional): New content for the to-do item.
    
    Returns:
        bool: True after successfully updating the object.
    """

    def update(self, isCompleted=None, content=None) -> bool:
        self.content = content if content is not None else self.content
        self.completed = isCompleted if isCompleted is not None else self.completed
        return True


"""
Represents a task with attributes such as title, content, completion status, time frame, and date. 
It also supports linking to other tasks.

Attributes:
    item_id (str): A unique identifier for the task.
    title (str): The title or name of the task.
    content (str): The content or description of the task.
    completed (bool): A flag indicating whether the task is completed.
    timeFrame (tuple): A tuple representing the time frame for the task.
    date (str): The date associated with the task.
    linked (str, optional): An optional linked task identifier, if any.
"""


class Task:

    __ITEM_TYPE = "TASK"

    """
    Initializes a Task object.

    Args:
        item_id (str): A unique identifier for the task.
        title (str): The title or name of the task.
        content (str): The content or description of the task.
        completed (bool): The completion status of the task.
        timeFrame (tuple): The time frame within which the task occurs.
        date (str): The date for the task.
        parent (str, optional): An optional task that this task is a child to.
    """

    def __init__(
        self, item_id, title, content, completed, timeFrame, date, parent=None
    ) -> None:

        self.item_id = item_id
        self.title = title
        self.content = content
        self.completed = completed
        self.timeFrame = timeFrame
        self.date = date
        self.parent:str = parent

    """
    Returns the type of the task, which is always "TASK".

    Returns:
        str: The item type (always "TASK").
    """

    def getItemType(self) -> str:

        return self.__ITEM_TYPE

    """
    Converts the Task object into a dictionary.

    Returns:
        dict: A dictionary representation of the Task object, including title, content,
                completion status, item type, time frame, date, and item ID.
    """

    def toDict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "completed": self.completed,
            "item_type": self.__ITEM_TYPE,
            "timeFrame": self.timeFrame,
            "date": self.date,
            "item_id": self.item_id,
            "parent": self.parent
        }

    """
    Updates the attributes of the task. Only non-None values will update the respective attributes.

    Args:
        isCompleted (bool, optional): New completion status of the task.
        title (str, optional): New title for the task.
        content (str, optional): New content for the task.
        timeFrame (tuple, optional): New time frame for the task.
        date (str, optional): New date for the task.
    """

    def update(
        self, isCompleted=None, title=None, content=None, timeFrame=None, date=None
    ) -> None:
        self.title = title if title is not None else self.title
        self.content = content if content is not None else self.content
        self.timeFrame = timeFrame if timeFrame is not None else self.timeFrame
        self.date = date if date is not None else self.date
        self.completed = isCompleted if isCompleted is not None else self.completed

    """
    Unlinks the task from any other linked task.
    """

    def unlink(self) -> None:
        self.parent = None


class FrequentTask:
    __ITEM_TYPE = "FREQUENT"

    def __init__(
        self, item_id, title, content, frequency, completed, timeFrame, endFrequency
    ) -> None:
        self.item_id = item_id
        self.title: str = title
        self.content: str = content
        self.frequency: list = frequency
        self.completed: bool = completed
        self.timeFrame: tuple = timeFrame
        self.endFrequency: str = endFrequency
        self.children: list[str] = []

    def getItemType(self) -> str:
        return self.__ITEM_TYPE

    def toDict(self) -> dict:
        # Convert the object to a dictionary
        return {
            "title": self.title,
            "content": self.content,
            "frequency": self.frequency,
            "completed": self.completed,
            "item_type": self.__ITEM_TYPE,  # Include item type if needed
            "timeFrame": self.timeFrame,
            "item_id": self.item_id,
            "endFrequency": self.endFrequency,
            "chidren": self.children
        }

    def generate(self, date) -> Task:
        newID = str(uuid.uuid4)
        return Task(
            item_id=newID,
            title=self.title,
            content=self.content,
            completed=False,
            timeFrame=self.timeFrame,
            date=date,
            parent=self.item_id,
        )

    def update(
        self,
        allTasks,
        isCompleted=None,
        title=None,
        content=None,
        timeFrame=None,
        endFrequency=None,
        frequency=None,
    ) -> None:
        self.title = title if title is not None else self.title
        self.content = content if content is not None else self.content
        self.timeFrame = timeFrame if timeFrame is not None else self.timeFrame
        self.completed = isCompleted if isCompleted is not None else self.completed
        self.endFrequency = (
            endFrequency if endFrequency is not None else self.endFrequency
        )
        self.frequency = frequency if frequency is not None else self.frequency

        for item_id in self.children:
            allTasks[item_id].update(title=title, content=content, timeFrame=timeFrame)


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

        self.__allFrequentTasks = {}

        self.__tasks: dict[str, Task] = {}
        self.__allTasks = {}

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
        for freq in freqTask.frequency:
            if freqTask.item_id in self.__frequentTasks[freq.upper()]:
                return False

        for freq in freqTask.frequency:
            self.__frequentTasks[freq.upper()][freqTask.item_id] = freqTask

        return True

    def delete_frequentTask(self, item_id) -> bool:
        for day in self.__frequentTasks:
            if item_id in day:
                del day[item_id]
                return True

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
        self.__allFrequentTasks[item_id].update(self.__allTasks,
            title=title,
            content=content,
            timeFrame=timeFrame,
            frequency=frequency,
            endFrequency=endFrequency,
        )

    """
        ALL TASKS METHODS
    """

    def add_task_from_db(self, task: Task) -> bool:
        if task.date in self.__tasks and task.item_id in self.__tasks[task.date]:
            return False

        if task.date not in self.__tasks:
            self.__tasks[task.date] = {}
            self.__tasks[task.date][task.item_id] = task
        else:
            self.__tasks[task.date][task.item_id] = task

        self.__allTasks[task.item_id] = task
        return True

    def create_task(self, task: Task) -> bool:
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
        self.__allTasks[task.item_id] = task
        return True

    def delete_task(self, item_id) -> bool:
        for dic in self.__tasks.values():
            if item_id in dic:
                del dic[item_id]
                return True

        del self.__allTasks[item_id]
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
        
        if item_id in self.__allTasks:
            self.__allTasks[item_id].update(isCompleted, title, content, timeFrame, date)
            return True
        return False

    """
    USER STUFF
    """

    def get_user_id(self):
        return self.__user_id

    def __checkIfDuplicate(self, newTask, d) -> bool:
        for task in self.__tasks[d].values():
            if task.parent is not None and newTask.parent == task.parent:
                return True
        return False

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

            if len(self.__frequentTasks[dayName.upper()]) != 0:
                for freqTask in self.__frequentTasks[dayName.upper()].values():
                    newTask = freqTask.generate(d)

                    if (
                        d in self.__tasks and not (self.__checkIfDuplicate(newTask, d))
                    ) or d not in self.__tasks:
                        self.add_task_from_db(newTask)

            if d in self.__tasks:
                for item_id, task in self.__tasks[d].items():
                    week[fullDay][item_id] = task.toDict()
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
