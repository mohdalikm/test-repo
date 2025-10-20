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

```
├── main.py                    # Main application with various performance issues
├── data_processor.py          # Data processing with pandas inefficiencies and memory leaks
├── database.py               # Database operations with N+1 queries and missing indexes
├── utils.py                  # Utility functions with algorithmic and caching issues
├── generate_test_data.py     # Script to create sample data for testing
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🐛 Performance Issues Included

### 1. **main.py** - Core Application Issues
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

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd test-repo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate test data:
```bash
python generate_test_data.py
```

### Running the Application

Run the main application to see all performance issues in action:
```bash
python main.py
```

**Warning**: The application will be slow due to intentional performance issues!

### Individual Module Testing

Test specific modules:
```bash
# Test data processing issues
python -c "from data_processor import DataProcessor; dp = DataProcessor(); dp.create_sample_data_files('test_data')"

# Test database issues
python -c "from database import DatabaseManager; db = DatabaseManager(); print(db.inefficient_aggregation_queries())"

# Test utility issues
python utils.py
```

## 📊 Expected Performance Problems

When running this application, you should observe:

- **High CPU usage** due to inefficient algorithms
- **High memory consumption** from memory leaks and poor data handling
- **Slow execution times** from O(n²) algorithms and redundant calculations
- **Excessive database queries** from N+1 query patterns
- **Blocking I/O operations** that could be parallelized
- **Poor cache hit rates** due to inefficient caching strategies

## 🔧 Tools for Performance Analysis

The following tools can help identify the performance issues:

### Profiling Tools
```bash
# CPU profiling with cProfile
python -m cProfile -s cumulative main.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler main.py

# Line-by-line profiling
pip install line-profiler
kernprof -l -v main.py
```

### Monitoring Tools
```bash
# Real-time performance monitoring
pip install py-spy
py-spy top --pid <process-id>

# Database query analysis (for SQLite)
# Enable query logging and analyze slow queries
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

## 📈 Performance Testing

The repository includes benchmarking capabilities:

```bash
# Run performance tests
python -m pytest tests/ --benchmark-only

# Generate performance reports
python -c "from main import PerformanceProblemApp; app = PerformanceProblemApp(); app.run_performance_test()"
```

## 🤖 For AI Agents

This repository is specifically designed for AI code analysis tools. The performance issues are:

1. **Well-documented** with clear comments explaining what's wrong
2. **Realistic** - based on real-world performance anti-patterns
3. **Varied** - covering different types of performance problems
4. **Measurable** - with clear before/after optimization opportunities
5. **Educational** - demonstrating both the problem and better alternatives

Each performance issue includes comments starting with "PERFORMANCE ISSUE" and "BAD:" to help identify problematic code patterns.

## 📝 License

This project is created for educational and testing purposes. Feel free to use it for training AI models, testing code analysis tools, or learning about performance optimization.

---

**Note**: This application is intentionally inefficient. Do not use these patterns in production code!