class AuthenticationError(Exception):
    def __init__(self, message="Ошибка аутентификации"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    def __init__(self, message="Ресурс не найден"):
        self.message = message
        super().__init__(self.message)
