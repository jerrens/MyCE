<!-- spell-checker:ignore MYCE -->
# Change History

## 26.7.10

* **Nested Command Invocation Syntax** - Added support for invoking another MyCE key inline using `${key args...}` inside command values
  * Enables concise alias chaining without needing to call `my` explicitly in the value (for example: `indir=${redir Hello}`)
  * First token inside `${...}` is treated as the command key, remaining tokens are passed as positional arguments to that nested key
  * Nested references resolve recursively with a depth guard to prevent infinite loops in cyclic definitions
  * Missing nested keys are preserved as-is and passed through to shell evaluation

## 26.7.8

* Increased variable substitution max loop count to avoid claiming infinite loop detection on complex/long commands

## 26.7.6

* **BugFix: Named Parameter Delimiter Preservation** - When a named parameter (e.g. `key:value`) is not referenced in the command definition, it was being reconstructed with `=` instead of the original delimiter
  * Arguments using `:` delimiter (e.g. `my artisan log:test-prints`) now correctly pass through as `log:test-prints` instead of `log=test-prints`
  * The original delimiter (`:` or `=`) is now captured during argument extraction and preserved when passing unconsumed parameters through to the underlying command

## 26.6.30

* **Enhanced Word Extraction Parser** - Replaced simple `read -ra` word splitting with bash syntax-aware character-by-character parser
  * Now properly handles command substitution `$(...)` with parenthesis depth tracking
  * Supports backtick command substitution `` `...` ``
  * Respects single quotes `'...'` and double quotes `"..."` with separate state tracking
  * Handles process substitution `<(...)` and `>(...)` with parenthesis nesting
  * Properly processes escaped characters via backslash escaping
  * Supports complex parameter expansion patterns `${VAR}`, `${VAR:offset}`, `${VAR#pattern}`, etc.
  * Fixed critical bug with boolean variable handling causing "1: command not found" errors
  * Fixed regex syntax error in process substitution detection pattern
* **Test Updates** - Added 18 subshell test cases with 12 new edge case variations

## 26.6.26

* **BugFix: Argument Expansion with Braced Syntax** - Fixed `${@}` and `${*}` expansion when combined with positional arguments
  * Regex pattern now detects both `$@`/`$*` and `${@}`/`${*}` forms (previously only detected unbraced forms)
  * Both braced and unbraced forms now expand correctly to include all arguments
* **Added Regression Tests** - Enhanced test coverage for argument expansion edge cases
  * All 8 new tests verify that `$@`/`${@}`/`$*`/`${*}` expand to ALL args (including referenced ones), distinguishing from `$@+`/`${@+}`/`$*+`/`${*+}` which expand to remaining args only

## 26.6.22

* **NEW FEATURE: Named Parameters** - Added support for `key=value` and `key:value` syntax for cleaner, more readable command definitions
  * Both `=` and `:` delimiters supported: `name=John` or `name:John`
  * Quoted values preserve spaces: `name="John Doe"` or `name='John Doe'`
  * Default value syntax: `${name:-Guest}` provides fallback for unreferenced parameters
  * Unconsumed parameters (not referenced in command definition) pass through to underlying command
  * Positional arguments ($1, $2, etc.) and named parameters work together seamlessly

## 26.6.11

* **NEW FEATURE: Remaining Arguments Syntax** - Added `$@+` and `$*+` for referencing non-referenced arguments
  * When command uses `$1` and `$3`, then `$@+` expands to args 2 and 4+ (skips referenced positions)
  * `$@+` preserves word boundaries (separate args), `$*+` joins to single string
  * Supports braced forms: `${@+}`, `${*+}`
  * Respects bash escaping: `\$@+` not expanded
  * Useful for extracting specific args while forwarding remaining args unchanged

## 26.5.21

* BugFix: commands inside `[IF]...[ELSE IF]...[ELSE]...[FI]` conditional blocks are now parsed and applied correctly
* Fixed conditional branch handling so only the matching block merges definitions

## 26.5.11

* BugFix: Output of dryrun does not preserve escaped characters and ANSI control
* Updated test.py to handle `cwd` as an argument to run_test function call and set in subprocess instead of chdir

## 26.4.30

* Added support for Heredoc style using double quotes
  * This form removes whitespace and results in a single line
  * Triple Single quote Heredoc style tweaked to maintain all whitespace
* Updated line continuation form to trim whitespace
* Fixed but where line count reference does not account for multiline values
* Changed zsh completion script path to be stored in `/usr/local/share/zsh/site-functions/_my`

## 26.4.29

* **ZSH Completion Support** - Added zsh autocompletion via new `auto-complete/_my.zsh` file
  * Installs to `/usr/share/zsh/site-functions/_my` when running `my update` from zsh
  * Detects shell type at runtime and installs appropriate completion file
