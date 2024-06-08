from abc import ABC, abstractmethod


class ProgramStateException(Exception):
    pass


class ProgramEndedException(Exception):
    pass


class FormattingInputException(ABC, Exception):
    @abstractmethod
    def __init__(self):
        self.correct_format_message = None
        self.should_finish_program = False


class DateInWrongFormat(FormattingInputException):
    def __init__(self):
        self.correct_format_message = "Error: The date format should be YYYY-MM-DD."
        self.should_finish_program = True
