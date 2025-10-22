# Python Application Development Framework

This repository contains a comprehensive Python application framework designed for development, testing, and analysis. The application demonstrates various programming patterns and provides a robust foundation for building and analyzing Python applications.

## 🎯 Purpose

This application serves as a comprehensive development framework featuring:

- **Modular architecture** - Clean separation of concerns across different modules
- **Data processing capabilities** - Comprehensive data handling and transformation tools
- **Database operations** - Full database management and query operations
- **Configuration management** - Flexible configuration system with JSON support
- **Command-line interface** - Professional CLI for application interaction
- **Testing framework** - Complete unit testing suite with coverage reporting

## 📁 Project Structure

This project follows standard Python package conventions with a clean, flat src-layout structure:

```
test-repo/
├── src/                       # Source code directory
│   ├── __init__.py           # Package initialization and exports
│   ├── app.py                # Main application class with core functionality
│   ├── cli.py                # Command-line interface
│   ├── config.py             # Configuration management system
│   ├── data_processor.py     # Data processing and transformation utilities
│   ├── database.py           # Database operations and management
│   └── utils.py              # General utility functions and helpers
├── tests/                    # Comprehensive unit test suite
│   ├── __init__.py          # Test package initialization
│   ├── test_app.py          # Tests for main application functionality
│   ├── test_data_processor.py # Data processing tests
│   └── test_database.py     # Database operation tests
├── config/                   # Configuration files
│   └── default_config.json  # Default application configuration
├── docs/                     # Documentation directory
├── sample_data/             # Sample data files for testing
├── venv/                    # Virtual environment (created during setup)
├── pyproject.toml           # Modern Python package configuration
├── setup.py                 # Backward compatibility setup file
├── requirements.txt         # Runtime dependencies
├── pytest.ini             # Test runner configuration
├── .flake8                 # Code linting configuration
├── .gitignore             # Git ignore patterns
├── mypy.ini               # Type checking configuration
└── README.md              # This documentation
```

## 🐛 Application Features

### 1. **app.py** - Core Application Module
- **Comprehensive functionality**: Main application logic with various operational features
- **Modular design**: Clean class structure with proper initialization and context management
- **Data processing integration**: Seamless integration with data processing components
- **Database connectivity**: Built-in database management and operations
- **Configurable operations**: Multiple operational modes and configuration options
- **Performance testing**: Built-in benchmarking and measurement capabilities
- **Error handling**: Robust error management and logging

### 2. **data_processor.py** - Data Processing Module
- **File format support**: CSV, JSON, and various data format processing
- **Pandas integration**: Advanced data manipulation and analysis capabilities
- **Memory management**: Efficient data handling and processing strategies
- **Batch processing**: Support for large dataset processing in chunks
- **Data validation**: Input validation and data quality checks

### 3. **database.py** - Database Management Module
- **SQLite integration**: Built-in SQLite database operations
- **Connection management**: Efficient database connection handling
- **Query operations**: Support for complex database queries and transactions
- **Data modeling**: Proper database schema and relationship management
- **Performance monitoring**: Database operation timing and optimization

### 4. **utils.py** - Utility Functions Module
- **Mathematical operations**: Advanced mathematical calculations and algorithms
- **File operations**: Comprehensive file handling and I/O operations
- **Network utilities**: HTTP requests and network communication tools
- **Caching system**: Flexible caching mechanisms for improved performance
- **String processing**: Text manipulation and parsing utilities

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

The application provides a comprehensive CLI for various operations:

```bash
# Run the main application with default settings
python src/cli.py run

# Run with specific dataset size and iterations
python src/cli.py run --size large --iterations 3

# Enable AWS CodeGuru Profiler for performance analysis
python src/cli.py run --size large --codeguru --profiling-group my-app-group

# Run with both local profiling and CodeGuru
python src/cli.py run --size medium --profile --codeguru --iterations 2

# Generate sample data for testing
python src/cli.py generate-data --file-count 10 --rows-per-file 5000

# Analyze application results
python src/cli.py analyze --input results.json --format table

# Test database operations
python src/cli.py database --test-queries

# Test utility functions
python src/cli.py utils --test-type math --iterations 2

# Get help for any command
python src/cli.py --help
python src/cli.py run --help
```

