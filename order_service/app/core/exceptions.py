class AppException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code


class NotFoundError(AppException):
    def __init__(self, detail: str = "Объект не найден"):
        super().__init__(detail=detail, status_code=404)


class AlreadyExistsError(AppException):
    def __init__(self, detail: str = "Объект уже существует"):
        super().__init__(detail=detail, status_code=409)


class CreateError(AppException):
    def __init__(self, detail: str = "Ошибка при создании"):
        super().__init__(detail=detail, status_code=400)


class DeleteError(AppException):
    def __init__(self, detail: str = "Ошибка при удалении"):
        super().__init__(detail=detail, status_code=400)
