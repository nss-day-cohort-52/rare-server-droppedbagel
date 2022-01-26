import sqlite3
import json
from models import PostTag

def create_entrytag(new_tag):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO PostTags (post_id, tag_id)
        VALUES (?,?)
        """,(new_tag['post_id'], new_tag["tag_id"]))
        
        id = db_cursor.lastrowid
        
        new_tag['id'] = id
    
    return json.dumps(new_tag)

