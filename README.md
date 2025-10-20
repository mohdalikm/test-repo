# Performance Issues Python Application

This repository contains a Python application specifically designed with multiple performance issues for AI agents to identify and recommend corrections. The application demonstrates common performance anti-patterns and inefficiencies that are frequently found in real-world codebases.

## 🎯 Purpose

This application serves as a testing ground for AI code analysis tools to identify and suggest optimizations for various performance problems including:

- **Algorithmic inefficiencies** - Poor algorithm choices and time complexity issues
- **Memory leaks and inefficient memory usage** - Unbounded caches and unnecessary data copies
- **Database performance problems** - N+1 queries, missing indexes, poor connection management
- **I/O inefficiencies** - Blocking operations, repeated file access, lack of batching
- **Data structure misuse** - Using inappropriate data structures for specific operations
- **Inefficient string and data processing** - Unnecessary iterations and transformations

## 📁 Project Structure

This project follows standard Python package conventions with a modern src-layout structure:

```
├── src/
│   └── performance_issues/     # Main package
│       ├── __init__.py        # Package initialization and exports
│       ├── app.py             # Main application class (formerly main.py)
│       ├── cli.py             # Command-line interface
│       ├── config.py          # Configuration management
│       ├── data_processor.py  # Data processing with performance issues
│       ├── database.py        # Database operations with inefficiencies
│       └── utils.py           # Utility functions with various issues
├── tests/                     # Comprehensive unit test suite
│   ├── test_app.py           # Tests for main application
│   ├── test_data_processor.py # Data processing tests
│   └── test_database.py      # Database operation tests
├── config/
│   └── default_config.json   # Default configuration file
├── pyproject.toml            # Modern Python package configuration
├── setup.py                  # Backward compatibility setup file
├── requirements.txt          # Runtime dependencies
├── pytest.ini              # Test configuration
├── .flake8                  # Linting configuration
├── .gitignore              # Git ignore patterns
├── mypy.ini                # Type checking configuration
└── README.md               # This documentation
```

## 🐛 Performance Issues Included

### 1. **app.py** - Core Application Issues
- **Inefficient list operations**: O(n²) list concatenation in loops
- **Redundant calculations**: Recalculating same values multiple times
- **Poor data structure choices**: Using lists for membership testing instead of sets
- **Memory inefficient processing**: Loading large datasets entirely into memory
- **Inefficient I/O operations**: Opening/closing files repeatedly
- **String concatenation issues**: Using string concatenation in loops instead of join
- **Algorithmic inefficiency**: Implementing bubble sort instead of using built-in sort

### 2. **data_processor.py** - Data Processing Issues
- **Inefficient CSV loading**: Multiple file reads, no chunking, missing dtype specifications
- **Pandas anti-patterns**: Using iterrows(), apply() with lambdas instead of vectorized operations
- **Memory leaks**: Storing all processed data in unbounded cache
- **Inefficient data aggregation**: Manual grouping instead of pandas groupby
- **Large JSON processing**: Loading entire files into memory without streaming

### 3. **database.py** - Database Performance Issues
- **N+1 query problem**: Separate queries for each related entity
- **Missing indexes**: No indexes on frequently queried columns
- **Poor connection management**: Creating connections without pooling
- **Inefficient bulk operations**: Inserting records one by one
- **Inefficient search queries**: Using LIKE with leading wildcards
- **Multiple separate queries**: Where single JOIN queries would suffice

### 4. **utils.py** - Utility Function Issues
- **Inefficient recursive algorithms**: Naive recursion without proper memoization
- **Poor algorithm choices**: Trial division for prime checking instead of optimized methods
- **Sequential I/O operations**: Processing files one by one instead of parallel processing
- **Inefficient HTTP requests**: Creating new sessions for each request
- **Poor caching implementation**: No TTL, size limits, or eviction policies
- **Inefficient string operations**: Multiple passes over the same data
- **Wrong data structure usage**: Linear searches where hash lookups would be faster

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd test-repo
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
# Install with all dependencies
pip install -e .

