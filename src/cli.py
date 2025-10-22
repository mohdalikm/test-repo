#!/usr/bin/env python3
"""
Command-line interface for the Performance Issues application.

Provides various commands to run performance tests, analyze results,
and manage the application configuration.
"""

import click
import json
import os
import time
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add src to path for imports
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

try:
    from app import PerformanceProblemApp
    from config import get_config_manager, initialize_config
    from data_processor import DataProcessor
    from database import DatabaseManager
except ImportError as e:
    click.echo(f"Error importing modules: {e}", err=True)
    click.echo("Make sure you have installed the package with: pip install -e .", err=True)
    sys.exit(1)

# AWS CodeGuru Profiler
try:
    from codeguru_profiler_agent import Profiler
    CODEGURU_AVAILABLE = True
except ImportError:
    CODEGURU_AVAILABLE = False


@click.group()
@click.option('--config', '-c', type=click.Path(exists=True), 
              help='Configuration file path')
@click.option('--debug/--no-debug', default=False, 
              help='Enable debug mode')
@click.option('--verbose', '-v', is_flag=True, 
              help='Verbose output')
@click.pass_context
def main(ctx: click.Context, config: Optional[str], debug: bool, verbose: bool):
    """
    Performance Issues CLI - A tool for analyzing performance problems in Python code.
    
    
    """
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    ctx.obj['verbose'] = verbose
    
    # Initialize configuration
    if config:
        config_manager = initialize_config(config)
    else:
        config_manager = get_config_manager()
    
    ctx.obj['config_manager'] = config_manager
    
    if debug:
        config_manager.update_config(debug=True, log_level='DEBUG')
        click.echo("Debug mode enabled")
    
    if verbose:
        click.echo("Performance Issues CLI initialized")


@main.command()
@click.option('--size', '-s', type=click.Choice(['small', 'medium', 'large']), 
              default='medium', help='Dataset size for testing')
@click.option('--iterations', '-i', type=int, default=1, 
              help='Number of test iterations')
@click.option('--output', '-o', type=click.Path(), 
              help='Output file for results')
@click.option('--profile/--no-profile', default=False,
              help='Enable performance profiling')
@click.option('--codeguru/--no-codeguru', default=False,
              help='Enable AWS CodeGuru Profiler')
@click.option('--profiling-group', default='ecocoder-default-profiling-group',
              help='CodeGuru profiling group name')
@click.pass_context
def run(ctx: click.Context, size: str, iterations: int, output: Optional[str], 
        profile: bool, codeguru: bool, profiling_group: str):
    """Run the performance test suite with intentional issues."""
    click.echo("Starting performance test suite...")
    
    config = ctx.obj['config_manager'].get_config()
    
    # Determine dataset size
    size_map = {
        'small': config.performance_test.small_dataset_size,
        'medium': config.performance_test.medium_dataset_size, 
        'large': config.performance_test.large_dataset_size
    }
    
    dataset_size = size_map[size]
    click.echo(f"Using {size} dataset size: {dataset_size} items")
    
    # Initialize CodeGuru Profiler if requested
    codeguru_profiler = None
    if codeguru and CODEGURU_AVAILABLE:
        try:
            codeguru_profiler = Profiler(profiling_group_name=profiling_group)
            codeguru_profiler.start()
            click.echo(f"✅ CodeGuru Profiler started with group: {profiling_group}")
        except Exception as e:
            click.echo(f"⚠️  Warning: Failed to start CodeGuru Profiler: {e}", err=True)
            codeguru_profiler = None
    elif codeguru and not CODEGURU_AVAILABLE:
        click.echo("⚠️  Warning: CodeGuru Profiler not available. Install with: pip install codeguru_profiler_agent", err=True)
    
    all_results = []
    
    for iteration in range(iterations):
        click.echo(f"\nIteration {iteration + 1}/{iterations}")
        
        with PerformanceProblemApp() as app:
            if profile:
                import cProfile
                import pstats
                
                profiler = cProfile.Profile()
                profiler.enable()
                
            # Run performance tests
            start_time = time.time()
            test_times = app.run_performance_test()
            total_time = time.time() - start_time
            
            if profile:
                profiler.disable()
                
                # Save profiling results
                profile_file = f"profile_iteration_{iteration + 1}.prof"
                profiler.dump_stats(profile_file)
                
                # Print top functions
                stats = pstats.Stats(profiler)
                click.echo("\nTop 10 functions by cumulative time:")
                stats.sort_stats('cumulative').print_stats(10)
            
            test_times['total_wall_time'] = total_time
            test_times['iteration'] = iteration + 1
            test_times['dataset_size'] = dataset_size
            
            all_results.append(test_times)
            
            # Display results for this iteration
            click.echo(f"Total execution time: {total_time:.2f} seconds")
            for test_name, test_time in test_times.items():
                if test_name not in ['total_wall_time', 'iteration', 'dataset_size']:
                    click.echo(f"  {test_name}: {test_time:.3f}s")
    
    # Calculate summary statistics
    if iterations > 1:
        click.echo(f"\n=== Summary Statistics ({iterations} iterations) ===")
        avg_total = sum(r['total_wall_time'] for r in all_results) / iterations
        min_total = min(r['total_wall_time'] for r in all_results)
        max_total = max(r['total_wall_time'] for r in all_results)
        
        click.echo(f"Average total time: {avg_total:.2f}s")
        click.echo(f"Min total time: {min_total:.2f}s") 
        click.echo(f"Max total time: {max_total:.2f}s")
    
    # Save results if output specified
    if output:
        with open(output, 'w') as f:
            json.dump(all_results, f, indent=2)
        click.echo(f"\nResults saved to {output}")
    
    # Stop CodeGuru Profiler if it was started
    if codeguru_profiler:
        try:
            codeguru_profiler.stop()
            click.echo("✅ CodeGuru Profiler stopped")
        except Exception as e:
            click.echo(f"⚠️  Warning: Error stopping CodeGuru Profiler: {e}", err=True)
    
    click.echo("\nPerformance test completed!")


