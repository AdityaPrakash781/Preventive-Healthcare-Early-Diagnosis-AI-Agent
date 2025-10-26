# core/database.py
"""
Simple SQLite wrapper for health metrics and reminders.
Why: Local persistence for auditability and offline demos.
How: Exposes init_db(), insert_metric(), fetch_metrics(), insert_reminder(), fetch_reminders()
"""

import os
import sqlite3
from datetime import datetime

DATA_DIR = "data" #A variable which stores the Folder Name 
DB_PATH = os.path.join(DATA_DIR, "health.db") #Creates the full path to the database file.

def get_conn():
    os.makedirs(DATA_DIR, exist_ok=True) #This line tells the OS to create the folder named "data"
    conn = sqlite3.connect(DB_PATH, check_same_thread=False) #This is the core line.This parameter tells SQLite to allow the database connection to be used by different threads. This is a common setting for web applications or multi-threaded programs, though for more complex apps, a "connection pool" is a safer pattern.
    return conn


def init_db():

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        timestamp TEXT,
        metric TEXT,
        value TEXT,
        source TEXT,
        risk TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        timestamp TEXT,
        task TEXT,
        time_of_day TEXT,
        active INTEGER
    )
    """)
    conn.commit()
    conn.close()

def insert_metric(user_id, metric, value, source="device", risk=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO health_metrics (user_id, timestamp, metric, value, source, risk) VALUES (?, ?, ?, ?, ?, ?)", #? are PlaceHolders for values
        (user_id, datetime.utcnow().isoformat(), metric, str(value), source, risk)
    )
    conn.commit() #This line saves the changes. When you execute commands, they are part of a "transaction.",This line finalizes them.
    conn.close() #Closes connection to the db ,Frees up the resources

def fetch_metrics(user_id=None, limit=100):
    conn = get_conn()
    cur = conn.cursor()
    if user_id:
        cur.execute("SELECT id, timestamp, metric, value, source, risk FROM health_metrics WHERE user_id=? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    else:
        cur.execute("SELECT id, timestamp, metric, value, source, risk FROM health_metrics ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_reminder(user_id, task, time_of_day):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO reminders (user_id, timestamp, task, time_of_day, active) VALUES (?, ?, ?, ?, ?)",
                (user_id, datetime.utcnow().isoformat(), task, time_of_day, 1))
    conn.commit()
    conn.close()

def fetch_reminders(user_id=None):
    conn = get_conn()
    cur = conn.cursor()
    if user_id:
        cur.execute("SELECT id, timestamp, task, time_of_day, active FROM reminders WHERE user_id=?", (user_id,))
    else:
        cur.execute("SELECT id, timestamp, task, time_of_day, active FROM reminders")
    rows = cur.fetchall()
    conn.close()
    return rows
