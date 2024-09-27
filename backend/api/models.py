"""
frequency: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

EVERYDAY, 2WEEKS, MONTHLY, YEARLY
"""

# For todo list 
class Todo:
    __ITEM_TYPE = 'TODO'

    def __init__(self, title, content, completed) -> None:
        self.title:str = title
        self.content: str = content
        self.completed: bool = completed

    def getItemType(self) -> str:
        return self.__ITEM_TYPE
    
    def to_dict(self) -> dict:
        # Convert the object to a dictionary
        return {
            'title': self.title,
            'content': self.content,
            'completed': self.completed,
            'item_type': self.getItemType()  # Include item type if needed
        }

class FrequentTask:
    ITEM_TYPE = 'FREQUENT'

    def __init__(self, title, content, frequency, completed, timeFrame) -> None:
        self.title: str = title
        self.content: str = content
        self.frequency: str = frequency
        self.completed: bool = completed
        self.timeFrame: tuple = timeFrame

    def to_dict(self) -> dict:
        pass

class Task:
    ITEM_TYPE = "TASK"

    def __init__(self, title, content, completed, timeFrame, date) -> None:
        self.title: str = title
        self.content: str = content
        self.completed: bool = completed
        self.timeFrame: tuple = timeFrame
        self.date: str = date

    def to_dict(self) -> dict:
        pass

class Goal:
    ITEM_TYPE = 'GOAL'

    def __init__(self, title, content, completed, started, completedBy, tasksMap) -> None:
        self.title: str = title
        self.content: str = content
        self.completed: bool = completed
        self.started: str = started
        self.completedBy: str = completedBy
        self.taskMap: dict = tasksMap

    def to_dict(self) -> dict:
        pass

