class FrequentTask:
    __ITEM_TYPE = 'FREQUENT'

    def __init__(self, title, content, frequency, completed, timeFrame) -> None:
        self.title: str = title
        self.content: str = content
        self.frequency: list = frequency
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


def time_frame_overlap(task1, task2) -> bool:
    """
    Check if two tasks overlap based on their time frames.

    :param task1: First task (FrequentTask or Task)
    :param task2: Second task (FrequentTask or Task)
    :return: True if the time frames overlap, False otherwise
    """
    start1, end1 = task1.timeFrame
    start2, end2 = task2.timeFrame
    
    # Convert military time to minutes since midnight for comparison
    def military_to_minutes(military_time):
        hours, minutes = map(int, military_time.split(':'))
        return hours * 60 + minutes
    
    start1_minutes = military_to_minutes(start1)
    end1_minutes = military_to_minutes(end1)
    start2_minutes = military_to_minutes(start2)
    end2_minutes = military_to_minutes(end2)
    
    # Check for overlap
    return not (end1_minutes <= start2_minutes or end2_minutes <= start1_minutes)

# Create test cases
def test_time_frame_overlap():
    # Overlapping time frames
    task1 = FrequentTask("Task 1", "Content 1", ["daily"], False, ("09:00", "11:00"))
    task2 = Task("Task 2", "Content 2", False, ("10:00", "12:00"), "2024-10-13")
    
    assert time_frame_overlap(task1, task2) == True, "Test Case 1 Failed"

    # Non-overlapping time frames
    task3 = FrequentTask("Task 3", "Content 3", ["weekly"], False, ("11:00", "12:00"))
    task4 = Task("Task 4", "Content 4", False, ("12:00", "13:00"), "2024-10-13")
    
    assert time_frame_overlap(task3, task4) == False, "Test Case 2 Failed"

    # Partial overlap
    task5 = FrequentTask("Task 5", "Content 5", ["monthly"], False, ("09:30", "10:30"))
    task6 = Task("Task 6", "Content 6", False, ("10:00", "11:00"), "2024-10-13")

    assert time_frame_overlap(task5, task6) == True, "Test Case 3 Failed"

    # Identical time frames
    task7 = FrequentTask("Task 7", "Content 7", ["bi-weekly"], False, ("09:00", "10:00"))
    task8 = Task("Task 8", "Content 8", False, ("09:00", "10:00"), "2024-10-13")
    
    assert time_frame_overlap(task7, task8) == True, "Test Case 4 Failed"

    # One task completely inside the other
    task9 = FrequentTask("Task 9", "Content 9", ["daily"], False, ("09:00", "12:00"))
    task10 = Task("Task 10", "Content 10", False, ("10:00", "11:00"), "2024-10-13")
    
    assert time_frame_overlap(task9, task10) == True, "Test Case 5 Failed"

    # Edge case: ending exactly when another starts
    task11 = FrequentTask("Task 11", "Content 11", ["daily"], False, ("09:00", "10:00"))
    task12 = Task("Task 12", "Content 12", False, ("10:00", "11:00"), "2024-10-13")
    
    assert time_frame_overlap(task11, task12) == False, "Test Case 6 Failed"

    task13 = FrequentTask("Task 12", "Content 12", ["daily"], False, ("09:00", "17:00"))
    task14 = Task("Task 12", "Content 12", True, ("16:00", "21:00"), "2024-10-13")
    
    assert time_frame_overlap(task13, task14) == True, "Test Case 6 Failed"

    print("All test cases passed!")

# Run the tests
test_time_frame_overlap()
