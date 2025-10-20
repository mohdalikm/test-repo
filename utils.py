"""
Utilities module with performance issues.
Demonstrates inefficient algorithms, poor caching, and synchronous operations that should be async.
"""

import time
import hashlib
import requests
import json
import os
from typing import List, Dict, Any, Optional
import threading
import pickle


class MathUtils:
    def __init__(self):
        self.calculation_cache = {}  # BAD: No size limit or TTL
        
    def expensive_calculation(self, n: int) -> float:
        """
        PERFORMANCE ISSUE 1: Inefficient recursive calculation
        - Using naive recursion without memoization for expensive operations
        - Not using dynamic programming approach
        """
        # BAD: Expensive calculation that could be optimized
        if n in self.calculation_cache:
            return self.calculation_cache[n]
        
        # Simulate expensive calculation with inefficient algorithm
        if n <= 1:
            result = 1.0
        else:
            # BAD: Recursive calls without proper memoization structure
            result = (self.expensive_calculation(n-1) * 1.1 + 
                     self.expensive_calculation(n-2) * 0.9)
        
        # BAD: Cache grows indefinitely
        self.calculation_cache[n] = result
        return result
    
    def inefficient_prime_check(self, n: int) -> bool:
        """
        PERFORMANCE ISSUE 2: Inefficient algorithm
        - Using trial division up to n instead of sqrt(n)
        - Not handling even numbers efficiently
        """
        if n < 2:
            return False
        
        # BAD: Checking all numbers up to n instead of sqrt(n)
        for i in range(2, n):
            if n % i == 0:
                return False
        return True
    
    def find_primes_inefficiently(self, limit: int) -> List[int]:
        """
        PERFORMANCE ISSUE 3: Not using Sieve of Eratosthenes
        - Checking each number individually for primality
        - O(n²) complexity instead of O(n log log n)
        """
        primes = []
        
        # BAD: Checking each number individually
        for num in range(2, limit + 1):
            if self.inefficient_prime_check(num):
                primes.append(num)
        
        return primes


class FileUtils:
    def __init__(self):
        self.file_cache = {}  # BAD: No size management
        self.processing_results = {}
    
    def process_file(self, filename: str) -> Dict[str, Any]:
        """
        PERFORMANCE ISSUE 4: Inefficient file processing
        - Reading file multiple times for different operations
        - Not using streaming for large files
        - Blocking I/O operations
        """
        if filename in self.file_cache:
            return self.file_cache[filename]
        
        # BAD: Multiple file reads for different information
        
        # First read: get file size
        file_size = os.path.getsize(filename)
        
        # Second read: get line count
        with open(filename, 'r') as f:
            line_count = sum(1 for line in f)
        
        # Third read: get word count
        with open(filename, 'r') as f:
            content = f.read()
            word_count = len(content.split())
        
        # Fourth read: get character distribution
        char_count = {}
        with open(filename, 'r') as f:
            while True:
                char = f.read(1)
                if not char:
                    break
                char_count[char] = char_count.get(char, 0) + 1
        
        # BAD: Storing everything in memory cache
        result = {
            'filename': filename,
            'file_size': file_size,
            'line_count': line_count,
            'word_count': word_count,
            'char_count': char_count,
            'content': content,  # Storing full content in memory
            'processed_at': time.time()
        }
        
        self.file_cache[filename] = result
        return result
    
    def batch_file_operations(self, filenames: List[str]) -> List[Dict[str, Any]]:
        """
        PERFORMANCE ISSUE 5: Sequential processing instead of parallel
        - Processing files one by one instead of in parallel
        - Not using async I/O for I/O bound operations
        """
        results = []
        
        # BAD: Sequential processing of files
        for filename in filenames:
            # BAD: Blocking operation for each file
            result = self.process_file(filename)
            results.append(result)
            
            # BAD: Artificial delay to simulate slow I/O
            time.sleep(0.1)  # Simulating slow file processing
        
        return results


class NetworkUtils:
    def __init__(self):
        self.url_cache = {}
        self.session = None  # BAD: Not reusing HTTP sessions
    
    def fetch_url_inefficiently(self, url: str) -> Optional[str]:
        """
        PERFORMANCE ISSUE 6: Inefficient HTTP requests
        - Creating new session for each request
        - Not using connection pooling
        - Synchronous requests where async would be better
        """
        if url in self.url_cache:
            return self.url_cache[url]
        
        try:
            # BAD: Creating new session for each request
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            content = response.text
            
            # BAD: Storing full response content in cache without size limits
            self.url_cache[url] = content
            
            return content
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def fetch_multiple_urls_inefficiently(self, urls: List[str]) -> List[Optional[str]]:
        """
        PERFORMANCE ISSUE 7: Sequential HTTP requests
        - Making HTTP requests one by one instead of concurrently
        - Not using async/await or threading for I/O bound operations
        """
        results = []
        
        # BAD: Sequential HTTP requests
        for url in urls:
            result = self.fetch_url_inefficiently(url)
            results.append(result)
            
            # BAD: Adding delay between requests (rate limiting done wrong)
            time.sleep(1)
        
        return results


