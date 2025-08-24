import sqlite3
import os

def init_db():
    # Use a path that works in both local and HF Spaces environments
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Table for tracking sessions and question limits
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE,
            questions_asked INTEGER DEFAULT 0
        )
    ''')
    
    # Table for storing known Q&A
    c.execute('''
        CREATE TABLE IF NOT EXISTS qa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    ''')
    
    # Table for storing unknown questions
    c.execute('''
        CREATE TABLE IF NOT EXISTS unknown_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_session(session_id):
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, questions_asked FROM sessions WHERE session_id = ?", (session_id,))
    row = c.fetchone()
    conn.close()
    return row

def add_session(session_id):
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO sessions (session_id, questions_asked) VALUES (?, ?)", (session_id, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def save_unknown_question(question):
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO unknown_questions (question) VALUES (?)", (question,))
    conn.commit()
    conn.close()

def add_qa(question, answer):
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO qa (question, answer) VALUES (?, ?)", (question, answer))
    except sqlite3.IntegrityError:
        # Update if question already exists
        c.execute("UPDATE qa SET answer = ? WHERE question = ?", (answer, question))
    conn.commit()
    conn.close()

def get_answer(question):
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT answer FROM qa WHERE question = ?", (question,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def add_unknown_question(question):
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO unknown_questions (question) VALUES (?)", (question,))
    conn.commit()
    conn.close()

def increment_questions(session_id):
    db_path = os.path.join(os.path.dirname(__file__), 'me', 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE sessions SET questions_asked = questions_asked + 1 WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

init_db()
