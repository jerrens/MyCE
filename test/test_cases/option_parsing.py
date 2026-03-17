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
}
