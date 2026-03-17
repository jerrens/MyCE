test_cases = {
    # --- Directory merge/override tests ---
    "PWD Merge: projectA hello": {
        "cmd": "alias.hello",
        "see": "Hello from projectA",
        "pwd": "projectA",
        "description": "Should use projectA's hello alias"
    },
    "PWD Merge: projectB hello": {
        "cmd": "alias.hello",
        "see": "Hello from projectB",
        "pwd": "projectB",
        "description": "Should use projectB's hello alias"
    },
    "PWD Merge: projectC hello": {
        "cmd": "alias.hello",
        "see": "Hello from projectC",
        "pwd": "projectC",
        "description": "Should use projectC's hello alias"
    },
    "PWD Merge: projectA shared": {
        "cmd": "alias.shared",
        "see": "Shared from projectA",
        "pwd": "projectA",
        "description": "Should use projectA's shared alias"
    },
    "PWD Merge: projectB shared": {
        "cmd": "alias.shared",
        "see": "Shared from projectB",
        "pwd": "projectB",
        "description": "Should use projectB's shared alias"
    },
    "PWD Merge: projectC shared": {
        "cmd": "alias.shared",
        "see": "Shared from projectC",
        "pwd": "projectC",
        "description": "Should use projectC's shared alias"
    },
}