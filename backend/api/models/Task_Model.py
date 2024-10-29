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

