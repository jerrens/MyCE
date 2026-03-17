test_cases = {
    # --- alias.merge value merge/override tests ---
    "PWD Merge: projectA alias.merge": {
        "cmd": "alias.merge",
        "see": "blueprint-default-value",
        "pwd": "projectA",
        "description": "Should use default alias.merge in projectA"
    },
    "PWD Merge: projectB alias.merge": {
        "cmd": "alias.merge",
        "see": "projectB-override-value",
        "pwd": "projectB",
        "description": "Should use overridden alias.merge in projectB"
    },
    "PWD Merge: projectC alias.merge": {
        "cmd": "alias.merge",
        "see": "blueprint-default-value",
        "pwd": "projectC",
        "description": "Should use default alias.merge in projectC"
    },
}