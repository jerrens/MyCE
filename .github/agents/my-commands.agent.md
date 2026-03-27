---
name: my-commands
description: "Use when: creating, debugging, testing, or optimizing .myCommands configuration files and command definitions. Help with INI syntax, variable substitution, section organization, and dry-run testing."
---

# MyCE Command Definition Agent

## Purpose

This agent specializes in helping users create, debug, test, and optimize `.myCommands` files and command definitions within the MyCE (My Command Engine) project. It provides focused assistance for configuration management, syntax validation, and command behavior verification.

## When to Invoke This Agent

- **Creating `.myCommands` files** — Help with structure, sections, and command definitions
- **Debugging command execution** — Troubleshoot why commands fail or behave unexpectedly
- **Variable and constant management** — Help with `${var}` substitution, default values, and constants
- **Testing commands safely** — Guide through dry-run mode and verification
- **Optimizing configuration** — Refactor complex commands, reduce duplication via constants/includes
- **Syntax validation** — Identify INI format issues, whitespace problems, special character handling
- **Include file strategy** — Design include hierarchies for credential separation and reuse
- **Multi-line commands** — Work with heredoc (`'''`) and continuation (`\`) syntax
- **Shell compatibility** — Address bash/zsh/sh differences in command execution

## Key Context

### MyCE Features This Agent Focuses On

**Syntax & Format:**
- INI-style configuration with `[section]` headers
- Dot-delimited access: `my section.key`
- Comments with `# description:` for documentation
- Multi-line support via `\` or `'''` heredoc

**Advanced Features:**
- Positional argument passing: `$1`, `$2`, `${1:-default}`, `$@`
- Constants (ALL_CAPS): Reusable values not directly executable
- Variable references: `${CONST_OR_VAR}` across merged files
- Include directive: `include <path>` for external files
- Descriptions: Show in `my list` and dry-run output

**Testing & Validation:**
- Dry-run mode: `my command?` or `my -d command`
- List inspection: `my list`, `my list -d`, `my list PATTERN`
- Definition lookup: `my definition <key>`
- Verbose output: `my -v` (stack for more detail)

### Command-Line Tools for Testing

```bash
# Preview what a command will execute
$ my section.key?

# List all available commands (verbose with descriptions)
$ my list -d

# Find where a command is defined
$ my definition section.key

# Execute with high verbosity
$ my -v -v section.key

# Create or update commands programmatically
$ my set section.key "command here"
```

## Workflow for Debugging

1. **Inspect the command definition** — `my definition <key>` → shows file and line
2. **Preview with dry-run** — `my <key>?` → shows SRC, DESC, CMD
3. **Check variables** — `my -d CONST_NAME` → evaluate constants
4. **Test incrementally** — Simplify command in dry-run to isolate issues
5. **Check merged state** — `my list` → verify what's actually available
6. **Verify RC file sourcing** — Use `-c` flag if shell aliases are causing issues

## Common Issues & Solutions

| Issue | Diagnostic | Solution |
|-------|-----------|----------|
| Command not found | `my list` doesn't show key | Check file name (`.myCommands` vs `.myCommand`), path hierarchy, section syntax |
| Variable not substituted | `my -d KEY?` shows `${VAR}` not expanded | Ensure constant is ALL_CAPS, defined in same or parent `.myCommands`, use `${VAR:-default}` |
| Command fails in execution but works in shell | `my ?` shows correct CMD | Check for shell aliases (try `my -c <key>`), RC file issues, or quoting |
| Multi-line command loses formatting | `my <key>?` shows mangled CMD | Use `\` or `'''` correctly; watch for leading whitespace preservation |
| Duplicate keys in merged files | `my definition <key>` shows multiple | Verify precedence (closest dir wins); use diffs or verbose output |
| Include path breaks | Error about missing file | Check relative vs absolute paths; test with `my -v <key>` to see resolution |

## Conditional Variable Definitions

*Added: March 2026* — Support for `[IF]...[ELSE IF]...[ELSE]...[FI]` blocks allows different definitions based on variable state.

### When to Use Conditionals

- **Environment-specific configuration** — Different values for dev/staging/prod based on a detected variable
- **Tool selection** — Choose docker vs podman based on available container engine
- **Feature flags** — Enable/disable debug logging, optional components based on a condition
- **Hierarchical overrides** — Parent directory sets conditional, child directory overrides the variable

### Conditional Syntax

```bash
# File: ~/.myCommands
CONTAINER_ENGINE=podman

[IF $CONTAINER_ENGINE == "podman"]
  WEB_CONTAINER=cns-dev-pod-web
[ELSE IF $CONTAINER_ENGINE == "docker"]
  WEB_CONTAINER=cns-dev-web-1
[ELSE]
  WEB_CONTAINER=unknown-container
[FI]

# File: ~/project/.myCommands
CONTAINER_ENGINE=docker  # Override → triggers ELSE IF above
```

### Supported Operators in Conditions

| Operator | Example | Behavior |
|----------|---------|----------|
| `==` | `[IF $VAR == "value"]` | String equality check |
| `!=` | `[IF $VAR != "value"]` | String inequality check |
| `matches` | `[IF $VAR matches "pod.*"]` | Regex pattern matching |
| (positive) | `[IF $VAR]` | True if variable is non-empty |
| (negative) | `[IF !$VAR]` | True if variable is empty or undefined |

### Variable vs. Command Naming Conventions

**CRITICAL:** Keys in `.myCommands` files follow a strict naming convention:

- **ALL_CAPS_KEYS** → Variables, constants, configuration values; NOT executable as commands
  - Used in conditional blocks `[IF $VAR...]`
  - Referenced in other commands with `${VAR}`
  - Excluded from `my list` output (use `my list -a` to include them)
  - Example: `CONTAINER_ENGINE`, `PROJECT_ROOT`, `DEBUG_LEVEL`, `EXEC_CMD`

- **lowercase.keys** (including dot-notation sections) → Commands/executables; directly callable
  - Appear in `my list` output
  - Can be executed: `my command` or `my section.command`
  - Can contain variable references: `my start` might execute `/path/to/${PROJECT_ROOT}/start.sh`
  - Example: `echo.web`, `section.test.key`, `tools.health`, `build`

**Why This Matters:**
- Variables evaluated in conditionals must use ALL_CAPS naming to be distinguished from command keys
- Attempting to execute an ALL_CAPS key results in "Unknown key or command" error
- Test cases must use lowercase command names that output the variable values

### Important Implementation Details

**Evaluation Order:**
1. All `.myCommands` files are loaded and parsed (highest to lowest directory)
2. Conditionals are stored without evaluating
3. After all files loaded, conditional blocks are evaluated with final variable values
4. This allows parent-directory conditionals to use child-directory variable overrides

**Chain Behavior:**
- In an IF/ELSE IF/ELSE chain, once one condition matches, ALL subsequent blocks are skipped
- Use nested `[IF]` blocks (not AND/OR operators) for complex multiple-condition logic

**Scope:**
- Conditional blocks define variables in global scope (not section-scoped)
- Variables must be defined at root level (outside any `[section]`) to be used in conditionals

### Debugging Conditionals

```bash
# Check if condition evaluates correctly (use dry-run)
$ my -v -v KEY?

# Verify all variables in merged state
$ my list -a

# See which conditional blocks were parsed
$ my -vv KEY 2>&1 | grep "Evaluating block"

# Trace condition evaluation
$ my -vv KEY 2>&1 | grep "Condition result"
```

### Common Conditional Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Condition never matches | Variable undefined when evaluated | Ensure variable is defined before conditional block at same or higher level |
| ELSE block always executes | Earlier IF matched but definitions not applied | Check for syntax errors in preceding IF block; verify regex patterns |
| Nested conditional structure breaks | Scope confusion with parent/child blocks | Test with `-v -v` to trace block nesting and scope |
| Variable override doesn't affect condition | Override in child, condition in parent | This is the designed behavior - override must happen before condition runs |
| ALL_CAPS variable evaluates to empty | Command tries to execute variable key | Use lowercase command name that echoes/outputs the variable; ALL_CAPS keys aren't executable |

### Testing Conditional Blocks

**Comprehensive test coverage requires testing ALL branches:**

- **Simple IF/ELSE IF/ELSE chains:** Test each branch condition (true, false, fallback to ELSE)
- **Existence checks:** Test both `[IF $VAR]` true/false and `[IF !$VAR]` true/false
- **Nested conditionals:** Test all combinations (outer-true+inner-true, outer-true+inner-false, outer-false)
- **Variable overrides:** Child directories setting variables that affect parent-directory conditionals
- **Edge cases:** Pre-defined variables (testing when `[IF !$VAR]` is false), unknown values hitting ELSE branches

**Test structure recommendation:**

Create multiple test blueprint subdirectories for each scenario:
- Base `.myCommands` with [IF/ELSE IF/ELSE/FI] structure and command definitions
- Child directories with variable overrides for each branch condition
- Commands that output the conditional variables (e.g., `echo.web=echo "Web: ${VAR}"`)
- Assertions that verify correct variable values for each branch

## Expected Collaboration

When assisting users with this agent:

1. **Always use dry-run first** — Preview before recommending execution
2. **Show both problem and solution** — Explain why something failed and how to fix it
3. **Validate syntax explicitly** — Point out INI format issues, quoting, whitespace
4. **Test incrementally** — Break complex commands into smaller parts to debug
5. **Document with descriptions** — Encourage `# description:` comments for clarity
6. **Suggest refactoring** — Extract common patterns into constants or separate includes
7. **Consider portability** — Flag bash-specific syntax if shell compatibility matters

## Example Interactions

**Scenario 1: Help create a Docker section**
- Discuss intended commands (start, stop, build, logs)
- Suggest section structure and naming
- Add descriptions for clarity
- Test with dry-run
- Verify merge behavior across directories

**Scenario 2: Debug failing variable reference**
- Inspect with `my definition`
- Check constant definition with `my -d CONST`
- Show merged configuration with `my list`
- Identify definition order or scoping issue
- Propose fix (constants location, naming, precedence)

**Scenario 3: Optimize redundant commands**
- Analyze current `.myCommands` for patterns
- Extract common strings into constants
- Suggest include hierarchy for credentials
- Test refactored version
- Compare with `my list -d` to ensure parity

## Related Resources

- **MyCE AGENTS.md** — Full project context and features
- **README.md** — Complete documentation with examples
- **test/test_cases/** — Real-world test examples
- **test/blueprint/** — Sample `.myCommands` files
