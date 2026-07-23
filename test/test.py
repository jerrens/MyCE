#!/usr/bin/env python3
# spell-checker:ignore MyCE

from datetime import datetime
import glob
import os
import re
import shutil
import shlex
import subprocess
import sys

exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "my"))

# Container execution settings
DEFAULT_CONTAINER_IMAGE = "docker.io/ohmyzsh/zsh:latest"
CONTAINER_WORKDIR = "/mnt/host"
CONTAINER_SHELL = "zsh"

# Array of command -> expected output pairs
# Use {{TEST_DIR}} in test values for temp directory substitution



# Keys of tests that should be run.  If empty, all tests will be run

# Keys of tests that should be run.  If empty, all tests will be run
focus_run_test = [
    # Enter test key here to only run specific tests.
    # This is useful during development to focus on a specific test or subset of tests without running the entire suite.

]


def parse_container_args(argv):
    """Parse --container/-c with optional image value.

    Returns:
        Tuple: (use_container: bool, container_image: str|None, remaining_args: list[str])
    """
    use_container = False
    container_image = None
    remaining_args = []
    i = 0

    while i < len(argv):
        arg = argv[i]

        if arg == "--container" or arg == "-c":
            use_container = True
            if i + 1 < len(argv) and not argv[i + 1].startswith("-"):
                container_image = argv[i + 1]
                i += 1
        elif arg.startswith("--container="):
            use_container = True
            container_image = arg.split("=", 1)[1].strip() or None
        elif arg.startswith("-c="):
            use_container = True
            container_image = arg.split("=", 1)[1].strip() or None
        else:
            remaining_args.append(arg)

        i += 1

    return use_container, container_image, remaining_args


def detect_container_engine():
    """Return preferred container engine: podman, docker, or None."""
    if shutil.which("podman"):
        return "podman"
    if shutil.which("docker"):
        return "docker"
    return None


def run_test_runner_in_container(container_image, forwarded_args):
    """Run this test runner inside a zsh container and return its exit code."""
    engine = detect_container_engine()
    if not engine:
        print("Error: Neither 'podman' nor 'docker' is installed. Install podman (preferred) or docker.")
        return 1

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    image = container_image or DEFAULT_CONTAINER_IMAGE

    inner_args = " ".join(shlex.quote(arg) for arg in forwarded_args)
    inner_command = (
        "if ! command -v python3 >/dev/null 2>&1; then "
        "echo 'python3 not found in container. Attempting install...' >&2; "
        "if command -v apt-get >/dev/null 2>&1; then "
        "apt-get update && apt-get install -y python3; "
        "elif command -v apk >/dev/null 2>&1; then "
        "apk add --no-cache python3; "
        "elif command -v dnf >/dev/null 2>&1; then "
        "dnf install -y python3; "
        "elif command -v yum >/dev/null 2>&1; then "
        "yum install -y python3; "
        "elif command -v microdnf >/dev/null 2>&1; then "
        "microdnf install -y python3; "
        "else "
        "echo 'Error: No supported package manager found to install python3.' >&2; "
        "exit 127; "
        "fi; "
        "fi; "
        "if ! command -v python3 >/dev/null 2>&1; then "
        f"echo 'Error: python3 is not installed in container image: {image}' >&2; "
        "exit 127; "
        "fi; "
        f"cd {CONTAINER_WORKDIR}/test && python3 test.py {inner_args}"
    )

    cmd = [
        engine,
        "run",
        "-i",
        "--rm",
        "-e",
        "ZSH_DISABLE_COMPFIX=true",
        "--volume",
        f"{repo_root}:{CONTAINER_WORKDIR}",
        "--volume",
        f"{repo_root}/my:/usr/local/bin/my",
        "--volume",
        f"{os.path.expanduser('~/.myCommands')}:/root/.myCommands",
        "--volume",
        f"{repo_root}/auto-complete/_my.zsh:/root/.oh-my-zsh/custom/functions/_my",
        "--workdir",
        CONTAINER_WORKDIR,
        image,
        CONTAINER_SHELL,
        "-c",
        inner_command,
    ]

    if "-d" in forwarded_args or "--debug" in forwarded_args:
        printable = " ".join(shlex.quote(part) for part in cmd)
        print(f"Container mode enabled ({engine}) using image: {image}")
        print(f">> Executing in container: {printable}")
    else:
        print(f"Container mode enabled ({engine}) using image: {image}")

    result = subprocess.run(cmd)
    return result.returncode


