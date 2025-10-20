#!/usr/bin/env python3
"""
Script to generate sample data files for testing the performance issues.
Run this script to create test data that will demonstrate the various performance problems.
"""

import os
import json
import csv
import random
import time
from typing import List, Dict, Any


def create_sample_csv_files(output_dir: str = "sample_data", file_count: int = 5, rows_per_file: int = 10000):
    """
    Create sample CSV files with various data types and sizes
    """
    os.makedirs(output_dir, exist_ok=True)
    
    categories = ["electronics", "books", "clothing", "home", "sports"]
    statuses = ["active", "inactive", "pending", "archived"]
    
    for i in range(file_count):
        filename = os.path.join(output_dir, f"data_{i}.csv")
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['id', 'name', 'category', 'value', 'price', 'status', 'created_at'])
            
            # Write data rows
            for j in range(rows_per_file):
                writer.writerow([
                    j + (i * rows_per_file),
                    f"Product_{j}_{i}",
                    random.choice(categories),
                    random.uniform(1.0, 1000.0),
                    random.uniform(10.0, 500.0),
                    random.choice(statuses),
                    f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
                ])
        
        print(f"Created {filename} with {rows_per_file} rows")


def create_sample_json_files(output_dir: str = "sample_data", file_count: int = 3, records_per_file: int = 5000):
    """
    Create sample JSON files with nested data structures
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(file_count):
        filename = os.path.join(output_dir, f"json_data_{i}.json")
        
        data = []
        for j in range(records_per_file):
            record = {
                "id": j + (i * records_per_file),
                "user_id": random.randint(1, 1000),
                "title": f"Item {j} from file {i}",
                "description": f"Description for item {j} " * random.randint(5, 20),
                "metadata": {
                    "created_at": time.time() - random.randint(0, 86400 * 365),
                    "updated_at": time.time() - random.randint(0, 86400 * 30),
                    "tags": [f"tag_{k}" for k in range(random.randint(1, 5))],
                    "rating": random.uniform(1.0, 5.0),
                    "views": random.randint(0, 10000)
                },
                "active": random.choice([True, False]),
                "category": random.choice(["tech", "science", "arts", "business", "health"]),
                "priority": random.randint(1, 10)
            }
            data.append(record)
        
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)
        
        print(f"Created {filename} with {records_per_file} records")


def create_large_text_files(output_dir: str = "sample_data", file_count: int = 3):
    """
    Create large text files for file processing performance tests
    """
    os.makedirs(output_dir, exist_ok=True)
    
    words = ["performance", "optimization", "algorithm", "database", "memory", "cache", 
             "network", "processing", "efficiency", "scalability", "bottleneck", "latency"]
    
    for i in range(file_count):
        filename = os.path.join(output_dir, f"large_text_{i}.txt")
        
        with open(filename, 'w') as f:
            # Create files of different sizes
            lines = 10000 * (i + 1)
            
            for j in range(lines):
                # Create lines with random words
                line_words = random.choices(words, k=random.randint(5, 15))
                line = " ".join(line_words)
                f.write(f"Line {j}: {line}\n")
        
        file_size = os.path.getsize(filename)
        print(f"Created {filename} with {lines} lines ({file_size / 1024 / 1024:.1f} MB)")


def create_duplicate_data_file(output_dir: str = "sample_data"):
    """
    Create a file with many duplicates to test deduplication performance
    """
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.join(output_dir, "duplicate_data.csv")
    
    # Create data with intentional duplicates
    base_records = []
    for i in range(1000):
        base_records.append({
            'id': i,
            'name': f"Name_{i % 100}",  # Only 100 unique names
            'email': f"user_{i % 50}@example.com",  # Only 50 unique emails
            'department': f"dept_{i % 10}",  # Only 10 unique departments
            'value': random.randint(1, 100)
        })
    
    # Duplicate the records multiple times
    all_records = base_records * 10  # 10,000 total records with many duplicates
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'name', 'email', 'department', 'value'])
        writer.writeheader()
        writer.writerows(all_records)
    
    print(f"Created {filename} with {len(all_records)} records (many duplicates)")


def create_nested_directory_structure(base_dir: str = "nested_files"):
    """
    Create a nested directory structure with files for testing directory traversal performance
    """
    os.makedirs(base_dir, exist_ok=True)
    
    # Create nested directories
    for level1 in range(5):
        level1_dir = os.path.join(base_dir, f"level1_{level1}")
        os.makedirs(level1_dir, exist_ok=True)
        
        for level2 in range(10):
            level2_dir = os.path.join(level1_dir, f"level2_{level2}")
            os.makedirs(level2_dir, exist_ok=True)
            
            # Create files in each directory
            for file_num in range(5):
                filename = os.path.join(level2_dir, f"file_{file_num}.txt")
                with open(filename, 'w') as f:
                    f.write(f"Content of file {file_num} in {level2_dir}\n" * 100)
    
    print(f"Created nested directory structure in {base_dir}")


def create_performance_test_config():
    """
    Create a configuration file for performance testing
    """
    config = {
        "test_settings": {
            "small_dataset_size": 1000,
            "medium_dataset_size": 10000,
            "large_dataset_size": 100000,
            "iterations": 10,
            "timeout_seconds": 60
        },
        "database_settings": {
            "user_count": 100,
            "posts_per_user": 5,
            "comments_per_post": 3
        },
        "file_settings": {
            "csv_files": 5,
            "json_files": 3,
            "text_files": 3,
            "rows_per_csv": 10000,
            "records_per_json": 5000
        },
        "performance_thresholds": {
            "max_execution_time": 30.0,
            "max_memory_usage_mb": 500,
            "max_database_queries": 100
        }
    }
    
    with open("performance_test_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Created performance_test_config.json")


def main():
    """
    Generate all sample data files for performance testing
    """
    print("Creating sample data files for performance testing...")
    
    # Create sample data directory
    sample_data_dir = "sample_data"
    
    # Generate different types of test data
    create_sample_csv_files(sample_data_dir, file_count=5, rows_per_file=10000)
    create_sample_json_files(sample_data_dir, file_count=3, records_per_file=5000)
    create_large_text_files(sample_data_dir, file_count=3)
    create_duplicate_data_file(sample_data_dir)
    create_nested_directory_structure("nested_files")
    create_performance_test_config()
    
    print("\nSample data generation completed!")
    print("\nGenerated files:")
    print("- sample_data/: CSV, JSON, and text files for testing")
    print("- nested_files/: Nested directory structure")
    print("- performance_test_config.json: Configuration for performance tests")
    
    # Calculate total size
    total_size = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(('.csv', '.json', '.txt')):
                filepath = os.path.join(root, file)
                total_size += os.path.getsize(filepath)
    
    print(f"\nTotal test data size: {total_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()