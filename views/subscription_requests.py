import sqlite3
import json
from datetime import datetime

from models import Subscription

def create_subscription(new_sub):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Subscriptions
            ( follower_id, author_id, created_on )
        VALUES
            ( ?, ?, ? );
        """, (new_sub['follower_id'], new_sub['author_id'], datetime.now()))
        id = db_cursor.lastrowid
        new_sub['id'] = id
    return json.dumps(new_sub)
