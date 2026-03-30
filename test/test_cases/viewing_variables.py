test_cases = {
    # Viewing variables
    "Should not show all-cap root variables": {
        "cmd": "list -l",
        "see": "(?!.*CONST)", # Should not show 'CONST' variable
    },

    "Should not show all-cap section variables": {
        "cmd": "list -l",
        "see": "section.SHOULD_(?!.*BE_HIDDEN)", # Should not show 'SHOULD_BE_HIDDEN' variable
    },

    "Should show all-cap variables with -a": {
        "cmd": "list -l -a",
        "see": "CONST",
    },

    "Should show all-cap section variables with -a": {
        "cmd": "list -l -a",
        "see": "section.SHOULD_BE_HIDDEN",
    },
    
    # =========================================================================
    # REGRESSION TESTS: grep pattern fix for mixed-case commands
    # =========================================================================
    # Issue: The grep pattern used to check if strings *ended* with non-uppercase,
    # which excluded commands like "checkCT" that ended with uppercase 'T'.
    # Fixed to check if strings *contain* any lowercase letter (for command detection).
    
    "Should show mixed-case root commands": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "checkCT",
        "description": "REGRESSION: Mixed-case commands (start lowercase, end uppercase) should appear"
    },
    
    "Should show mixed-case section commands": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "section\\.test\\.key",
        "description": "REGRESSION: Section commands with any lowercase should appear (section+lowercase)"
    },
    
    "Should exclude all-uppercase no-section": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "(?!.*CONTAINER_ENGINE$).*(?!.*ENABLE_DEBUG$).*checkCT",
        "description": "REGRESSION: Root-level all-uppercase variables should be excluded while commands appear"
    },
    
    "Should include lowercase in sections": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "echo\\.web",
        "description": "REGRESSION: Section commands (final segment with lowercase) should be included"
    },
}