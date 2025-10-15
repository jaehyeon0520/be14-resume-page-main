import json
import pathlib
import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

logger = logging.getLogger(__name__)

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    projects = []
    try:
        with open(BASE_DIR.parent / "projects.json", "r", encoding="utf-8") as f:
            projects = json.load(f)
    except Exception as e:
        logger.error(f"projects.json 읽기 실패: {e}")

    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "projects": projects
        }
    )
