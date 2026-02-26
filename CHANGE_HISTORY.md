<!-- spell-checker:ignore MYCE -->
# Change History

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
