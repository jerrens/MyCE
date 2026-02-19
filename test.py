#!/usr/bin/env python3
# spell-checker:ignore MyCE

from datetime import datetime
import os
import re
import shutil
import subprocess
import sys

exe="./my"


# Array of command -> expected output pairs
test_cases = {
    "version": "\d{2}.\d{1,2}.\d{1,2}",
    "help": "USAGE:",

    "tmp": "^/home/.*/.myCommand",
    "echo_bin 42": "42",

    "section.tmp": "hello",

    # Ensure the token is properly read and expanded into the command
    "toolA.health": "^curl .* Bearer 0123456789ABCDEF",

    "test.sub1": "^$",
    "test.sub1 John": "^John$",
    "test.sub1 John Doe": "^John Doe$",

    "test.sub2 John Doe": "^John Doe$",
    "test.sub3 John Doe": "^John Doe$",
    "test.sub4 John Doe": "^John Doe$",

    "test.subdef1": "^def$",
    "test.subdef1 Alice": "^Alice$",
    "test.subdef2": "^def$",
    "test.subdef2 Bob": "^Bob$",
    "test.subdef3": "^def ALT$",
    "test.subdef3 Charlie Delta": "^Charlie Delta$",
    "test.subdef4": "^def ALT$",
    "test.subdef4 Eve Frank": "^Frank Eve$",

    "test.var1": "^foo$",
    "test.var2": "^foo$",
    "test.var3": "^foo$",

    "test.env1": "^/home/.*",
    "test.env2": "^/home/.*",
    "test.env3": "^/home/.*",
    "test.env4": "^/home/.*",

    "test.unk1": "^$",
    "test.unk2": "^$",
    "test.unk3": "^default$",

    # Since the variable is escaped, the system value should be used and not the value in the .myCommand file
    "test.esc1": "^$",
    "test.esc2": "^$",
    "test.esc3": "^default$",
    "test.esc4": "^$",
    "test.esc5 John Doe": "^def Doe$",

    "test.pos $(seq 1 15)": "^10 1 5 11 12 13 14 15$",

    "test.dblpos1 $(seq 1 15)": "^1 2 3 4 5 6 7 8 9 10 11 12 13 14 15$",
    "test.dblpos2 $(seq 1 15)": "^2 4 6 8 10 12 14 15$",
    "test.dblpos3 $(seq 1 15)": "^15 14 13 12 11 10 - 1 3 5 7 9$",

    "test.nested.sub Alice Blue": "Testing Nested Subst\n\x1b\[31mAlice!\x1b\[0m Other Blue",

    "multiline": "This is a multi-line command that should be treated as a single command",
    "multi.cmd1": "First command",
    "multi.cmd2": "Second command",
    "multi.cmd3": "^Third command with a continuation \s{4}\(leading whitespace preserved\) text from line 2 and line 3",
    "multi.cmd4": "Fourth command with a continuation text from line 2\nand line 3",
    "multi.cmd5": "0\n2\n4\n6\n8\n10\n12\n14\n16\n18\n20",

    "multi.heredoc": "^This is a heredoc test.\nIt should be included in the value with line wraps\n    and indentation preserved.",

    "line.len 10": "^-{10}$",

    # Commands with ENV definitions
    "time": "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [AP]M$",
    "timestamp": "^\d{8}_\d{6}$",

    # Commands with pipes
    "line.len 30": "^-{30}$",

    # System Commands
    "echo 'Hello World'": "Hello World",
    
    '#STDERR': "STDERR Filtering",
    "unknown cmd": "^Unknown key or command",
    "ls /bad": "ls: cannot access '/bad': No such file or directory",

    '#ENV': 'Checking ENV Variables',
    # f"MYCE_RUNCOM=false {exe} -vv time": "MYCE_RUNCOM file not found or set to 'false'",
    "-vv time": {
        "env": {"MYCE_RUNCOM": "false"},
        "see": "MYCE_RUNCOM file not found or set to 'false'",
    },

    "-c -vv time" : "MYCE_RUNCOM file not found or set to 'false'",

    "Advanced Test": {
        "cmd": "-d alt", # Overrides the command given to MyCE.  If not defined, the test key is used as with simple test
        "pre": "echo", # OPTIONAL: Prefix to include before the MyCE exe.  This may be used to 'echo' or in-line variables
        "see": f"{exe} -d alt", # REQUIRED: the grep pattern expected to be seen in the output
        "env": {}, # OPTIONAL: Dictionary of environment variables to set in the subshell for the test
        "description": "Optional description", # OPTIONAL: A description to print in the test output
    },

    # Viewing definitions
    "definition timestamp": ".myCommands:\d{1,3}\s+timestamp\s+TZ=",

    # Viewing variables
    "Should not show all-cap root variables": {
        "cmd": "list -l",
        "see": "(?!.*CONST)", # Should not show 'CONST' variable
    },
    
    "Should not show all-cap section variables": {
        "cmd": "list -l",
        "see": "section.SHOULD_(?!.*BE_HIDDEN)", # Should not show 'SHOULD_BE_HIDDEN' variable
    },

    "Should show all-cap variables with -a": {
        "cmd": "list -l -a",
        "see": "CONST",
    },
    
    "Should show all-cap section variables with -a": {
        "cmd": "list -l -a",
        "see": "section.SHOULD_BE_HIDDEN",
    },


}


# Keys of tests that should be run.  If empty, all tests will be run
focus_run_test = [  
    # Enter test key here to only run specific tests.  
    # This is useful during development to focus on a specific test or subset of tests without running the entire suite.
    
]

if len( focus_run_test) > 0:
    test_cases = {key: test_cases[key] for key in focus_run_test}


def run_tests():
    failed = 0
    for command, val in test_cases.items():
        try:
            if isinstance(val, dict):
                cmd_prefix = val.get("pre", "")
                cmd_suffix = val.get("cmd", command) # Allow overwritting with the 'cmd' key if present
                env_list = val.get("env", None)
                expected_output = val.get("see", "Missing 'see' property in test")
                description = val.get("description", "")
            else:
                cmd_prefix = ""
                cmd_suffix=command
                env_list = None
                expected_output = val
                description = ""

            # Handle section headers
            if command.startswith('#'):
                print(f"\n{expected_output}\n" + "-" * 30)
                continue
           
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

            expected_pattern = re.compile(expected_output)

            if expected_pattern.search(actual_output):
                print(f"✓ {command:<40} {description}")
            else:
                print("\033[1;31m", end='')
                print(f"✗ {command:<40} {description}")
                print(f"    Expected: '{expected_output}'")
                print(f"    Got:      '{actual_output}'")
                print(f"    Command   {test_cmd}")
                print("\033[0m", end='')
                failed += 1
        except Exception as e:
            print(f"✗ {command} - Error: {e}")
            failed += 1

    return failed

if __name__ == "__main__":
    # Backup .myCommands before running tests
    my_command_backup = ".myCommands.bak-" + str(datetime.now().timestamp())
    print(f"Creating backup of .myCommands at {my_command_backup}")
    if os.path.exists(".myCommands"):
        shutil.move(".myCommands", my_command_backup)

    # Move .myCommands.test to .myCommands for testing
    print("Setting up .myCommands for testing")
    shutil.copy(".myCommands.test", ".myCommands")
    print("Starting tests...\n")

    # Run the tests
    try:
        failed = run_tests()
    except Exception as e:
        print(f"Error running tests: {e}")
        failed = 1

    # Restore original .myCommands after tests
    print("\nRestoring original .myCommands")
    shutil.move(my_command_backup, ".myCommands")

    sys.exit(failed)