@main.command()
@click.option('--input', '-i', type=click.Path(exists=True), required=True,
              help='Input JSON file with test results')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'csv']), 
              default='table', help='Output format')
@click.option('--output', '-o', type=click.Path(),
              help='Output file (stdout if not specified)')
def analyze(input: str, format: str, output: Optional[str]):
    """Analyze performance test results from a JSON file."""
    click.echo(f"Analyzing results from {input}...")
    
    try:
        with open(input, 'r') as f:
            results = json.load(f)
    except Exception as e:
        click.echo(f"Error reading results file: {e}", err=True)
        return
    
    if not results:
        click.echo("No results found in input file", err=True)
        return
    
    # Prepare analysis
    analysis = analyze_results(results)
    
    # Format output
    if format == 'table':
        output_text = format_table(analysis)
    elif format == 'json':
        output_text = json.dumps(analysis, indent=2)
    elif format == 'csv':
        output_text = format_csv(analysis)
    
    # Write output
    if output:
        with open(output, 'w') as f:
            f.write(output_text)
        click.echo(f"Analysis saved to {output}")
    else:
        click.echo(output_text)


@main.command()
@click.option('--output-dir', '-o', type=click.Path(), default='sample_data',
              help='Output directory for sample data')
@click.option('--file-count', type=int, default=5, 
              help='Number of files to create')
@click.option('--rows-per-file', type=int, default=10000,
              help='Number of rows per CSV file')
def generate_data(output_dir: str, file_count: int, rows_per_file: int):
    """Generate sample data files for testing."""
    click.echo(f"Generating {file_count} sample data files in {output_dir}...")
    
    processor = DataProcessor()
    
    try:
        processor.create_sample_data_files(
            output_dir=output_dir,
            file_count=file_count,
            rows_per_file=rows_per_file
        )
        click.echo(f"Sample data generated successfully in {output_dir}")
    except Exception as e:
        click.echo(f"Error generating sample data: {e}", err=True)


@main.command()
@click.option('--show/--no-show', default=False, help='Show current configuration')
@click.option('--save', type=click.Path(), help='Save configuration to file')
@click.option('--validate/--no-validate', default=False, help='Validate configuration')
@click.option('--reset/--no-reset', default=False, help='Reset to default configuration')
@click.pass_context
def config(ctx: click.Context, show: bool, save: Optional[str], validate: bool, reset: bool):
    """Manage application configuration."""
    config_manager = ctx.obj['config_manager']
    
    if reset:
        config_manager.reset_to_defaults()
        click.echo("Configuration reset to defaults")
    
    if validate:
        is_valid = config_manager.validate_config()
        if is_valid:
            click.echo("✅ Configuration is valid")
        else:
            click.echo("❌ Configuration validation failed", err=True)
            return
    
    if show:
        config_manager.print_config()
    
    if save:
        config_manager.save_config(save)


@main.command()
@click.option('--db-path', type=click.Path(), help='Database file path')
@click.option('--show-info/--no-show-info', default=True, help='Show database info')
@click.option('--test-queries/--no-test-queries', default=False, help='Test database queries')
def database(db_path: Optional[str], show_info: bool, test_queries: bool):
    """Manage and test database operations."""
    if db_path:
        db_manager = DatabaseManager(db_path)
    else:
        db_manager = DatabaseManager()
    
    try:
        if show_info:
            click.echo("Database Information:")
            info = db_manager.get_database_info()
            for key, value in info.items():
                click.echo(f"  {key}: {value}")
        
        if test_queries:
            click.echo("\nTesting database queries...")
            
            # Test N+1 queries
            click.echo("Testing N+1 query performance...")
            start_time = time.time()
            users = db_manager.get_users_with_posts_n_plus_1([1, 2, 3, 4, 5])
            n_plus_1_time = time.time() - start_time
            click.echo(f"  N+1 queries time: {n_plus_1_time:.3f}s for {len(users)} users")
            
            # Test search queries
            click.echo("Testing search queries...")
            start_time = time.time()
            search_results = db_manager.inefficient_search_queries("user")
            search_time = time.time() - start_time
            click.echo(f"  Search time: {search_time:.3f}s for {len(search_results)} results")
            
            # Test aggregation
            click.echo("Testing aggregation queries...")
            start_time = time.time()
            stats = db_manager.inefficient_aggregation_queries()
            agg_time = time.time() - start_time
            click.echo(f"  Aggregation time: {agg_time:.3f}s")
            
    finally:
        db_manager.close_all_connections()


