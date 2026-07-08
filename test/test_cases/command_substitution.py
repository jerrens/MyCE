# Test cases for command substitutions and word extraction in command paths
# Regression tests for __extract_first_word() function that handles various bash syntaxes

test_cases = {
    "# Word Extraction & Command Substitution": "Tests for various bash syntaxes in command paths",

    # Test basic command substitution in command path using echo (portable across systems)
    "subshell.subshellPath": {
        "cmd": "subshell.subshellPath 'Command substitution works!'",
        "see": "Command substitution works!",
        "description": "REGRESSION: Command substitution $(...) - should properly extract as atomic unit"
    },

    # Test command substitution in command path (alternative form)
    "subshell.backtickPath": {
        "cmd": "subshell.backtickPath 'Backtick works!'",
        "see": "Backtick works!",
        "description": "REGRESSION: Backtick command substitution `...` - should properly extract as atomic unit"
    },

    # Test double-quoted argument with spaces
    "subshell.quotedArg": {
        "cmd": "subshell.quotedArg",
        "see": "This is a quoted string",
        "description": "REGRESSION: Double-quoted strings with spaces - should not split on spaces inside quotes"
    },

    # Test single-quoted argument (preserves literal characters)
    "subshell.singleQuotedArg": {
        "cmd": "subshell.singleQuotedArg",
        "see": "Single quoted: \\$VARIABLE",
        "description": "REGRESSION: Single-quoted strings - should preserve literal characters and not expand variables"
    },

    # Test process substitution <(...)
    "subshell.processSub": {
        "cmd": "subshell.processSub",
        "see": "hello",
        "description": "REGRESSION: Process substitution <(...) - should properly extract as atomic unit"
    },

    # Test complex parameter expansion
    "subshell.complexExpansion": {
        "cmd": "subshell.complexExpansion",
        "see": "/bin/echo",
        "description": "REGRESSION: Complex parameter expansion ${...} - should handle colons and slashes"
    },

    # Test command substitution in path
    "subshell.subshellPath": {
        "cmd": "subshell.subshellPath 'Command substitution works!'",
        "see": "Command substitution works!",
        "description": "REGRESSION: Command substitution in path - should extract $(echo /usr/bin)/echo correctly"
    },

    # Additional edge case variations
    "subshell.processSubOut": {
        "cmd": "subshell.processSubOut <<< 'test'",
        "see": "test",
        "description": "REGRESSION: Process substitution output form >(...)  - should extract correctly"
    },

    "subshell.escapedSpace": {
        "cmd": "subshell.escapedSpace",
        "see": "hello world",
        "description": "REGRESSION: Escaped spaces in arguments - should not split on escaped spaces"
    },

    "subshell.nestedSub": {
        "cmd": "subshell.nestedSub",
        "see": "2026",
        "description": "REGRESSION: Nested command substitution $(echo $(echo 2026)) - should extract correctly"
    },

    "subshell.mixedQuotes": {
        "cmd": "subshell.mixedQuotes",
        "see": "single double",
        "description": "REGRESSION: Mixed single and double quotes - should preserve both quote types"
    },

    "subshell.quotedWithSub": {
        "cmd": "subshell.quotedWithSub",
        "see": "Today is",
        "description": "REGRESSION: Double-quoted string with command substitution inside - should extract correctly"
    },

    "subshell.paramDefault": {
        "cmd": "subshell.paramDefault",
        "see": "fallback",
        "description": "REGRESSION: Parameter expansion with default value ${VAR:-default} - should extract correctly"
    },

    "subshell.paramSubstr": {
        "cmd": "subshell.paramSubstr",
        "see": "/bin",
        "description": "REGRESSION: Parameter expansion with substring offset ${VAR:0:4} - should extract correctly"
    },

    "subshell.paramPattern": {
        "cmd": "subshell.paramPattern",
        "see": "test",
        "description": "REGRESSION: Simple parameter expansion test - should extract correctly"
    },

    "subshell.multiSub": {
        "cmd": "subshell.multiSub",
        "see": "helloworld",
        "description": "REGRESSION: Multiple consecutive command substitutions in word - should extract correctly"
    },

    "subshell.subWithSpaces": {
        "cmd": "subshell.subWithSpaces",
        "see": "spaced output",
        "description": "REGRESSION: Escaped spaces in command - should preserve spaces"
    },

    "subshell.escapedDollar": {
        "cmd": "subshell.escapedDollar",
        "see": "Literal: \\$VARIABLE",
        "description": "REGRESSION: Literal dollar sign with single quotes - should output literal \\$"
    },
}
