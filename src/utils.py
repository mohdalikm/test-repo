"""
Utilities module with performance issues.

Demonstrates inefficient algorithms, poor caching, and synchronous operations 
that should be async. This module contains various utility classes with 
intentional performance anti-patterns for AI analysis.
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
    """
    Math utilities with inefficient algorithms and poor caching.
    
    Demonstrates:
    - Inefficient recursive calculations
    - Poor algorithm choices
    - Unbounded cache growth
    """
    
    def __init__(self):
        """Initialize with problematic cache."""
        self.calculation_cache = {}  # BAD: No size limit or TTL
        
    def expensive_calculation(self, n: int) -> float:
        """
        PERFORMANCE ISSUE 1: Inefficient recursive calculation.
        
        Demonstrates:
        - Using naive recursion without memoization for expensive operations
        - Not using dynamic programming approach
        
        Args:
            n: Input number for calculation
            
        Returns:
            Result of expensive calculation
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
        PERFORMANCE ISSUE 2: Inefficient algorithm.
        
        Demonstrates:
        - Using trial division up to n instead of sqrt(n)
        - Not handling even numbers efficiently
        
        Args:
            n: Number to check for primality
            
        Returns:
            True if n is prime, False otherwise
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
        PERFORMANCE ISSUE 3: Not using Sieve of Eratosthenes.
        
        Demonstrates:
        - Checking each number individually for primality
        - O(n²) complexity instead of O(n log log n)
        
        Args:
            limit: Upper limit for prime search
            
        Returns:
            List of prime numbers up to limit
        """
        primes = []
        
        # BAD: Checking each number individually
        for num in range(2, limit + 1):
            if self.inefficient_prime_check(num):
                primes.append(num)
        
        return primes
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the cache state."""
        return {
            'cache_size': len(self.calculation_cache),
            'cache_keys_sample': list(self.calculation_cache.keys())[:10]
        }
    
    def clear_cache(self) -> None:
        """Clear the calculation cache."""
        self.calculation_cache.clear()


class FileUtils:
    """
    File utilities with inefficient I/O operations.
    
    Demonstrates:
    - Inefficient file processing
    - Multiple file reads
    - Poor batch processing
    """
    
    def __init__(self):
        """Initialize with problematic cache."""
        self.file_cache = {}  # BAD: No size management
        self.processing_results = {}
    
    def process_file(self, filename: str) -> Dict[str, Any]:
        """
        PERFORMANCE ISSUE 4: Inefficient file processing.
        
        Demonstrates:
        - Reading file multiple times for different operations
        - Not using streaming for large files
        - Blocking I/O operations
        
        Args:
            filename: Path to file to process
            
        Returns:
            Dictionary with file processing results
        """
        if not os.path.exists(filename):
            return {}
            
        if filename in self.file_cache:
            return self.file_cache[filename]
        
        # BAD: Multiple file reads for different information
        
        # First read: get file size
        file_size = os.path.getsize(filename)
        
        # Second read: get line count
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line_count = sum(1 for line in f)
        except UnicodeDecodeError:
            line_count = 0
        
        # Third read: get word count
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                word_count = len(content.split())
        except UnicodeDecodeError:
            content = ""
            word_count = 0
        
        # Fourth read: get character distribution
        char_count = {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                while True:
                    char = f.read(1)
                    if not char:
                        break
                    char_count[char] = char_count.get(char, 0) + 1
        except UnicodeDecodeError:
            pass
        
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
        PERFORMANCE ISSUE 5: Sequential processing instead of parallel.
        
        Demonstrates:
        - Processing files one by one instead of in parallel
        - Not using async I/O for I/O bound operations
        
        Args:
            filenames: List of file paths to process
            
        Returns:
            List of file processing results
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
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the file cache state."""
        return {
            'cache_size': len(self.file_cache),
            'cached_files': list(self.file_cache.keys())
        }
    
    def clear_cache(self) -> None:
        """Clear the file processing cache."""
        self.file_cache.clear()
        self.processing_results.clear()


class NetworkUtils:
    """
    Network utilities with inefficient HTTP operations.
    
    Demonstrates:
    - Poor HTTP session management
    - Sequential network requests
    - Inefficient caching
    """
    
    def __init__(self):
        """Initialize with problematic session management."""
        self.url_cache = {}
        self.session = None  # BAD: Not reusing HTTP sessions
    
    def fetch_url_inefficiently(self, url: str) -> Optional[str]:
        """
        PERFORMANCE ISSUE 6: Inefficient HTTP requests.
        
        Demonstrates:
        - Creating new session for each request
        - Not using connection pooling
        - Synchronous requests where async would be better
        
        Args:
            url: URL to fetch
            
        Returns:
            Response content or None if error
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
        PERFORMANCE ISSUE 7: Sequential HTTP requests.
        
        Demonstrates:
        - Making HTTP requests one by one instead of concurrently
        - Not using async/await or threading for I/O bound operations
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of response contents
        """
        results = []
        
        # BAD: Sequential HTTP requests
        for url in urls:
            result = self.fetch_url_inefficiently(url)
            results.append(result)
            
            # BAD: Adding delay between requests (rate limiting done wrong)
            time.sleep(1)
        
        return results
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about the URL cache state."""
        return {
            'cache_size': len(self.url_cache),
            'cached_urls': list(self.url_cache.keys())
        }
    
    def clear_cache(self) -> None:
        """Clear the URL cache."""
        self.url_cache.clear()


class CacheUtils:
    """
    Caching utilities with poor implementation.
    
    Demonstrates:
    - No cache expiration
    - No size limits
    - Poor eviction policies
    """
    
    def __init__(self):
        """Initialize with problematic cache settings."""
        self.cache = {}
        self.cache_stats = {'hits': 0, 'misses': 0}
        self.max_cache_size = None  # BAD: No size limit
    
    def get_cached_result(self, key: str, compute_func, *args, **kwargs) -> Any:
        """
        PERFORMANCE ISSUE 8: Poor caching implementation.
        
        Demonstrates:
        - No cache expiration (TTL)
        - No cache size limits
        - No cache eviction policy
        
        Args:
            key: Cache key
            compute_func: Function to compute result if not cached
            *args: Arguments for compute function
            **kwargs: Keyword arguments for compute function
            
        Returns:
            Cached or computed result
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
        PERFORMANCE ISSUE 9: Inefficient cache key generation.
        
        Demonstrates:
        - Using pickle for serialization which is slow
        - Not handling unhashable types properly
        
        Args:
            key: Base key string
            args: Function arguments
            kwargs: Function keyword arguments
            
        Returns:
            Generated cache key
        """
        # BAD: Using pickle to serialize arguments (slow and unsafe)
        try:
            args_str = pickle.dumps(args)
            kwargs_str = pickle.dumps(kwargs)
            combined = f"{key}_{args_str}_{kwargs_str}".encode()
            
            # BAD: Using MD5 which is not necessary for cache keys and adds overhead
            return hashlib.md5(combined).hexdigest()
        except Exception:
            # BAD: Fallback that might not be unique
            return f"{key}_{str(args)}_{str(kwargs)}"
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'size': len(self.cache),
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'hit_rate': (
                self.cache_stats['hits'] / 
                (self.cache_stats['hits'] + self.cache_stats['misses'])
                if (self.cache_stats['hits'] + self.cache_stats['misses']) > 0 
                else 0
            )
        }
    
    def clear_cache(self) -> None:
        """Clear all cached data."""
        self.cache.clear()
        self.cache_stats = {'hits': 0, 'misses': 0}