class CacheUtils:
    def __init__(self):
        self.cache = {}
        self.cache_stats = {'hits': 0, 'misses': 0}
        self.max_cache_size = None  # BAD: No size limit
    
    def get_cached_result(self, key: str, compute_func, *args, **kwargs) -> Any:
        """
        PERFORMANCE ISSUE 8: Poor caching implementation
        - No cache expiration (TTL)
        - No cache size limits
        - No cache eviction policy
        """
        cache_key = self._generate_cache_key(key, args, kwargs)
        
        if cache_key in self.cache:
            self.cache_stats['hits'] += 1
            return self.cache[cache_key]['value']
        
        # BAD: No size checking before adding to cache
        self.cache_stats['misses'] += 1
        result = compute_func(*args, **kwargs)
        
        # BAD: No expiration time, cache grows indefinitely
        self.cache[cache_key] = {
            'value': result,
            'created_at': time.time(),
            'access_count': 1
        }
        
        return result
    
    def _generate_cache_key(self, key: str, args: tuple, kwargs: dict) -> str:
        """
        PERFORMANCE ISSUE 9: Inefficient cache key generation
        - Using pickle for serialization which is slow
        - Not handling unhashable types properly
        """
        # BAD: Using pickle to serialize arguments (slow and unsafe)
        try:
            args_str = pickle.dumps(args)
            kwargs_str = pickle.dumps(kwargs)
            combined = f"{key}_{args_str}_{kwargs_str}"
            
            # BAD: Using MD5 which is not necessary for cache keys and adds overhead
            return hashlib.md5(combined.encode()).hexdigest()
        except Exception:
            # BAD: Fallback that might not be unique
            return f"{key}_{str(args)}_{str(kwargs)}"


class StringUtils:
    @staticmethod
    def inefficient_string_search(text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """
        PERFORMANCE ISSUE 10: Inefficient string searching
        - Using naive string search instead of optimized algorithms
        - Searching for each pattern separately
        """
        results = {}
        
        # BAD: Naive string search for each pattern
        for pattern in patterns:
            positions = []
            
            # BAD: Manual string searching instead of using built-in methods or regex
            for i in range(len(text) - len(pattern) + 1):
                if text[i:i+len(pattern)] == pattern:
                    positions.append(i)
            
            results[pattern] = positions
        
        return results
    
    @staticmethod
    def inefficient_string_processing(strings: List[str]) -> List[str]:
        """
        PERFORMANCE ISSUE 11: Inefficient string operations
        - Multiple passes over the same data
        - Creating unnecessary intermediate strings
        """
        # BAD: Multiple passes over the same data
        
        # First pass: convert to lowercase
        lowercase_strings = []
        for s in strings:
            lowercase_strings.append(s.lower())
        
        # Second pass: remove whitespace
        trimmed_strings = []
        for s in lowercase_strings:
            trimmed_strings.append(s.strip())
        
        # Third pass: remove duplicates (inefficient way)
        unique_strings = []
        for s in trimmed_strings:
            if s not in unique_strings:  # BAD: O(n) lookup in list
                unique_strings.append(s)
        
        # Fourth pass: sort
        sorted_strings = []
        for s in unique_strings:
            # BAD: Manual insertion sort instead of using built-in sort
            inserted = False
            for i, existing in enumerate(sorted_strings):
                if s < existing:
                    sorted_strings.insert(i, s)
                    inserted = True
                    break
            if not inserted:
                sorted_strings.append(s)
        
        return sorted_strings


class DataStructureUtils:
    @staticmethod
    def inefficient_data_grouping(data: List[Dict[str, Any]], group_key: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        PERFORMANCE ISSUE 12: Inefficient data structure operations
        - Using list operations where dict operations would be faster
        - Not using appropriate data structures for the task
        """
        groups = {}
        
        # BAD: Linear search for each item to find existing groups
        for item in data:
            key_value = item.get(group_key)
            
            # BAD: Checking if key exists this way is inefficient
            found_group = False
            for existing_key in groups.keys():
                if existing_key == key_value:
                    groups[existing_key].append(item)
                    found_group = True
                    break
            
            if not found_group:
                groups[key_value] = [item]
        
        return groups
    
    @staticmethod
    def inefficient_data_deduplication(data: List[Any]) -> List[Any]:
        """
        PERFORMANCE ISSUE 13: Inefficient deduplication
        - Using list membership testing (O(n)) instead of set (O(1))
        - Not preserving order efficiently
        """
        unique_data = []
        
        # BAD: O(n²) algorithm due to list membership testing
        for item in data:
            if item not in unique_data:  # BAD: O(n) operation
                unique_data.append(item)
        
        return unique_data


# Example usage and testing functions
def create_sample_files_for_testing():
    """Create sample files for testing FileUtils performance issues"""
    os.makedirs("sample_files", exist_ok=True)
    
    for i in range(5):
        filename = f"sample_files/test_file_{i}.txt"
        with open(filename, 'w') as f:
            # Create files with different sizes
            lines = 1000 * (i + 1)
            for j in range(lines):
                f.write(f"This is line {j} in file {i}. " * 10 + "\n")


def demonstrate_performance_issues():
    """
    Function to demonstrate all the performance issues
    """
    print("Demonstrating performance issues in utils...")
    
    # Math utils issues
    math_utils = MathUtils()
    print("Testing expensive calculations...")
    for i in range(20, 25):  # Will be very slow due to inefficient recursion
        result = math_utils.expensive_calculation(i)
        print(f"Calculation({i}) = {result:.2f}")
    
    # Prime finding issues
    print("Finding primes inefficiently...")
    primes = math_utils.find_primes_inefficiently(100)
    print(f"Found {len(primes)} primes up to 100")
    
    # File processing issues
    create_sample_files_for_testing()
    file_utils = FileUtils()
    print("Processing files inefficiently...")
    sample_files = [f"sample_files/test_file_{i}.txt" for i in range(3)]
    results = file_utils.batch_file_operations(sample_files)
    print(f"Processed {len(results)} files")
    
    # String processing issues
    print("Processing strings inefficiently...")
    test_strings = [f"  TEST STRING {i}  " for i in range(100)] * 5  # Creates duplicates
    processed = StringUtils.inefficient_string_processing(test_strings)
    print(f"Processed {len(processed)} unique strings")
    
    print("Performance issues demonstration completed!")


if __name__ == "__main__":
    demonstrate_performance_issues()