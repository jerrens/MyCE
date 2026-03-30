# Test cases for conditional variable definitions [IF]/[ELSE IF]/[ELSE]/[FI]

test_cases = {
    # Test commands that use conditional variables
    # The conditionals define variables in the .myCommands file
    # and commands use those variables
    
    "echo.web": {
        "pwd": "projectConditionals",
        "see": "^Web container is: cns-dev-pod-web$",
        "description": "Test basic [IF] equality - should match podman condition and echo web container"
    },
    
    "echo.tool": {
        "pwd": "projectConditionals",
        "see": "^Container tool is: podman$",
        "description": "Test [IF] block definition - should set CONTAINER_TOOL to podman and echo it"
    },
    
    "echo.debug": {
        "pwd": "projectConditionals",
        "see": "^Debug level is: quiet$",
        "description": "Test [IF !$VAR] (existence check) - undefined var should use ELSE condition"
    },
    
    # Test parent-level conditional with child override
    # Parent has CONTAINER_ENGINE=podman, child has CONTAINER_ENGINE=docker
    "echo.web override": {
        "cmd": "echo.web",
        "pwd": "projectConditionals/parentOverride/docker",
        "see": "^Web container is: cns-dev-web-1$",
        "description": "Test variable override affecting conditional - child overrides engine to docker"
    },
    
    # Test section-scoped key still works alongside conditionals
    "section.test.key": {
        "pwd": "projectConditionals",
        "see": "^basic_value$",
        "description": "Test that section-scoped keys work with conditionals"
    },
    
    # Test simple folder - docker engine with debug enabled
    # simple/.myCommands has CONTAINER_ENGINE=docker and ENABLE_DEBUG=true
    "simple echo.web": {
        "cmd": "echo.web",
        "pwd": "projectConditionals/simple",
        "see": "^Web container is: cns-dev-web-1$",
        "description": "Test [ELSE IF] branch - docker engine should match second condition"
    },
    
    "simple echo.tool": {
        "cmd": "echo.tool",
        "pwd": "projectConditionals/simple",
        "see": "^Container tool is: docker$",
        "description": "Test [ELSE IF] variable set - should set CONTAINER_TOOL to docker"
    },
    
    "simple echo.debug": {
        "cmd": "echo.debug",
        "pwd": "projectConditionals/simple",
        "see": "^Debug level is: verbose$",
        "description": "Test [IF] branch - ENABLE_DEBUG=true should trigger verbose level"
    },
    
    # Test ELSE branch of CONTAINER_ENGINE - unknown value triggers ELSE
    "unknown echo.web": {
        "cmd": "echo.web",
        "pwd": "projectConditionals/unknown",
        "see": "^Web container is: unknown-container$",
        "description": "Test [ELSE] branch - unknown CONTAINER_ENGINE triggers ELSE with default values"
    },
    
    "unknown echo.tool": {
        "cmd": "echo.tool",
        "pwd": "projectConditionals/unknown",
        "see": "^Container tool is: unknown$",
        "description": "Test [ELSE] branch - unknown value sets CONTAINER_TOOL to unknown"
    },
    
    # Test [IF !$VAR] when variable is pre-set - should NOT redefine
    "with-optional echo.optional": {
        "cmd": "echo.optional",
        "pwd": "projectConditionals/with-optional",
        "see": "^Optional var is: pre_defined_value$",
        "description": "Test [IF !$VAR] false - pre-set variable prevents [IF] body from executing"
    },
    
    # Test nested conditionals - prod branch with USE_POD=true, POD_TYPE=prod
    "prod echo.pod": {
        "cmd": "echo.pod",
        "pwd": "projectConditionals/parentOverride/docker",
        "see": "^Pod config is: production$",
        "description": "Test nested [IF] and inner [IF] branches - USE_POD=true and POD_TYPE=prod triggers innermost [IF]"
    },
    
    "prod echo.exec": {
        "cmd": "echo.exec",
        "pwd": "projectConditionals/parentOverride/docker",
        "see": "^Exec command is: docker",
        "description": "Test [ELSE IF] branch - CONTAINER_ENGINE=docker variable is resolved from conditional"
    },
    
    # Test nested conditionals - dev branch with USE_POD=true, POD_TYPE=dev
    "dev echo.pod": {
        "cmd": "echo.pod",
        "pwd": "projectConditionals/parentOverride/dev",
        "see": "^Pod config is: development$",
        "description": "Test nested [IF] and inner [ELSE] branch - USE_POD=true and POD_TYPE=dev triggers inner [ELSE]"
    },
    
    # Test nested conditionals - ELSE branch with USE_POD not set
    "no-pod echo.pod": {
        "cmd": "echo.pod",
        "pwd": "projectConditionals/parentOverride/no-pod",
        "see": "^Pod config is: not_set$",
        "description": "Test nested [IF] ELSE branch - USE_POD not set triggers outer [ELSE]"
    },
    
    # =========================================================================
    # REGRESSION TESTS: Command/Variable Listing (grep pattern fix)
    # =========================================================================
    # Issue: Commands with uppercase endings (e.g., checkCT) were excluded from
    # `my list` output due to incorrect grep pattern that checked the END of
    # the string instead of looking for presence of lowercase letters.
    # See: https://github.com/[repo]/issues/[issue] - March 2026 fix
    
    "list contains mixed-case command": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "checkCT",
        "description": "REGRESSION: Mixed-case commands like checkCT should appear in list (not excluded for uppercase ending)"
    },
    
    "list excludes root variables": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "checkCT.*(?!CONTAINER_ENGINE)",
        "description": "REGRESSION: All-caps variables should NOT appear while commands like checkCT do"
    },
    
    "list includes section commands": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "section\\.test\\.key",
        "description": "REGRESSION: Commands in sections should appear if final segment has lowercase"
    },
    
    "list includes all expected commands": {
        "cmd": "list -l",
        "pwd": "projectConditionals",
        "see": "checkCT",
        "description": "REGRESSION: All expected commands should be in list with correct grep pattern"
    },
}
