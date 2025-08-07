from typing import Any, Optional
from pydantic import BaseModel

class DefaultResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None