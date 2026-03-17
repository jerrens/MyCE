# Test cases for todo-test #2: Error Handling
# Covers missing arguments, non-existent keys, and CRLF handling
# Add more files in this folder to extend test coverage

test_cases = {
    # Missing arguments for 'set' (should show error)
    "set": "^Missing key or value!",
    "set onlykey": "^Missing key or value!",

    # Missing arguments for 'definition' (should show error or usage)
    "definition": "^Missing key argument!",

    # Non-existent key (should fallback to system command or error)
    "nonexistent.key": "^(Unknown key|not found|command not found|ERROR)",
    "nonexistent.key arg1": "^(Unknown key|not found|command not found|ERROR)",
    "nonexistent.deepness.key": "^(Unknown key|not found|command not found|ERROR)",

    # Test with system command fallback (if no key found, try system command)
    "echo test": "^test$",
    "ls /nonexistent": "^(ls: cannot access|cannot find|No such file)",

    # CRLF warning test
    "Skip CRLF .myCommands files": {
        "cmd": "very.unique",
        "pwd": "projectCRLF",
        "see": "WARNING: Detected CRLF.*Unknown key or command",
    },    
    
}
