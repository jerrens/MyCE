<!-- spell-checker:ignore subshell MyCE -->

# Bash Syntax Support in MyCE

This guide documents the bash syntaxes that MyCE supports when parsing command definitions from `.myCommands` files.

> [!NOTE]
> This document was generated with AI assistance and may contain inaccuracies or errors.
> Please verify examples against the actual MyCE source and test suite and report any discrepancies found.

## Supported Bash Syntaxes

### 1. Command Substitution with Dollar-Parentheses

**Syntax:** `$(command)`

**Examples:**

```ini
# Simple command substitution in path
buildPath=$(echo /build)/system

# Nested command substitutions
version=$(echo $(git describe --tags))

# Command substitution with arguments
installer=$(find . -name install.sh)

# Multiple uses in single command
report=echo "Built by $(whoami) in $(pwd)"
```

### 2. Backtick Command Substitution (Legacy)

**Syntax:** `` `command` ``

**Examples:**

```ini
# Legacy backtick syntax (still supported)
binPath=`echo /usr/bin`/echo

# Multiple backtick substitutions
timestamp=echo "Started at `date` in `pwd`"
```

> [!NOTE]
> Backticks in `.myCommands` files may be evaluated by bash during file sourcing. Prefer `$(...)` syntax for better compatibility.

### 3. Single Quoted Strings

**Syntax:** `'...'`

Everything inside single quotes is treated literally—no variable expansion, no command substitution, no escaping.

**Examples:**

```ini
# Preserve literal dollar signs and variables
display=echo 'Price is $100 and VAR=$VAR'

# Preserve spaces without escaping
message=echo 'This is a multi word string'

# Combine with other syntaxes
combine=echo 'Literal' $(date)
```

### 4. Double Quoted Strings

**Syntax:** `"..."`

Double quotes allow variable expansion and command substitution, but protect spaces and most special characters.

**Examples:**

```ini
# Variables and command substitution work inside double quotes
display=echo "File created at $(date) by $USER"

# Spaces are preserved inside double quotes
message=echo "Multi word string stays intact"

# Combining with unquoted parts
full=echo "Start" middle "End"
```

### 5. Process Substitution (Input Form)

**Syntax:** `<(command)`

Provides input from a command's output.

**Examples:**

```ini
# Read from process substitution
compare=diff <(sort file1) <(sort file2)

# Use in pipe
analyze=cat <(echo "header") myfile

# Multiple process substitutions
merge=paste <(seq 1 10) <(seq 11 20)
```

### 6. Process Substitution (Output Form)

**Syntax:** `>(command)`

Sends output to a command's input.

**Examples:**

```ini
# Write to process substitution
tee_copy=tee >(cat > backup.txt)

# Log output while filtering
tee_filter=tee >(grep ERROR > errors.log)

# Multiple outputs
split_output=tee >(cat > file1) >(cat > file2)
```

### 7. Escaped Spaces

<!-- markdownlint-disable-next-line MD038 -->
**Syntax:** `\ ` (backslash-space)

A backslash escapes the next character, allowing spaces to be included in a single word without quoting.

**Examples:**

```ini
# Escaped space in command argument
space_cmd=echo hello\ world

# Useful in file paths
run=echo /path/to\ dir/with\ spaces/script

# Can combine with quotes
mixed=echo 'quoted' unquoted\ space quoted
```

### 8. Parameter Expansion

**Syntax:** `${VAR}`, `${VAR:-default}`, `${VAR:offset}`, `${VAR#pattern}`, etc.

Parameter expansion provides variable references with optional default values, substring extraction, and pattern removal.

**Examples:**

```ini
# Basic variable reference
path=echo ${HOME}/projects

# Default values
config=echo ${CONFIG_FILE:-/etc/default.conf}

# Substring operations
truncate=echo ${LONG_VAR:0:10}

# Pattern removal (trailing)
strip=echo ${PATH%:/usr/bin}

# Nested expansions
complex=echo ${FINAL_PATH#${PREFIX}/}
```

### 9. Mixed Syntax Combinations

You can freely combine any of the above syntaxes.

**Examples:**

```ini
# Mixed quotes and substitution
report=echo "Report generated on $(date) in $(pwd)"

# Escaped space with quotes
file=echo 'file\ name' "/escaped\ path"

# Nested and combined
complex=cat <(echo "Header") "$(dirname $0)/data.txt" output\ file

# Multiple substitution forms
multi=$(dirname $1)\ $(basename $2)
```

## Comprehensive Test Suite

MyCE includes 18 regression tests covering all supported bash syntaxes:

### Core Syntax Tests

- **subshell.subshellPath** - Command substitution `$(...)`
- **subshell.backtickPath** - Backtick substitution `` `...` ``
- **subshell.quotedArg** - Double-quoted arguments with spaces
- **subshell.singleQuotedArg** - Single-quoted literal preservation
- **subshell.processSub** - Process substitution input `<(...)`
- **subshell.complexExpansion** - Parameter expansion with special characters

### Edge Case Tests

- **subshell.processSubOut** - Process substitution output `>(...)`
- **subshell.escapedSpace** - Escaped spaces in command arguments
- **subshell.nestedSub** - Nested command substitution
- **subshell.mixedQuotes** - Single and double quotes together
- **subshell.quotedWithSub** - Command substitution inside double quotes
- **subshell.paramDefault** - Parameter expansion with default value
- **subshell.paramSubstr** - Parameter substring extraction
- **subshell.paramPattern** - Pattern removal in parameter expansion
- **subshell.multiSub** - Multiple consecutive substitutions in one word
- **subshell.subWithSpaces** - Spaces in substitution output preserved
- **subshell.escapedDollar** - Literal dollar sign with single quotes

## Common Usage Patterns

### Complex Command Paths

Use command substitution to compute executable paths dynamically:

```ini
# Path from variable
install=$(which npm)/npm-install

# Path from git repository
gitutil=$(git rev-parse --show-toplevel)/bin/util
```

### Commands with Conditional Output

Combine process substitution with comparison tools:

```ini
# Compare sorted outputs
diff_sorted=diff <(sort "$1") <(sort "$2")

# Filter and process
parse=grep pattern <(command)
```

### Multi-Step Processing

Chain multiple substitutions for complex workflows:

```ini
# Extract, format, and display
report=echo "Report for $(whoami) at $(date)" | tee >(mail admin)
```

### Template Commands

Use parameter expansion with defaults for flexible command templates:

```ini
# Port defaults to 8080 if not specified
server=node server.js --port ${PORT:-8080}

# Config path with fallback
deploy=./deploy.sh --config ${CONFIG_FILE:-/etc/deploy.conf}
```

## Tips and Best Practices

1. **Prefer `$(...)` over backticks** - More readable and nests better
2. **Quote command arguments** - Use `"..."` when arguments contain spaces
3. **Use single quotes for literal values** - Prevents accidental expansion
4. **Escape special characters** - Use `\$` for literal dollar signs
5. **Test complex commands** - Use `my command ?` to preview before execution
6. **Document with descriptions** - Add `# description:` comments for clarity

**Example:**

```ini
# description: Compile with optimization flags
build=$(find . -name Makefile)/Makefile \
  && make -f "$1" CFLAGS="${CFLAGS:-O2}"
```

## Further Reading

- See [README.md](../README.md) for general MyCE features
- Check [CHANGE_HISTORY.md](../CHANGE_HISTORY.md) for implementation details
- Review test cases in `/test/test_cases/command_substitution.py` for comprehensive examples