# Dynamically load all test_cases dicts from files in test_cases directory
def load_all_test_cases(test_cases_dir, only_files=None):
    """
    Load test cases from files in test_cases_dir.

    Args:
        test_cases_dir: Path to the test_cases directory
        only_files: List of file patterns (without .py extension) to include.
                   If None, all .py files are loaded.
                   Example: ['basic', 'option_parsing'] or ['option_parsing']

    Returns:
        Tuple of (all_cases dict, source_file dict mapping test key to filename)
    """
    all_cases = {}
    source_files = {}

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
                for key in local_ns['test_cases']:
                    source_files[key] = base_name
                all_cases.update(local_ns['test_cases'])
            else:
                print(f"Warning: {file} does not define a test_cases dictionary.")

    return all_cases, source_files

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


def run_tests(test_dir):
    failed = 0
    orig_cwd = os.getcwd()
    for command, val in test_cases.items():
        try:
            if isinstance(val, dict):
                cmd_prefix = val.get("pre", "")
                cmd_suffix = val.get("cmd", command) # Allow overwritting with the 'cmd' key if present
                raw_cmd = val.get("raw_cmd", None) # Optional full command override (bypasses __exe__ injection)
                env_list = val.get("env", None)
                expected_output = val.get("see", "Missing 'see' property in test")
                description = val.get("description", "")
                pwd = val.get("pwd", test_dir)  # Default to test_dir instead of orig_cwd
            else:
                cmd_prefix = ""
                cmd_suffix = command
                raw_cmd = None
                env_list = None
                expected_output = val
                description = ""
                pwd = test_dir  # Default to test_dir

            # Update any special character references in the expected output (e.g. __exe__)
            expected_output = expected_output.replace("__exe__", exe)

            # Handle section headers
            if command.startswith('#'):
                print(f"\n{expected_output}\n" + "-" * 30)
                continue

            test_cwd = os.path.join(orig_cwd, pwd) if not os.path.isabs(pwd) else pwd
            # Don't change directory, use cwd in subprocess.run

            if raw_cmd is not None:
                test_cmd = raw_cmd
            else:
                test_cmd = f"{cmd_prefix} {exe} {cmd_suffix}"

            # Allow test commands to reference the executable path via __exe__ token.
            test_cmd = test_cmd.replace("__exe__", exe)

            if "-d" in sys.argv or "--debug" in sys.argv:
                print(f">> Executing: {test_cmd}\n\t", end="")

            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                timeout=5,
                shell=True,
                env=env_list,
                cwd=test_cwd,  # Run in test_cwd
            )
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            actual_output = (stdout + ("\n" if stdout and stderr else "") + stderr).strip()
            alternate_output = (stderr + ("\n" if stderr and stdout else "") + stdout).strip()

            expected_pattern = re.compile(expected_output, re.DOTALL)

            if expected_pattern.search(actual_output) or expected_pattern.search(alternate_output):
                print(f"✓ {command:<60} {description}")
            else:
                print("\033[1;31m", end='')
                print(f"✗ {command:<60} {description}")
                print(f"    Expected: '{expected_output}'")
                print(f"    Got:      '{actual_output}'")
                print(f"    Alternate: '{alternate_output}'")
                print(f"    Command   {test_cmd}")
                print("\033[0m", end='')
                failed += 1
        except Exception as e:
            print(f"✗ {command} - Error: {e}")
            failed += 1
        # No need to change directory back since we don't change it

    return failed

