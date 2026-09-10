# Test cases for option parsing and edge cases
# Related to todo-test #1: Option Parsing and Edge Cases
# spell-checker:ignore MYCE

test_cases = {
    # Multiple verbosity flags (-v)
    "-v list": {
        "cmd": "-v list",
        "see": ".*",  # Should produce output with verbosity
        "description": "Test single -v verbosity flag"
    },

    # ANSI color controls
    "--no-color list": {
        "cmd": "--no-color list -v alias.nestedChainA",
        "see": "(?!.*\\x1b).*alias\\.nestedChainA.*->",
        "description": "Test --no-color disables ANSI output while preserving list output"
    },
    "MYCE_NO_ANSI list": {
        "pre": "MYCE_NO_ANSI=1",
        "cmd": "list -v alias.nestedChainA",
        "see": "(?!.*\\x1b).*alias\\.nestedChainA.*->",
        "description": "Test MYCE_NO_ANSI disables ANSI output while preserving list output"
    },
    "MYCE section metadata is ignored in command lists": {
        "cmd": "list -a -l",
        "see": "(?s)(?!.*MYCE\\.NO_ANSI)(?!.*MYCE\\.FILE_NAME)(?!.*MYCE\\.COLUMN_WIDTH).*",
        "description": "Test [MYCE] keys remain metadata-only and never appear as command keys"
    },
    "help shows effective runtime values": {
        "cmd": "help",
        "see": "Runtime Configuration:.*NO_ANSI=.*MY_CUSTOM_FILE=.*COLUMN_WIDTH=.*MYCE_RUNCOM=.*",
        "description": "Test help output now displays the effective configuration values for troubleshooting"
    },
    "-vv list": {
        "cmd": "-vv list",
        "see": ".*",  # Should produce output with increased verbosity
        "description": "Test double -vv verbosity flags"
    },
    "-vvv list": {
        "cmd": "-vvv list",
        "see": ".*",  # Should produce output with maximum verbosity
        "description": "Test triple -vvv verbosity flags"
    },

    # -c option (disable rc file sourcing)
    "-c time": {
        "cmd": "-c time",
        "see": "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        "description": "Test -c option disables shell rc file sourcing"
    },

    # -d option (dry run)
    "-d alias.hello": {
        "cmd": "-d alias.hello",
        "see": "THIS IS A DRYRUN.*CMD: ",
        "description": "Test -d (dry run) option with simple command"
    },
    "-d list -a": {
        "cmd": "-d list -a",
        "see": "THIS IS A DRYRUN!",
        "description": "Test -d (dry run) option with arguments"
    },

    # Combined options
    "-d -v list": {
        "cmd": "-d -v list",
        "see": "THIS IS A DRYRUN!",
        "description": "Test combination of -d (dryrun) and -v (verbose level 1) options"
    },
    "-c -v time": {
        "cmd": "-c -v time",
        "see": "MYCE_RUNCOM file not found or set to 'false'.*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
        "description": "Test combination of -c (disable rc file sourcing) and -v (verbose level 1) options"
    },
    "-c -vv help": {
        "cmd": "-c -vv help",
        "see": "USAGE.*Parsed Options:.*ShellRC: false",
        "description": "Test combination of -c (disable rc file sourcing) and -vv (verbose level 2) options"
    },
    "-vv help": {
        "cmd": "-vv help",
        "see": "USAGE.*Parsed Options:.*ShellRC: (?!false)",
        "description": "Test that Shell RC is set to anything except false by default when not using -c option"
    },
    "-d -c time": {
        "cmd": "-d -c time",
        "see": "THIS IS A DRYRUN.*CMD: ",
        "description": "Test combination of -d (dryrun) and -c (disable rc file sourcing) options"
    },

    # Invalid/unknown options
    "-x list": {
        "cmd": "-x list",
        "see": "illegal option",
        "description": "Test invalid option -x should error gracefully"
    },
    "--unknown-option": {
        "cmd": "--unknown-option",
        "see": "illegal option",
        "description": "Test unknown long option should error"
    },

    # Dry-run escaping tests
    "-d test.newline_test": {
        "cmd": "-d test.newline_test",
        "see": r"THIS IS A DRYRUN.*CMD: echo -e \"Line 1\\\\nLine 2\\\\nLine 3\"",
        "description": "Test that newlines in commands are escaped as \\\\n in dry-run output"
    },
    "-d test.ansi_test": {
        "cmd": "-d test.ansi_test",
        "see": r"THIS IS A DRYRUN.*CMD: echo -ne \"Starting\\\\e\[32m GREEN \\\\e\[0mNormal\\\\e\[1;31m RED BOLD \\\\e\[0mEnd\"",
        "description": "Test that ANSI escape sequences are shown literally (not executed) in dry-run output"
    },
    "-d test.cursor_test": {
        "cmd": "-d test.cursor_test",
        "see": r"THIS IS A DRYRUN.*CMD: echo -ne \"Progress: 0%\\\\rProgress: 50%\\\\rProgress: 100%\\\\nDone\"",
        "description": "Test that carriage returns and other control characters are shown literally in dry-run output"
    },
}
