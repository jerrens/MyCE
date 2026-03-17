#!/usr/bin/env python3
# spell-checker:ignore MyCE

from datetime import datetime
import glob
import os
import re
import shutil
import subprocess
import sys

exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "my"))

# Array of command -> expected output pairs
# Use {{TEST_DIR}} in test values for temp directory substitution



# Keys of tests that should be run.  If empty, all tests will be run

# Keys of tests that should be run.  If empty, all tests will be run
focus_run_test = [
    # Enter test key here to only run specific tests.
    # This is useful during development to focus on a specific test or subset of tests without running the entire suite.

]


# Dynamically load all test_cases dicts from files in test_cases directory
def load_all_test_cases(test_cases_dir, only_files=None):
    """
    Load test cases from files in test_cases_dir.
    
    Args:
        test_cases_dir: Path to the test_cases directory
        only_files: List of file patterns (without .py extension) to include.
                   If None, all .py files are loaded.
                   Example: ['basic', 'option_parsing'] or ['option_parsing']
    """
    all_cases = {}

    # Load and merge test_cases from all files in test/test_cases directory
    if os.path.isdir(test_cases_dir):
        py_files = glob.glob(os.path.join(test_cases_dir, '*.py'))
        
        for file in py_files:
            # Extract base filename without .py extension
            base_name = os.path.splitext(os.path.basename(file))[0]
            
            # If only_files is specified, skip files not in the list
            if only_files is not None and base_name not in only_files:
                continue
            
            local_ns = {}
            with open(file, 'r') as f:
                code = f.read()
            exec(code, {}, local_ns)
            if 'test_cases' in local_ns and isinstance(local_ns['test_cases'], dict):
                all_cases.update(local_ns['test_cases'])
            else:
                print(f"Warning: {file} does not define a test_cases dictionary.")
        
    return all_cases

# Substitute {{TEST_DIR}} in test values with the actual temp directory
def substitute_testdir_in_testcases(test_cases, testdir):
    def subst(val):
        if isinstance(val, dict):
            return {k: subst(v) for k, v in val.items()}
        elif isinstance(val, str):
            return val.replace("{{TEST_DIR}}", testdir)
        else:
            return val
    return {k: subst(v) for k, v in test_cases.items()}

if len(focus_run_test) > 0:
    test_cases = {key: test_cases[key] for key in focus_run_test}


def run_tests():
    failed = 0
    orig_cwd = os.getcwd()
    for command, val in test_cases.items():
        try:
            if isinstance(val, dict):
                cmd_prefix = val.get("pre", "")
                cmd_suffix = val.get("cmd", command) # Allow overwritting with the 'cmd' key if present
                env_list = val.get("env", None)
                expected_output = val.get("see", "Missing 'see' property in test")
                description = val.get("description", "")
                pwd = val.get("pwd", orig_cwd)
            else:
                cmd_prefix = ""
                cmd_suffix = command
                env_list = None
                expected_output = val
                description = ""
                pwd = orig_cwd

            # Update any special character references in the expected output (e.g. __exe__)
            expected_output = expected_output.replace("__exe__", exe)

            # Handle section headers
            if command.startswith('#'):
                print(f"\n{expected_output}\n" + "-" * 30)
                continue

            test_cwd = os.path.join(orig_cwd, pwd) if not os.path.isabs(pwd) else pwd
            os.chdir(test_cwd)

            test_cmd = f"{cmd_prefix} {exe} {cmd_suffix}"

            if "-d" in sys.argv or "--debug" in sys.argv:
                print(f">> Executing: {test_cmd}\n\t", end="")

            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                timeout=5,
                shell=True,
                env=env_list,
            )
            actual_output = result.stdout.strip() + result.stderr.strip()

            expected_pattern = re.compile(expected_output, re.DOTALL)

            if expected_pattern.search(actual_output):
                print(f"✓ {command:<60} {description}")
            else:
                print("\033[1;31m", end='')
                print(f"✗ {command:<60} {description}")
                print(f"    Expected: '{expected_output}'")
                print(f"    Got:      '{actual_output}'")
                print(f"    Command   {test_cmd}")
                print("\033[0m", end='')
                failed += 1
        except Exception as e:
            print(f"✗ {command} - Error: {e}")
            failed += 1
        finally:
            os.chdir(orig_cwd)
    return failed

