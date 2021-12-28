import psycopg2  # Untuk PostgreSQL

# Semua SQL query dalam ""


def create_table():
    conn = psycopg2.connect(
        "dbname='udemy' user='postgres' password='postgres12345' host='localhost' port='5432'"
    )  # Perbedaan SQLITE3 dan PostgreSQL terbesar di sini
    cur = conn.cursor()  # cursor object
    cur.execute(
        "CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)"  # Membuat tabel bila tidak ada
    )
    conn.commit()
    conn.close()


def insert(item, quantity, price):  # Dibuat function supaya ga duplikasi data
    conn = psycopg2.connect(
        "dbname='udemy' user='postgres' password='postgres12345' host='localhost' port='5432'"
    )
    cur = conn.cursor()

    # (%s,%s,%s) untuk mencegah hacking SQL injection
    cur.execute(
        "INSERT INTO store VALUES (%s,%s,%s)", (item, quantity, price)
    )  # PostgreSQL pakai %s
    conn.commit()
    conn.close()


def view():
    conn = psycopg2.connect(
        "dbname='udemy' user='postgres' password='postgres12345' host='localhost' port='5432'"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()  # Ga perlu conn.commit() karena ga writing data ke DB
    conn.close()
    return rows  # Menghasilkan list


def delete(item):
    conn = psycopg2.connect(
        "dbname='udemy' user='postgres' password='postgres12345' host='localhost' port='5432'"
    )
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM store WHERE item=%s", (item,)
    )  # ada koma setelah item karena memang syntax gitu
    conn.commit()
    conn.close()


def update(quantity, price, item):
    conn = psycopg2.connect(
        "dbname='udemy' user='postgres' password='postgres12345' host='localhost' port='5432'"
    )
    cur = conn.cursor()
    cur.execute(
        "UPDATE store SET quantity=%s, price=%s WHERE item=%s",
        (quantity, price, item),  # Ga ada koma di belakang karena > 1 variable
    )
    conn.commit()
    conn.close()


insert("Coursera Course", 1, 50)
print(view())
