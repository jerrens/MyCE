# Test cases for command substitutions in command paths
# Regression tests for issue where commands with $(...)  syntax would fail

test_cases = {
    "# Command Substitution": "Tests for command substitution $(...)  in command definitions",

    # Test basic command substitution in command path using echo (portable across systems)
    "test.testSubshellPath": {
        "cmd": "test.testSubshellPath 'Command substitution works!'",
        "see": "Command substitution works!",
        "description": "REGRESSION: Command substitution in path - $(echo /usr/bin)/echo should properly expand and execute"
    },
}
