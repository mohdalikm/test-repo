#!/usr/bin/env python3
"""
Main application with multiple performance issues.
This file demonstrates various performance anti-patterns that an AI agent should identify.
"""

import time
import random
import json
from typing import List, Dict
from data_processor import DataProcessor
from database import DatabaseManager
from utils import MathUtils, FileUtils


class PerformanceProblemApp:
    def __init__(self):
        self.data = []
        self.results = {}
        self.db_manager = DatabaseManager()
        self.data_processor = DataProcessor()
        self.math_utils = MathUtils()
        self.file_utils = FileUtils()
    
    def inefficient_list_operations(self, size: int = 10000) -> List[int]:
        """
        PERFORMANCE ISSUE 1: Inefficient list operations
        - Using list concatenation in loop (O(n²) complexity)
        - Should use list.extend() or list comprehension
        """
        result = []
        for i in range(size):
            # BAD: Creates new list each time
            result = result + [i * 2]
        return result
    
    def redundant_calculations(self, numbers: List[int]) -> Dict[str, float]:
        """
        PERFORMANCE ISSUE 2: Redundant calculations and inefficient loops
        - Recalculating same values multiple times
        - Nested loops where not necessary
        - Converting to string and back unnecessarily
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
        PERFORMANCE ISSUE 3: Poor data structure choice
        - Using list for membership testing (O(n) instead of O(1))
        - Should use set for faster lookups
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
        PERFORMANCE ISSUE 4: Memory inefficient processing
        - Loading all data into memory at once
        - Creating unnecessary copies of large data structures
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
        PERFORMANCE ISSUE 5: Inefficient I/O operations
        - Opening/closing files repeatedly
        - Not using context managers properly
        - Synchronous file operations that could be async
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
        PERFORMANCE ISSUE 6: Database performance problems
        - N+1 query problem
        - Not using prepared statements
        - Missing connection pooling
        """
        users = []
        
        # BAD: N+1 query pattern
        for user_id in user_ids:
            # Each call results in a separate database query
            user = self.db_manager.get_user_by_id(user_id)
            user_posts = self.db_manager.get_user_posts(user_id)
            user['posts'] = user_posts
            users.append(user)
        
        return users
    
    def algorithmic_inefficiency(self, data: List[int]) -> List[int]:
        """
        PERFORMANCE ISSUE 7: Inefficient algorithms
        - Using bubble sort instead of built-in sort
        - O(n²) algorithm where O(n log n) is available
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
        PERFORMANCE ISSUE 8: Inefficient string operations
        - Using string concatenation in loop instead of join
        - Creating intermediate strings unnecessarily
        """
        result = ""
        
        # BAD: String concatenation in loop (O(n²) complexity)
        for word in words:
            result = result + word + " "
        
        # BAD: More unnecessary string operations
        result = result.strip()
        result = result.replace("  ", " ")  # Fix double spaces
        
        return result
    
    def run_performance_test(self):
        """
        Run all performance-problematic methods to demonstrate issues
        """
        print("Starting performance test with multiple issues...")
        
        start_time = time.time()
        
        # Test 1: Inefficient list operations
        print("Test 1: Inefficient list operations...")
        inefficient_list = self.inefficient_list_operations(5000)
        
        # Test 2: Redundant calculations
        print("Test 2: Redundant calculations...")
        test_numbers = list(range(1000))
        stats = self.redundant_calculations(test_numbers)
        
        # Test 3: Poor data structure choice
        print("Test 3: Poor data structure choice...")
        test_items = [f"item_{i % 100}" for i in range(1000)]  # Creates duplicates
        duplicates = self.inefficient_data_structure_choice(test_items)
        
        # Test 4: Memory inefficient processing
        print("Test 4: Memory inefficient processing...")
        self.memory_inefficient_processing(50000)  # Reduced size for demo
        
        # Test 5: I/O intensive operations
        print("Test 5: I/O intensive operations...")
        self.io_intensive_operations(10)  # Reduced count for demo
        
        # Test 6: Database issues
        print("Test 6: Database performance issues...")
        user_ids = list(range(1, 21))  # 20 users
        users = self.database_performance_issues(user_ids)
        
        # Test 7: Algorithmic inefficiency
        print("Test 7: Algorithmic inefficiency...")
        test_data = [random.randint(1, 1000) for _ in range(500)]
        sorted_data = self.algorithmic_inefficiency(test_data)
        
        # Test 8: String concatenation issues
        print("Test 8: String concatenation issues...")
        words = [f"word{i}" for i in range(1000)]
        concatenated = self.string_concatenation_issues(words)
        
        end_time = time.time()
        print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
        print("Performance test completed. Check the issues in the code!")


if __name__ == "__main__":
    app = PerformanceProblemApp()
    app.run_performance_test()