import json
import pathlib
import smtplib
from email.mime.text import MIMEText

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def load_projects():
    """projects.json 파일을 읽어 반환하는 함수"""
    projects_path = BASE_DIR.parent / "projects.json"
    try:
        with open(projects_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []  # 혹은 빈 리스트 반환하여 템플릿 에러 방지


@router.get("/contact", response_class=HTMLResponse)
async def contact_form(request: Request):
    projects = load_projects()
    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "projects": projects,
            "contact_email": settings.CONTACT_EMAIL,
        },
    )


@router.post("/contact", response_class=HTMLResponse)
async def send_mail(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form("문의"),
    message: str = Form(...),
):
    projects = load_projects()

    try:
        body = f"보낸 사람: {name} ({email})\n\n{message}"
        msg = MIMEText(body, _charset="utf-8")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_USER
        msg["To"] = settings.EMAIL_USER

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.send_message(msg)

        result = "메일이 성공적으로 전송되었습니다."
    except Exception as e:
        # 실제 운영환경에선 logging 추가 권장
        result = "메일 전송에 실패했습니다. 잠시 후 다시 시도해주세요."

    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "projects": projects,
            "contact_email": settings.CONTACT_EMAIL,
            "result": result,
        },
    )
