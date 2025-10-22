#!/usr/bin/env python3
"""
Main application module with multiple performance issues.

This module demonstrates various performance anti-patterns that an AI agent should identify
and provides methods for testing different types of performance problems.
"""

import time
import random
import json
from typing import List, Dict, Optional

from data_processor import DataProcessor
from database import DatabaseManager
from utils import MathUtils, FileUtils

# AWS CodeGuru Profiler
try:
    from codeguru_profiler_agent import Profiler
    CODEGURU_AVAILABLE = True
except ImportError:
    CODEGURU_AVAILABLE = False
    print("Warning: CodeGuru Profiler agent not available. Install with: pip install codeguru_profiler_agent")


class PerformanceProblemApp:
    """
    Main application class containing various performance issues for AI analysis.
    
    This class demonstrates poor performance patterns including:
    - Inefficient list operations
    - Redundant calculations
    - Poor data structure choices
    - Memory inefficient processing
    - I/O intensive operations
    - Database performance issues
    - Algorithmic inefficiency
    - String concatenation problems
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the performance problem application.
        
        Args:
            db_path: Optional path to database file
        """
        self.data = []
        self.results = {}
        self.db_manager = DatabaseManager(db_path) if db_path else DatabaseManager()
        self.data_processor = DataProcessor()
        self.math_utils = MathUtils()
        self.file_utils = FileUtils()
    
    def inefficient_list_operations(self, size: int = 10000) -> List[int]:
        """
        PERFORMANCE ISSUE 1: Inefficient list operations.
        
        Demonstrates:
        - Using list concatenation in loop (O(n²) complexity)
        - Should use list.extend() or list comprehension
        
        Args:
            size: Number of elements to process
            
        Returns:
            List of processed integers
        """
        result = []
        for i in range(size):
            # BAD: Creates new list each time
            result = result + [i * 2]
        return result
    
    def redundant_calculations(self, numbers: List[int]) -> Dict[str, float]:
        """
        PERFORMANCE ISSUE 2: Redundant calculations and inefficient loops.
        
        Demonstrates:
        - Recalculating same values multiple times
        - Nested loops where not necessary
        - Converting to string and back unnecessarily
        
        Args:
            numbers: List of numbers to process
            
        Returns:
            Dictionary containing calculated statistics
        """
        stats = {}
        
        # BAD: Calculating sum multiple times
        for operation in ['mean', 'variance', 'std_dev']:
            total = 0
            for num in numbers:
                # BAD: Unnecessary string conversion
                str_num = str(num)
                converted_num = int(str_num)
                total += converted_num
            
            if operation == 'mean':
                stats['mean'] = total / len(numbers)
            elif operation == 'variance':
                # BAD: Recalculating mean instead of reusing
                mean = sum(numbers) / len(numbers)
                variance = 0
                for num in numbers:
                    variance += (num - mean) ** 2
                stats['variance'] = variance / len(numbers)
            elif operation == 'std_dev':
                # BAD: Recalculating variance
                mean = sum(numbers) / len(numbers)
                variance = 0
                for num in numbers:
                    variance += (num - mean) ** 2
                variance = variance / len(numbers)
                stats['std_dev'] = variance ** 0.5
        
        return stats
    
    def inefficient_data_structure_choice(self, items: List[str]) -> List[str]:
        """
        PERFORMANCE ISSUE 3: Poor data structure choice.
        
        Demonstrates:
        - Using list for membership testing (O(n) instead of O(1))
        - Should use set for faster lookups
        
        Args:
            items: List of items to process
            
        Returns:
            List of duplicate items found
        """
        processed_items = []
        duplicates = []
        
        for item in items:
            # BAD: O(n) lookup in list
            if item in processed_items:
                # BAD: Another O(n) lookup
                if item not in duplicates:
                    duplicates.append(item)
            else:
                processed_items.append(item)
        
        return duplicates
    
    def memory_inefficient_processing(self, data_size: int = 1000000) -> None:
        """
        PERFORMANCE ISSUE 4: Memory inefficient processing.
        
        Demonstrates:
        - Loading all data into memory at once
        - Creating unnecessary copies of large data structures
        
        Args:
            data_size: Size of dataset to process
        """
        # BAD: Creating large list in memory all at once
        large_dataset = [random.randint(1, 100) for _ in range(data_size)]
        
        # BAD: Creating multiple copies of the same data
        copy1 = large_dataset.copy()
        copy2 = large_dataset.copy()
        copy3 = large_dataset.copy()
        
        # BAD: Processing entire dataset at once instead of in chunks
        processed_data = []
        for item in large_dataset:
            # BAD: Expensive operation on each item without batching
            result = self.math_utils.expensive_calculation(item)
            processed_data.append(result)
        
        # Store unnecessary copies
        self.data = [copy1, copy2, copy3, processed_data]
    
    def io_intensive_operations(self, file_count: int = 100) -> None:
        """
        PERFORMANCE ISSUE 5: Inefficient I/O operations.
        
        Demonstrates:
        - Opening/closing files repeatedly
        - Not using context managers properly
        - Synchronous file operations that could be async
        
        Args:
            file_count: Number of files to process
        """
        results = []
        
        for i in range(file_count):
            filename = f"temp_file_{i}.json"
            
            # BAD: Opening and closing file multiple times
            with open(filename, 'w') as f:
                json.dump({"id": i, "value": random.randint(1, 1000)}, f)
            
            # BAD: Immediately reading the file we just wrote
            with open(filename, 'r') as f:
                data = json.load(f)
                results.append(data)
            
            # BAD: Not batching file operations
            self.file_utils.process_file(filename)
    
    def database_performance_issues(self, user_ids: List[int]) -> List[Dict]:
        """
        PERFORMANCE ISSUE 6: Database performance problems.
        
        Demonstrates:
        - N+1 query problem
        - Not using prepared statements
        - Missing connection pooling
        
        Args:
            user_ids: List of user IDs to fetch
            
        Returns:
            List of user data with posts
        """
        users = []
        
        # BAD: N+1 query pattern
        for user_id in user_ids:
            # Each call results in a separate database query
            user = self.db_manager.get_user_by_id(user_id)
            if user:
                user_posts = self.db_manager.get_user_posts(user_id)
                user['posts'] = user_posts
                users.append(user)
        
        return users
    
    def algorithmic_inefficiency(self, data: List[int]) -> List[int]:
        """
        PERFORMANCE ISSUE 7: Inefficient algorithms.
        
        Demonstrates:
        - Using bubble sort instead of built-in sort
        - O(n²) algorithm where O(n log n) is available
        
        Args:
            data: List of integers to sort
            
        Returns:
            Sorted list of integers
        """
        # BAD: Implementing bubble sort instead of using built-in sort
        sorted_data = data.copy()
        n = len(sorted_data)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_data[j] > sorted_data[j + 1]:
                    sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
        
        return sorted_data
    
    def string_concatenation_issues(self, words: List[str]) -> str:
        """
        PERFORMANCE ISSUE 8: Inefficient string operations.
        
        Demonstrates:
        - Using string concatenation in loop instead of join
        - Creating intermediate strings unnecessarily
        
        Args:
            words: List of words to concatenate
            
        Returns:
            Concatenated string
        """
        result = ""
        
        # BAD: String concatenation in loop (O(n²) complexity)
        for word in words:
            result = result + word + " "
        
        # BAD: More unnecessary string operations
        result = result.strip()
        result = result.replace("  ", " ")  # Fix double spaces
        
        return result
    
    def run_performance_test(self) -> Dict[str, float]:
        """
        Run all performance-problematic methods to demonstrate issues.
        
        Returns:
            Dictionary containing execution times for each test
        """
        print("Starting performance test with multiple issues...")
        
        test_times = {}
        overall_start = time.time()
        
        # Test 1: Inefficient list operations
        print("Test 1: Inefficient list operations...")
        start_time = time.time()
        inefficient_list = self.inefficient_list_operations(5000)
        test_times['list_operations'] = time.time() - start_time
        
        # Test 2: Redundant calculations
        print("Test 2: Redundant calculations...")
        start_time = time.time()
        test_numbers = list(range(1000))
        stats = self.redundant_calculations(test_numbers)
        test_times['redundant_calculations'] = time.time() - start_time
        
        # Test 3: Poor data structure choice
        print("Test 3: Poor data structure choice...")
        start_time = time.time()
        test_items = [f"item_{i % 100}" for i in range(1000)]  # Creates duplicates
        duplicates = self.inefficient_data_structure_choice(test_items)
        test_times['data_structure_choice'] = time.time() - start_time
        
        # Test 4: Memory inefficient processing
        print("Test 4: Memory inefficient processing...")
        start_time = time.time()
        self.memory_inefficient_processing(50000)  # Reduced size for demo
        test_times['memory_processing'] = time.time() - start_time
        
        # Test 5: I/O intensive operations
        print("Test 5: I/O intensive operations...")
        start_time = time.time()
        self.io_intensive_operations(10)  # Reduced count for demo
        test_times['io_operations'] = time.time() - start_time
        
        # Test 6: Database issues
        print("Test 6: Database performance issues...")
        start_time = time.time()
        user_ids = list(range(1, 21))  # 20 users
        users = self.database_performance_issues(user_ids)
        test_times['database_issues'] = time.time() - start_time
        
        # Test 7: Algorithmic inefficiency
        print("Test 7: Algorithmic inefficiency...")
        start_time = time.time()
        test_data = [random.randint(1, 1000) for _ in range(500)]
        sorted_data = self.algorithmic_inefficiency(test_data)
        test_times['algorithmic_inefficiency'] = time.time() - start_time
        
        # Test 8: String concatenation issues
        print("Test 8: String concatenation issues...")
        start_time = time.time()
        words = [f"word{i}" for i in range(1000)]
        concatenated = self.string_concatenation_issues(words)
        test_times['string_concatenation'] = time.time() - start_time
        
        total_time = time.time() - overall_start
        test_times['total_execution'] = total_time
        
        print(f"\nTotal execution time: {total_time:.2f} seconds")
        print("Performance test completed. Check the issues in the code!")
        
        return test_times
    
    def cleanup(self):
        """Clean up resources and temporary files."""
        try:
            self.db_manager.close_all_connections()
            self.data_processor.clear_cache()
            # Clean up any temporary files
            import os
            for i in range(100):
                filename = f"temp_file_{i}.json"
                if os.path.exists(filename):
                    os.remove(filename)
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()


def start_application():
    """Start the main application with performance testing."""
    print("Starting application with CodeGuru Profiler...")
    with PerformanceProblemApp() as app:
        results = app.run_performance_test()
        print(f"\nApplication completed. Total tests run: {len(results)}")
        return results


if __name__ == "__main__":
    # Start CodeGuru Profiler if available
    profiler = None
    if CODEGURU_AVAILABLE:
        try:
            profiler = Profiler(profiling_group_name="ecocoder-default-profiling-group")
            profiler.start()
            print("CodeGuru Profiler started successfully")
        except Exception as e:
            print(f"Warning: Failed to start CodeGuru Profiler: {e}")
            profiler = None
    
    try:
        # Run the application
        start_application()
    finally:
        # Stop profiler if it was started
        if profiler and CODEGURU_AVAILABLE:
            try:
                profiler.stop()
                print("CodeGuru Profiler stopped")
            except Exception as e:
                print(f"Warning: Error stopping CodeGuru Profiler: {e}")