# Or install dependencies separately
pip install -r requirements.txt
```

### Command-Line Interface

The application provides a comprehensive CLI for running performance tests:

```bash
# Run the complete performance test suite
performance-issues run

# Run with specific dataset size
performance-issues run --size large --iterations 3

# Generate sample data for testing
performance-issues generate-data --file-count 10 --rows-per-file 5000

# Analyze previous test results
performance-issues analyze --input results.json --format table

# Test database operations
performance-issues database --test-queries

# Test utility functions
performance-issues utils --test-type math --iterations 2

# Get help for any command
performance-issues --help
performance-issues run --help
```

### Python API Usage

You can also use the package programmatically:

```python
from performance_issues import PerformanceProblemApp, DataProcessor, DatabaseManager

# Run performance tests
with PerformanceProblemApp() as app:
    results = app.run_performance_test()
    print(f"Total execution time: {sum(results.values()):.2f} seconds")

# Test data processing issues
processor = DataProcessor()
processor.create_sample_data_files('test_data', file_count=5)

# Test database operations
db = DatabaseManager()
try:
    stats = db.inefficient_aggregation_queries()
    print(f"Database stats: {stats}")
finally:
    db.close_all_connections()
```

### Running Tests

Execute the comprehensive test suite:

```bash
# Run all tests with coverage
pytest

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m performance   # Performance tests only
pytest -m slow          # Skip slow tests: pytest -m "not slow"

# Run tests with coverage report
pytest --cov=src/performance_issues --cov-report=html

# Run tests for a specific module
pytest tests/test_app.py
```

## 📊 Expected Performance Problems

When running this application, you should observe:

- **High CPU usage** due to inefficient algorithms (O(n²) operations, poor sorting choices)
- **High memory consumption** from memory leaks and unbounded caches
- **Slow execution times** from redundant calculations and inefficient loops
- **Excessive database queries** from N+1 query patterns and missing indexes
- **Blocking I/O operations** that could be parallelized or batched
- **Poor cache hit rates** due to inefficient caching strategies
- **String processing inefficiencies** from repeated concatenation and parsing
- **Inefficient data structure usage** (lists for membership testing, etc.)

## 🔧 Tools for Performance Analysis

The application includes built-in profiling support and can be analyzed with various tools:

### Built-in Profiling
```bash
# Run performance tests with profiling enabled
performance-issues run --profile --iterations 3

# Analyze results from multiple runs  
performance-issues analyze --input results.json --format table
```

### External Profiling Tools
```bash
# CPU profiling with cProfile
python -m cProfile -s cumulative -m performance_issues.cli run

# Memory profiling with memory-profiler (already installed)
python -m memory_profiler -m performance_issues.app

# Line-by-line profiling with line-profiler
pip install line-profiler
kernprof -l -v src/performance_issues/app.py

# Real-time performance monitoring with py-spy (already installed)
performance-issues run --size large &
py-spy top --pid $!
```

### Code Quality and Analysis
```bash
# Type checking with mypy
mypy src/performance_issues/

# Code formatting with black
black src/ tests/

# Linting with flake8
flake8 src/ tests/