* **Completion Directory Renamed** - Renamed `bash-completion/` to `auto-complete/` for clarity
  * `my.bash` → bash completion file
  * `_my.zsh` → zsh completion file
* **Update Script Improvements** - Refactored `update_script` function to detect shell type
  * Checks `$ZSH_VERSION` and `$BASH_VERSION` to determine shell
  * Single code path for installation with shell-specific paths defined inline
* **Documentation Updates** - Updated README.md and AGENTS.md to reflect new completion file locations
* **New Command** - Added `zsh` command to launch zsh container with MyCE and completion pre-configured

## 26.4.24

* **Improved Error Handling** - Enhanced "command not found" error reporting by filtering stderr to show only relevant errors while suppressing script-sourced shell errors
* **Logging Improvements** - Fixed logging to properly direct verbose output to stderr while keeping standard output clean for piping and command substitution
* **Shell Quoting & Escaping** - Fixed variable expansion issues throughout the script with proper quoting for commands, paths, and variable references
* **Code Cleanup** - Removed unused variables and commented-out code from conditional block handling
* **Test Enhancements** - Improved `test.py` output handling to properly combine and match stdout/stderr in any order, with added test summary statistics

## 26.4.21

* **NEW FEATURE: Definition Preview Shorthand** - Added support for trailing '@' character to quickly preview command definitions
  * Commands ending with '@' (e.g., `my command @`) show where the command is defined in .myCommands files
  * Similar to the existing '?' dry-run syntax but displays definition information instead of command execution
  * Shows "No definition found" for commands that don't exist in any .myCommands file
  * Provides quick access to definition information without needing to use the separate `definition` command

## 26.4.11

* Fix to allow ANSI colors from executed commands to flow through to the current terminal while still providing a helpful error to the user for unknown commands

## 26.3.30

* **BugFix: Some commands missing in  `my list` output and not available for autocomplete** - Fixed grep pattern that was incorrectly excluding commands with uppercase endings
* **Test Coverage:** Added regression tests ensuring mixed-case commands appear in list while all-uppercase variables remain excluded
* **BugFix: Update action not working as expected**
  * Changes introduced recently for printing source and description during dry runs modified the runCMD function arguments.
  * Reverted to previous signature and updated how Source location and description are looked up when DRYRUN mode is enabled, reducing unnecessary parameter passing
* **BugFix: Conditional definitions in sections not working**
  * Conditional keywords treated as section headers preventing `definition` command from finding keys inside `[section]` blocks
* **BugFix: Multi-word values corrupted**
  * Multi-word definition values split incorrectly by switching to newline separator
* **BugFix: Condition evaluation broken**
  * Log output corrupting condition results by using global variable instead of command substitution

## 26.3.28

* **NEW FEATURE: Conditional Variable Definitions** - Added support for `[IF]...[ELSE IF]...[ELSE]...[FI]` blocks to conditionally define variables based on variable values
  * Allows environment-specific configurations, tool selection, and feature flags from a single `.myCommands` file
  * Supports multiple operators: `==` (equality), `!=` (inequality), `matches` (regex), and existence checks `[IF $VAR]` / `[IF !$VAR]`
  * Conditionals are evaluated after all `.myCommands` files are loaded, enabling child-directory variable overrides to affect parent-directory conditional behavior
  * Proper IF/ELSE IF/ELSE chain short-circuiting prevents multiple branches from executing
* Enhanced documentation with comprehensive conditional examples and use cases in README.md
* Added extensive test coverage for conditional feature including:
  * All operator types (equality, inequality, regex matching, existence checks)
  * All conditional branches (IF, ELSE IF, ELSE fallback)
  * Nested conditional structures with multiple decision paths
  * Variable override scenarios where child directories affect parent conditionals
  * Edge cases like pre-defined variables blocking conditional definitions
* Updated agent documentation (AGENTS.md and my-commands.agent.md) with:
  * Key/value naming conventions (ALL_CAPS for variables, lowercase for commands)
  * Conditional implementation details and gotchas discovered during development
  * Comprehensive test coverage guidelines
  * Debugging techniques for tracing conditional evaluation

## 26.3.26

* Added support for optional command descriptions in `.myCommands` files using `# description: <text>` comment syntax
* Descriptions appear in the output of the following:
  * Dry-run preview (`my key ?` or `my -d key`) shows SRC (file location), DESC (description if defined), and CMD
  * `my definition <key>` shows descriptions alongside each file's definition
  * `my list -d [PATTERN]` displays commands with their descriptions in a two-column format
