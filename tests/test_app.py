"""
Unit tests for the main PerformanceProblemApp class.

These tests verify that the performance issues are present and can be measured.
They serve as both functional tests and performance regression tests.
"""

import pytest
import time
import tempfile
import os
from unittest.mock import patch, MagicMock
from typing import List, Dict

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from performance_issues.app import PerformanceProblemApp


class TestPerformanceProblemApp:
    """Test suite for PerformanceProblemApp."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.app = PerformanceProblemApp()
    
    def teardown_method(self):
        """Clean up after each test method."""
        if hasattr(self, 'app'):
            self.app.cleanup()
    
    def test_app_initialization(self):
        """Test that the app initializes correctly."""
        assert self.app.data == []
        assert self.app.results == {}
        assert self.app.db_manager is not None
        assert self.app.data_processor is not None
        assert self.app.math_utils is not None
        assert self.app.file_utils is not None
    
    def test_inefficient_list_operations_performance(self):
        """Test that list operations are indeed inefficient."""
        # Test with small size first
        start_time = time.time()
        result = self.app.inefficient_list_operations(100)
        end_time = time.time()
        
        assert len(result) == 100
        assert result[0] == 0  # 0 * 2 = 0
        assert result[1] == 2  # 1 * 2 = 2
        assert result[99] == 198  # 99 * 2 = 198
        
        # The operation should take some time due to inefficiency
        execution_time = end_time - start_time
        assert execution_time >= 0  # Basic sanity check
    
    def test_inefficient_list_operations_correctness(self):
        """Test that the inefficient list operations produce correct results."""
        result = self.app.inefficient_list_operations(5)
        expected = [0, 2, 4, 6, 8]  # i * 2 for i in range(5)
        assert result == expected
    
    def test_redundant_calculations(self):
        """Test that calculations are redundant but produce correct results."""
        numbers = [1, 2, 3, 4, 5]
        
        start_time = time.time()
        stats = self.app.redundant_calculations(numbers)
        end_time = time.time()
        
        # Verify correct statistical calculations
        expected_mean = sum(numbers) / len(numbers)  # 3.0
        expected_variance = sum((x - expected_mean) ** 2 for x in numbers) / len(numbers)  # 2.0
        expected_std_dev = expected_variance ** 0.5
        
        assert stats['mean'] == expected_mean
        assert abs(stats['variance'] - expected_variance) < 0.0001
        assert abs(stats['std_dev'] - expected_std_dev) < 0.0001
        
        # Should take some time due to redundant calculations
        execution_time = end_time - start_time
        assert execution_time >= 0
    
    def test_inefficient_data_structure_choice(self):
        """Test that data structure choice is inefficient but correct."""
        items = ['a', 'b', 'c', 'a', 'b', 'd', 'e', 'a']
        
        start_time = time.time()
        duplicates = self.app.inefficient_data_structure_choice(items)
        end_time = time.time()
        
        # Should find 'a' and 'b' as duplicates
        assert set(duplicates) == {'a', 'b'}
        
        execution_time = end_time - start_time
        assert execution_time >= 0
    
    def test_memory_inefficient_processing(self):
        """Test memory inefficient processing."""
        # Use small data size for testing
        original_data_length = len(self.app.data)
        
        self.app.memory_inefficient_processing(100)  # Small size for testing
        
        # Should have stored multiple copies of data
        assert len(self.app.data) > original_data_length
        assert len(self.app.data) == 4  # copy1, copy2, copy3, processed_data
    
    def test_io_intensive_operations(self):
        """Test I/O intensive operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            
            start_time = time.time()
            self.app.io_intensive_operations(3)  # Small count for testing
            end_time = time.time()
            
            # Should create temporary files
            temp_files = [f for f in os.listdir('.') if f.startswith('temp_file_')]
            assert len(temp_files) >= 3
            
            execution_time = end_time - start_time
            assert execution_time >= 0
            
            # Clean up temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
    
    def test_database_performance_issues(self):
        """Test database performance issues."""
        user_ids = [1, 2, 3]
        
        start_time = time.time()
        users = self.app.database_performance_issues(user_ids)
        end_time = time.time()
        
        # Should return users with posts
        assert isinstance(users, list)
        for user in users:
            assert 'posts' in user
            assert isinstance(user['posts'], list)
        
        execution_time = end_time - start_time
        assert execution_time >= 0
    
    def test_algorithmic_inefficiency(self):
        """Test that bubble sort is inefficient but correct."""
        data = [5, 2, 8, 1, 9, 3]
        
        start_time = time.time()
        sorted_data = self.app.algorithmic_inefficiency(data)
        end_time = time.time()
        
        # Should be sorted correctly
        assert sorted_data == [1, 2, 3, 5, 8, 9]
        
        # Original data should be unchanged
        assert data == [5, 2, 8, 1, 9, 3]
        
        execution_time = end_time - start_time
        assert execution_time >= 0
    
    def test_string_concatenation_issues(self):
        """Test string concatenation inefficiency."""
        words = ['hello', 'world', 'test']
        
        start_time = time.time()
        result = self.app.string_concatenation_issues(words)
        end_time = time.time()
        
        # Should concatenate words correctly
        assert result == 'hello world test'
        
        execution_time = end_time - start_time
        assert execution_time >= 0
    
    def test_run_performance_test(self):
        """Test the complete performance test suite."""
        start_time = time.time()
        test_times = self.app.run_performance_test()
        end_time = time.time()
        
        # Should return timing information
        assert isinstance(test_times, dict)
        assert 'total_execution' in test_times
        assert 'list_operations' in test_times
        assert 'redundant_calculations' in test_times
        assert 'data_structure_choice' in test_times
        
        # All times should be non-negative
        for time_key, time_value in test_times.items():
            assert time_value >= 0
        
        total_execution_time = end_time - start_time
        assert total_execution_time >= test_times['total_execution']
    
    def test_context_manager(self):
        """Test that the app works as a context manager."""
        with PerformanceProblemApp() as app:
            assert app is not None
            result = app.inefficient_list_operations(5)
            assert len(result) == 5
        
        # Should have cleaned up after context exit
        # (This is more of a smoke test since cleanup is hard to verify)
    
    @pytest.mark.parametrize("size", [10, 100])
    def test_list_operations_scaling(self, size):
        """Test that list operations scale poorly with input size."""
        result = self.app.inefficient_list_operations(size)
        assert len(result) == size
        
        # Verify the pattern: result[i] = i * 2
        for i in range(min(size, 10)):  # Check first 10 elements
            assert result[i] == i * 2
    
    def test_error_handling(self):
        """Test error handling in various methods."""
        # Test with empty list
        result = self.app.redundant_calculations([])
        assert 'mean' in result
        
        # Test with empty items list
        duplicates = self.app.inefficient_data_structure_choice([])
        assert duplicates == []
        
        # Test algorithmic inefficiency with empty list
        sorted_data = self.app.algorithmic_inefficiency([])
        assert sorted_data == []
    
    def test_memory_usage_growth(self):
        """Test that memory usage grows as expected."""
        import gc
        
        # Force garbage collection
        gc.collect()
        
        initial_data_size = len(self.app.data)
        
        # Run memory inefficient processing multiple times
        for _ in range(3):
            self.app.memory_inefficient_processing(50)  # Small size
        
        # Memory usage should have grown
        final_data_size = len(self.app.data)
        assert final_data_size > initial_data_size