"""
Data processing module with performance issues.

Demonstrates inefficient pandas operations, memory leaks, and poor file handling.
This module is intentionally designed with performance anti-patterns for AI analysis.
"""

import pandas as pd
import numpy as np
import json
import csv
import time
import os
from typing import List, Dict, Any, Optional


class DataProcessor:
    """
    Data processor with intentional performance issues.
    
    Demonstrates poor patterns in:
    - CSV loading and processing
    - Pandas operations
    - Memory management
    - File handling
    - Data aggregation
    - JSON processing
    """
    
    def __init__(self):
        """Initialize the data processor with problematic cache."""
        self.cache = {}  # Will become a memory leak
        self.processed_files = []
    
    def load_csv_inefficiently(self, filename: str) -> pd.DataFrame:
        """
        PERFORMANCE ISSUE 1: Inefficient CSV loading.
        
        Demonstrates:
        - Loading entire file into memory without chunking
        - Not specifying data types, causing inference overhead
        - Reading same file multiple times without caching
        
        Args:
            filename: Path to CSV file to load
            
        Returns:
            Loaded DataFrame with inefficient processing
        """
        # BAD: Reading file multiple times for different operations
        
        # First read to get row count
        with open(filename, 'r') as f:
            row_count = sum(1 for line in f)
        
        # Second read to get column info
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
        # Third read to actually load data
        df = pd.read_csv(filename)  # BAD: No dtype specification, no chunking
        
        # BAD: Storing everything in memory cache without size limits
        self.cache[filename] = df.copy()
        self.cache[f"{filename}_metadata"] = {
            'rows': row_count,
            'columns': headers,
            'loaded_at': time.time()
        }
        
        return df
    
    def inefficient_pandas_operations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        PERFORMANCE ISSUE 2: Inefficient pandas operations.
        
        Demonstrates:
        - Using iterrows() instead of vectorized operations
        - Applying functions row by row instead of using built-in methods
        - Creating unnecessary copies of DataFrames
        
        Args:
            df: DataFrame to process inefficiently
            
        Returns:
            Processed DataFrame with performance issues
        """
        # BAD: Using iterrows() which is very slow
        processed_data = []
        for index, row in df.iterrows():
            # BAD: Manual calculations instead of vectorized operations
            if 'value' in row:
                new_value = row['value'] * 2 + 10
                processed_data.append({
                    'index': index,
                    'original_value': row['value'],
                    'new_value': new_value,
                    'is_even': new_value % 2 == 0
                })
        
        # BAD: Converting list of dicts back to DataFrame (very inefficient)
        result_df = pd.DataFrame(processed_data)
        
        # BAD: More inefficient operations
        # Using apply with lambda instead of vectorized operations
        result_df['squared'] = result_df['new_value'].apply(lambda x: x ** 2)
        result_df['log_value'] = result_df['new_value'].apply(
            lambda x: np.log(x) if x > 0 else 0
        )
        
        # BAD: Unnecessary DataFrame copies
        temp_df1 = result_df.copy()
        temp_df2 = result_df.copy()
        temp_df3 = result_df.copy()
        
        # Store copies in cache (memory leak)
        self.cache[f"temp_df_{time.time()}_1"] = temp_df1
        self.cache[f"temp_df_{time.time()}_2"] = temp_df2
        self.cache[f"temp_df_{time.time()}_3"] = temp_df3
        
        return result_df
    
    def memory_leaking_file_processor(self, directory: str) -> Dict[str, Any]:
        """
        PERFORMANCE ISSUE 3: Memory leaks and inefficient file processing.
        
        Demonstrates:
        - Storing all processed data in memory indefinitely
        - Not releasing resources properly
        - Processing files sequentially instead of in batches
        
        Args:
            directory: Directory containing files to process
            
        Returns:
            Dictionary of processed file data (causes memory leak)
        """
        results = {}
        
        if not os.path.exists(directory):
            return results
        
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                full_path = os.path.join(directory, filename)
                
                try:
                    # BAD: Loading entire file into memory
                    with open(full_path, 'r') as f:
                        content = f.read()  # Loads entire file into memory
                    
                    # BAD: Processing data inefficiently
                    lines = content.split('\n')
                    processed_lines = []
                    
                    for line in lines:
                        if line.strip():
                            # BAD: String manipulation in loop
                            processed_line = line.replace(',', '|').replace('"', "'")
                            processed_lines.append(processed_line)
                    
                    # BAD: Storing everything in memory without cleanup
                    results[filename] = {
                        'original_content': content,  # Duplicate storage
                        'processed_lines': processed_lines,  # More duplicate storage
                        'line_count': len(lines),
                        'processed_at': time.time(),
                        'file_size': len(content)
                    }
                    
                    # BAD: Adding to instance cache (never cleaned up)
                    self.cache[f"file_{filename}"] = results[filename].copy()
                    self.processed_files.append(filename)
                    
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return results
    
    def inefficient_data_aggregation(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        PERFORMANCE ISSUE 4: Inefficient data aggregation.
        
        Demonstrates:
        - Using nested loops instead of pandas groupby
        - Recalculating aggregates multiple times
        - Not using efficient data structures for grouping
        
        Args:
            data: List of dictionaries to aggregate
            
        Returns:
            Aggregated data with inefficient calculations
        """
        # BAD: Manual grouping instead of using pandas or proper data structures
        groups = {}
        
        # First pass: Create groups manually
        for item in data:
            category = item.get('category', 'unknown')
            if category not in groups:
                groups[category] = []
            groups[category].append(item)
        
        # BAD: Calculate aggregates manually with nested loops
        aggregates = {}
        for category, items in groups.items():
            # BAD: Multiple passes through the same data
            total_value = 0
            count = 0
            values = []
            
            for item in items:
                if 'value' in item:
                    total_value += item['value']
                    count += 1
                    values.append(item['value'])
            
            # BAD: Calculating min/max inefficiently
            min_value = values[0] if values else 0
            max_value = values[0] if values else 0
            
            for value in values:
                if value < min_value:
                    min_value = value
                if value > max_value:
                    max_value = value
            
            # BAD: Storing intermediate results unnecessarily
            aggregates[category] = {
                'total': total_value,
                'count': count,
                'average': total_value / count if count > 0 else 0,
                'min': min_value,
                'max': max_value,
                'values': values.copy(),  # Unnecessary copy
                'items': items.copy()     # Another unnecessary copy
            }
        
        # BAD: Store in cache without cleanup
        self.cache[f"aggregates_{time.time()}"] = aggregates.copy()
        
        return aggregates
    
    def inefficient_json_processing(self, json_files: List[str]) -> List[Dict]:
        """
        PERFORMANCE ISSUE 5: Inefficient JSON processing.
        
        Demonstrates:
        - Loading large JSON files completely into memory
        - Not using streaming JSON parsers for large files
        - Inefficient filtering and transformation
        
        Args:
            json_files: List of JSON file paths to process
            
        Returns:
            List of processed JSON data
        """
        all_data = []
        
        for json_file in json_files:
            if not os.path.exists(json_file):
                continue
                
            try:
                # BAD: Loading entire JSON file into memory
                with open(json_file, 'r') as f:
                    data = json.load(f)  # Loads entire file
                
                # BAD: Inefficient filtering with multiple passes
                if isinstance(data, list):
                    # First pass: filter by some criteria
                    filtered_data = []
                    for item in data:
                        if isinstance(item, dict) and 'active' in item and item['active']:
                            filtered_data.append(item)
                    
                    # Second pass: transform data
                    transformed_data = []
                    for item in filtered_data:
                        # BAD: Manual transformation instead of efficient methods
                        transformed_item = {}
                        for key, value in item.items():
                            if isinstance(value, str):
                                transformed_item[key] = value.lower().strip()
                            else:
                                transformed_item[key] = value
                        transformed_data.append(transformed_item)
                    
                    # Third pass: add computed fields
                    for item in transformed_data:
                        # BAD: Expensive computation in loop
                        item['hash'] = hash(str(item))
                        item['processed_at'] = time.time()
                    
                    all_data.extend(transformed_data)
                
                # BAD: Store original data in cache (memory leak)
                self.cache[f"json_{json_file}_{time.time()}"] = data
                
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
        
        return all_data
    
    def create_sample_data_files(self, output_dir: str, file_count: int = 5, 
                                 rows_per_file: int = 1000) -> None:
        """
        Helper method to create sample data files for testing.
        
        Args:
            output_dir: Directory to create files in
            file_count: Number of files to create
            rows_per_file: Number of rows per CSV file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(file_count):
            # Create CSV files
            csv_filename = os.path.join(output_dir, f"sample_data_{i}.csv")
            with open(csv_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['id', 'value', 'category', 'active'])
                
                for j in range(rows_per_file):
                    writer.writerow([
                        j,
                        np.random.randint(1, 1000),
                        f"category_{j % 5}",
                        j % 2 == 0
                    ])
            
            # Create JSON files
            json_filename = os.path.join(output_dir, f"sample_data_{i}.json")
            json_data = []
            for j in range(rows_per_file):
                json_data.append({
                    'id': j,
                    'value': int(np.random.randint(1, 1000)),
                    'category': f"category_{j % 5}",
                    'active': j % 2 == 0,
                    'metadata': {
                        'created_at': time.time(),
                        'source': f"file_{i}"
                    }
                })
            
            with open(json_filename, 'w') as jsonfile:
                json.dump(json_data, jsonfile)
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the current cache state.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            'cache_size': len(self.cache),
            'processed_files_count': len(self.processed_files),
            'cache_keys': list(self.cache.keys())[:10]  # First 10 keys for preview
        }
    
    def clear_cache(self) -> None:
        """
        Method to clear cache - should be called automatically
        to prevent memory leaks in a production application.
        """
        self.cache.clear()
        self.processed_files.clear()