* File-specific descriptions allow different `.myCommands` files to provide descriptions for commands with the same key without cross-file inheritance
* Fallback formatting for systems without the `column` utility ensures descriptions display correctly on all platforms

## 26.3.24

* Removed extra print when using trailing '?' (view command mode)

## 26.3.17

* Fixed bug for key values that referenced `$@` for substitution

## 26.3.16

* Fixed error message when invalid syntax usd for set command
* Refactored test.py to load test cases from different files for easier test management
* Exit when unknown option given
* Return error when no key given with `definition` action
* Added several test cases

## 26.3.6

* Work towards zsh compatibility

## 26.3.5

* BugFix: Positional Argument Substitution at the beginning of a command may fail
* BugFix: Variable substitution at the beginning of a command may fail
* Optimized while look to break when no progress was made on variable substitutions
* Shell state protection: The original IFS is now saved at script start and restored on exit (including interrupts/errors) to prevent accidental shell state corruption.

## 26.2.25

* Added special dry-run syntax - add ' ?' at the end of a command to print the command that would be executed

## 26.2.23

* Bugfix: Legacy named .myCommand file in the home directory was not found if executing outside of the home directory tree
* BugFix: `update` action prompts in a (hidden) sub shell to overwrite existing files
* Added support for grep pattern to `list` action to filter results (e.g., `my list partial`)

## 26.2.19

* Added support for multiline entries in the .myCommand file using a continuation character '\'
* Heredoc support using ''' to allow for easier readability of multiline entries
* Added Magic Constant `__DIRECTORY` to allow referencing the directory of the .myCommand file being processed
* BugFix: Lines with CRLF line endings cause parsing anomalies.
  * Added line ending detection and provide user-friendly warning message about it being skipped

## 26.2.14

* Enhanced `update` subcommand to support targeting a specific release tag

## 26.2.13

* Provides a user-friendly error message if the given command is not known, while allowing STD_ERR output from executed commands to be passed on.
* Changed to using `type` command for checking if utility exist.
* Sources the shell's rc file to allow aliases defined there to be used.
  * The file to source can be specified by setting 'MYCE_RUNCOM' (default is ~/.bashrc)
  * This can be disabled by setting 'MYCE_RUNCOM=false'

## 26.2.6

* Added support for hiding variables (all uppercase letters) defined in sections.
* `update` command now retrieves latest released instead of latest committed.
* bash-completion file installed if the expected directory exists

## 26.1.26

* Added support for `include <file>` statements.

## 26.1.5

* Changing naming from '.myCommand' to '.myCommands' (added 's') for clarity.
* For backwards compatibility, will still check for 'myCommand' files.
* Default command file name can be overridden by defining 'MYCE_FILE_NAME' variable.
* Default column width for 'list' command can be overridden by defining 'MYCE_COLUMN_WIDTH' variable.

## 25.12.18

* BugFix: Nested substitutions not handled correctly
* BugFix: Positional arguments not handled correctly

## 25.12.10

* BugFix: Infinite loop possible when an expanded reference contains a variable that was already expanded

## 25.12.9

* Added support for default values in variable references (e.g., ${VAR_NAME:-default})

## 25.11.7

* Added `definition <key>` command
* Removed duplicate processing of .myCommand in user's home directory
* Dry-run output now escapes \n instead of interpretting as a new line
* Added COLUMN_WIDTH variable to reduce column width when printing list
* Added `-a` option to `list` command to include variables in output (for auto-complete)

## 24.11.28

* Added 'help' output and additional log output

## 24.11.12

* Improvements to 'update' command handling.
* Added 'update diff' command.

## 24.11.8

* Added 'update' command

## 24.11.7

* Added support for positional args ($1, $2) within the .myCommand values
* Always load the .myCommand file in the user home directory (even if not in current directory tree)

## 24.10.16

* BugFix: Replacing variables in array when merging causes order issues

## 24.10.15.1731

* Added code to preserve command order
* Partial command match no longer supported
* BugFix: Infinite loops possible by variable dereferencing

## 24.10.15.1457

* Unknown variable references are passed on to eval

## 24.10.15

* BugFix: Commands containing \n not processed correctly

## 24.10.14

* Added support to combine all .myCommand files in the directory tree
* Added support for INI section grouping
* Changed 'add' command to 'set'

## 24.10.10

* Added support for surrounding variables with '{}'

## 24.10.9.1616

* Fix to preserve quotes around arguments when passing

## 24.10.9

* Added 'list' command

## 24.10.7.1312

* Changed to using file ".myCommand" as default

## 24.10.7.1216

* Added ability to define variables within the .myVersion file that can be referenced and expanded in the key values

## 24.10.7

* Initial Creation