class StringUtils:
    """String utilities with inefficient operations."""
    
    @staticmethod
    def inefficient_string_search(text: str, patterns: List[str]) -> Dict[str, List[int]]:
        """
        PERFORMANCE ISSUE 10: Inefficient string searching.
        
        Demonstrates:
        - Using naive string search instead of optimized algorithms
        - Searching for each pattern separately
        
        Args:
            text: Text to search in
            patterns: List of patterns to find
            
        Returns:
            Dictionary mapping patterns to their positions
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
        PERFORMANCE ISSUE 11: Inefficient string operations.
        
        Demonstrates:
        - Multiple passes over the same data
        - Creating unnecessary intermediate strings
        
        Args:
            strings: List of strings to process
            
        Returns:
            Processed and deduplicated strings
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
    """Data structure utilities with inefficient operations."""
    
    @staticmethod
    def inefficient_data_grouping(data: List[Dict[str, Any]], 
                                  group_key: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        PERFORMANCE ISSUE 12: Inefficient data structure operations.
        
        Demonstrates:
        - Using list operations where dict operations would be faster
        - Not using appropriate data structures for the task
        
        Args:
            data: List of dictionaries to group
            group_key: Key to group by
            
        Returns:
            Dictionary of grouped data
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
        PERFORMANCE ISSUE 13: Inefficient deduplication.
        
        Demonstrates:
        - Using list membership testing (O(n)) instead of set (O(1))
        - Not preserving order efficiently
        
        Args:
            data: List of items to deduplicate
            
        Returns:
            List with duplicates removed
        """
        unique_data = []
        
        # BAD: O(n²) algorithm due to list membership testing
        for item in data:
            if item not in unique_data:  # BAD: O(n) operation
                unique_data.append(item)
        
        return unique_data


# Example usage and testing functions
def create_sample_files_for_testing(output_dir: str = "sample_files") -> None:
    """Create sample files for testing FileUtils performance issues."""
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(5):
        filename = os.path.join(output_dir, f"test_file_{i}.txt")
        with open(filename, 'w') as f:
            # Create files with different sizes
            lines = 1000 * (i + 1)
            for j in range(lines):
                f.write(f"This is line {j} in file {i}. " * 10 + "\n")


def demonstrate_performance_issues() -> None:
    """Function to demonstrate all the performance issues."""
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