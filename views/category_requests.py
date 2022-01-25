import sqlite3
import json
from models import Category


def get_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM Categories c
        ORDER BY label ASC
        """)
        categories = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__) #python __ is dunder
    return json.dumps(categories)

def create_category(new_cat):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Categories
            ( label )
        VALUES
            ( ? );
        """, (new_cat['label'],))
        id = db_cursor.lastrowid
        new_cat['id'] = id
    return json.dumps(new_cat)

def delete_category(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (id, ))

def edit_category(id, updated_cat):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Categories
            SET
                label = ?
        WHERE id = ?
        """, (updated_cat['label'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True