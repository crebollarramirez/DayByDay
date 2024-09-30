"""
frequency: MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY

EVERYDAY, BIWEEKLEY, MONTHLY, YEARLY
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
    
    def setCompleted(self, stat: bool):
        self.completed = stat


class FrequentTask:
    __ITEM_TYPE = 'FREQUENT'

    def __init__(self, title, content, frequency, completed, timeFrame) -> None:
        self.title: str = title
        self.content: str = content
        self.frequency: str = frequency
        self.completed: bool = completed
        self.timeFrame: tuple = timeFrame

    def getItemType(self) -> str:
        return self.__ITEM_TYPE

    def toDict(self) -> dict:
        # Convert the object to a dictionary
        return {
            'title': self.title,
            'content': self.content,
            'frequency': self.frequency,
            'completed': self.completed,
            'item_type': self.getItemType(),  # Include item type if needed
            'timeFrame': self.timeFrame
        }

class Task:
    __ITEM_TYPE = "TASK"

    def __init__(self, title, content, completed, timeFrame, date) -> None:
        self.title: str = title
        self.content: str = content
        self.completed: bool = completed
        self.timeFrame: tuple = timeFrame
        self.date: str = date

    def getItemType(self) -> str:
        return self.__ITEM_TYPE

    def toDict(self) -> dict:
        return {
            'title': self.title,
            'content': self.content,
            'completed': self.completed,
            'item_type': self.getItemType(),  # Include item type if needed
            'timeFrame': self.timeFrame,
            'date': self.date
        }

class Goal:
    ITEM_TYPE = 'GOAL'

    def __init__(self, title, content, completed, started, completedBy, tasksMap) -> None:
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
            'content': self.content,
            'completed': self.completed,
            'started': self.started,
            'completedBy': self.completedBy,
            'taskMap': self.tasksMap,
            'item_type': self.getItemType()
        }

