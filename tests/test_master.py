"""
Master Test Runner for Enhanced AI Design Engineer System
========================================================

This script runs all tests and provides comprehensive validation
of the enhanced Voice-to-CAD system capabilities.
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
import importlib.util

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def setup_logging():
    """Setup comprehensive logging for test session"""
    log_dir = os.path.join(project_root, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'test_master_{timestamp}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__), log_file

def run_single_test(test_file, logger):
    """Run a single test file and capture results"""
    test_name = os.path.basename(test_file).replace('.py', '')
    logger.info(f"Running test: {test_name}")
    
    try:
        # Run the test file
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logger.info(f"✅ {test_name} PASSED")
            return True, result.stdout
        else:
            logger.error(f"❌ {test_name} FAILED")
            logger.error(f"Error output: {result.stderr}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        logger.error(f"⏱️ {test_name} TIMEOUT")
        return False, "Test timed out after 5 minutes"
    except Exception as e:
        logger.error(f"💥 {test_name} ERROR: {str(e)}")
        return False, str(e)

def discover_test_files():
    """Discover all test files in the tests directory"""
    test_dir = os.path.dirname(__file__)
    test_files = []
    
    for file in os.listdir(test_dir):
        if file.startswith('test_') and file.endswith('.py') and file != 'test_master.py':
            test_files.append(os.path.join(test_dir, file))
    
    return sorted(test_files)

def check_prerequisites(logger):
    """Check if all prerequisites are met for testing"""
    logger.info("Checking prerequisites...")
    
    checks = []
    
    # Check if main.py exists
    main_file = os.path.join(project_root, 'main.py')
    checks.append(("Main application file", os.path.exists(main_file)))
    
    # Check if config exists
    config_dir = os.path.join(project_root, 'config')
    checks.append(("Config directory", os.path.exists(config_dir)))
    
    # Check if services directory exists (for AI service)
    services_dir = os.path.join(project_root, 'services')
    checks.append(("Services directory", os.path.exists(services_dir)))
    
    # Check if requirements.txt exists
    req_file = os.path.join(project_root, 'requirements.txt')
    checks.append(("Requirements file", os.path.exists(req_file)))
    
    all_good = True
    for check_name, check_result in checks:
        if check_result:
            logger.info(f"✅ {check_name}")
        else:
            logger.warning(f"❌ {check_name}")
            all_good = False
    
    return all_good

def run_comprehensive_test_suite():
    """Run the complete test suite with detailed reporting"""
    logger, log_file = setup_logging()
    
    print("🚀 ENHANCED AI DESIGN ENGINEER - MASTER TEST RUNNER")
    print("=" * 60)
    print(f"📅 Test Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 Log File: {log_file}")
    print("=" * 60)
    
    logger.info("Starting comprehensive test suite for Enhanced AI Design Engineer")
    
    # Check prerequisites
    if not check_prerequisites(logger):
        logger.warning("Some prerequisites are missing. Tests may fail.")
        print("⚠️  Some prerequisites are missing. Continue anyway? (y/n): ", end="")
        if input().lower() != 'y':
            return
    
    # Discover test files
    test_files = discover_test_files()
    logger.info(f"Discovered {len(test_files)} test files")
    
    print(f"\n📊 Found {len(test_files)} test files:")
    for i, test_file in enumerate(test_files, 1):
        test_name = os.path.basename(test_file)
        print(f"  {i:2d}. {test_name}")
    
    print("\n🎯 TEST EXECUTION OPTIONS:")
    print("1. Run all tests automatically")
    print("2. Run tests interactively (confirm each)")
    print("3. Run specific test only")
    print("4. Run guided manual testing")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    results = []
    
    if choice == "1":
        # Run all tests automatically
        logger.info("Running all tests automatically")
        for test_file in test_files:
            success, output = run_single_test(test_file, logger)
            results.append((os.path.basename(test_file), success, output))
    
    elif choice == "2":
        # Run tests interactively
        logger.info("Running tests interactively")
        for test_file in test_files:
            test_name = os.path.basename(test_file)
            run_test = input(f"\nRun {test_name}? (y/n/q): ").lower()
            
            if run_test == 'q':
                break
            elif run_test == 'y':
                success, output = run_single_test(test_file, logger)
                results.append((test_name, success, output))
            else:
                logger.info(f"Skipped: {test_name}")
                results.append((test_name, None, "Skipped by user"))
    
    elif choice == "3":
        # Run specific test
        print("\nAvailable tests:")
        for i, test_file in enumerate(test_files, 1):
            print(f"  {i}. {os.path.basename(test_file)}")
        
        try:
            test_idx = int(input("\nEnter test number: ")) - 1
            if 0 <= test_idx < len(test_files):
                test_file = test_files[test_idx]
                success, output = run_single_test(test_file, logger)
                results.append((os.path.basename(test_file), success, output))
            else:
                print("Invalid test number")
                return
        except ValueError:
            print("Invalid input")
            return
    
    elif choice == "4":
        # Run guided manual testing
        print("\n🎯 Starting guided manual testing session...")
        try:
            from testing_guide import run_manual_test_session
            run_manual_test_session()
        except ImportError:
            logger.error("Could not import testing_guide module")
            print("❌ Guided testing not available")
        return
    
    else:
        print("Invalid choice")
        return
    
    # Generate test report
    generate_test_report(results, logger, log_file)

def generate_test_report(results, logger, log_file):
    """Generate comprehensive test report"""
    print("\n" + "=" * 60)
    print("📊 TEST EXECUTION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success is True)
    failed = sum(1 for _, success, _ in results if success is False)
    skipped = sum(1 for _, success, _ in results if success is None)
    total = len(results)
    
    print(f"📈 OVERALL RESULTS:")
    print(f"   Total Tests: {total}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️ Skipped: {skipped}")
    
    if total > 0:
        success_rate = (passed / total) * 100
        print(f"   📊 Success Rate: {success_rate:.1f}%")
    
    print(f"\n📋 DETAILED RESULTS:")
    for test_name, success, output in results:
        if success is True:
            status = "✅ PASS"
        elif success is False:
            status = "❌ FAIL"
        else:
            status = "⏭️ SKIP"
        
        print(f"   {status} - {test_name}")
        
        if success is False and output:
            # Show first few lines of error
            error_lines = output.split('\n')[:3]
            for line in error_lines:
                if line.strip():
                    print(f"     └─ {line.strip()}")
    
    print(f"\n📁 Detailed logs saved to: {log_file}")
    print("=" * 60)
    
    logger.info(f"Test suite completed. {passed}/{total} tests passed")
    
    # Provide recommendations
    if failed > 0:
        print("\n💡 RECOMMENDATIONS:")
        print("   - Check failed test logs for specific issues")
        print("   - Ensure all dependencies are installed")
        print("   - Verify Streamlit app is running (for integration tests)")
        print("   - Run individual tests for detailed debugging")

def main():
    """Main entry point"""
    try:
        run_comprehensive_test_suite()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test execution interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()