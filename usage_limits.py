"""Atomic, app-wide rolling API request limits stored on the server."""
import sqlite3
import time
from pathlib import Path


class UsageLimitError(RuntimeError):
    pass


def reserve_request(db_path=None, now=None):
    """Reserve before calling the API; failed calls count conservatively too."""
    path = Path(db_path) if db_path is not None else Path(__file__).parent / '.usage' / 'requests.sqlite'
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.time() if now is None else now
    conn = sqlite3.connect(path, timeout=10)
    try:
        conn.execute('BEGIN IMMEDIATE')
        conn.execute('CREATE TABLE IF NOT EXISTS requests (created REAL NOT NULL)')
        conn.execute('DELETE FROM requests WHERE created <= ?', (timestamp - 86400,))
        daily = conn.execute('SELECT COUNT(*) FROM requests').fetchone()[0]
        minute = conn.execute('SELECT COUNT(*) FROM requests WHERE created > ?', (timestamp - 60,)).fetchone()[0]
        if daily >= 50:
            raise UsageLimitError('This demo has reached its shared daily AI limit. Please try again later.')
        if minute >= 5:
            raise UsageLimitError('This demo is busy. Please wait a minute before trying again.')
        conn.execute('INSERT INTO requests VALUES (?)', (timestamp,))
        conn.commit()
    finally:
        conn.close()
