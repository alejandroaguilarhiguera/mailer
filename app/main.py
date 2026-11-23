import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.routes import api_router
from app.utils.exceptions import global_exception_handler
from dotenv import load_dotenv
import os

load_dotenv()

if os.environ.get("SMTP_HOST") is None:
    raise ValueError("SMTP_HOST environment variable is not set. Please set it in the .env file.")

if os.environ.get("SMTP_USERNAME") is None:
    raise ValueError("SMTP_USERNAME environment variable is not set. Please set it in the .env file.")

if os.environ.get("SMTP_PORT") is None:
    raise ValueError("SMTP_PORT environment variable is not set. Please set it in the .env file.")

if os.environ.get("SMTP_PASSWORD") is None:
    raise ValueError("SMTP_PASSWORD environment variable is not set. Please set it in the .env file.")


if os.environ.get("MAIL_FROM") is None:
    raise ValueError("MAIL_FROM environment variable is not set. Please set it in the .env file.")

if os.environ.get("SMTP_USE_TLS") is None:
    raise ValueError("SMTP_USE_TLS environment variable is not set. Please set it in the .env file.")


app = FastAPI(
    title="mailer interface",
    version="1.0.0",
)
@app.get("/")
def root():
    return {"message": "Welcome to the mailer API"}

# Incluir todas las rutas desde el router centralizado
app.include_router(api_router)

# Exception handlers
app.add_exception_handler(Exception, global_exception_handler)