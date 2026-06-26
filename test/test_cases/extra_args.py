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
    
    # Test command execution with braced $@ expansion (regression test for argument duplication bug)
    "Command execution with braced $@ expansion": {
        "cmd": "extra.multibraced World",
        "see": "^Multiple args: World$",
        "pwd": "projectE",
        "description": "Regression test: ${@} should not duplicate arguments (bug: was outputting 'World World' instead of 'World')",
    },
    
    # Test command execution with braced $@ expansion with multiple arguments
    "Command execution with braced $@ and multiple args": {
        "cmd": "extra.multibraced Foo Bar Baz",
        "see": "^Multiple args: Foo Bar Baz$",
        "pwd": "projectE",
        "description": "Regression test: ${@} with multiple args should expand correctly without duplication",
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

    # Named parameter tests
    "Named params: basic usage": {
        "cmd": "named.greet first=John last=Doe",
        "see": "^Hello John Doe$",
        "pwd": "projectE",
        "description": "Test basic named parameter substitution with = delimiter",
    },

    "Named params: colon delimiter": {
        "cmd": "named.greet.colon first:Alice last:Smith",
        "see": "^Hello Alice Smith$",
        "pwd": "projectE",
        "description": "Test named parameter substitution with : delimiter",
    },

    "Named params: single parameter": {
        "cmd": "named.message msg='Hello World'",
        "see": "^Message: Hello World$",
        "pwd": "projectE",
        "description": "Test single named parameter with quoted value",
    },

    "Named params: multiple named with spaces": {
        "cmd": "named.quoted first=John last=Smith location='New York'",
        "see": "^Full name: John Smith at New York$",
        "pwd": "projectE",
        "description": "Test multiple named parameters with quoted values containing spaces",
    },

    "Named params: with defaults": {
        "cmd": "named.with.default age=30",
        "see": "^Name: Guest Age: 30$",
        "pwd": "projectE",
        "description": "Test named parameters with default values for unreferenced params",
    },

    "Named params: with default not provided": {
        "cmd": "named.with.default",
        "see": "^Name: Guest Age: 25$",
        "pwd": "projectE",
        "description": "Test named parameters using defaults when no args provided",
    },

    "Named params: undefined reference": {
        "cmd": "named.undefined.ref",
        "see": "^Value:$",
        "pwd": "projectE",
        "description": "Test that undefined named parameter references are left in command but expand to empty when bash evaluates them",
    },

    "Named params: mixed positional and named": {
        "cmd": "named.mixed Alice name=Bob extra",
        "see": "^Positional: Alice, Named: Bob, Remaining: extra$",
        "pwd": "projectE",
        "description": "Test mixing positional and named parameters in same command",
    },

    "Named params: pass-through unconsumed": {
        "cmd": "named.pass.through param1=value1 param2=value2",
        "see": "^This command doesn't reference any named params param1=value1 param2=value2$",
        "pwd": "projectE",
        "description": "Test that unconsumed named parameters are passed through to the command",
    },

    "Named params: special chars - colons in value with = delimiter": {
        "cmd": "named.special.colon value='url:with:colons'",
        "see": "^Got: url:with:colons$",
        "pwd": "projectE",
        "description": "Test that colons in parameter values work without escaping (using = delimiter)",
    },

    "Named params: special chars - colons in value with : delimiter": {
        "cmd": "named.special.colon value:url:with:colons",
        "see": "^Got: url:with:colons$",
        "pwd": "projectE",
        "description": "Test that colons in parameter values work without escaping (using : delimiter)",
    },

    "Named params: special chars - equals in value with = delimiter": {
        "cmd": "named.special.equals value='foo=bar=baz'",
        "see": "^Got: foo=bar=baz$",
        "pwd": "projectE",
        "description": "Test that equals signs in parameter values work without escaping (using = delimiter)",
    },

    "Named params: special chars - equals in value with : delimiter": {
        "cmd": "named.special.equals value:foo=bar=baz",
        "see": "^Got: foo=bar=baz$",
        "pwd": "projectE",
        "description": "Test that equals signs in parameter values work without escaping (using : delimiter)",
    },

    "Named params: special chars - both delimiters in value": {
        "cmd": "named.special.both value='proto:http=default'",
        "see": "^Got: proto:http=default$",
        "pwd": "projectE",
        "description": "Test that both colon and equals can exist in parameter values",
    },

    # Test $@ with positional args (should include ALL args including referenced ones)
    "All args with positional: single positional and $@": {
        "cmd": "extra.all.with.pos John Doe",
        "see": "^First: John, All: John Doe$",
        "pwd": "projectE",
        "description": "Regression test: $@ should include ALL args (including $1), not just remaining",
    },

    # Test ${@} with positional args (should include ALL args including referenced ones)
    "All args braced with positional: single positional and ${@}": {
        "cmd": "extra.all.braced.with.pos Jane Smith",
        "see": "^First: Jane, All: Jane Smith$",
        "pwd": "projectE",
        "description": "Regression test: ${@} should include ALL args (including $1), not just remaining",
    },

    # Test $@ with multiple positional args (should include ALL args)
    "All args with multiple positional: $1, $2, and $@": {
        "cmd": "extra.all.with.multi.pos Alice Bob Charlie",
        "see": "^Start: Alice, Second: Bob, All: Alice Bob Charlie$",
        "pwd": "projectE",
        "description": "Regression test: $@ should include ALL args (including $1 and $2), not just remaining",
    },

    # Test ${@} with multiple positional args (should include ALL args)
    "All args braced with multiple positional: $1, $2, and ${@}": {
        "cmd": "extra.all.braced.with.multi.pos Tom Jerry Spike",
        "see": "^Start: Tom, Second: Jerry, All: Tom Jerry Spike$",
        "pwd": "projectE",
        "description": "Regression test: ${@} should include ALL args (including $1 and $2), not just remaining",
    },

    # Test $* with positional args (should include ALL args as single string)
    "All args star with positional: $1 and $*": {
        "cmd": "extra.all.star.with.pos One Two Three",
        "see": "^First: One, All: One Two Three$",
        "pwd": "projectE",
        "description": "Test $* should include ALL args as single string (including $1), not just remaining",
    },

    # Test ${*} with positional args (should include ALL args as single string)
    "All args star braced with positional: $1 and ${*}": {
        "cmd": "extra.all.star.braced.with.pos First Second Third",
        "see": "^First: First, All: First Second Third$",
        "pwd": "projectE",
        "description": "Test ${*} should include ALL args as single string (including $1), not just remaining",
    },
}
