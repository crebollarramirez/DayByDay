from datetime import datetime, timedelta
import uuid

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

    # def generate(self, date) -> Task:
    #     newID = str(uuid.uuid4())
    #     return Task(
    #         item_id=newID,
    #         title=self.title,
    #         content=self.content,
    #         completed=False,
    #         timeFrame=self.timeFrame,
    #         date=date,
    #         parent=self.item_id,
    #     )

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