#### AWS CodeGuru Profiler Integration

The application includes built-in support for AWS CodeGuru Profiler:

```bash
# Enable CodeGuru Profiler with default settings
python src/cli.py run --codeguru

# Specify custom profiling group
python src/cli.py run --codeguru --profiling-group my-custom-group

# Run with CodeGuru for extended analysis
python src/cli.py run --size large --iterations 5 --codeguru --output results.json
```

**Prerequisites for CodeGuru Profiler:**
- AWS account with CodeGuru Profiler enabled
- Proper AWS credentials configured (AWS CLI, environment variables, or IAM role)
- CodeGuru profiling group created in your AWS account
- `codeguru_profiler_agent` package installed (included in requirements)

### Python API Usage

You can also use the package programmatically:

```python
# Add src to Python path for direct imports
import sys
sys.path.insert(0, 'src')

from app import PerformanceProblemApp
from data_processor import DataProcessor
from database import DatabaseManager

# Run the main application
with PerformanceProblemApp() as app:
    results = app.run_performance_test()
    print(f"Total execution time: {sum(results.values()):.2f} seconds")

# Use data processing features
processor = DataProcessor()
processor.create_sample_data_files('test_data', file_count=5)

# Work with database operations
db = DatabaseManager()
try:
    stats = db.inefficient_aggregation_queries()
    print(f"Database stats: {stats}")
finally:
    db.close_all_connections()
```

### Running Tests

Execute the comprehensive test suite with clear steps:

#### 1. **Basic Test Execution**
```bash
# Activate the virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=src --cov-report=html
```

#### 2. **Category-Specific Testing**
```bash
# Run only unit tests
pytest -m unit

# Run application functionality tests
pytest -m performance

# Skip slow-running tests
pytest -m "not slow"

# Run tests for a specific module
pytest tests/test_app.py
pytest tests/test_data_processor.py
pytest tests/test_database.py
```

#### 3. **Advanced Testing Options**
```bash
# Run tests with detailed coverage
pytest --cov=src --cov-report=term-missing --cov-report=html

# Run specific test methods
pytest tests/test_app.py::TestPerformanceProblemApp::test_app_initialization

# Run tests with benchmark reporting
pytest --benchmark-only

# Generate test reports
pytest --html=report.html --self-contained-html
```

#### 4. **Test Verification Steps**
1. **Environment Setup**: Ensure virtual environment is activated
2. **Dependency Check**: Verify all packages are installed (`pip list`)
3. **Module Import**: Test that all modules can be imported
4. **Basic Functionality**: Run core application features
5. **Database Operations**: Test database connectivity and operations
6. **CLI Interface**: Verify command-line interface works
7. **Configuration**: Test configuration loading and validation

## 📊 Application Capabilities

When running this application, you can expect:

- **Comprehensive data processing** with support for multiple file formats and large datasets
- **Robust database operations** with SQLite integration and query optimization
- **Flexible configuration management** supporting JSON configuration files and environment variables
- **Professional CLI interface** with command completion and help documentation
- **Extensive testing framework** with unit tests, integration tests, and coverage reporting
- **Modular architecture** allowing easy extension and customization
- **Type safety** with comprehensive type hints throughout the codebase
- **Documentation** with detailed docstrings and API documentation

## 🔧 Development Tools and Analysis

The application includes comprehensive development and analysis tools:

