"""
Unit tests for the DataProcessor class.

Tests the various performance issues in data processing operations.
"""

import pytest
import tempfile
import os
import csv
import json
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import DataProcessor


class TestDataProcessor:
    """Test suite for DataProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.processor = DataProcessor()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up after each test method."""
        self.processor.clear_cache()
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_sample_csv(self, filename: str, rows: int = 10):
        """Create a sample CSV file for testing."""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'value', 'category'])
            
            for i in range(rows):
                writer.writerow([i, i * 10, f'cat_{i % 3}'])
        
        return filepath
    
    def create_sample_json(self, filename: str, records: int = 10):
        """Create a sample JSON file for testing."""
        filepath = os.path.join(self.temp_dir, filename)
        data = []
        for i in range(records):
            data.append({
                'id': i,
                'value': i * 10,
                'category': f'cat_{i % 3}',
                'active': i % 2 == 0
            })
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
        
        return filepath
    
    def test_processor_initialization(self):
        """Test that the processor initializes correctly."""
        assert self.processor.cache == {}
        assert self.processor.processed_files == []
    
    def test_load_csv_inefficiently(self):
        """Test inefficient CSV loading."""
        csv_file = self.create_sample_csv('test.csv', 5)
        
        # Load CSV
        df = self.processor.load_csv_inefficiently(csv_file)
        
        # Verify DataFrame is loaded correctly
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert list(df.columns) == ['id', 'value', 'category']
        
        # Verify cache is populated (memory leak)
        assert csv_file in self.processor.cache
        assert f"{csv_file}_metadata" in self.processor.cache
        
        # Verify metadata
        metadata = self.processor.cache[f"{csv_file}_metadata"]
        assert metadata['rows'] == 6  # Including header
        assert 'loaded_at' in metadata
    
    def test_inefficient_pandas_operations(self):
        """Test inefficient pandas operations."""
        # Create a simple DataFrame
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [10, 20, 30]
        })
        
        initial_cache_size = len(self.processor.cache)
        
        result_df = self.processor.inefficient_pandas_operations(df)
        
        # Verify result DataFrame structure
        assert isinstance(result_df, pd.DataFrame)
        expected_columns = ['index', 'original_value', 'new_value', 'is_even', 'squared', 'log_value']
        for col in expected_columns:
            assert col in result_df.columns
        
        # Verify calculations
        assert result_df.iloc[0]['new_value'] == 30  # 10 * 2 + 10 = 30
        assert result_df.iloc[0]['is_even'] == True  # 30 is even
        assert result_df.iloc[0]['squared'] == 900   # 30^2 = 900
        
        # Verify cache has grown (memory leak)
        final_cache_size = len(self.processor.cache)
        assert final_cache_size > initial_cache_size
    
    def test_memory_leaking_file_processor(self):
        """Test memory leaking file processor."""
        # Create multiple CSV files
        csv_files = []
        for i in range(3):
            csv_file = self.create_sample_csv(f'test_{i}.csv', 5)
            csv_files.append(csv_file)
        
        initial_cache_size = len(self.processor.cache)
        initial_processed_files = len(self.processor.processed_files)
        
        results = self.processor.memory_leaking_file_processor(self.temp_dir)
        
        # Verify results structure
        assert isinstance(results, dict)
        assert len(results) == 3
        
        for filename, result in results.items():
            assert 'original_content' in result
            assert 'processed_lines' in result
            assert 'line_count' in result
            assert 'file_size' in result
            assert 'processed_at' in result
        
        # Verify memory leaks
        final_cache_size = len(self.processor.cache)
        final_processed_files = len(self.processor.processed_files)
        
        assert final_cache_size > initial_cache_size
        assert final_processed_files > initial_processed_files
    
    def test_inefficient_data_aggregation(self):
        """Test inefficient data aggregation."""
        data = [
            {'category': 'A', 'value': 10},
            {'category': 'B', 'value': 20},
            {'category': 'A', 'value': 15},
            {'category': 'B', 'value': 25},
            {'category': 'C', 'value': 30}
        ]
        
        initial_cache_size = len(self.processor.cache)
        
        aggregates = self.processor.inefficient_data_aggregation(data)
        
        # Verify aggregation results
        assert isinstance(aggregates, dict)
        assert 'A' in aggregates
        assert 'B' in aggregates
        assert 'C' in aggregates
        
        # Verify category A aggregations
        cat_a = aggregates['A']
        assert cat_a['total'] == 25  # 10 + 15
        assert cat_a['count'] == 2
        assert cat_a['average'] == 12.5  # 25 / 2
        assert cat_a['min'] == 10
        assert cat_a['max'] == 15
        
        # Verify category B aggregations
        cat_b = aggregates['B']
        assert cat_b['total'] == 45  # 20 + 25
        assert cat_b['count'] == 2
        assert cat_b['average'] == 22.5  # 45 / 2
        
        # Verify cache growth (memory leak)
        final_cache_size = len(self.processor.cache)
        assert final_cache_size > initial_cache_size
    
    def test_inefficient_json_processing(self):
        """Test inefficient JSON processing."""
        # Create JSON files
        json_files = []
        for i in range(2):
            json_file = self.create_sample_json(f'test_{i}.json', 5)
            json_files.append(json_file)
        
        initial_cache_size = len(self.processor.cache)
        
        all_data = self.processor.inefficient_json_processing(json_files)
        
        # Verify processing results
        assert isinstance(all_data, list)
        
        # Should only include active records (even IDs)
        active_count = sum(1 for item in all_data if item.get('active', False))
        assert active_count == len([item for item in all_data if item['active']])
        
        # Verify transformations
        for item in all_data:
            assert 'hash' in item
            assert 'processed_at' in item
            # String values should be lowercased and stripped
            if 'category' in item:
                assert item['category'].islower()
        
        # Verify cache growth (memory leak)
        final_cache_size = len(self.processor.cache)
        assert final_cache_size > initial_cache_size
    
    def test_create_sample_data_files(self):
        """Test sample data file creation."""
        output_dir = os.path.join(self.temp_dir, 'sample_output')
        
        self.processor.create_sample_data_files(output_dir, file_count=2, rows_per_file=5)
        
        # Verify files were created
        assert os.path.exists(output_dir)
        
        # Check CSV files
        csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
        assert len(csv_files) == 2
        
        # Check JSON files
        json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
        assert len(json_files) == 2
        
        # Verify CSV content
        csv_file = os.path.join(output_dir, csv_files[0])
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert headers == ['id', 'value', 'category', 'active']
            
            rows = list(reader)
            assert len(rows) == 5  # rows_per_file
    
    def test_get_cache_info(self):
        """Test cache information retrieval."""
        # Initially empty
        cache_info = self.processor.get_cache_info()
        assert cache_info['cache_size'] == 0
        assert cache_info['processed_files_count'] == 0
        
        # Add some data to cache
        self.processor.cache['test_key'] = 'test_value'
        self.processor.processed_files.append('test_file.csv')
        
        cache_info = self.processor.get_cache_info()
        assert cache_info['cache_size'] == 1
        assert cache_info['processed_files_count'] == 1
    
    def test_clear_cache(self):
        """Test cache clearing functionality."""
        # Add data to cache
        self.processor.cache['test_key'] = 'test_value'
        self.processor.processed_files.append('test_file.csv')
        
        assert len(self.processor.cache) > 0
        assert len(self.processor.processed_files) > 0
        
        # Clear cache
        self.processor.clear_cache()
        
        assert len(self.processor.cache) == 0
        assert len(self.processor.processed_files) == 0
    
    def test_error_handling_nonexistent_directory(self):
        """Test error handling for non-existent directory."""
        results = self.processor.memory_leaking_file_processor('/nonexistent/directory')
        assert results == {}
    
    def test_error_handling_nonexistent_json_files(self):
        """Test error handling for non-existent JSON files."""
        nonexistent_files = ['/path/to/nonexistent1.json', '/path/to/nonexistent2.json']
        
        all_data = self.processor.inefficient_json_processing(nonexistent_files)
        assert all_data == []
    
    @pytest.mark.parametrize("file_count", [1, 3, 5])
    def test_scaling_with_file_count(self, file_count):
        """Test how processing scales with number of files."""
        # Create multiple CSV files
        for i in range(file_count):
            self.create_sample_csv(f'scale_test_{i}.csv', 5)
        
        results = self.processor.memory_leaking_file_processor(self.temp_dir)
        
        # Should process all CSV files
        csv_results = {k: v for k, v in results.items() if k.endswith('.csv')}
        assert len(csv_results) == file_count
    
    def test_performance_degradation(self):
        """Test that performance degrades as cache grows."""
        # This is more of a smoke test - in a real scenario,
        # we'd measure actual performance degradation
        
        import time
        
        # Load multiple files to grow cache
        for i in range(5):
            csv_file = self.create_sample_csv(f'perf_test_{i}.csv', 10)
            
            start_time = time.time()
            self.processor.load_csv_inefficiently(csv_file)
            end_time = time.time()
            
            # Just verify the operation completes
            assert end_time >= start_time
        
        # Cache should have grown significantly
        assert len(self.processor.cache) >= 10  # At least 2 entries per file