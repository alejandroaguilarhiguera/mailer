from fastapi import APIRouter

router = APIRouter(tags=["Health"])
from app.services.mail_service import MailService
from app.schemas.schemas import TestMailRequest

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/test")
def test_endpoint(request: TestMailRequest):
    MailService().send_mail(
        to=request.email,
        subject="Test Email",
        text="This is a test email."
    )
    return {"message": "mail enviado"}