import sqlite3

class PostDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        
    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS posts(id text PRIMARY KEY)')
        
    def has_post(self, post_id):
        self.cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
        return self.cursor.fetchone() is not None
    
    def add_post(self, post_id):
        if not self.has_post(post_id):
            self.cursor.execute('INSERT INTO posts VALUES (?)', (post_id,))
            self.conn.commit()
