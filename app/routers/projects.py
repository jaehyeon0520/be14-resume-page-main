import json
import pathlib

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def load_projects_json():
    try:
        with open(BASE_DIR.parent / "projects.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] projects.json 로딩 실패: {e}")
        return []

@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    projects = load_projects_json()
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})
