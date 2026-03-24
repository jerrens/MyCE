# Example test cases split from test.py
# Add more files in this folder to extend test coverage

test_cases = {
    "version": "\d{2}.\d{1,2}.\d{1,2}",
    "help": "USAGE:",

    "tmp": "^/(home|root)/.*/.myCommand",
    "echo_bin 42": "42",

    "section.tmp": "hello",

    # Ensure the token is properly read and expanded into the command
    "toolA.health": "^curl .* Bearer 0123456789ABCDEF",

    "test.sub1": "^$",
    "test.sub1 John": "^John$",
    "test.sub1 John Doe": "^John Doe$",

    "test.sub2 John Doe": "^John Doe$",
    "test.sub3 John Doe": "^John Doe$",
    "test.sub4 John Doe": "^John Doe$",

    "test.subdef1": "^def$",
    "test.subdef1 Alice": "^Alice$",
    "test.subdef2": "^def$",
    "test.subdef2 Bob": "^Bob$",
    "test.subdef3": "^def ALT$",
    "test.subdef3 Charlie Delta": "^Charlie Delta$",
    "test.subdef4": "^def ALT$",
    "test.subdef4 Eve Frank": "^Frank Eve$",

    "test.var1": "^foo$",
    "test.var2": "^foo$",
    "test.var3": "^foo$",

    "test.env1": "^/(home|root).*",
    "test.env2": "^/(home|root).*",
    "test.env3": "^/(home|root).*",
    "test.env4": "^/(home|root).*",

    "test.unk1": "^$",
    "test.unk2": "^$",
    "test.unk3": "^default$",

    # Since the variable is escaped, the system value should be used and not the value in the .myCommand file
    "test.esc1": "^$",
    "test.esc2": "^$",
    "test.esc3": "^default$",
    "test.esc4": "^$",
    "test.esc5 John Doe": "^def Doe$",

    "test.pos $(seq 1 15)": "^10 1 5 11 12 13 14 15$",

    "test.dblpos1 $(seq 1 15)": "^1 2 3 4 5 6 7 8 9 10 11 12 13 14 15$",
    "test.dblpos2 $(seq 1 15)": "^2 4 6 8 10 12 14 15$",
    "test.dblpos3 $(seq 1 15)": "^15 14 13 12 11 10 - 1 3 5 7 9$",

    "test.nested.sub Alice Blue": "Testing Nested Subst\n\x1b\[31mAlice!\x1b\[0m Other Blue",

    "multiline": "This is a multi-line command that should be treated as a single command",
    "multi.cmd1": "First command",
    "multi.cmd2": "Second command",
    "multi.cmd3": "^Third command with a continuation \s{4}\(leading whitespace preserved\) text from line 2 and line 3",
    "multi.cmd4": "Fourth command with a continuation text from line 2\nand line 3",
    "multi.cmd5": "0\n2\n4\n6\n8\n10\n12\n14\n16\n18\n20",

    "multi.heredoc": "^This is a heredoc test.\nIt should be included in the value with line wraps\n    and indentation preserved.",

    "line.len 10": "^-{10}$",

    # Commands with ENV definitions
    "time": "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}( [AP]M)?$",
    "timestamp": "^\d{8}_\d{6}$",

    # Commands with pipes
    "line.len 30": "^-{30}$",

    # System Commands
    "echo 'Hello World'": "Hello World",

    '#STDERR': "STDERR Filtering",
    "unknown cmd": "^Unknown key or command",
    "ls /bad": "ls: cannot access '/bad': No such file or directory",

    '#ENV': 'Checking ENV Variables',
    # f"MYCE_RUNCOM=false {exe} -vv time": "MYCE_RUNCOM file not found or set to 'false'",
    "-vv time": {
        "env": {"MYCE_RUNCOM": "false"},
        "see": "MYCE_RUNCOM file not found or set to 'false'",
    },

    "-c -vv time" : "MYCE_RUNCOM file not found or set to 'false'",

    "Advanced Test": {
        "cmd": "-d alt", # Overrides the command given to MyCE.  If not defined, the test key is used as with simple test
        "pre": "echo", # OPTIONAL: Prefix to include before the MyCE exe.  This may be used to 'echo' or in-line variables
        "see": "__exe__ -d alt", # REQUIRED: the grep pattern expected to be seen in the output
        "env": {}, # OPTIONAL: Dictionary of environment variables to set in the subshell for the test
        "description": "Optional description", # OPTIONAL: A description to print in the test output
    },

    # Viewing definitions
    "definition timestamp": ".myCommands:\d{1,3}\s+timestamp\s+TZ=",

    # Special Variables
    "dir.path": "{{TEST_DIR}}",
    "-d THIS_DIR": "CMD: {{TEST_DIR}}",
    
    "Directory Special Variable (projectA)": {
        "cmd": "dir.path",
        "see": "{{TEST_DIR}}",
        "pwd": "projectA",        
        "description": "Should use the __DIRECTORY__ variable to show the test directory"
    },

    # Dry Run Special Syntax
    "-d time": "THIS IS A DRYRUN.*CMD: ",
    "time ?": "^CMD: ",

    # Positional arguments at start of command
    "positional.start.echo_first echo": "^hello$",
    "positional.start.echo_with_prefix world": "^prefix: world$",

    # Variable replacement at start and mid-command
    "variable.replacement.test_var_sub": "^result_echo_end$",
    "variable.replacement.test_var_start": "^is here$",
}
