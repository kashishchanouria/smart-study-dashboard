import sqlite3
from datetime import datetime
import pandas as pd

DB_NAME = "study_tracker.db"

SUBJECT_TOPICS = {
    "Math": ["Formulas", "Practice Questions", "Trigonometry", "Algebra", "Revision"],
    "Physics": ["Concepts", "Numericals", "Diagrams", "Revision", "Mock Test"],
    "CS": ["Python Basics", "SQL", "DBMS", "Coding Practice", "Revision"],
    "History": ["Dates", "Important Events", "Chapter Reading", "Notes", "Revision"],
    "Accounts": ["Journal Entries", "Ledger", "Trial Balance", "Practice", "Revision"]
}

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            created_at TEXT,
            sleep REAL,
            focus REAL,
            study_hours REAL,
            breaks REAL,
            predicted_score REAL,
            subject TEXT,
            difficulty TEXT,
            plan TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_history(username, sleep, focus, study_hours, breaks, predicted_score,
                 subject="", difficulty="", plan=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO history (
            username, created_at, sleep, focus, study_hours, breaks,
            predicted_score, subject, difficulty, plan
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        float(sleep),
        float(focus),
        float(study_hours),
        float(breaks),
        float(predicted_score),
        subject,
        difficulty,
        plan
    ))
    conn.commit()
    conn.close()

def load_history(username=None):
    conn = get_connection()
    if username:
        query = """
            SELECT * FROM history
            WHERE username = ?
            ORDER BY id DESC
        """
        df = pd.read_sql_query(query, conn, params=(username,))
    else:
        query = """
            SELECT * FROM history
            ORDER BY id DESC
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def smart_suggestion(subject, difficulty, days_left, daily_hours, focus, sleep, username="user"):
    topic_list = SUBJECT_TOPICS.get(subject, ["Concepts", "Revision", "Practice", "Mock Test"])

    history_df = load_history(username)
    recent_count = len(history_df.head(5))

    variant = (int(days_left) + recent_count + int(focus)) % 3

    if difficulty.lower() == "hard":
        templates = [
            ["30 min: Weak concepts", "45 min: Practice", "30 min: Revision", "15 min: Quick test"],
            ["40 min: Weak concepts", "40 min: Practice", "20 min: Revision", "20 min: MCQs"],
            ["25 min: Concept reading", "50 min: Problem solving", "30 min: Revision", "15 min: Recap"]
        ]
    elif difficulty.lower() == "medium":
        templates = [
            ["25 min: Reading", "35 min: Practice", "20 min: Revision", "10 min: Notes"],
            ["30 min: Practice", "30 min: Revision", "20 min: Doubt solving", "10 min: Recap"],
            ["20 min: Reading", "40 min: Practice", "20 min: Revision", "20 min: Test"]
        ]
    else:
        templates = [
            ["20 min: Quick reading", "30 min: Practice", "15 min: Revision", "10 min: Recap"],
            ["15 min: Important points", "35 min: Practice", "15 min: Revision", "15 min: Test"],
            ["20 min: Notes", "25 min: Practice", "15 min: Revision", "10 min: Recall"]
        ]

    plan = templates[variant]
    topic_choice = topic_list[variant % len(topic_list)]

    suggestion_text = f"""
Subject: {subject}
Topic focus: {topic_choice}
Difficulty: {difficulty}
Days left: {days_left}
Daily hours: {daily_hours}

Recommended plan:
1. {plan[0]}
2. {plan[1]}
3. {plan[2]}
4. {plan[3]}

Extra advice:
- Sleep target: 7 to 8 hours
- If focus is low, start with easy topics
- End session with short revision
""".strip()

    return suggestion_text

def logical_adjustment(score, sleep, focus, study_hours, breaks):
    adjusted = float(score)

    adjusted += (float(study_hours) - 3) * 6
    adjusted += (float(focus) - 5) * 4
    adjusted += (float(sleep) - 6) * 2
    adjusted -= float(breaks) * 2

    adjusted = max(0, min(100, adjusted))
    return round(adjusted, 2)