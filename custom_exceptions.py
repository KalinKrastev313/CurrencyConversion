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


class APIResponseError(CustomException):
    # When ForexAPI is down or the api key is expired, further attempts wouldn't bring different result
    CODES_WHICH_STOP_THE_PROGRAM = [503, 504, 509, 511, 599]

    def __init__(self, response):
        self.response = response
        self.error_message = f"The requested information is not cached and the API didn't provide it. Error {response.status_code}: {response.text}"
        self.should_finish_program = True if response.status_code == self.CODES_WHICH_STOP_THE_PROGRAM else False
