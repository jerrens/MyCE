# Test cases for command execution with additional arguments
# Tests for todo-test #4: Command Execution

test_cases = {
    # Test command execution without additional arguments
    "Command execution without args": {
        "cmd": "extra.noargs",
        "see": "^Execute noargs$",
        "pwd": "projectE",
        "description": "Test command execution with no additional arguments",
    },
    
    # Test command execution with single additional argument
    "Command execution with single arg": {
        "cmd": "extra.single Alice",
        "see": "^Hello Alice$",
        "pwd": "projectE",
        "description": "Test command execution with single positional argument",
    },
    
    # Test command execution with multiple additional arguments
    "Command execution with multiple args": {
        "cmd": "extra.multi John Doe",
        "see": "^Multiple args: John Doe$",
        "pwd": "projectE",
        "description": "Test command execution with multiple positional arguments",
    },
    
    # Test command execution with arguments containing spaces
    "Command execution with quoted args": {
        "cmd": "extra.quote 'Hello World'",
        "see": "^Quoted Hello World$",
        "pwd": "projectE",
        "description": "Test command execution with quoted arguments containing spaces",
    },
    
    # Test command execution with $* (all args as single string)
    "Command execution with $* expansion": {
        "cmd": "extra.varargs John Doe",
        "see": "^Variable args: John Doe$",
        "pwd": "projectE",
        "description": "Test command execution with $* variable expansion (all arguments as single string)",
    },
    
    # Test command execution with variables and positional arguments combined
    "Command execution with vars and args": {
        "cmd": "extra.withvar Smith",
        "see": "^Name: Smith Age: 25$",
        "pwd": "projectE",
        "description": "Test command execution with variables and positional arguments combined",
    },
    
    # Test command execution with numbered positional arguments
    "Command execution with numbered args": {
        "cmd": "extra.pos1 arg1 arg2 arg3",
        "see": "^First: arg1 Second: arg2 Third: arg3$",
        "pwd": "projectE",
        "description": "Test command execution with numbered positional arguments",
    },
    
    # Test command execution with default arguments when none provided
    "Command execution with defaults": {
        "cmd": "extra.default",
        "see": "^With defaults$",
        "pwd": "projectE",
        "description": "Test command execution with default arguments when none provided",
    },
    
    # Test command execution when MYCE_RUNCOM is set to non-existent file
    "Command execution with non-existent MYCE_RUNCOM": {
        "cmd": "-v extra.noargs",
        "see": "MYCE_RUNCOM file not found or set to 'false'.*Execute noargs$",
        "pwd": "projectE",
        "env": {"MYCE_RUNCOM": "/tmp/nonexistent_mycommands_file_12345"},
        "description": "Test command execution when MYCE_RUNCOM is set to non-existent file",
    },
}
