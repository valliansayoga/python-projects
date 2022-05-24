import sqlite3

# Semua SQL query dalam ""


def create_table():
    conn = sqlite3.connect(
        "lite.db"
    )  # variable of connection. Will make a new one if did not exist.

    cur = conn.cursor()  # cursor object
    cur.execute(
        "CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)"  # Membuat tabel bila tidak ada
    )
    conn.commit()
    conn.close()


def insert(item, quantity, price):  # Dibuat function supaya ga duplikasi data
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()

    # (?,?,?) untuk mencegah hacking SQL injection
    cur.execute("INSERT INTO store VALUES (?,?,?)", (item, quantity, price))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()  # Ga perlu conn.commit() karena ga writing data ke DB
    conn.close()
    return rows  # Menghasilkan list


def delete(item):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM store WHERE item=?", (item,)
    )  # ada koma setelah item karena memang syntax gitu
    conn.commit()
    conn.close()


def update(quantity, price, item):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute(
        "UPDATE store SET quantity=?, price=? WHERE item=?",
        (quantity, price, item),  # Ga ada koma di belakang karena > 1 variable
    )
    conn.commit()
    conn.close()


update(10, 100, "Pizza")
print(view())
