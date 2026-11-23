from datetime import date
from typing import Optional, Union
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Dict, Any

class MailResponse(BaseModel):
    message: str

class MailRequest(BaseModel):
    to: Union[EmailStr, List[EmailStr]] = Field(..., description="Recipient email address or list of addresses")
    subject: str = Field(..., description="Subject of the email")
    text: str = Field(..., description="Plain text content of the email")
    html: Optional[str] = Field(None, description="HTML content of the email (optional)")

class TestMailRequest(BaseModel):
    email: EmailStr