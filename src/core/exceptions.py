class FilterNotAllowed(Exception):
    def __init__(self, message="This filter is not allowed"):
        self.message = message
        super().__init__(self.message)