# Run all quality checks
pytest --cov=src/performance_issues --mypy --flake8
```

## 🎯 AI Agent Recommendations

An AI agent analyzing this code should identify and recommend:

### Algorithmic Improvements
- Replace O(n²) algorithms with O(n log n) or O(n) alternatives
- Use appropriate data structures (sets for membership, dicts for lookups)
- Implement proper memoization for recursive functions
- Use built-in functions instead of manual implementations

### Memory Optimization
- Implement cache size limits and TTL
- Use generators and iterators for large datasets
- Process data in chunks instead of loading everything into memory
- Clear unused references and implement proper cleanup

### Database Optimization
- Add indexes on frequently queried columns
- Use JOIN queries instead of N+1 patterns
- Implement connection pooling
- Use bulk operations for multiple inserts/updates
- Add query optimization and prepared statements

### I/O Optimization
- Batch file operations
- Use async/await for I/O bound operations
- Implement connection reuse for HTTP requests
- Use streaming for large files
- Cache frequently accessed data

### Data Processing Improvements
- Use vectorized pandas operations
- Implement proper data pipeline with chunking
- Use appropriate pandas dtypes
- Minimize DataFrame copies
- Use efficient aggregation methods

## 📈 Performance Testing and Benchmarking

The package includes comprehensive performance testing and benchmarking:

### CLI Performance Testing
```bash
# Quick performance test
performance-issues run

# Comprehensive benchmarking with multiple iterations
performance-issues run --size large --iterations 5 --profile --output benchmark_results.json

# Generate test data and run analysis
performance-issues generate-data --file-count 20 --rows-per-file 10000
performance-issues run --size large --output results.json
performance-issues analyze --input results.json --format table --output analysis.txt
```

### Unit Test Benchmarking
```bash
# Run performance regression tests
pytest tests/ -m performance

# Run with coverage and performance markers
pytest --cov=src/performance_issues -m "unit or performance"

# Benchmark specific functions
pytest tests/test_app.py::TestPerformanceProblemApp::test_run_performance_test -v
```

### Configuration Management
```bash
# View current configuration
performance-issues config --show

# Validate configuration
performance-issues config --validate

# Save configuration to file
performance-issues config --save my_config.json --show

# Use custom configuration
performance-issues --config my_config.json run --size small
```

## 🤖 For AI Agents

This repository is specifically designed for AI code analysis tools. The performance issues are:

1. **Well-documented** with clear comments explaining what's wrong
2. **Realistic** - based on real-world performance anti-patterns  
3. **Varied** - covering different types of performance problems
4. **Measurable** - with clear before/after optimization opportunities
5. **Educational** - demonstrating both the problem and better alternatives
6. **Testable** - comprehensive test suite to verify optimizations don't break functionality
7. **Configurable** - flexible configuration system for different testing scenarios
8. **CLI-accessible** - easy command-line interface for automated analysis

### Key Features for AI Analysis

- **Structured codebase** following modern Python package conventions
- **Type hints** throughout for better static analysis
- **Comprehensive testing** with performance regression tests
- **Configuration management** for different analysis scenarios
- **CLI interface** for automated testing and benchmarking
- **Detailed documentation** with clear performance anti-patterns
- **Profiling integration** for before/after optimization measurement

Each performance issue includes comments starting with "PERFORMANCE ISSUE" and "BAD:" to help identify problematic code patterns. The package structure allows for easy integration with automated analysis tools.

## 🏗️ Development

### Package Installation for Development

```bash
# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Or install all optional dependencies
pip install -e ".[dev,profiling,cli]"
```

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Check types
mypy src/

# Lint code  
flake8 src/ tests/

# Run all checks
pre-commit run --all-files  # If using pre-commit hooks
```

### Adding New Performance Issues

1. Add the performance issue to the appropriate module in `src/performance_issues/`
2. Include clear comments explaining the problem
3. Add corresponding unit tests in `tests/`
4. Update the CLI interface if needed in `src/performance_issues/cli.py`
5. Document the issue in this README

### Package Structure Guidelines

- Follow PEP 8 and modern Python conventions
- Include type hints for all public APIs
- Write comprehensive docstrings
- Add unit tests for all new functionality
- Use the configuration system for customizable behavior
- Maintain backward compatibility in the CLI interface

## 📝 License

This project is created for educational and testing purposes. Feel free to use it for training AI models, testing code analysis tools, or learning about performance optimization.

---

**⚠️ Important Note**: This application is intentionally inefficient and contains performance anti-patterns. Do not use these code patterns in production systems! The purpose is to demonstrate common performance problems for educational and AI analysis purposes.