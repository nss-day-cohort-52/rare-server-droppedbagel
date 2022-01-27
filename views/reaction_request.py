import sqlite3
import json
from models import Reaction

def get_all_reactions():
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            r.id,
            r.label
        FROM Reactions t
        """)
        
        reactions = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            reaction = Reaction(row['id'], row['label'])
            reactions.append(reaction.__dict__)
    
    return json.dumps(reactions)


def get_single_reaction(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            r.id,
            r.label
        FROM Reactions t
        WHERE id = ?
        """, (id, ))
        
        data = db_cursor.fetchone()
        
        reaction = Reaction(data['id'], data['label'])
        
        return json.dumps(reaction.__dict__)

def create_reaction(new_reaction):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Reactions (label)
        VALUES (?)
        """,(new_reaction['label'],))
        
        id = db_cursor.lastrowid
        
        new_reaction['id'] = id
    
    return json.dumps(new_reaction)


def delete_reaction(id):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Reactions
        WHERE id = ?
        """, (id, ))
        
        db_cursor.execute("""
        DELETE FROM PostReactions
        WHERE reaction_id = ?
        """, (id, ))


def update_reaction(id, new_reaction):
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Reactions
            SET
                label = ?
        WHERE id = ?
        """, (new_reaction['label'], id))
        
        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            return False
        else:
            return True