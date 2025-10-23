from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class AIOptions(BaseModel):
    enable_pbr: bool = True
    should_remesh: bool = True
    should_texture: bool = True
    ai_model: Literal["latest", "meshy-5"] = "latest"

class SetEmailRequest(BaseModel):
    recipient_email: EmailStr = Field(..., description="결과를 통보받을 이메일 주소")