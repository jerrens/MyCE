#!/usr/bin/env python3
import subprocess
import sys
import re

# Array of command -> expected output pairs
test_cases = {
    "version": "\d{2}.\d{1,2}.\d{1,2}",    
    "help": "USAGE:",

    "tmp": "^/home/.*/.myCommand",
    "echo_bin 42": "42",

    "section.tmp": "hello",

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
    

    # System Commands
    "echo 'Hello World'": "Hello World",
    "unknown 'Hello World'": "Unknown command: unknown Hello World",
}

failing_keys = [  # Keys of tests that are currently failing
    'test.sub1',
    'test.subdef1',
    'test.subdef2',
    'test.subdef3',
    'test.subdef4',
]

# test_cases = {key: test_cases[key] for key in failing_keys}

def run_tests():
    failed = 0
    for command, expected_output in test_cases.items():
        try:
            # print(f"Executing command: ./my {command}")

            result = subprocess.run(
                f"./my {command}",
                capture_output=True,
                text=True,
                timeout=5,
                shell=True
            )
            actual_output = result.stdout.strip()
            
            expected_pattern = re.compile(expected_output)

            if expected_pattern.search(actual_output):
                print(f"✓ {command}")
            else:
                print(f"✗ {command}")
                print(f"    Expected: {expected_output}")
                print(f"    Got:      {actual_output}")
                failed += 1
        except Exception as e:
            print(f"✗ {command} - Error: {e}")
            failed += 1
    
    return failed

if __name__ == "__main__":
    failed = run_tests()
    sys.exit(failed)
