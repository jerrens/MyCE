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
        "env": {"MYCE_RUNCOM": "/tmp/nonexistent_myCommands_file_12345"},
        "description": "Test command execution when MYCE_RUNCOM is set to non-existent file",
    },

    # Test remaining args feature: all non-referenced arguments
    "Remaining args: all arguments": {
        "cmd": "extra.remaining.all John Carter Doe",
        "see": "^Hello John Carter Doe! How are you today$",
        "pwd": "projectE",
        "description": "Test $@+ expansion with all arguments (no positional args referenced)",
    },

    # Test remaining args feature: with one positional arg reference
    "Remaining args: with single positional": {
        "cmd": "extra.remaining.with.pos John Carter Doe",
        "see": "^First: John, Remaining: Carter Doe$",
        "pwd": "projectE",
        "description": "Test $@+ expansion after $1 reference - should skip arg 1, include 2+",
    },

    # Test remaining args feature: with multiple positional arg references
    "Remaining args: with multiple positional": {
        "cmd": "extra.remaining.multi.pos John Arthur Carter Doe",
        "see": "^Start: John - Mid: Carter - Rest: Arthur Doe$",
        "pwd": "projectE",
        "description": "Test $@+ expansion with $1 and $3 referenced - should include args 2 and 4+",
    },

    # Test remaining args feature: with $*+ (star variant)
    "Remaining args: with star variant": {
        "cmd": "extra.remaining.star Alice Bob Charlie",
        "see": "^All: Alice Bob Charlie!$",
        "pwd": "projectE",
        "description": "Test $*+ expansion (all remaining args as single string)",
    },

    # Test remaining args feature: with $*+ (star variant)
    "Remaining args: with star multiple positional": {
        "cmd": "extra.remaining.starPos Alpha Bravo Charlie Delta Echo",
        "see": "^Start: Alpha; Rest: Bravo Delta Echo; Mid: Charlie$",
        "pwd": "projectE",
        "description": "Test $*+ expansion (all remaining args as single string)",
    },

    # Test remaining args feature with braced syntax ${@+} and ${*+}
    "Remaining args: braced form - all arguments": {
        "cmd": "extra.remaining.braced.all John Carter Doe",
        "see": "^Hello John Carter Doe! How are you today$",
        "pwd": "projectE",
        "description": "Test ${@+} expansion with all arguments (braced form)",
    },

    "Remaining args: braced form - with single positional": {
        "cmd": "extra.remaining.braced.pos John Carter Doe",
        "see": "^First: John, Remaining: Carter Doe$",
        "pwd": "projectE",
        "description": "Test ${@+} expansion after $1 reference (braced form)",
    },

    "Remaining args: braced form - with multiple positional": {
        "cmd": "extra.remaining.braced.multi John Arthur Carter Doe",
        "see": "^Start: John - Mid: Carter - Rest: Arthur Doe$",
        "pwd": "projectE",
        "description": "Test ${@+} expansion with $1 and $3 referenced (braced form)",
    },

    "Remaining args: braced star form": {
        "cmd": "extra.remaining.braced.star Alice Bob Charlie",
        "see": "^All: Alice Bob Charlie!$",
        "pwd": "projectE",
        "description": "Test ${*+} expansion (braced form, all remaining args as single string)",
    },
}
