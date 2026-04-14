"""
backend.py
ImageShield backend module for encryption, decryption, and SQLite storage.
"""

import os
import sqlite3
import io
import hashlib
import base64
from datetime import datetime
from typing import Optional, List, Tuple

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT = b"ImageShieldSalt2026"
DEFAULT_DB_FILENAME = "imageshield.db"


def derive_key_from_password(password: str, salt: bytes = SALT) -> bytes:
    """Derive a Fernet-compatible key from a password."""
    if not password:
        raise ValueError("Password must not be empty")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def calculate_sha256(data: bytes) -> str:
    """Return the SHA-256 hash of the provided data."""
    return hashlib.sha256(data).hexdigest()


def encrypt_image_bytes(image_bytes: bytes, password: str) -> bytes:
    """Encrypt raw image bytes and return encrypted payload."""
    key = derive_key_from_password(password)
    fernet = Fernet(key)
    return fernet.encrypt(image_bytes)


def decrypt_image_bytes(encrypted_bytes: bytes, password: str) -> bytes:
    """Decrypt encrypted image bytes and return original image bytes."""
    key = derive_key_from_password(password)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_bytes)


def encrypt_image_file(input_path: str, password: str) -> bytes:
    """Read an image file and return encrypted bytes."""
    with open(input_path, "rb") as f:
        image_bytes = f.read()
    return encrypt_image_bytes(image_bytes, password)


def decrypt_image_file(input_path: str, password: str, output_path: Optional[str] = None) -> str:
    """Decrypt an encrypted file and save decrypted bytes to output_path."""
    with open(input_path, "rb") as f:
        encrypted_bytes = f.read()

    decrypted_bytes = decrypt_image_bytes(encrypted_bytes, password)

    if output_path is None:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(os.path.dirname(input_path), f"{base_name}_decrypted")

    with open(output_path, "wb") as f:
        f.write(decrypted_bytes)

    return output_path


def init_database(db_path: str = DEFAULT_DB_FILENAME) -> None:
    """Create the images table if it does not already exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            format TEXT,
            size INTEGER,
            encrypted_at TEXT,
            file_hash TEXT,
            tags TEXT,
            data BLOB
        )
        """
    )
    conn.commit()
    conn.close()


def save_encrypted_image_to_database(
    filename: str,
    file_format: str,
    size: int,
    encrypted_bytes: bytes,
    password: str,
    tags: str = "",
    db_path: str = DEFAULT_DB_FILENAME,
) -> int:
    """Encrypt image content and store it in the SQLite database."""
    init_database(db_path)

    file_hash = calculate_sha256(encrypted_bytes)
    encrypted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO images (filename, format, size, encrypted_at, file_hash, tags, data) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (filename, file_format, size, encrypted_at, file_hash, tags, sqlite3.Binary(encrypted_bytes)),
    )
    image_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return image_id


def list_encrypted_images(db_path: str = DEFAULT_DB_FILENAME, search: Optional[str] = None) -> List[Tuple]:
    """Return a list of stored encrypted images."""
    init_database(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if search:
        search_term = f"%{search.lower()}%"
        cursor.execute(
            "SELECT id, filename, format, size, encrypted_at, tags FROM images WHERE lower(filename) LIKE ? OR lower(tags) LIKE ? ORDER BY encrypted_at DESC",
            (search_term, search_term),
        )
    else:
        cursor.execute(
            "SELECT id, filename, format, size, encrypted_at, tags FROM images ORDER BY encrypted_at DESC"
        )
    rows = cursor.fetchall()
    conn.close()
    return rows


def load_encrypted_image(db_path: str, image_id: int) -> Optional[Tuple]:
    """Return the database row for a given encrypted image id."""
    init_database(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, filename, format, size, encrypted_at, tags, data FROM images WHERE id = ?",
        (image_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def delete_encrypted_image(db_path: str, image_id: int) -> None:
    """Delete an encrypted image record from the database."""
    init_database(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("ImageShield backend module is ready.")
    print(f"Database path: {DEFAULT_DB_FILENAME}")
