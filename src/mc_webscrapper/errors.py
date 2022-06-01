
class Error(Exception):
    """Base class for other exceptions"""


    def __init__(self, msg=''):
        self.message = msg


    def __str__(self):
        return f"ERROR: Somethign went wrong with {self.message}"

