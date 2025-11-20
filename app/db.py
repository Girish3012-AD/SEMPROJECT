import sqlite3
from flask import g
from config import Config

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(Config.DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        """)
        
        # Create admins table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        
        # Create complaints table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                complaint_text TEXT NOT NULL,
                category TEXT,
                status TEXT DEFAULT 'Pending',
                submitted_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Add password_hash to users if it doesn't exist (migration)
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'password_hash' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        
        # Create default admin if none exists
        cursor.execute("SELECT COUNT(*) FROM admins")
        if cursor.fetchone()[0] == 0:
            from werkzeug.security import generate_password_hash
            default_username = 'admin'
            default_password = 'admin123'
            hashed_password = generate_password_hash(default_password)
            cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", 
                           (default_username, hashed_password))
            print(f"Default admin created: username={default_username}")
        
        db.commit()
