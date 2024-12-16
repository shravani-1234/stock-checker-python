from flask import g
import sqlite3

DATABASE = "stock_likes.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    db = get_db()
    c = db.cursor()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS like(stock TEXT NOT NULL, ip TEXT NOT NULL);
        CREATE UNIQUE INDEX IF NOT EXISTS like_idx ON like(stock, ip);
        """
    )
    db.commit()
