import sqlite3
import hashlib
import os
import re

DB_FILE = "users.db"

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            key_salt BLOB NOT NULL,
            email TEXT UNIQUE NOT NULL      
        )
    ''')
    conn.commit()
    conn.close()



def register_user(username, password, email):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        return "Użytkownik już istnieje!"
    
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone():
        conn.close()
        return "Podany e-mail jest już zarejestrowany!"

    salt = os.urandom(16) 
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("INSERT INTO users (username, password_hash, key_salt, email) VALUES (?, ?, ?, ?)", 
                   (username, password_hash, salt, email))
    conn.commit()
    conn.close()
    return "Rejestracja zakończona sukcesem!"

def get_user_salt(username, password):
    """Pobieranie hasła, soli i e-maila użytkownika"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash, key_salt, email FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return "Użytkownik nie istnieje", None

    if len(result) == 2:
        stored_password_hash, salt = result
        email = None  
    elif len(result) == 3:
        stored_password_hash, salt, email = result
    else:
        return "Błąd w bazie danych", None

    if hashlib.sha256(password.encode()).hexdigest() != stored_password_hash:
        return "Niepoprawne hasło", None

    return None, salt, email




def check_password_strength(password):    
    if len(password) < 8:
        return "Hasło musi mieć co najmniej 8 znaków!"
    if not any(char.isupper() for char in password):
        return "Hasło musi zawierać co najmniej jedną wielką literę!"
    if not any(char.islower() for char in password):
        return "Hasło musi zawierać co najmniej jedną małą literę!"
    if not any(char.isdigit() for char in password):
        return "Hasło musi zawierać co najmniej jedną cyfrę!"
    if not re.search(r"[!@#$%^&*]", password):
        return "Hasło musi zawierać co najmniej jeden znak specjalny (!@#$%^&*)!"
    return None


def is_valid_username(username):
    if len(username) < 4:
        return "Nazwa użytkownika musi mieć co najmniej 4 znaki!"
    if not re.match(r"^[a-zA-Z0-9_.-]+$", username):
        return "Nazwa użytkownika może zawierać tylko litery, cyfry i znaki: _ . -"
    return None