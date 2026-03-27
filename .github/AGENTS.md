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
build=docker build -t ${1:-myimage} .
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

```
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
2. **Syntax Validation:** Understand INI format edge cases (colons, special chars, whitespace)
3. **Variable Scope:** Remember that variables work across merged `.myCommands` files but closest file wins
4. **Include Paths:** When suggesting includes, clarify absolute vs. relative path context
5. **Shell Compatibility:** Consider bash compatibility (not all features work in all shells)
6. **Help Content:** Reference the built-in help with `my help` for accurate command syntax

## Related Resources

- **README.md** — Full feature documentation and examples
- **CHANGE_HISTORY.md** — Version history and changelog
- **test/** — Test suite with real-world examples
- **bash-completion/my** — Shell completion definitions
