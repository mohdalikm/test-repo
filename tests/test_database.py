"""
Unit tests for the DatabaseManager class.

Tests database performance issues including N+1 queries, missing indexes, etc.
"""

import pytest
import tempfile
import os
import sqlite3
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import DatabaseManager


class TestDatabaseManager:
    """Test suite for DatabaseManager class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        os.close(self.db_fd)  # Close the file descriptor
        self.db_manager = DatabaseManager(self.db_path)
    
    def teardown_method(self):
        """Clean up after each test method."""
        self.db_manager.close_all_connections()
        # Remove the temporary database file
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_database_initialization(self):
        """Test that the database initializes correctly."""
        # Verify tables exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'users' in tables
        assert 'posts' in tables
        assert 'comments' in tables
        
        # Check sample data was inserted
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        assert user_count > 0
        
        cursor.execute("SELECT COUNT(*) FROM posts")
        post_count = cursor.fetchone()[0]
        assert post_count > 0
        
        cursor.execute("SELECT COUNT(*) FROM comments")
        comment_count = cursor.fetchone()[0]
        assert comment_count > 0
        
        conn.close()
    
    def test_get_user_by_id(self):
        """Test single user retrieval."""
        user = self.db_manager.get_user_by_id(1)
        
        assert user is not None
        assert user['id'] == 1
        assert user['username'] == 'user_1'
        assert user['email'] == 'user_1@example.com'
        assert user['status'] == 'active'
    
    def test_get_user_by_id_nonexistent(self):
        """Test retrieving non-existent user."""
        user = self.db_manager.get_user_by_id(999999)
        assert user is None
    
    def test_get_user_posts(self):
        """Test retrieving user posts."""
        posts = self.db_manager.get_user_posts(1)
        
        assert isinstance(posts, list)
        assert len(posts) > 0
        
        # All posts should belong to user 1
        for post in posts:
            assert post['user_id'] == 1
            assert 'title' in post
            assert 'content' in post
    
    def test_get_users_with_posts_n_plus_1(self):
        """Test the N+1 query problem."""
        user_ids = [1, 2, 3]
        
        # This should trigger N+1 queries (inefficient)
        users = self.db_manager.get_users_with_posts_n_plus_1(user_ids)
        
        assert len(users) == len(user_ids)
        
        for user in users:
            assert 'posts' in user
            assert isinstance(user['posts'], list)
            
            # Each post should have comments
            for post in user['posts']:
                assert 'comments' in post
                assert isinstance(post['comments'], list)
    
    def test_get_post_comments(self):
        """Test retrieving post comments."""
        # Get a post first
        posts = self.db_manager.get_user_posts(1)
        assert len(posts) > 0
        
        post_id = posts[0]['id']
        comments = self.db_manager.get_post_comments(post_id)
        
        assert isinstance(comments, list)
        
        # Verify comment structure
        for comment in comments:
            assert comment['post_id'] == post_id
            assert 'username' in comment  # Joined from users table
            assert 'content' in comment
    
    def test_inefficient_bulk_operations(self):
        """Test inefficient bulk insert operations."""
        data = [
            {'user_id': 1, 'title': 'Test Post 1', 'content': 'Test Content 1'},
            {'user_id': 2, 'title': 'Test Post 2', 'content': 'Test Content 2'},
            {'user_id': 3, 'title': 'Test Post 3', 'content': 'Test Content 3'}
        ]
        
        # Count posts before insert
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM posts")
        initial_count = cursor.fetchone()[0]
        conn.close()
        
        # Perform inefficient bulk insert
        self.db_manager.inefficient_bulk_operations(data)
        
        # Count posts after insert
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM posts")
        final_count = cursor.fetchone()[0]
        conn.close()
        
        assert final_count == initial_count + len(data)
    
    def test_inefficient_search_queries(self):
        """Test inefficient search operations."""
        search_term = "Post"
        
        results = self.db_manager.inefficient_search_queries(search_term)
        
        assert isinstance(results, list)
        
        # Should have different types of results
        result_types = set(result['type'] for result in results)
        assert 'post' in result_types  # Should find posts with "Post" in title
        
        # Verify structure
        for result in results:
            assert 'type' in result
            assert 'data' in result
            assert result['type'] in ['post', 'user', 'comment']
    
    def test_inefficient_aggregation_queries(self):
        """Test inefficient aggregation operations."""
        stats = self.db_manager.inefficient_aggregation_queries()
        
        assert isinstance(stats, dict)
        assert 'total_users' in stats
        assert 'total_posts' in stats
        assert 'total_comments' in stats
        assert 'avg_likes' in stats
        assert 'user_post_counts' in stats
        
        # Verify values are reasonable
        assert stats['total_users'] > 0
        assert stats['total_posts'] > 0
        assert stats['total_comments'] > 0
        assert isinstance(stats['user_post_counts'], dict)
    
    def test_missing_indexes_demo(self):
        """Test queries that would benefit from indexes."""
        results = self.db_manager.missing_indexes_demo()
        
        assert isinstance(results, dict)
        assert 'user_by_email' in results
        assert 'active_users_count' in results
        assert 'user_posts_count' in results
        assert 'post_comments_count' in results
        
        # Verify counts are non-negative
        assert results['active_users_count'] >= 0
        assert results['user_posts_count'] >= 0
        assert results['post_comments_count'] >= 0
    
    def test_get_database_info(self):
        """Test database information retrieval."""
        info = self.db_manager.get_database_info()
        
        assert isinstance(info, dict)
        assert 'users_count' in info
        assert 'posts_count' in info
        assert 'comments_count' in info
        assert 'db_file_size_mb' in info
        assert 'active_connections' in info
        
        # Verify counts are positive
        assert info['users_count'] > 0
        assert info['posts_count'] > 0
        assert info['comments_count'] > 0
        assert info['db_file_size_mb'] > 0
    
    def test_connection_management(self):
        """Test connection management behavior."""
        # Initially should have one connection from setup
        initial_connections = len(self.db_manager.connections)
        
        # Perform some operations that should reuse connections
        self.db_manager.get_user_by_id(1)
        self.db_manager.get_user_posts(1)
        
        # Should still have same number of connections (reuse)
        final_connections = len(self.db_manager.connections)
        assert final_connections == initial_connections
    
    def test_close_all_connections(self):
        """Test connection cleanup."""
        # Perform some operations to create connections
        self.db_manager.get_user_by_id(1)
        
        assert len(self.db_manager.connections) > 0
        
        # Close all connections
        self.db_manager.close_all_connections()
        
        assert len(self.db_manager.connections) == 0
    
    @pytest.mark.parametrize("user_count", [1, 3, 5])
    def test_n_plus_1_scaling(self, user_count):
        """Test how N+1 queries scale with user count."""
        user_ids = list(range(1, user_count + 1))
        
        users = self.db_manager.get_users_with_posts_n_plus_1(user_ids)
        
        # Should return users for all valid IDs
        assert len(users) <= user_count  # May be less if some users don't exist
        
        for user in users:
            assert user['id'] in user_ids
    
    def test_error_handling_database_operations(self):
        """Test error handling in database operations."""
        # Test with invalid user ID (should return None, not crash)
        user = self.db_manager.get_user_by_id(-1)
        assert user is None
        
        # Test with empty bulk data
        self.db_manager.inefficient_bulk_operations([])
        
        # Test search with empty term
        results = self.db_manager.inefficient_search_queries("")
        assert isinstance(results, list)
    
    def test_database_file_creation(self):
        """Test that database file is created."""
        # Database file should exist after initialization
        assert os.path.exists(self.db_path)
        
        # File should have content (not be empty)
        assert os.path.getsize(self.db_path) > 0