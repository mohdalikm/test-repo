"""
Configuration management module.

Provides centralized configuration for the performance issues application.
"""

import os
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    db_path: str = "performance_test.db"
    connection_timeout: int = 30
    max_connections: int = 10
    enable_foreign_keys: bool = True
    

@dataclass
class PerformanceTestConfig:
    """Performance testing configuration."""
    small_dataset_size: int = 1000
    medium_dataset_size: int = 10000
    large_dataset_size: int = 100000
    iterations: int = 10
    timeout_seconds: int = 60
    enable_profiling: bool = False


@dataclass
class CacheConfig:
    """Cache configuration settings."""
    max_cache_size: int = 1000
    ttl_seconds: int = 3600
    enable_cache: bool = True
    cleanup_interval: int = 300


@dataclass
class FileProcessingConfig:
    """File processing configuration."""
    chunk_size: int = 8192
    max_file_size_mb: int = 100
    temp_dir: str = "tmp"
    parallel_processing: bool = False
    max_workers: int = 4


@dataclass
class NetworkConfig:
    """Network configuration settings."""
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    use_session_pooling: bool = False
    max_connections_per_host: int = 10


@dataclass
class AppConfig:
    """Main application configuration."""
    debug: bool = False
    log_level: str = "INFO"
    output_dir: str = "output"
    data_dir: str = "data"
    
    # Sub-configurations
    database: DatabaseConfig
    performance_test: PerformanceTestConfig
    cache: CacheConfig
    file_processing: FileProcessingConfig
    network: NetworkConfig
    
    def __init__(self):
        """Initialize with default sub-configurations."""
        self.database = DatabaseConfig()
        self.performance_test = PerformanceTestConfig()
        self.cache = CacheConfig()
        self.file_processing = FileProcessingConfig()
        self.network = NetworkConfig()


