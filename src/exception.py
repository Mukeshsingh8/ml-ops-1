import sys 
from src.logger import logging

def build_detailed_error_message(error: BaseException) -> str:
    #use the imported sys directly; don't pass it around
    _, _, exc_tb = sys.exc_info()
    if exc_tb is None:
        # Called outside an except block
        return f"Error: {error}"
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno
    return f"Error occured in Python script [{file_name}] at line[{line_no}] : {error}"

class CustomException(Exception):
    def __init__(self, error: BaseException):
        #compute the detailed message first
        detailed = build_detailed_error_message(error)
        # Initialize the base Exception with a sensible message
        super().__init__(detailed) #or super().__init__(str(error))
        #keep it as instance state if you want to control __str__
        self.error_message = detailed

    def __str__(self) -> str:
        return self.error_message

"""
__str__ controls what gets printed for your exception.

When you do print(e), f"{e}", or when many loggers render the exception, Python calls e.__str__().

By returning self.error_message, you force the displayed text to be that value.

In your current class, since you already did super().__init__(detailed), the base Exception would make str(e) 
show the same detailed message anyway. So this __str__ is redundant right now.
"""


# try:
#     1 / 0
# except Exception as e:
#     ce = CustomException(e)
#     logging.error(str(ce), exc_info=False)