@main.command()
@click.option('--test-type', type=click.Choice(['math', 'file', 'network', 'string']),
              help='Specific utility test to run')
@click.option('--iterations', type=int, default=1, help='Number of iterations')
def utils(test_type: Optional[str], iterations: int):
    """Test utility functions with performance issues."""
    from utils import (
        MathUtils, FileUtils, NetworkUtils, StringUtils, 
        create_sample_files_for_testing
    )
    
    click.echo(f"Testing utility functions ({iterations} iterations)...")
    
    for iteration in range(iterations):
        if iterations > 1:
            click.echo(f"\nIteration {iteration + 1}/{iterations}")
        
        if not test_type or test_type == 'math':
            click.echo("Testing math utilities...")
            math_utils = MathUtils()
            
            start_time = time.time()
            for i in range(15, 20):  # Small range to avoid excessive time
                result = math_utils.expensive_calculation(i)
            math_time = time.time() - start_time
            click.echo(f"  Math calculations time: {math_time:.3f}s")
            
            start_time = time.time()
            primes = math_utils.find_primes_inefficiently(100)
            prime_time = time.time() - start_time
            click.echo(f"  Prime finding time: {prime_time:.3f}s ({len(primes)} primes)")
        
        if not test_type or test_type == 'file':
            click.echo("Testing file utilities...")
            file_utils = FileUtils()
            
            # Create sample files
            create_sample_files_for_testing()
            
            start_time = time.time()
            sample_files = [f"sample_files/test_file_{i}.txt" for i in range(3)]
            results = file_utils.batch_file_operations(sample_files)
            file_time = time.time() - start_time
            click.echo(f"  File processing time: {file_time:.3f}s ({len(results)} files)")
        
        if not test_type or test_type == 'string':
            click.echo("Testing string utilities...")
            
            test_strings = [f"  TEST STRING {i}  " for i in range(100)] * 3
            start_time = time.time()
            processed = StringUtils.inefficient_string_processing(test_strings)
            string_time = time.time() - start_time
            click.echo(f"  String processing time: {string_time:.3f}s ({len(processed)} unique)")


def analyze_results(results: list) -> Dict[str, Any]:
    """Analyze performance test results."""
    if not results:
        return {}
    
    # Calculate statistics for each test
    test_names = set()
    for result in results:
        test_names.update(k for k in result.keys() 
                         if k not in ['total_wall_time', 'iteration', 'dataset_size'])
    
    analysis = {
        'summary': {
            'total_iterations': len(results),
            'dataset_size': results[0].get('dataset_size', 'unknown'),
        },
        'test_statistics': {}
    }
    
    for test_name in test_names:
        values = [r.get(test_name, 0) for r in results if test_name in r]
        if values:
            analysis['test_statistics'][test_name] = {
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values),
                'total': sum(values)
            }
    
    return analysis


def format_table(analysis: Dict[str, Any]) -> str:
    """Format analysis results as a table."""
    lines = []
    lines.append("=== Performance Analysis Results ===")
    lines.append(f"Iterations: {analysis['summary']['total_iterations']}")
    lines.append(f"Dataset Size: {analysis['summary']['dataset_size']}")
    lines.append("")
    lines.append("Test Statistics:")
    lines.append(f"{'Test Name':<25} {'Min':<8} {'Max':<8} {'Avg':<8} {'Total':<8}")
    lines.append("-" * 65)
    
    for test_name, stats in analysis['test_statistics'].items():
        lines.append(f"{test_name:<25} {stats['min']:<8.3f} {stats['max']:<8.3f} "
                    f"{stats['avg']:<8.3f} {stats['total']:<8.3f}")
    
    return "\n".join(lines)


def format_csv(analysis: Dict[str, Any]) -> str:
    """Format analysis results as CSV."""
    lines = []
    lines.append("test_name,min_time,max_time,avg_time,total_time")
    
    for test_name, stats in analysis['test_statistics'].items():
        lines.append(f"{test_name},{stats['min']},{stats['max']},"
                    f"{stats['avg']},{stats['total']}")
    
    return "\n".join(lines)


# Convenience commands
@main.command()
@click.pass_context
def run_performance_test(ctx: click.Context):
    """Quick command to run performance test (alias for 'run')."""
    ctx.invoke(run)


@main.command()
@click.option('--input', '-i', type=click.Path(exists=True), required=True)
@click.pass_context
def analyze_performance(ctx: click.Context, input: str):
    """Quick command to analyze performance (alias for 'analyze')."""
    ctx.invoke(analyze, input=input)


if __name__ == "__main__":
    main()