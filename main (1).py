from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db_requests import *


app = FastAPI()
conn = get_db_connection()
cur = conn.cursor()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_notes(request: Request):
    notes = get_note(cur)
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes.keys()})

@app.post("/add")
async def add_note(request: Request, note: str = Form(...), name: str = Form(...)):
    add_new_note(conn, name, note)
    return await read_notes(request)


@app.get('/note/{note_name}')
async def read_note(reuest: Request, note_name: str):
    notes = get_note(cur)
    return templates.TemplateResponse('read.html', {'request': reuest, "note": notes[note_name]})
