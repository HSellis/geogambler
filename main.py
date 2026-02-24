from fastapi import FastAPI, Form, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from typing import List
import sqlite3
import os
import logging

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="supersecret")

# Static files (optional, for CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_PATH = "geogamblr.db"

# Automaatne andmebaasi loomine
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            name TEXT PRIMARY KEY,
            points INTEGER DEFAULT 0
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            is_open INTEGER
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_id INTEGER,
            choice TEXT,
            FOREIGN KEY(round_id) REFERENCES rounds(id)
        );
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_id INTEGER,
            name TEXT,
            answer TEXT,
            FOREIGN KEY(round_id) REFERENCES rounds(id)
        );
        """)
        conn.commit()
        conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def user_home(request: Request):
    conn = get_db()
    leaderboard = conn.execute("SELECT name, points FROM leaderboard ORDER BY points DESC").fetchall()
    round_info = conn.execute("SELECT * FROM rounds WHERE is_open=1").fetchone()
    choices = []
    question = None
    if round_info:
        question = round_info["question"]
        choices = conn.execute("SELECT choice FROM choices WHERE round_id=?", (round_info["id"],)).fetchall()
    return templates.TemplateResponse("user_home.html", {"request": request, "leaderboard": leaderboard, "question": question, "choices": [c["choice"] for c in choices]})

@app.post("/predict")
def predict(name: str = Form(...), answer: str = Form(...)):
    conn = get_db()
    round_info = conn.execute("SELECT * FROM rounds WHERE is_open=1").fetchone()
    if not round_info:
        return JSONResponse(content={"error": "Ennustusvoor pole avatud."}, status_code=status.HTTP_400_BAD_REQUEST)
    already_predicted = conn.execute("SELECT * FROM predictions WHERE round_id=? AND name=?", (round_info["id"], name)).fetchone()
    if already_predicted:
        return JSONResponse(content={"error": "Selle nimega on juba ennustatud!"}, status_code=status.HTTP_409_CONFLICT)
    conn.execute("INSERT INTO predictions (round_id, name, answer) VALUES (?, ?, ?)", (round_info["id"], name, answer))
    conn.commit()
    return JSONResponse(content={"success": "Ennustatud!"}, status_code=status.HTTP_200_OK)

@app.get("/admin")
def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin")
def admin_auth(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        request.session["admin"] = True
        return RedirectResponse("/admin/dashboard", status_code=302)
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Vale parool!"})

@app.get("/admin/dashboard")
def admin_dashboard(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse("/admin", status_code=302)
    conn = get_db()
    leaderboard = conn.execute("SELECT name, points FROM leaderboard ORDER BY points DESC").fetchall()
    round_info = conn.execute("SELECT * FROM rounds WHERE is_open=1").fetchone()
    choices = []
    if round_info:
        choices_db = conn.execute("SELECT choice FROM choices WHERE round_id=?", (round_info["id"],)).fetchall()
        choices = [c["choice"] for c in choices_db]
        round_info = dict(round_info)
        round_info["choices"] = choices
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "leaderboard": leaderboard, "round_info": round_info})

@app.post("/admin/start-round")
def start_round(request: Request, question: str = Form(...), choices: List[str] = Form([])):
    if not request.session.get("admin"):
        return RedirectResponse("/admin", status_code=302)
    conn = get_db()
    open_round = conn.execute("SELECT * FROM rounds WHERE is_open=1").fetchone()
    if open_round:
        return templates.TemplateResponse("admin_dashboard.html", {"request": request, "error": "Voor on juba avatud!"})
    conn.execute("INSERT INTO rounds (question, is_open) VALUES (?, 1)", (question,))
    round_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    for choice in choices:
        conn.execute("INSERT INTO choices (round_id, choice) VALUES (?, ?)", (round_id, choice)) 
    conn.commit()
    return RedirectResponse("/admin/dashboard", status_code=302)

@app.post("/admin/end-round")
def end_round(request: Request, correct_answers: List[str] = Form([])):
    if not request.session.get("admin"):
        return RedirectResponse("/admin", status_code=302)
    conn = get_db()
    round_info = conn.execute("SELECT * FROM rounds WHERE is_open=1").fetchone()
    if not round_info:
        return templates.TemplateResponse("admin_dashboard.html", {"request": request, "error": "Avatud vooru pole!"})
    predictions = conn.execute("SELECT name, answer FROM predictions WHERE round_id=?", (round_info["id"],)).fetchall()
    for pred in predictions:
        logging.debug(f"Checking prediction: {pred['name']} - {pred['answer']} against correct answers: {correct_answers}")
        if pred["answer"] in correct_answers:
            conn.execute("INSERT OR IGNORE INTO leaderboard (name, points) VALUES (?, 0)", (pred["name"],))
            conn.execute("UPDATE leaderboard SET points = points + 1 WHERE name=?", (pred["name"],))
    conn.execute("UPDATE rounds SET is_open=0 WHERE id=?", (round_info["id"],))
    conn.commit()
    return RedirectResponse("/admin/dashboard", status_code=302)
