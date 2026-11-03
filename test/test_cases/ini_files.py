# Test cases for INI File Processing (#3 from todo-test.md)
# Tests include directives, heredoc parsing, whitespace handling, and variable substitution

test_cases = {
    # Test include directive with a missing file (should warn but not fail)
    "include.missing": {
        "cmd": "include.missing",
        "pwd": "projectMissingInclude",
        "see": ".*",  # Command should still work despite missing include file
        "description": "Test include directive with a missing file - should warn but not fail"
    },

    "include.order.before": {
        "cmd": "include.before",
        "pwd": "projectIncludeOrder",
        "see": "^before$",
        "description": "Include directives preserve definitions before the include"
    },
    "include.order.inline": {
        "cmd": "include.middle",
        "pwd": "projectIncludeOrder",
        "see": "^included$",
        "description": "Included files are parsed inline, including paths with spaces"
    },
    "include.order.after": {
        "cmd": "include.after",
        "pwd": "projectIncludeOrder",
        "see": "^after$",
        "description": "Definitions after an include are parsed afterward"
    },
    "include.order.override": {
        "cmd": "include.override",
        "pwd": "projectIncludeOrder",
        "see": "^local$",
        "description": "Definitions after an include override definitions from it"
    },
    "include.environmentPath": {
        "cmd": "include.envpath",
        "pre": "INCLUDE_TEST_DIR='{{TEST_DIR}}/include files'",
        "pwd": "projectIncludeEnv",
        "see": "^environment path$",
        "description": "Environment variables in include paths expand without splitting paths"
    },
    "include.tildePath": {
        "cmd": "include.tildepath",
        "pre": "HOME='{{TEST_DIR}}/home with spaces'",
        "pwd": "projectIncludeTilde",
        "see": "^tilde path$",
        "description": "Leading tilde in include paths expands to HOME"
    },
    "include.cycle": {
        "cmd": "include.aftercycle",
        "pwd": "projectIncludeCycle",
        "see": "cycle handled",
        "description": "Include cycles are detected and parsing continues"
    },
    "include.commandSubstitutionIsNotRun": {
        "raw_cmd": "INCLUDE_MARKER='{{TEST_DIR}}/include-pwned' __exe__ include.safe; if [ -e '{{TEST_DIR}}/include-pwned' ]; then echo PWNED; else echo SAFE; fi",
        "pwd": "projectIncludeUnsafe",
        "see": "SAFE",
        "description": "Shell syntax in include paths is rejected, not evaluated"
    },

    # Test section/key parsing with unusual whitespace
    "ini.whitespace.key1": {
        "pwd": "projectD",
        "see":"^value1$",
    },
    "ini.whitespace.key2": {
        "pwd": "projectD",
        "see":"^value2$",
    },
    "ini.whitespace.key3": {
        "pwd": "projectD",
        "see":"^value3$",
    },

    # Test section/key parsing with multiple spaces/tabs around equals sign
    "ini.whitespace.spaced_key": {
        "pwd": "projectD",
        "see":"^spaced_value$",
    },

    # Test heredoc parsing with standard heredoc
    "ini.heredoc.standard": {
        "pwd": "projectD",
        "see": "^This is a standard heredoc with multiple lines but parsed as a single line due to backslashes$",
    },
    

    # Test heredoc parsing with nested quotes
    "ini.heredoc.quoted": {
        "pwd": "projectD",
        "see": "^Heredoc with 'single' and \"double\" quotes preserved$",
    },

    # Test variable substitution with defined variables
    "ini.var.defined": {
        "pwd": "projectD",
        "see": "^defined_value$",
    },

    # Test variable substitution with undefined variables (should escape or warn)
    "ini.var.undefined (with ENV)": {
        "cmd": "ini.var.undefined",
        "env": {"undefined_var": "hello"},
        "pwd": "projectE",
        "see": "hello",  # Should resolve to env var
        "description": "Test variable substitution with undefined variables"
    },

    "ini.var.undefined (without ENV)": {
        "cmd": "ini.var.undefined",
        "pwd": "projectE",
        "see": "^$",  # Should be empty
        "description": "Test that undefined variable in value is treated as empty or literal reference"
    },

    "-d ini.var.undefined": {
        "pwd": "projectE",
        "see": "CMD: echo \"\$\{undefined_var\}\"",  # Should show the literal command with the variable unexpanded
        "description": "Test that undefined variable in command is treated as literal and not expanded"
    },

    # Test variable substitution with recursive references (should detect infinite loop)
    "ini.var.recursive": {
        "cmd": "ini.var.recursive",
        "pwd": "projectE",
        "see": "There appears to be an infinite loop in your command references!",
        "description": "Test variable substitution with recursive references"
    },

    # Test simple variable substitution in command
    "ini.var.simple TEST": {
        "pwd": "projectD",
        "see": "^TEST$",
    },

    # Test escaped dollar signs
    "ini.var.escaped": {
        "pwd": "projectD",
        "see": "^\\$notavar$",
    },

    # Test variable substitution with defined variables
    "ini.var.use_defined": {
        "pwd": "projectE",
        "see": "defined_value",
        "description": "Test variable substitution with defined variables"
    },
}
