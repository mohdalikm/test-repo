"""
Database operations module with performance issues.
Demonstrates N+1 queries, missing connection pooling, and inefficient database operations.
"""

import sqlite3
import time
import threading
from typing import List, Dict, Any, Optional
import json


class DatabaseManager:
    def __init__(self, db_path: str = "performance_test.db"):
        self.db_path = db_path
        self.connections = {}  # BAD: Manual connection management without pooling
        self._setup_database()
    
    def _setup_database(self):
        """
        Set up the database with sample tables and data
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create tables without proper indexes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # BAD: Missing index on frequently queried columns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                likes INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # BAD: Missing index on foreign key
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                post_id INTEGER,
                user_id INTEGER,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Insert sample data if tables are empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            self._insert_sample_data(cursor)
        
        conn.commit()
        cursor.close()
    
    def _insert_sample_data(self, cursor):
        """Insert sample data for testing"""
        # Insert users
        users_data = [
            (i, f"user_{i}", f"user_{i}@example.com", "active")
            for i in range(1, 101)  # 100 users
        ]
        cursor.executemany(
            "INSERT INTO users (id, username, email, status) VALUES (?, ?, ?, ?)",
            users_data
        )
        
        # Insert posts (5 posts per user)
        posts_data = []
        for user_id in range(1, 101):
            for post_num in range(1, 6):
                posts_data.append((
                    user_id * 10 + post_num,
                    user_id,
                    f"Post {post_num} by User {user_id}",
                    f"Content for post {post_num} by user {user_id}",
                    post_num * 10  # likes
                ))
        
        cursor.executemany(
            "INSERT INTO posts (id, user_id, title, content, likes) VALUES (?, ?, ?, ?, ?)",
            posts_data
        )
        
        # Insert comments (3 comments per post)
        comments_data = []
        for post_id in range(11, 1001):  # All post IDs
            for comment_num in range(1, 4):
                commenter_id = (post_id + comment_num) % 100 + 1
                comments_data.append((
                    post_id,
                    commenter_id,
                    f"Comment {comment_num} on post {post_id}"
                ))
        
        cursor.executemany(
            "INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
            comments_data
        )
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        PERFORMANCE ISSUE 1: Poor connection management
        - Creating new connection for each thread without pooling
        - Not reusing connections efficiently
        - No connection limits or cleanup
        """
        thread_id = threading.get_ident()
        
        # BAD: Creating new connection for each thread without limits
        if thread_id not in self.connections:
            # BAD: No connection pooling or reuse strategy
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # This is actually good
            self.connections[thread_id] = conn
        
        return self.connections[thread_id]
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        PERFORMANCE ISSUE 2: Inefficient single record queries
        - Opening new connection for simple queries
        - Not using prepared statements effectively
        """
        # BAD: Getting new connection for each query
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # BAD: String formatting instead of parameterized queries (security + performance)
        # Note: Using parameterized query here but the pattern shows inefficiency
        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return dict(result)
        return None
    
    def get_user_posts(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Part of N+1 query problem - this method will be called for each user
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # BAD: This will be called once per user, creating N+1 queries
        cursor.execute(
            "SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        
        results = cursor.fetchall()
        cursor.close()
        
        return [dict(row) for row in results]
    
    def get_users_with_posts_n_plus_1(self, user_ids: List[int]) -> List[Dict[str, Any]]:
        """
        PERFORMANCE ISSUE 3: Classic N+1 query problem
        - Making 1 query to get users + N queries to get posts for each user
        - Should use JOIN or batch queries instead
        """
        users = []
        
        # BAD: N+1 query pattern
        for user_id in user_ids:
            # Query 1: Get user (this happens N times)
            user = self.get_user_by_id(user_id)
            if user:
                # Query 2: Get user's posts (this also happens N times)
                user['posts'] = self.get_user_posts(user_id)
                
                # Query 3: Get post comments (making it even worse - N*M queries)
                for post in user['posts']:
                    post['comments'] = self.get_post_comments(post['id'])
                
                users.append(user)
        
        return users
    
    def get_post_comments(self, post_id: int) -> List[Dict[str, Any]]:
        """
        Another part of the N+1 problem - gets comments for each post
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # BAD: Another query for each post
        cursor.execute(
            "SELECT c.*, u.username FROM comments c "
            "JOIN users u ON c.user_id = u.id "
            "WHERE c.post_id = ? ORDER BY c.created_at",
            (post_id,)
        )
        
        results = cursor.fetchall()
        cursor.close()
        
        return [dict(row) for row in results]
    
    def inefficient_bulk_operations(self, data: List[Dict[str, Any]]) -> None:
        """
        PERFORMANCE ISSUE 4: Inefficient bulk operations
        - Inserting records one by one instead of batch insert
        - Not using transactions properly
        - Autocommit for each operation
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # BAD: Inserting one record at a time without transaction
        for item in data:
            # BAD: Each insert is a separate transaction
            cursor.execute(
                "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                (item['user_id'], item['title'], item['content'])
            )
            conn.commit()  # BAD: Committing after each insert
        
        cursor.close()
    
    def inefficient_search_queries(self, search_term: str) -> List[Dict[str, Any]]:
        """
        PERFORMANCE ISSUE 5: Inefficient search operations
        - Using LIKE with leading wildcards (can't use indexes)
        - Not using full-text search for text content
        - Multiple separate queries instead of single optimized query
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # BAD: LIKE with leading wildcard prevents index usage
        cursor.execute(
            "SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?",
            (f"%{search_term}%", f"%{search_term}%")
        )
        
        posts = [dict(row) for row in cursor.fetchall()]
        
        # BAD: Separate query for users
        cursor.execute(
            "SELECT * FROM users WHERE username LIKE ? OR email LIKE ?",
            (f"%{search_term}%", f"%{search_term}%")
        )
        
        users = [dict(row) for row in cursor.fetchall()]
        
        # BAD: Another separate query for comments
        cursor.execute(
            "SELECT * FROM comments WHERE content LIKE ?",
            (f"%{search_term}%",)
        )
        
        comments = [dict(row) for row in cursor.fetchall()]
        
        cursor.close()
        
        # BAD: Combining results inefficiently
        results = []
        results.extend([{'type': 'post', 'data': post} for post in posts])
        results.extend([{'type': 'user', 'data': user} for user in users])
        results.extend([{'type': 'comment', 'data': comment} for comment in comments])
        
        return results
    
    def inefficient_aggregation_queries(self) -> Dict[str, Any]:
        """
        PERFORMANCE ISSUE 6: Inefficient aggregation
        - Multiple queries for data that could be computed in one query
        - Not using database aggregation functions efficiently
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # BAD: Multiple separate queries for counts
        cursor.execute("SELECT COUNT(*) FROM users")
        stats['total_users'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM posts")
        stats['total_posts'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM comments")
        stats['total_comments'] = cursor.fetchone()[0]
        
        # BAD: Calculating averages with separate queries
        cursor.execute("SELECT AVG(likes) FROM posts")
        stats['avg_likes'] = cursor.fetchone()[0]
        
        # BAD: Getting user post counts one by one
        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        user_post_counts = {}
        for user_id in user_ids:
            cursor.execute("SELECT COUNT(*) FROM posts WHERE user_id = ?", (user_id,))
            user_post_counts[user_id] = cursor.fetchone()[0]
        
        stats['user_post_counts'] = user_post_counts
        
        cursor.close()
        return stats
    
    def missing_indexes_demo(self) -> List[Dict[str, Any]]:
        """
        PERFORMANCE ISSUE 7: Missing indexes on frequently queried columns
        - Queries on non-indexed columns will be slow
        - Foreign key columns without indexes
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # These queries will be slow due to missing indexes:
        
        # BAD: No index on email column
        cursor.execute("SELECT * FROM users WHERE email = ?", ("user_50@example.com",))
        user_by_email = cursor.fetchone()
        
        # BAD: No index on status column
        cursor.execute("SELECT * FROM users WHERE status = ?", ("active",))
        active_users = cursor.fetchall()
        
        # BAD: No index on user_id in posts table (foreign key)
        cursor.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY likes DESC", (50,))
        user_posts = cursor.fetchall()
        
        # BAD: No index on post_id in comments table (foreign key)
        cursor.execute("SELECT * FROM comments WHERE post_id = ?", (505,))
        post_comments = cursor.fetchall()
        
        cursor.close()
        
        return {
            'user_by_email': dict(user_by_email) if user_by_email else None,
            'active_users_count': len(active_users),
            'user_posts_count': len(user_posts),
            'post_comments_count': len(post_comments)
        }
    
    def close_all_connections(self):
        """
        Clean up connections - should be called when application shuts down
        """
        for conn in self.connections.values():
            conn.close()
        self.connections.clear()
    
    def __del__(self):
        """
        Destructor to clean up connections
        """
        self.close_all_connections()