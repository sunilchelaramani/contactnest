# Create Not Found Exception
class NotFoundException(Exception):
    def __init__(self, message: str = "contact not found"):
        super().__init__(message)
        self.message = message

class UnauthorizedException(Exception):
    def __init__(self, message: str = "unauthorized"):
        super().__init__(message)
        self.message = message