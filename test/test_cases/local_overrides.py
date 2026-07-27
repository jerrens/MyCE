# Test cases for .local file override functionality

test_cases = {
    # --- Basic local file override tests ---
    "LOCAL: alias override": {
        "cmd": "alias.greeting",
        "see": "Hello from local override",
        "pwd": "projectLocalOverride",
        "description": "Should use .myCommands.local greeting override"
    },
    
    "LOCAL: command not in .local": {
        "cmd": "alias.local_only",
        "see": "defined in main only",
        "pwd": "projectLocalOverride",
        "description": "Should use main definition (not in .local)"
    },
    
    "LOCAL: .local can override main": {
        "cmd": "alias.shared",
        "see": "Shared from local override",
        "pwd": "projectLocalOverride",
        "description": "Should use .local command that overrides main"
    },

    # --- Nested local override tests ---
    "LOCAL: nested .local override": {
        "cmd": "alias.nested_greeting",
        "see": "Hello from nested local",
        "pwd": "projectLocalOverride/nested",
        "description": "Should use nested .myCommands.local override"
    },
    
    "LOCAL: nested .local overrides shared": {
        "cmd": "alias.shared",
        "see": "Shared from nested local",
        "pwd": "projectLocalOverride/nested",
        "description": "Should use nested .myCommands.local shared override"
    },

    "LOCAL: nested-only command": {
        "cmd": "alias.nested_only",
        "see": "defined in nested only",
        "pwd": "projectLocalOverride/nested",
        "description": "Should use command defined only in nested main"
    },

    # --- Definition command tests ---
    "LOCAL: definition shows .local override": {
        "cmd": "definition alias.greeting",
        "see": ".myCommands.local.*greeting.*echo \"Hello from local override\"",
        "pwd": "projectLocalOverride",
        "description": "definition command should show .myCommands.local for overridden command"
    },

    "LOCAL: definition shows main when not overridden": {
        "cmd": "definition alias.local_only",
        "see": ".myCommands.*local_only.*echo \"defined in main only\"",
        "pwd": "projectLocalOverride",
        "description": "definition command should show .myCommands for non-overridden command"
    },

    "LOCAL: definition preview shows .local": {
        "cmd": "alias.greeting @",
        "see": ".myCommands.local.*greeting.*echo \"Hello from local override\"",
        "pwd": "projectLocalOverride",
        "description": "@ syntax should show definition from .myCommands.local"
    },

    "LOCAL: definition preview shows main": {
        "cmd": "alias.local_only @",
        "see": ".myCommands.*local_only.*echo \"defined in main only\"",
        "pwd": "projectLocalOverride",
        "description": "@ syntax should show definition from .myCommands when not overridden"
    },

    "LOCAL: nested definition shows .local": {
        "cmd": "definition alias.nested_greeting",
        "see": "nested/.myCommands.local.*nested_greeting.*echo \"Hello from nested local\"",
        "pwd": "projectLocalOverride/nested",
        "description": "definition command should show nested .myCommands.local"
    },

    "LOCAL: dryrun shows .local file location": {
        "cmd": "-d alias.greeting",
        "see": "SRC: .*/projectLocalOverride/.myCommands.local",
        "pwd": "projectLocalOverride",
        "description": "Dryrun should show SRC from .myCommands.local for overridden command"
    },
}

