from fastapi import Request, status
from fastapi.responses import JSONResponse

class ModelNotLoadedException(Exception):
    def __init__(self, message: str = "Machine Learning model pipeline is not loaded or missing."):
        self.message = message
        super().__init__(self.message)

class InvalidInputException(Exception):
    def __init__(self, message: str = "Input text is invalid or empty."):
        self.message = message
        super().__init__(self.message)

async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": exc.message, "status": "model_unavailable"}
    )

async def invalid_input_handler(request: Request, exc: InvalidInputException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.message, "status": "invalid_input"}
    )
