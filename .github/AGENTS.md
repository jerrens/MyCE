---
description: "MyCE (My Command Engine) - Context for all agents working on this Bash command scripting project"
---

# MyCE Project Context for Agents

## Project Summary

**MyCE (My Command Engine)** is a pure Bash command engine that enables hierarchical, context-aware project commands stored in `.myCommands` files. It eliminates the need for global aliases by providing scoped, mergeable command definitions throughout the directory tree.

**Key Strengths:**

- No external dependencies (pure Bash)
- Context-aware: commands inherit from parent directories
- INI-style configuration with dot-delimited sections
- Smart argument passing and variable substitution
- Transparent fallback to shell when key not found
- Dry-run mode with `?` suffix for safe inspection

## Script Overview

**Main Script:** `my` (executable Bash script)

### Core Features

1. **Hierarchical Command Lookup**
   - Searches from `~/.myCommands` → root → current directory
   - Merges configurations: closest directory takes precedence
   - Supports `.myCommand` (legacy) and `.myCommands` (current)

2. **Configuration Format**
   - INI-style syntax with optional sections: `[section]`
   - Access via dot notation: `my section.command`
   - Key-value pairs: `command="full command here"`

3. **Advanced Syntax**
   - **Positional args:** `$1`, `$2`, `$@`, `$*`
   - **Default values:** `${1:-defaultValue}`
   - **Multi-line commands:** Use `\` or `'''` heredoc
   - **Descriptions:** `# description: Text` before command
   - **Constants:** ALL_CAPS keys (not executable, used in other commands)
   - **Includes:** `include <path>` for importing other files
   - **Conditionals:** `[IF]...[ELSE IF]...[ELSE]...[FI]` blocks for variable-based definitions (NEW - March 2026)

4. **Built-in Commands**
   - `my list [-l] [-a] [-d] [PATTERN]` — List available keys
   - `my definition <key>` — Show where key is defined
   - `my set <key> <command>` — Add/update command in `.myCommands`
   - `my help` — Show usage
   - `my version` — Show version
   - `my COMMAND?` — Dry-run (preview what would execute)

5. **Command-line Options**
   - `-d` — Dry-run mode (preview command)
   - `-v` — Verbose output (stack for more verbosity)
   - `-c` — Skip shell RC file sourcing

6. **Dry-run Modes**
   - **Suffix syntax:** `my server.start?` (quick preview)
   - **Flag syntax:** `my -d server.start` (explicit)
   - **Output:** SRC (file:line), DESC (description), CMD (evaluated command)

## Common Workflows

### Creating `.myCommands` Files

```ini
# ~/.myCommands (home-level commands)
[tools]
# description: Show current date and time
now=date +%T

[docker]
# description: Start Docker containers
start=docker-compose up -d
stop=docker-compose down
ps=docker ps -a

# description: Build Docker image with tag
build=docker build -t ${1:-myImage} .
```

### Using Variables and Defaults

```ini
[build]
# description: Build project (optional target)
project=pushd "$PROJECT_ROOT" && ./build.sh ${1:-default}

[vars]
# Constants for reuse
PROJECT_ROOT=/path/to/project
BUILD_CMD=make build
```

### Testing Before Execution

```bash
# Inspect what the command will do
$ my server.start?
# Output:
# SRC: /home/user/.myCommands:5
# DESC: Start development server
# CMD: npm run dev

# Arrow-up to recall, remove ? and execute
$ my server.start
```

## File Structure

```shell
.myCommands
  ├─ [section1]
  │   └─ command_key=command_value
  ├─ [section2]
  │   ├─ CONST_VAR=value
  │   └─ command=${CONST_VAR} with args
  └─ include ../shared/.myCommands
```

## Key Behaviors to Understand

1. **Fallback to Shell:** If a key is not found, the script passes the argument to the shell as-is
2. **RC File Sourcing:** By default, shell RC files (`.bashrc`, `.zshrc`) are sourced before execution to support aliases
3. **Description Extraction:** Descriptions from `# description:` comments are shown in `list` and dry-run output
4. **Constants Are Ignored:** All-uppercase keys don't appear in `my list` output unless `-a` flag is used
5. **Merge Order:** Root → directories → current → closest to pwd takes priority
6. **Include Paths:** Both absolute and relative paths work with `include` directive
7. **Key Naming Convention:** ALL_CAPS keys are variables/constants (not executable); lowercase keys are commands (executable)
   - `CONTAINER_ENGINE`, `PROJECT_ROOT`, `DEBUG_LEVEL` (variables) ≠ `echo.web`, `docker.start`, `tools.health` (commands)
   - Attempting to execute ALL_CAPS keys results in "Unknown key or command"
   - Variables are referenced in conditionals and command definitions using `${var_name}`
8. **Conditionals Evaluation:** Conditional blocks are parsed during file loading but evaluated AFTER all files are loaded, allowing child-directory variable overrides to affect parent-directory conditionals (NEW - March 2026)

### Conditionals: New Feature (March 2026)

Conditional blocks `[IF]...[ELSE IF]...[ELSE]...[FI]` allow variable-dependent definitions:

```ini
# ~/.myCommands
CONTAINER_ENGINE=podman

[IF $CONTAINER_ENGINE == "podman"]
  POD_CMD=podman
[ELSE IF $CONTAINER_ENGINE == "docker"]
  POD_CMD=docker
[ELSE]
  POD_CMD=unknown
[FI]

# ~/work/.myCommands
CONTAINER_ENGINE=docker  # Override → affects conditional above
```

**Implementation Key Points:**

- Conditionals are **stored without evaluating** during file parsing
- **Final evaluation** happens after all `.myCommands` files are loaded (ensuring all variable values are resolved)
- Conditions compare variables to literal values: `[IF $VAR == "value"]`, `[IF $VAR != "value"]`, `[IF $VAR matches "regex"]`, `[IF $VAR]`, `[IF !$VAR]`
- IF/ELSE IF/ELSE chains properly short-circuit: once one condition matches, subsequent blocks in that chain are skipped
- Variables used in conditions must be at root scope (not section-scoped)

**Technical Implementation:**

- `process_ini_file()` detects `[IF]`, `[ELSE IF]`, `[ELSE]`, `[FI]` bracket syntax and stores definitions without applying them
- New associative arrays: `conditionalConditions[]`, `conditionalDefinitions[]`, `conditionalBlockOrder[]`
- `evaluate_conditionals()` processes blocks after `load_my_custom_files()`, enabling cross-file variable dependencies
- `__evaluate_condition()` helper evaluates condition expressions using already-loaded variable values
- Output must redirect to stderr (not stdout) to avoid interfering with command substitution

## Development Context

- **Language:** Bash (POSIX-compatible where possible)
- **Version:** 26.3.26
- **Author:** Jerren Saunders
- **Test Suite:** Located in `test/` directory with test cases for various features
- **Documentation:** README.md with comprehensive feature guide
- **Bash Completion:** `bash-completion/my` for shell completions

## Agent Guidelines

When working on MyCE tasks:

1. **Testing Commands:** Always use dry-run mode (`?` suffix) to preview commands before recommending execution
2. **Absolute Paths When Testing:** Use the full path to the `my` script under development: `/path/to/MyCE/my` instead of just `my`
   - Multiple versions of `my` may exist on a system (global install vs. development repo)
   - `which my` may not point to the development copy
   - Code changes only take effect when invoking the correct script
   - Users should find repo root with: `git rev-parse --show-toplevel`
3. **Syntax Validation:** Understand INI format edge cases (colons, special chars, whitespace)
4. **Variable vs. Command Naming:**
   - ALL_CAPS keys are variables (config values, conditional references) — NOT directly executable
   - lowercase keys are commands (callable with `my command`) — appear in `my list`
   - Keys in sections are stored as `section.key` and follow same naming rules (only final segment matters for command vs. variable)
   - Never try to execute a variable with `my VARIABLE` — create a lowercase command that outputs the variable instead
5. **Variable Scope:** Remember that variables work across merged `.myCommands` files but closest file wins
6. **Include Paths:** When suggesting includes, clarify absolute vs. relative path context
7. **Shell Compatibility:** Consider bash compatibility (not all features work in all shells)
8. **Help Content:** Reference the built-in help with `my help` for accurate command syntax
9. **Conditionals:** When using `[IF]` blocks, remember they evaluate after all files load; child-directory variable overrides will affect parent-directory conditionals

## Implementation Notes for Future Developers

### Important Gotchas Discovered During Conditional Implementation

1. **Log Output to stderr, Not stdout**
   - The `log()` function was redirecting to stdout, which interfered with command substitution: `condition=$(__evaluate_condition "...")`
   - Fixed by redirecting all log output to `>&2`
   - Lesson: Any logging mixed with return values will cause subtle bugs

2. **Variable Resolution Timing**
   - Conditionals must be evaluated AFTER all `.myCommands` files are loaded so that final variable values (after merging) are available
   - If evaluating during file parsing, child-directory overrides wouldn't affect parent-directory conditionals
   - Solution: Two-phase approach - parse and store without evaluating, then evaluate in `find_and_run_cmd()` after `load_my_custom_files()`

3. **IF/ELSE IF/ELSE Chain Handling**
   - Simple boolean checks don't work for chains (e.g., evaluating all blocks and applying all true ones)
   - Must track which chains have matched per source file to skip subsequent conditions
   - Implemented with `chain_matched[]` associative array keyed by filename

4. **Bracket Syntax vs Shell Syntax**
   - Initial design used shell-like `IF ... FI` (no brackets)
   - Switched to `[IF ...]...[FI]` for clarity and INI consistency
   - Benefits: Unambiguous parsing, consistent with `[section]` syntax, easy to distinguish from key=value lines

5. **Key Naming Convention (ALL_CAPS vs Lowercase)**
   - ALL_CAPS keys are variables/constants; lowercase keys are commands
   - Attempting to execute an ALL_CAPS variable as a command returns "Unknown key or command"
   - Test cases must use lowercase command definitions that output/echo the conditional variables
   - Example: Don't test `my OPTIONAL_VAR`, instead define `echo.optional=echo "Optional var is: ${OPTIONAL_VAR}"` and test `my echo.optional`

6. **ELSE IF Condition Parsing**
   - ELSE IF blocks must be distinguished from simple IF blocks during parsing to properly track chain membership
   - Initial implementation stored both as plain conditions, causing all branches to evaluate
   - Solution: Prefix ELSE IF conditions with "ELSE IF: " during parsing, then strip before evaluation
   - Lesson: Condition metadata matters for proper chain short-circuiting behavior

### Testing Conditionals

- Test cases in `test/test_cases/conditionals.py`
- Blueprint files in `test/blueprint/projectConditionals/` with hierarchical directory structure
- Verify parent-directory conditionals with child-directory variable overrides using multiple test directories
- Use `-vv` or `-vvv` flags to trace condition evaluation: `my -vv KEY 2>&1 | grep "Evaluating block"`

**Comprehensive Coverage Requirements:**

- Test every branch of IF/ELSE IF/ELSE chains (not just happy path)
- Test existence checks with variables both set and undefined
- Test nested conditional structures with all paths (outer-true+inner-true, outer-false, etc.)
- Test variable override scenarios where child directories affect parent conditionals
- Test edge cases like pre-defined variables blocking conditional definitions
- Create separate test subdirectories for each scenario rather than testing multiple branches from same location

## Related Resources

- **README.md** — Full feature documentation and examples
- **CHANGE_HISTORY.md** — Version history and changelog
- **test/** — Test suite with real-world examples
- **bash-completion/my** — Shell completion definitions
