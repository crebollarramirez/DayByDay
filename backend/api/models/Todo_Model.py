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
        date (str): What day is this todo for.
    """

    def __init__(self, item_id, content, completed, date) -> None:

        self.item_id = item_id
        self.content = content
        self.completed = completed
        self.date = date

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
            "date": self.date
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