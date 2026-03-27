# Test cases for description feature
# Tests the `# description:` comment syntax for commands in .myCommands files
# Descriptions are shown in dry-run mode, definition command, and list command with -d flag

test_cases = {
    # Test dry-run output includes SRC, DESC, and CMD lines
    "time ?": {
        "pwd": "projectDescriptions",
        "see": "^SRC: .*\\.myCommands:\\d+.*DESC: Get the current date.*CMD:",
        "description": "Dry-run should show SRC with file:line, DESC with description, and CMD with command"
    },

    # Test command without description doesn't show DESC line (only SRC and CMD)
    "simple ?": {
        "pwd": "projectDescriptions",
        "see": "^SRC: .*\\.myCommands:\\d+\nCMD:",
        "description": "Command without description should not have DESC line"
    },

    # Test definition command shows descriptions
    "definition time": {
        "pwd": "projectDescriptions",
        "see": "Get the current date and time",
        "description": "definition command should show description for the time key"
    },

    # Test list -d shows descriptions for filtered keys in two-column format
    "list -d time": {
        "pwd": "projectDescriptions",
        "see": "time\\s+Get the current date",
        "description": "list -d should show keys with descriptions in two-column format"
    },

    # Test list -d with timestamp shows description
    "list -d timestamp": {
        "pwd": "projectDescriptions",
        "see": "timestamp\\s+.*YYYYMMDD_HHMMSS",
        "description": "list -d should show timestamp with its description in two-column format"
    },

    # Test sectioned command description in definition
    "definition tools.health": {
        "pwd": "projectDescriptions",
        "see": "Tool A",
        "description": "definition should show description for sectioned commands"
    },

    # Test description in sectioned list using two-column format
    "list -d tools": {
        "pwd": "projectDescriptions",
        "see": "health\\s+.*Tool A",
        "description": "list -d should show sectioned command descriptions in two-column format"
    },

    # Test dry-run with sectioned command
    "tools.health ?": {
        "pwd": "projectDescriptions",
        "see": "SRC: .*\n.*DESC: .*Tool A.*\nCMD:",
        "description": "Dry-run for sectioned commands should show SRC, description, and CMD"
    },

    # Test command with arguments shows description
    "testing.arg1 ?": {
        "pwd": "projectDescriptions",
        "see": "DESC: Echo the first positional argument",
        "description": "Dry-run should show description before argument expansion"
    },

    # Test definition for command without description
    "definition simple": {
        "pwd": "projectDescriptions",
        "see": "simple.*echo \"hello world\"",
        "description": "definition should work for commands without descriptions"
    },

    # Test that descriptions work with variable substitution
    "definition tools.config": {
        "pwd": "projectDescriptions",
        "see": "Get configuration from Tool A",
        "description": "definition should show descriptions for commands with variable references"
    },

    # Test list -d with pattern matching using two-column format
    "list -d database": {
        "pwd": "projectDescriptions",
        "see": "connect\\s+.*PostgreSQL",
        "description": "list -d should filter by pattern and show descriptions in two-column format"
    },

    # Test testing section commands
    "definition testing.allargs": {
        "pwd": "projectDescriptions",
        "see": "Echo all positional arguments",
        "description": "definition should show descriptions for commands using $@"
    },
}