if __name__ == "__main__":
    use_container, container_image, parsed_args = parse_container_args(sys.argv[1:])

    # Display help message
    if "--help" in parsed_args or "-h" in parsed_args:
        help_text = """
Usage: python test.py [OPTIONS]

Test runner for MyCE script. Executes test cases loaded from test_cases/*.py files.

OPTIONS:
  --help, -h                    Show this help message and exit
  --container, -c [IMAGE]       Run tests inside a zsh container
                                Optional IMAGE default: docker.io/ohmyzsh/zsh:latest
  --test-file FILE1,FILE2,...   Load only specific test case files (comma-separated)
                                File names without .py extension
  --filter REGEX, -f REGEX      Run only tests whose names match the given regex pattern
                                 Example: -f "^list" to run tests starting with "list"
  --dryrun, -n                  List tests that would be run without executing them
  --debug, -d                   Print debug information during test execution

EXAMPLES:
  # Run all test cases
  python test.py

  # Run all test cases in the default zsh container
  python test.py --container

  # Run in a specific container image
  python test.py --container docker.io/ohmyzsh/zsh:5.9
  python test.py --container=docker.io/ohmyzsh/zsh:5.9

  # Run only basic test cases
  python test.py --test-file basic

  # Run only option_parsing test cases
  python test.py --test-file option_parsing

  # Run multiple specific test files
  python test.py --test-file basic,option_parsing

  # Run tests with names matching a regex pattern
  python test.py -f "echo"
  python test.py --filter "^list"

  # Run with debug output
  python test.py --debug

  # Run in container with debug output
  python test.py --container --debug

  # Specific tests in container with debug
  python test.py --test-file option_parsing --debug

  # Dry run: list tests without executing
  python test.py --dryrun
  python test.py -n
  python test.py -n -f "^list"
"""
        print(help_text)
        sys.exit(0)

    # If container mode is requested, run the full test runner inside the container.
    if use_container:
        sys.exit(run_test_runner_in_container(container_image, parsed_args))

    # Parse --test-file flag to only load specific test case files
    only_test_files = None
    test_filter = None
    dryrun = False

    # Check for dryrun first - list tests and exit early
    for flag in ("-n", "--dryrun"):
        if flag in parsed_args:
            dryrun = True
            break

    if "--test-file" in parsed_args:
        idx = parsed_args.index("--test-file")
        if idx + 1 < len(parsed_args):
            # Split comma-separated file names and remove .py extension if present
            files_arg = parsed_args[idx + 1]
            only_test_files = [f.replace('.py', '') for f in files_arg.split(',')]
            print(f"Loading only test cases from: {', '.join(only_test_files)}")

    # Parse -f/--filter flag to filter test cases by regex
    for flag in ("-f", "--filter"):
        if flag in parsed_args:
            idx = parsed_args.index(flag)
            if idx + 1 < len(parsed_args):
                test_filter = parsed_args[idx + 1]
                print(f"Filtering tests by regex: {test_filter}")
            break

    test_cases_dir = os.path.join(os.path.dirname(__file__), 'test_cases')
    test_cases, source_files = load_all_test_cases(test_cases_dir, only_files=only_test_files)

    # Apply regex filter to test case names if specified
    if test_filter:
        try:
            filter_pattern = re.compile(test_filter)
            test_cases = {k: v for k, v in test_cases.items() if filter_pattern.search(k)}
            print(f"After filter, running {len(test_cases)} test cases")
        except re.error as e:
            print(f"Error: Invalid regex pattern '{test_filter}': {e}")
            sys.exit(1)

    # Print the number of test cases loaded for verification
    print(f"Number of test cases: {len(test_cases)}")

    # Dryrun mode: just list tests without running
    if dryrun:
        # Calculate column widths for alignment
        max_key_len = max(len(k) for k in test_cases.keys()) if test_cases else 0
        max_src_len = max(len(v) for v in source_files.values()) if source_files else 0
        
        print("\n=== Tests that would be run ===\n")
        print(f"{'Test Name':<{max_key_len}}    {'Group':<{max_src_len}}    Description")
        print("-" * (max_key_len + max_src_len + 50))
        for key, val in test_cases.items():
            src_file = source_files.get(key, "unknown")
            if isinstance(val, dict):
                desc = val.get("description", "")
            else:
                desc = ""
            print(f"{key:<{max_key_len}}    {src_file:<{max_src_len}}    {desc}")
        print(f"\nTotal: {len(test_cases)} tests")
        sys.exit(0)

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
    failed = 0
    try:
        try:
            failed = run_tests(test_dir)
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user (Ctrl+C)")
            failed = 1
        except Exception as e:
            print(f"Error running tests: {e}")
            failed = 1
    finally:
        # Cleanup: remove the test directory and restore CWD
        # Guarantee cleanup happens even on Ctrl+C or exception
        os.chdir(orig_cwd)
        try:
            shutil.rmtree(test_dir)
            print(f"Cleaned up test directory: {test_dir}")
        except Exception as e:
            print(f"Warning: Failed to clean up test directory: {e}")

        # Print test summary
        total_tests = len(test_cases)
        passed_tests = total_tests - failed
        print(f"\n{'='*40}")
        print(f"Test Summary: {passed_tests}/{total_tests} passed")
        if failed > 0:
            print(f"Failed: {failed}")
        print(f"{'='*40}")

    sys.exit(failed)
