# Test cases for shorthand definition preview and edge cases
# Tests the `@` shorthand and `definition` command for nested .myCommands

test_cases = {
    # Test definition command at each level
    "definition test.dir": {
        "pwd": "projectNested",
        "see": "projectNested/.myCommands:\d+\s+\[test\]⇒ dir",
        "description": "definition command should show the test.dir key at root level"
    },
    "definition test.dir - level1": {
        "cmd": "definition test.dir",
        "pwd": "projectNested/level1",
        "see": "projectNested/.myCommands:\d+\s+\[test\]⇒ dir.*projectNested/level1/.myCommands:\d+\s+\[test\]⇒ dir",
        "description": "definition command should show the test.dir key at root and level1"
    },
    "definition test.dir - level2": {
        "cmd": "definition test.dir",
        "pwd": "projectNested/level1/level2",
        "see": "projectNested/.myCommands:\d+\s+\[test\]⇒ dir.*projectNested/level1/.myCommands:\d+\s+\[test\]⇒ dir.*projectNested/level1/level2/.myCommands:\d+\s+\[test\]⇒ dir",
        "description": "definition command should show the test.dir key at level2"
    },

    # Test @ shorthand at each level
    "test.dir @ - root": {
        "cmd": "test.dir @",
        "pwd": "projectNested",
        "see": "projectNested/.myCommands:\d+\s+\[test\]⇒ dir",
        "description": "@ shorthand should show the test.dir key at root level"
    },
    "test.dir @ - level1": {
        "cmd": "test.dir @",
        "pwd": "projectNested/level1",
        "see": "projectNested/.myCommands:\d+\s+\[test\]⇒ dir.*projectNested/level1/.myCommands:\d+\s+\[test\]⇒ dir",
        "description": "@ shorthand should show the test.dir key at level1"
    },
    "test.dir @ - level2": {
        "cmd": "test.dir @",
        "pwd": "projectNested/level1/level2",
        "see": "projectNested/.myCommands:\d+\s+\[test\]⇒ dir.*projectNested/level1/.myCommands:\d+\s+\[test\]⇒ dir.*projectNested/level1/level2/.myCommands:\d+\s+\[test\]⇒ dir",
        "description": "@ shorthand should show the test.dir key at level2"
    },

    # Test fallback for unknown key
    "definition unknown.key": {
        "pwd": "projectNested/level1/level2",
        "see": "^$",
        "description": "definition command should show nothing if key has no definition"
    },
    "unknown.key @": {
        "pwd": "projectNested/level1/level2",
        "see": "No definition found",
        "description": "@ shorthand should show not found for unknown key"
    },

    # Test that the value is the correct directory at each level
    "test.dir - root": {
        "cmd": "test.show_dir",
        "pwd": "projectNested",
        "see": "projectNested$",
        "description": "test.dir should expand to the root projectNested directory"
    },
    "test.dir - level1": {
        "cmd": "test.show_dir",
        "pwd": "projectNested/level1",
        "see": "projectNested/level1$",
        "description": "test.dir should expand to the level1 directory"
    },
    "test.dir - level2": {
        "cmd": "test.show_dir",
        "pwd": "projectNested/level1/level2",
        "see": "/projectNested/level1/level2$",
        "description": "test.dir should expand to the level2 directory"
    },
}
