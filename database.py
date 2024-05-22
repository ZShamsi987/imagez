
import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS images (
                                id integer PRIMARY KEY,
                                label text NOT NULL,
                                image_path text NOT NULL
                            ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)

def insert_image(conn, label, image_path):
    sql = ''' INSERT INTO images(label,image_path)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (label, image_path))
    conn.commit()
    return cur.lastrowid

database = "data/images.db"
conn = create_connection(database)
create_table(conn)
