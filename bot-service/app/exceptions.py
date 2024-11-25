class NotExpensesFound(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = "Failed to get a valid expenses."
        super().__init__(msg)