### Built-in Analysis Features
```bash
# Run application with built-in monitoring
python src/cli.py run --profile --iterations 3

# Enable AWS CodeGuru Profiler for cloud-based analysis
python src/cli.py run --codeguru --size large --iterations 3

# Combine local profiling with CodeGuru
python src/cli.py run --profile --codeguru --output detailed_results.json

# Analyze results from multiple runs  
python src/cli.py analyze --input results.json --format table

# Generate comprehensive reports
python src/cli.py config --show --validate
```

### AWS CodeGuru Profiler Integration
```bash
# Set up CodeGuru Profiler (requires AWS credentials)
# 1. Configure AWS credentials
aws configure

# 2. Create profiling group (one-time setup)
aws codeguruprofiler create-profiling-group --profiling-group-name ecocoder-default-profiling-group

# 3. Run application with CodeGuru enabled
python src/cli.py run --codeguru --size large

# 4. View results in AWS Console
# Navigate to AWS CodeGuru Profiler in your AWS Console
```

### External Development Tools
```bash
# Code profiling for optimization
python -m cProfile -s cumulative -m src.cli run

# Memory usage analysis
python -m memory_profiler src/app.py

# Line-by-line performance analysis
pip install line-profiler
kernprof -l -v src/app.py

# Real-time monitoring during execution
pip install py-spy
python src/cli.py run --size large &
py-spy top --pid $!
```

### Code Quality and Standards
```bash
# Type checking with mypy
mypy src/

# Code formatting with black
black src/ tests/

# Linting with flake8
flake8 src/ tests/

# Run all quality checks together
pytest --cov=src --mypy --flake8
```

## 📈 Application Testing and Benchmarking

The application includes comprehensive testing and benchmarking capabilities:

### CLI Application Testing
```bash
# Quick application test
python src/cli.py run

# Comprehensive benchmarking with multiple iterations
python src/cli.py run --size large --iterations 5 --profile --output benchmark_results.json

# Generate test data and run analysis
python src/cli.py generate-data --file-count 20 --rows-per-file 10000
python src/cli.py run --size large --output results.json
python src/cli.py analyze --input results.json --format table --output analysis.txt
```

### Unit Test Execution
```bash
# Run functional tests
pytest tests/ -m unit

# Run with coverage and detailed reporting
pytest --cov=src -m "unit or integration"

# Benchmark specific application functions
pytest tests/test_app.py::TestPerformanceProblemApp::test_run_performance_test -v
```

### Configuration Testing
```bash
# View current configuration
python src/cli.py config --show

# Validate configuration
python src/cli.py config --validate

# Save configuration to file
python src/cli.py config --save my_config.json --show

# Use custom configuration
python src/cli.py --config my_config.json run --size small
```

## 🤖 For Developers and Code Analysis

This repository is designed for comprehensive code analysis and development learning. Key features include:

1. **Well-documented codebase** with clear comments explaining functionality and design decisions
2. **Realistic implementation** - based on real-world development patterns and practices
3. **Varied functionality** - covering different types of application features and operations
4. **Measurable outcomes** - with clear before/after optimization opportunities
5. **Educational value** - demonstrating both current implementation and potential improvements
6. **Comprehensive testing** - full test suite to verify functionality and catch regressions
7. **Configurable behavior** - flexible configuration system for different usage scenarios
8. **Professional CLI** - easy command-line interface for automated analysis and operation

### Key Features for Analysis

- **Structured codebase** following modern Python package conventions
- **Type hints** throughout for better static analysis and IDE support
- **Comprehensive testing** with unit tests and integration testing
- **Configuration management** for different analysis and operational scenarios
- **CLI interface** for automated testing, benchmarking, and operation
- **Detailed documentation** with clear explanations of functionality and design
- **Profiling integration** for before/after optimization measurement
- **Modular design** allowing for easy analysis of individual components

### Development Patterns Demonstrated

The codebase demonstrates various development patterns and techniques that can be analyzed and potentially improved. Each module includes comprehensive documentation explaining the current implementation approach and design decisions. The package structure allows for easy integration with automated analysis tools and provides clear separation of concerns across different functional areas.

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
