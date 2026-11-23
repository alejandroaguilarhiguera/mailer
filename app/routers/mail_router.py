from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemas.schemas import MailResponse, MailRequest
from app.services.mail_service import MailService
# from app.services.quotation_service import QuotationService

router = APIRouter(tags=["mail"])


@router.post(
    "/send_mail",
    response_model=MailResponse,
    status_code=status.HTTP_200_OK
)
def send_mail(
    mail_in: MailRequest,
    service: MailService = Depends(MailService),
):
   return service.send_mail(mail_in.to, mail_in.subject, mail_in.text, mail_in.html)

