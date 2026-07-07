"""
OptiCrop - Database Manager
Handles SQLite connection, table creation, user registration/login,
prediction tracking, and system stats.
"""

import sqlite3
import os
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = Path(__file__).resolve().parent / "opticrop.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and seed default administrator account."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create Predictions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            nitrogen REAL NOT NULL,
            phosphorus REAL NOT NULL,
            potassium REAL NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            ph REAL NOT NULL,
            rainfall REAL NOT NULL,
            predicted_crop TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    # Check if admin exists, if not, create default admin
    cursor.execute("SELECT * FROM users WHERE role = 'admin' LIMIT 1")
    admin = cursor.fetchone()
    if not admin:
        admin_fullname = "System Administrator"
        admin_username = "admin"
        admin_email = "admin@opticrop.com"
        admin_password_hash = generate_password_hash("admin123")
        cursor.execute("""
            INSERT INTO users (fullname, username, email, password_hash, role)
            VALUES (?, ?, ?, ?, 'admin')
        """, (admin_fullname, admin_username, admin_email, admin_password_hash))
        print("[INFO] Default admin account created.")
        
    conn.commit()
    conn.close()

def register_user(fullname, username, email, password, role='user'):
    """Registers a new user in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check username or email uniqueness
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        return False, "Username or Email already registered."
        
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("""
            INSERT INTO users (fullname, username, email, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        """, (fullname, username, email, hashed_password, role))
        conn.commit()
        conn.close()
        return True, "Registration successful."
    except Exception as e:
        conn.close()
        return False, f"Database error: {str(e)}"

def verify_user(username_or_email, password):
    """Verifies user credentials. Handles username or email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM users 
        WHERE username = ? OR email = ?
    """, (username_or_email, username_or_email))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return {
            'id': user['id'],
            'fullname': user['fullname'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fullname, username, email, role, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fullname, username, email, role, created_at FROM users ORDER BY id DESC")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ? AND role != 'admin'", (user_id,))
    conn.commit()
    conn.close()
    return True

def add_prediction(user_id, nitrogen, phosphorus, potassium, temp, humidity, ph, rainfall, predicted_crop, confidence):
    """Log a crop recommendation prediction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (user_id, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, predicted_crop, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, nitrogen, phosphorus, potassium, temp, humidity, ph, rainfall, predicted_crop, confidence))
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prediction_id

def get_prediction_by_id(prediction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions WHERE id = ?", (prediction_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_predictions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_all_predictions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, u.username as username 
        FROM predictions p 
        LEFT JOIN users u ON p.user_id = u.id 
        ORDER BY p.created_at DESC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def clear_all_predictions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()
    return True

def get_system_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'user'")
    stats['total_users'] = cursor.fetchone()[0]
    
    # Total Predictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    stats['total_predictions'] = cursor.fetchone()[0]
    
    # Average soil parameters
    cursor.execute("""
        SELECT AVG(nitrogen), AVG(phosphorus), AVG(potassium), AVG(temperature), AVG(humidity), AVG(ph), AVG(rainfall) 
        FROM predictions
    """)
    avg_row = cursor.fetchone()
    if avg_row and avg_row[0] is not None:
        stats['avg_n'] = round(avg_row[0], 1)
        stats['avg_p'] = round(avg_row[1], 1)
        stats['avg_k'] = round(avg_row[2], 1)
        stats['avg_temp'] = round(avg_row[3], 1)
        stats['avg_hum'] = round(avg_row[4], 1)
        stats['avg_ph'] = round(avg_row[5], 1)
        stats['avg_rain'] = round(avg_row[6], 1)
    else:
        stats['avg_n'] = stats['avg_p'] = stats['avg_k'] = stats['avg_temp'] = stats['avg_hum'] = stats['avg_ph'] = stats['avg_rain'] = 0.0
        
    # Most predicted crop
    cursor.execute("""
        SELECT predicted_crop, COUNT(*) as count 
        FROM predictions 
        GROUP BY predicted_crop 
        ORDER BY count DESC 
        LIMIT 1
    """)
    crop_row = cursor.fetchone()
    stats['most_predicted_crop'] = crop_row[0] if crop_row else "None"
    
    conn.close()
    return stats

if __name__ == "__main__":
    init_db()
    print("Database initialised successfully.")