class ConfigManager:
    """
    Configuration manager for the performance issues application.
    
    Handles loading, saving, and managing application configuration.
    """
    
    DEFAULT_CONFIG_FILE = "config.json"
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self.config = AppConfig()
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file or environment variables."""
        # Try to load from file first
        if os.path.exists(self.config_file):
            try:
                self._load_from_file()
            except Exception as e:
                print(f"Error loading config from {self.config_file}: {e}")
                print("Using default configuration")
        
        # Override with environment variables
        self._load_from_environment()
    
    def _load_from_file(self) -> None:
        """Load configuration from JSON file."""
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
        
        # Update configuration with loaded data
        self._update_config_from_dict(config_data)
    
    def _load_from_environment(self) -> None:
        """Load configuration from environment variables."""
        # Database configuration
        if os.getenv('DB_PATH'):
            self.config.database.db_path = os.getenv('DB_PATH')
        if os.getenv('DB_CONNECTION_TIMEOUT'):
            self.config.database.connection_timeout = int(os.getenv('DB_CONNECTION_TIMEOUT'))
        
        # Performance test configuration
        if os.getenv('PERF_LARGE_DATASET_SIZE'):
            self.config.performance_test.large_dataset_size = int(os.getenv('PERF_LARGE_DATASET_SIZE'))
        if os.getenv('PERF_TIMEOUT'):
            self.config.performance_test.timeout_seconds = int(os.getenv('PERF_TIMEOUT'))
        
        # Cache configuration
        if os.getenv('CACHE_MAX_SIZE'):
            self.config.cache.max_cache_size = int(os.getenv('CACHE_MAX_SIZE'))
        if os.getenv('CACHE_TTL'):
            self.config.cache.ttl_seconds = int(os.getenv('CACHE_TTL'))
        
        # Application configuration
        if os.getenv('DEBUG'):
            self.config.debug = os.getenv('DEBUG').lower() in ('true', '1', 'yes')
        if os.getenv('LOG_LEVEL'):
            self.config.log_level = os.getenv('LOG_LEVEL')
        if os.getenv('OUTPUT_DIR'):
            self.config.output_dir = os.getenv('OUTPUT_DIR')
        if os.getenv('DATA_DIR'):
            self.config.data_dir = os.getenv('DATA_DIR')
    
    def _update_config_from_dict(self, config_data: Dict[str, Any]) -> None:
        """Update configuration from dictionary data."""
        # Update main config
        for key, value in config_data.items():
            if hasattr(self.config, key) and not isinstance(getattr(self.config, key), (DatabaseConfig, PerformanceTestConfig, CacheConfig, FileProcessingConfig, NetworkConfig)):
                setattr(self.config, key, value)
        
        # Update sub-configurations
        if 'database' in config_data:
            self._update_dataclass_from_dict(self.config.database, config_data['database'])
        
        if 'performance_test' in config_data:
            self._update_dataclass_from_dict(self.config.performance_test, config_data['performance_test'])
        
        if 'cache' in config_data:
            self._update_dataclass_from_dict(self.config.cache, config_data['cache'])
        
        if 'file_processing' in config_data:
            self._update_dataclass_from_dict(self.config.file_processing, config_data['file_processing'])
        
        if 'network' in config_data:
            self._update_dataclass_from_dict(self.config.network, config_data['network'])
    
    def _update_dataclass_from_dict(self, dataclass_instance, data: Dict[str, Any]) -> None:
        """Update dataclass instance from dictionary."""
        for key, value in data.items():
            if hasattr(dataclass_instance, key):
                setattr(dataclass_instance, key, value)
    
    def save_config(self, config_file: Optional[str] = None) -> None:
        """
        Save current configuration to file.
        
        Args:
            config_file: Path to save configuration (optional)
        """
        file_path = config_file or self.config_file
        
        config_dict = {
            'debug': self.config.debug,
            'log_level': self.config.log_level,
            'output_dir': self.config.output_dir,
            'data_dir': self.config.data_dir,
            'database': asdict(self.config.database),
            'performance_test': asdict(self.config.performance_test),
            'cache': asdict(self.config.cache),
            'file_processing': asdict(self.config.file_processing),
            'network': asdict(self.config.network)
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        print(f"Configuration saved to {file_path}")
    
    def get_config(self) -> AppConfig:
        """
        Get current configuration.
        
        Returns:
            Current application configuration
        """
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """
        Update configuration with keyword arguments.
        
        Args:
            **kwargs: Configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = AppConfig()
    
    def validate_config(self) -> bool:
        """
        Validate current configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Validate database configuration
            if not self.config.database.db_path:
                print("Error: Database path cannot be empty")
                return False
            
            if self.config.database.connection_timeout <= 0:
                print("Error: Database connection timeout must be positive")
                return False
            
            # Validate performance test configuration
            if self.config.performance_test.small_dataset_size <= 0:
                print("Error: Dataset sizes must be positive")
                return False
            
            if self.config.performance_test.timeout_seconds <= 0:
                print("Error: Timeout must be positive")
                return False
            
            # Validate cache configuration
            if self.config.cache.max_cache_size <= 0:
                print("Error: Cache size must be positive")
                return False
            
            if self.config.cache.ttl_seconds <= 0:
                print("Error: TTL must be positive")
                return False
            
            # Validate file processing configuration
            if self.config.file_processing.chunk_size <= 0:
                print("Error: Chunk size must be positive")
                return False
            
            if self.config.file_processing.max_workers <= 0:
                print("Error: Max workers must be positive")
                return False
            
            # Validate network configuration
            if self.config.network.timeout_seconds <= 0:
                print("Error: Network timeout must be positive")
                return False
            
            # Validate directories exist (create if needed)
            for dir_path in [self.config.output_dir, self.config.data_dir, self.config.file_processing.temp_dir]:
                os.makedirs(dir_path, exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"Configuration validation error: {e}")
            return False
    
    def print_config(self) -> None:
        """Print current configuration in a readable format."""
        print("\n=== Current Configuration ===")
        print(f"Debug: {self.config.debug}")
        print(f"Log Level: {self.config.log_level}")
        print(f"Output Directory: {self.config.output_dir}")
        print(f"Data Directory: {self.config.data_dir}")
        
        print("\n--- Database Configuration ---")
        print(f"DB Path: {self.config.database.db_path}")
        print(f"Connection Timeout: {self.config.database.connection_timeout}s")
        print(f"Max Connections: {self.config.database.max_connections}")
        
        print("\n--- Performance Test Configuration ---")
        print(f"Small Dataset Size: {self.config.performance_test.small_dataset_size}")
        print(f"Medium Dataset Size: {self.config.performance_test.medium_dataset_size}")
        print(f"Large Dataset Size: {self.config.performance_test.large_dataset_size}")
        print(f"Test Iterations: {self.config.performance_test.iterations}")
        print(f"Timeout: {self.config.performance_test.timeout_seconds}s")
        
        print("\n--- Cache Configuration ---")
        print(f"Max Cache Size: {self.config.cache.max_cache_size}")
        print(f"TTL: {self.config.cache.ttl_seconds}s")
        print(f"Cache Enabled: {self.config.cache.enable_cache}")
        
        print("\n--- File Processing Configuration ---")
        print(f"Chunk Size: {self.config.file_processing.chunk_size} bytes")
        print(f"Max File Size: {self.config.file_processing.max_file_size_mb} MB")
        print(f"Temp Directory: {self.config.file_processing.temp_dir}")
        print(f"Parallel Processing: {self.config.file_processing.parallel_processing}")
        print(f"Max Workers: {self.config.file_processing.max_workers}")
        
        print("\n--- Network Configuration ---")
        print(f"Timeout: {self.config.network.timeout_seconds}s")
        print(f"Max Retries: {self.config.network.max_retries}")
        print(f"Retry Delay: {self.config.network.retry_delay}s")
        print(f"Session Pooling: {self.config.network.use_session_pooling}")


# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """
    Get the global configuration manager instance.
    
    Returns:
        Global ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config() -> AppConfig:
    """
    Get the current application configuration.
    
    Returns:
        Current application configuration
    """
    return get_config_manager().get_config()


def initialize_config(config_file: Optional[str] = None) -> ConfigManager:
    """
    Initialize the global configuration manager.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Initialized ConfigManager instance
    """
    global _config_manager
    _config_manager = ConfigManager(config_file)
    return _config_manager