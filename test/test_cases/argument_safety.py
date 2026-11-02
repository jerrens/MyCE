test_cases = {
    "test.inertQuoted command substitution": {
        "cmd": "test.inertQuoted '$(printf PWNED)'",
        "see": r"^<\$\(printf PWNED\)>$",
        "description": "Runtime positional arguments remain data inside double quotes"
    },
    "test.inertQuoted shell operator": {
        "cmd": "test.inertQuoted 'safe; printf PWNED'",
        "see": r"^<safe; printf PWNED>$",
        "description": "Runtime positional arguments cannot add shell commands"
    },
    "test.inertDefault command substitution": {
        "cmd": "test.inertDefault '$(printf PWNED)'",
        "see": r"^<\$\(printf PWNED\)>$",
        "description": "Defaulted positional references keep runtime arguments literal"
    },
    "test.inertNamed shell operator": {
        "cmd": "test.inertNamed 'value=safe; printf PWNED'",
        "see": r"^<safe; printf PWNED>$",
        "description": "Named parameter values cannot add shell commands"
    },
    "test.inertAll command substitutions": {
        "cmd": "test.inertAll '$(printf PWNED)' '; printf PWNED2'",
        "see": r"^<\$\(printf PWNED\) ; printf PWNED2>$",
        "description": "All-argument references keep shell syntax in each argument inert"
    },
    "test.inertQuoted dry-run": {
        "cmd": "test.inertQuoted '$(printf PWNED)' ?",
        "see": r'''CMD: printf '<%s>\\\\n' "\$\(printf PWNED\)"''',
        "description": "Dry-run output displays the literal runtime argument"
    },
}
