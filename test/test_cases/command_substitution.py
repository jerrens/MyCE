# Test cases for command substitutions and word extraction in command paths
# Regression tests for __extract_first_word() function that handles various bash syntaxes

test_cases = {
    "# Word Extraction & Command Substitution": "Tests for various bash syntaxes in command paths",

    # Nested invocation syntax tests: ${commandKey args...}
    "alias.nestedSimple": {
        "cmd": "alias.nestedSimple",
        "see": "^Hello World$",
        "description": "NESTED: ${key args} resolves nested key with positional arg"
    },

    "alias.nestedChainA": {
        "cmd": "alias.nestedChainA",
        "see": "^Nested chain works$",
        "description": "NESTED: chained nested references resolve recursively"
    },

    "alias.nestedMissing": {
        "cmd": "alias.nestedMissing",
        "see": "bad substitution",
        "description": "NESTED: missing nested key is preserved for shell expansion"
    },

    "alias.nestedLoopA": {
        "cmd": "alias.nestedLoopA",
        "see": "Nested invocation depth exceeded",
        "description": "NESTED: recursive loop is bounded by depth guard"
    },

    "alias.nestedCallAllAt": {
        "cmd": "alias.nestedCallAllAt",
        "see": "^AT:one two three$",
        "description": "NESTED: target alias expands $@ from multiple nested args"
    },

    "alias.nestedCallAllStar": {
        "cmd": "alias.nestedCallAllStar",
        "see": "^STAR:one two three$",
        "description": "NESTED: target alias expands $* from multiple nested args"
    },

    "alias.nestedCallRemainingAt": {
        "cmd": "alias.nestedCallRemainingAt",
        "see": "^KEEP:two REST:one three four five$",
        "description": "NESTED: target alias expands $@+ with explicit $2 reference"
    },

    "alias.nestedCallRemainingStar": {
        "cmd": "alias.nestedCallRemainingStar",
        "see": "^KEEP:two REST:one three four five$",
        "description": "NESTED: target alias expands $*+ with explicit $2 reference"
    },

    "alias.nestedCallSecond": {
        "cmd": "alias.nestedCallSecond",
        "see": "^SECOND:two three$",
        "description": "NESTED: target alias expands $2 and appends unreferenced trailing args"
    },

    "alias.nestedCallThree": {
        "cmd": "alias.nestedCallThree",
        "see": "^A:arg1 B:arg2 C:arg3$",
        "description": "NESTED: target alias receives and expands 3 nested args"
    },

    "alias.nestedCallUnrefAppend": {
        "cmd": "alias.nestedCallUnrefAppend",
        "see": "^FIRST:one two three$",
        "description": "NESTED: unreferenced args in target alias are appended to command tail"
    },

    "alias.nestedNamedCall": {
        "cmd": "alias.nestedNamedCall",
        "see": "^Output: Hello$",
        "description": "NESTED: inline named parameters are available in target alias"
    },

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
