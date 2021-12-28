"""
Ini adalah backend dari:
Book Storage Database

Powered by SQLITE3
"""

import sqlite3 as sq3


def connect():
    conn = sq3.connect("books.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)"
    )
    conn.commit()
    conn.close()


def insert(title, author, year, isbn):
    conn = sq3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book VALUES(NULL,?,?,?,?)", (title, author, year, isbn))
    conn.commit()
    conn.close()


def view():
    conn = sq3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows


def search(title="", author="", year="", isbn=""):  # Empty string for default value
    conn = sq3.connect("books.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",
        (title, author, year, isbn),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def delete(id):  # Grabs the ID for delete function based on a selection on the list
    conn = sq3.connect("books.db")
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM book WHERE id=?", (id,)
    )  # Jangan lupa 1 koma kalau 1 parameter
    conn.commit()
    conn.close()


def update(id, title, author, year, isbn):
    conn = sq3.connect("books.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",
        (title, author, year, isbn, id),  # Ingat posisi argument penting
    )
    conn.commit()
    conn.close()


# update(1, "The Hell?", "Joe Mama", 1919, 123456)
# print(view())
