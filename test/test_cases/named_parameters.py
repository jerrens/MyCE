# Test cases for named parameter delimiter preservation
# Ensures that ':' and '=' delimiters are preserved in parameter passing
# All tests run from projectNamedParam directory

test_cases = {
    # ========== SINGLE PARAMETER TESTS ==========
    
    # Colon delimiter - parameter referenced in command
    "namedparam.refSingleColon action:build": {
        "cmd": "namedparam.refSingleColon action:build",
        "pwd": "projectNamedParam",
        "see": "referenced:build$",
    },
    "namedparam.refSingleColon action:deploy": {
        "cmd": "namedparam.refSingleColon action:deploy",
        "pwd": "projectNamedParam",
        "see": "referenced:deploy$",
    },
    
    # Equals delimiter - parameter referenced in command
    "namedparam.refSingleEquals action=build": {
        "cmd": "namedparam.refSingleEquals action=build",
        "pwd": "projectNamedParam",
        "see": "referenced=build$",
    },
    "namedparam.refSingleEquals action=deploy": {
        "cmd": "namedparam.refSingleEquals action=deploy",
        "pwd": "projectNamedParam",
        "see": "referenced=deploy$",
    },
    
    # Colon delimiter - parameter NOT referenced (should pass through)
    "namedparam.passthrough action:build": {
        "cmd": "namedparam.passthrough action:build",
        "pwd": "projectNamedParam",
        "see": "^no-substitution-here action:build$",
    },
    "namedparam.passthrough action:test": {
        "cmd": "namedparam.passthrough action:test",
        "pwd": "projectNamedParam",
        "see": "^no-substitution-here action:test$",
    },
    
    # Equals delimiter - parameter NOT referenced (should pass through)
    "namedparam.passthrough action=build": {
        "cmd": "namedparam.passthrough action=build",
        "pwd": "projectNamedParam",
        "see": "^no-substitution-here action=build$",
    },
    "namedparam.passthrough action=test": {
        "cmd": "namedparam.passthrough action=test",
        "pwd": "projectNamedParam",
        "see": "^no-substitution-here action=test$",
    },
    
    # ========== MULTIPLE PARAMETER TESTS ==========
    
    # Multiple parameters with colon delimiter - all referenced
    "namedparam.refMultiColon action:start target:finish": {
        "cmd": "namedparam.refMultiColon action:start target:finish",
        "pwd": "projectNamedParam",
        "see": "^start:finish:done$",
    },
    "namedparam.refMultiColon action:begin target:end": {
        "cmd": "namedparam.refMultiColon action:begin target:end",
        "pwd": "projectNamedParam",
        "see": "^begin:end:done$",
    },
    
    # Multiple parameters with equals delimiter - all referenced
    "namedparam.refMultiEquals action=start target=finish": {
        "cmd": "namedparam.refMultiEquals action=start target=finish",
        "pwd": "projectNamedParam",
        "see": "^start=finish=done$",
    },
    "namedparam.refMultiEquals action=begin target=end": {
        "cmd": "namedparam.refMultiEquals action=begin target=end",
        "pwd": "projectNamedParam",
        "see": "^begin=end=done$",
    },
    
    # ========== MIXED DELIMITER TESTS ==========
    
    # Mixed delimiters on different parameters - all referenced
    "namedparam.refMixed action:deploy target=production": {
        "cmd": "namedparam.refMixed action:deploy target=production",
        "pwd": "projectNamedParam",
        "see": "^deploy:production$",
    },
    "namedparam.refMixed action=build target:staging": {
        "cmd": "namedparam.refMixed action=build target:staging",
        "pwd": "projectNamedParam",
        "see": "^build:staging$",
    },
    
    # Multiple params with mixed delimiters - not all referenced (should pass through)
    "namedparam.passthroughEcho action:build target=staging": {
        "cmd": "namedparam.passthroughEcho action:build target=staging",
        "pwd": "projectNamedParam",
        "see": "^Original command action:build target=staging$",
    },
    "namedparam.passthroughEcho action=deploy target:prod": {
        "cmd": "namedparam.passthroughEcho action=deploy target:prod",
        "pwd": "projectNamedParam",
        "see": "^Original command action=deploy target:prod$",
    },
    
    # ========== PARTIAL REFERENCE TESTS ==========
    
    # One parameter referenced with colon, one passed through
    "namedparam.refPartial action:build mode:fast": {
        "cmd": "namedparam.refPartial action:build mode:fast",
        "pwd": "projectNamedParam",
        "see": "^Referenced:build mode:fast$",
    },
    "namedparam.refPartial action:deploy mode:slow": {
        "cmd": "namedparam.refPartial action:deploy mode:slow",
        "pwd": "projectNamedParam",
        "see": "^Referenced:deploy mode:slow$",
    },
    
    # One parameter referenced with equals, one passed through (command uses '=')
    "namedparam.refPartialEquals action=deploy mode=slow": {
        "cmd": "namedparam.refPartialEquals action=deploy mode=slow",
        "pwd": "projectNamedParam",
        "see": "^Referenced=deploy mode=slow$",
    },
    "namedparam.refPartialEquals action=build opt1=yes opt2=no": {
        "cmd": "namedparam.refPartialEquals action=build opt1=yes opt2=no",
        "pwd": "projectNamedParam",
        "see": "^Referenced=build opt1=yes opt2=no$",
    },
    
    # Multiple parameters, some referenced, some not (colon delimiter)
    "namedparam.refPartialMulti action:test cmd:deploy": {
        "cmd": "namedparam.refPartialMulti action:test cmd:deploy",
        "pwd": "projectNamedParam",
        "see": "^Action:test Command: passthrough cmd:deploy$",
    },
    # Multiple parameters, some referenced, some not (equals delimiter)
    "namedparam.refPartialMultiEquals action=build cmd=run": {
        "cmd": "namedparam.refPartialMultiEquals action=build cmd=run",
        "pwd": "projectNamedParam",
        "see": "^Action=build Command: passthrough cmd=run$",
    },
    
    # ========== DUPLICATE PARAMETER TESTS ==========
    
    # Same parameter referenced multiple times - colon delimiter
    "namedparam.refDuplicate action:test": {
        "cmd": "namedparam.refDuplicate action:test",
        "pwd": "projectNamedParam",
        "see": "^test-then-test$",
    },
    "namedparam.refDuplicate action:x": {
        "cmd": "namedparam.refDuplicate action:x",
        "pwd": "projectNamedParam",
        "see": "^x-then-x$",
    },
    
    # Same parameter referenced multiple times - equals delimiter
    "namedparam.refDuplicate action=deploy": {
        "cmd": "namedparam.refDuplicate action=deploy",
        "pwd": "projectNamedParam",
        "see": "^deploy-then-deploy$",
    },
    "namedparam.refDuplicate action=y": {
        "cmd": "namedparam.refDuplicate action=y",
        "pwd": "projectNamedParam",
        "see": "^y-then-y$",
    },
    
    # ========== PARAMETER POSITION TESTS ==========
    
    # Parameter in middle of command - colon delimiter
    "namedparam.refMiddle action:mid": {
        "cmd": "namedparam.refMiddle action:mid",
        "pwd": "projectNamedParam",
        "see": "^mid middle-text end$",
    },
    "namedparam.refMiddle action:center": {
        "cmd": "namedparam.refMiddle action:center",
        "pwd": "projectNamedParam",
        "see": "^center middle-text end$",
    },
    
    # Parameter in middle of command - equals delimiter
    "namedparam.refMiddle action=mid": {
        "cmd": "namedparam.refMiddle action=mid",
        "pwd": "projectNamedParam",
        "see": "^mid middle-text end$",
    },
    "namedparam.refMiddle action=center": {
        "cmd": "namedparam.refMiddle action=center",
        "pwd": "projectNamedParam",
        "see": "^center middle-text end$",
    },
    
    # Parameter at end of command - colon delimiter
    "namedparam.refEnd action:finish": {
        "cmd": "namedparam.refEnd action:finish",
        "pwd": "projectNamedParam",
        "see": "^start middle finish$",
    },
    "namedparam.refEnd action:x": {
        "cmd": "namedparam.refEnd action:x",
        "pwd": "projectNamedParam",
        "see": "^start middle x$",
    },
    
    # Parameter at end of command - equals delimiter
    "namedparam.refEnd action=complete": {
        "cmd": "namedparam.refEnd action=complete",
        "pwd": "projectNamedParam",
        "see": "^start middle complete$",
    },
    "namedparam.refEnd action=z": {
        "cmd": "namedparam.refEnd action=z",
        "pwd": "projectNamedParam",
        "see": "^start middle z$",
    },
    
    # ========== EDGE CASES AND COMBINATIONS ==========
    
    # Multiple parameters of same type with different delimiters (all referenced)
    "namedparam.refMultiColon action:deploy target:live": {
        "cmd": "namedparam.refMultiColon action:deploy target:live",
        "pwd": "projectNamedParam",
        "see": "^deploy:live:done$",
    },
    "namedparam.refMultiEquals action=deploy target=live": {
        "cmd": "namedparam.refMultiEquals action=deploy target=live",
        "pwd": "projectNamedParam",
        "see": "^deploy=live=done$",
    },
    
    # Pass through with multiple unreferenced parameters (order may vary due to hash iteration)
    "namedparam.passthrough x:y z:a": {
        "cmd": "namedparam.passthrough x:y z:a",
        "pwd": "projectNamedParam",
        "see": "no-substitution-here.*(x:y|z:a).*(x:y|z:a)",
    },
    "namedparam.passthrough x=1 y=2 z=3": {
        "cmd": "namedparam.passthrough x=1 y=2 z=3",
        "pwd": "projectNamedParam",
        "see": "no-substitution-here.*(x=1|y=2|z=3).*(x=1|y=2|z=3).*(x=1|y=2|z=3)",
    },
    
    # Mixed delimiter passthrough (order may vary)
    "namedparam.passthrough x:1 y=2 z:3": {
        "cmd": "namedparam.passthrough x:1 y=2 z:3",
        "pwd": "projectNamedParam",
        "see": "no-substitution-here.*(x:1|y=2|z:3).*(x:1|y=2|z:3).*(x:1|y=2|z:3)",
    },
    
    # Partial reference with multiple unreferenced params (order may vary for unreferenced)
    "namedparam.refPartial action:test mode:fast speed:high": {
        "cmd": "namedparam.refPartial action:test mode:fast speed:high",
        "pwd": "projectNamedParam",
        "see": "^Referenced:test (mode:fast|speed:high).*(mode:fast|speed:high)",
    },
    
    # ========== EMPTY VALUE TESTS ==========
    
    # Empty value with colon delimiter - referenced parameter
    "namedparam.refSingleColon action:": {
        "cmd": "namedparam.refSingleColon action:",
        "pwd": "projectNamedParam",
        "see": "^referenced:$",
    },
    
    # Empty value with equals delimiter - referenced parameter
    "namedparam.refSingleEquals action=": {
        "cmd": "namedparam.refSingleEquals action=",
        "pwd": "projectNamedParam",
        "see": "^referenced=$",
    },
    
    # Empty value with colon delimiter - passthrough (not referenced)
    "namedparam.passthrough action:": {
        "cmd": "namedparam.passthrough action:",
        "pwd": "projectNamedParam",
        "see": "^no-substitution-here action:$",
    },
    
    # Empty value with equals delimiter - passthrough (not referenced)
    "namedparam.passthrough action=": {
        "cmd": "namedparam.passthrough action=",
        "pwd": "projectNamedParam",
        "see": "^no-substitution-here action=$",
    },
    
    # Multiple parameters, one with empty value - all referenced
    "namedparam.refMultiColon action: target:done": {
        "cmd": "namedparam.refMultiColon action: target:done",
        "pwd": "projectNamedParam",
        "see": "^:done:done$",
    },
    "namedparam.refMultiColon action:start target:": {
        "cmd": "namedparam.refMultiColon action:start target:",
        "pwd": "projectNamedParam",
        "see": "^start::done$",
    },
    "namedparam.refMultiEquals action= target=done": {
        "cmd": "namedparam.refMultiEquals action= target=done",
        "pwd": "projectNamedParam",
        "see": "^=done=done$",
    },
    "namedparam.refMultiEquals action=start target=": {
        "cmd": "namedparam.refMultiEquals action=start target=",
        "pwd": "projectNamedParam",
        "see": "^start==done$",
    },
    
    # Mixed empty and non-empty values
    "namedparam.refMixed action: target=production": {
        "cmd": "namedparam.refMixed action: target=production",
        "pwd": "projectNamedParam",
        "see": "^:production$",
    },
    "namedparam.refMixed action=build target:": {
        "cmd": "namedparam.refMixed action=build target:",
        "pwd": "projectNamedParam",
        "see": "^build:$",
    },
    
    # Empty values in passthrough with multiple parameters
    "namedparam.passthrough x: y=": {
        "cmd": "namedparam.passthrough x: y=",
        "pwd": "projectNamedParam",
        "see": "no-substitution-here.*(x:|y=).*(x:|y=)",
    },
    "namedparam.passthrough x= y:": {
        "cmd": "namedparam.passthrough x= y:",
        "pwd": "projectNamedParam",
        "see": "no-substitution-here.*(x=|y:).*(x=|y:)",
    },
    
    # Partial reference with empty value
    "namedparam.refPartial action: mode=fast": {
        "cmd": "namedparam.refPartial action: mode=fast",
        "pwd": "projectNamedParam",
        "see": "^Referenced: mode=fast$",
    },
    "namedparam.refPartialEquals action= mode:slow": {
        "cmd": "namedparam.refPartialEquals action= mode:slow",
        "pwd": "projectNamedParam",
        "see": "^Referenced= mode:slow$",
    },
    
    # Duplicate parameter with empty value
    "namedparam.refDuplicate action:": {
        "cmd": "namedparam.refDuplicate action:",
        "pwd": "projectNamedParam",
        "see": "^-then-$",
    },
    "namedparam.refDuplicate action=": {
        "cmd": "namedparam.refDuplicate action=",
        "pwd": "projectNamedParam",
        "see": "^-then-$",
    },
    
    # Parameters in middle/end position with empty values
    "namedparam.refMiddle action:": {
        "cmd": "namedparam.refMiddle action:",
        "pwd": "projectNamedParam",
        "see": "^middle-text end$",
    },
    "namedparam.refEnd action=": {
        "cmd": "namedparam.refEnd action=",
        "pwd": "projectNamedParam",
        "see": "^start middle",
    },
}

