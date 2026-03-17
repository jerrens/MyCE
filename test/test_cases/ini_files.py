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
