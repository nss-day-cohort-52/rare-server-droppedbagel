from pdb import post_mortem
import sqlite3
import json

from models import Post
from models.category import Category
from models.posttags import PostTag
from models.user_model import User

def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT 
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.id, 
            u.username,
            u.first_name,
            u.last_name,
            c.id,
            c.label
        FROM Posts p
        LEFT JOIN Users u
        ON p.user_id = u.id
        LEFT JOIN Categories c
        ON p.category_id = c.id
        ORDER BY publication_date DESC                
        """)
        
        posts = []
        
        dataset = db_cursor.fetchall()
        
        for row in dataset: 
            post = Post(row["id"], row["user_id"], row["category_id"], row["title"], row["publication_date"], row["image_url"], row["content"], row["approved"])
            user = User(row["user_id"], row["username"], row["first_name"], row["last_name"])
            category = Category(row["category_id"], row["label"])
            
            db_cursor.execute("""
            SELECT
                ep.id,
                ep.post_id,
                ep.tag_id,
                t.id,
                t.label
            FROM PostTags ep
            Left Join Tags t
            ON t.id = ep.tag_id
            WHERE post_id = ?             
            """, (row["id"],))
            
            tags = []
            database = db_cursor.fetchall()
            
            for row in database:
                tags.append(row["label"])
                
            post.tags = tags
            post.category = category.__dict__
            post.user = user.__dict__
            posts.append(post.__dict__)
            
    return json.dumps(posts) 
    
def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT 
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.id, 
            u.username,
            u.first_name,
            u.last_name,
            c.id,
            c.label
        FROM Posts p
        LEFT JOIN Users u
        ON p.user_id = u.id
        LEFT JOIN Categories c
        ON p.category_id = c.id
        WHERE p.id = ?
        ORDER BY publication_date DESC                
        """, (id,))
        
        dataset = db_cursor.fetchone()
        
        post = Post(dataset["id"], dataset["user_id"], dataset["category_id"], dataset["title"], dataset["publication_date"], dataset["image_url"], dataset["content"], dataset["approved"])
        post.user = User(dataset["user_id"], dataset["username"], dataset["first_name"], dataset["last_name"]).__dict__
        post.category = Category(dataset["category_id"], dataset["label"]).__dict__
        
        db_cursor.execute("""
            SELECT
                ep.id,
                ep.post_id,
                ep.tag_id,
                t.id,
                t.label
            FROM PostTags ep
            Left Join Tags t
            ON t.id = ep.tag_id
            WHERE post_id = ?             
            """, (dataset["id"],))
            
        tags = []
        database = db_cursor.fetchall()
            
        for row in database:
            tags.append(row["tag_id"])
                
        post.tags = tags
            
    return json.dumps(post.__dict__) 

def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        DELETE from Posts
        WHERE id = ?
        """, (id,))
        
        db_cursor.execute("""
        DELETE from PostTags
        WHERE post_id = ?
        """, (id,))
        
        db_cursor.execute("""
        DELETE from Comments
        WHERE post_id = ?                  
        """, (id, ))
        
def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES 
            (?,?,?,?,?,?,?)                  
        """, (new_post["user_id"], new_post["category_id"], new_post["title"], new_post["publication_date"], new_post["image_url"], new_post["content"], new_post["approved"]))
        
        id = db_cursor.lastrowid
        new_post["id"] = id
        
    return json.dumps(new_post)

def update_post(id, updated_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?   
        """, (updated_post["user_id"], updated_post["category_id"], updated_post["title"], updated_post["publication_date"], updated_post["image_url"], updated_post["content"], updated_post["approved"], id))

        if "tags" in updated_post:
            db_cursor.execute("""
            DELETE FROM PostTags
            WHERE post_id = ?
            """, (id, ))
            for tag_id in updated_post["tags"]:
                db_cursor.execute("""
                INSERT INTO PostTags (post_id, tag_id)
                VALUES (?, ?)
                """, (updated_post["id"], tag_id))
        
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else: 
        return True 