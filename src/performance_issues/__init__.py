"""
Performance Issues Package

A Python application designed with intentional performance issues for AI agents
to identify and recommend corrections.

This package demonstrates common performance anti-patterns including:
- Algorithmic inefficiencies
- Memory leaks and inefficient memory usage
- Database performance problems
- I/O inefficiencies
- Data structure misuse
- Inefficient string and data processing
"""

__version__ = "1.0.0"
__author__ = "Performance Issues Demo"
__description__ = "Python application with intentional performance issues for AI analysis"

from .app import PerformanceProblemApp
from .data_processor import DataProcessor
from .database import DatabaseManager
from .utils import MathUtils, FileUtils, NetworkUtils, CacheUtils

__all__ = [
    "PerformanceProblemApp",
    "DataProcessor", 
    "DatabaseManager",
    "MathUtils",
    "FileUtils",
    "NetworkUtils", 
    "CacheUtils",
]