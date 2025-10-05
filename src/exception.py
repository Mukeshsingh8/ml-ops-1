import sys
import traceback
from typing import Optional

# --- Composition + Abstraction ---
# This helper is NOT a class; the exception class will USE it.
# It hides the nitty-gritty of extracting traceback details.
def build_detailed_error_message(error:BaseException) -> str: # error:BaseException says: error parameter is an instance of BaseException (or a subclass)
    """
    Abstraction: provide a simple function that returns a nice message.
    Internally, it uses sys.exc_info() and traceback objects (details hidden).

    Why baseException? In python the exception hierarchy starts at BaseException -> Exception -> ValueError, TypeError,. etc.
    Using BaseException mean "I accept any real exception object."

    Type hints don't change runtime behavior; they help readbility, IDRs, and static checkers (e.g., mypy)
    """
    _,_,exc_tb = sys.exc_info()  # returns (exc_type, exc_value, traceback)

    if exc_tb is None:
        # Called outside an except block; fall back to a plain message
        """
        Why can exc_tb be None?
        sys.exc_info() only contains meaningful data while you'r inside an except block on the same thread
        outside an except, Python has no "current exception", so it returns (None) - and then exc_tb is None

        So the guard is defensive programming: if someone mistakenly calls the helper outside an except,
        we still return a plain message instead of crashing by accessing exc_tb.tb_frame.
        """
        return f"Error: {error}"

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno

    return f"Error occurred in Python script [{file_name}] at line [{line_no}] : {error}"

# --- Inheritance + Encapsulation + Polymorphism ---
class CustomException(Exception):
    """
    Inheritance: CustomException IS-A Python Exception.

    Encapsulation: it stores its own state (error_message) and exposes behavior
    via __str__() while hiding how the message is constructed.

    Polymorphism: it overrides __str__ to change how it prints.
    """
    def __init__(self, error:BaseException, context:Optional[dict]=None):
        """
        Constructor chaining: call parent to initialize base Exception.
        Store extra state (context) and build a detailed message.
        """
        #Initialize the parent Exception with minimal message
        super().__init__(str(error)) #Inheritance + proper base init
        # Encapsulated state (kept inside the object)
        self.context = context or {}
        self.error_message = build_detailed_error_message(error)  # Composition

    def __str__(self) -> str:
        """
        Polymorphism: overrides Exception.__str__ to control string output.
        """
        if self.context:
            return f"{self.error_message} | context={self.context}"
        return self.error_message