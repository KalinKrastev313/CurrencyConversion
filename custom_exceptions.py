from abc import ABC, abstractmethod


class CustomException(ABC, Exception):
    @abstractmethod
    def __init__(self):
        self.error_message = None
        self.should_finish_program = False


class ProgramEndedException(CustomException):
    def __init__(self):
        self.error_message = ""
        self.should_finish_program = True


class DateInWrongFormat(CustomException):
    def __init__(self):
        self.error_message = "Error: The date format should be YYYY-MM-DD."
        self.should_finish_program = True
