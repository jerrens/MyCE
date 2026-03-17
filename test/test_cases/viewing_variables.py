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
}