if __name__ == "__main__":
    # Display help message
    if "--help" in sys.argv or "-h" in sys.argv:
        help_text = """
Usage: python test.py [OPTIONS]

Test runner for MyCE script. Executes test cases loaded from test_cases/*.py files.

OPTIONS:
  --help, -h                    Show this help message and exit
  --test-file FILE1,FILE2,...   Load only specific test case files (comma-separated)
                                File names without .py extension
  --debug, -d                   Print debug information during test execution

EXAMPLES:
  # Run all test cases
  python test.py

  # Run only basic test cases
  python test.py --test-file basic

  # Run only option_parsing test cases  
  python test.py --test-file option_parsing

  # Run multiple specific test files
  python test.py --test-file basic,option_parsing

  # Run with debug output
  python test.py --debug

  # Run specific tests with debug
  python test.py --test-file option_parsing --debug
"""
        print(help_text)
        sys.exit(0)
    
    # Parse --test-file flag to only load specific test case files
    only_test_files = None
    if "--test-file" in sys.argv:
        idx = sys.argv.index("--test-file")
        if idx + 1 < len(sys.argv):
            # Split comma-separated file names and remove .py extension if present
            files_arg = sys.argv[idx + 1]
            only_test_files = [f.replace('.py', '') for f in files_arg.split(',')]
            print(f"Loading only test cases from: {', '.join(only_test_files)}")
    
    test_cases_dir = os.path.join(os.path.dirname(__file__), 'test_cases')
    test_cases = load_all_test_cases(test_cases_dir, only_files=only_test_files)

    # Print the number of test cases loaded for verification
    print(f"Number of test cases: {len(test_cases)}")
    # print("Test case keys:")
    # [print(f"  {key}") for key in test_cases.keys()]
    # sys.exit(0)

    # Create a temp test directory in /tmp
    import tempfile
    test_dir = os.path.join(tempfile.gettempdir(), f"myce_test_{os.getpid()}")
    os.makedirs(test_dir, exist_ok=True)
    print(f"Created test directory: {test_dir}")


    # Copy all contents of ./test/blueprint (including subfolders/files) to the temp test directory
    import pathlib
    blueprint_dir = os.path.join(os.path.dirname(__file__), "blueprint")
    if os.path.exists(blueprint_dir):
        for root, dirs, files in os.walk(blueprint_dir):
            rel_root = os.path.relpath(root, blueprint_dir)
            dest_root = os.path.join(test_dir, rel_root) if rel_root != "." else test_dir
            os.makedirs(dest_root, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest_root, file)
                shutil.copy2(src_file, dst_file)
    else:
        print(f"Warning: blueprint directory '{blueprint_dir}' does not exist.")


    # Substitute {{TEST_DIR}} in test values
    test_cases = substitute_testdir_in_testcases(test_cases, test_dir)

    # Set CWD to the test directory for the duration of the test
    orig_cwd = os.getcwd()
    os.chdir(test_dir)
    print("Starting tests...\n")

    # Run the tests
    try:
        failed = run_tests()
    except Exception as e:
        print(f"Error running tests: {e}")
        failed = 1

    # Cleanup: remove the test directory and restore CWD
    os.chdir(orig_cwd)
    try:
        shutil.rmtree(test_dir)
        print(f"Cleaned up test directory: {test_dir}")
    except Exception as e:
        print(f"Warning: Failed to clean up test directory: {e}")

    sys.exit(failed)
