<!-- markdownlint-configure-file {
    "no-inline-html": {
        "allowed_elements": [ "div" ]
    },
    "no-multiple-blanks": {
        "maximum": 4
    }
}
-->
<!-- spell-checker:ignore MyCE sdiff kshrc -->
<div align="center"><img src="./logo/MyCEv2.png" alt="MyCE Logo"></div>

# My Command Engine (MyCE)


## Overview

My Command Engine or MyCE (as in "Mice") is a powerful, context-aware command-line tool, written intirely in bash, and designed to streamline project workflows by utilizing custom command definitions stored in `.myCommands` files within the directory tree.
It searches for `.myCommands` files from the root down to the current directory, merging commands to create a localized and context-sensitive command set.
The `~/.myCommands` file will always be processed first, even if not executed within your $HOME directory.
This tool is ideal for developers who frequently switch between projects or environments and need specific commands scoped to each context.

```ini
[server]
start="docker-compose up"
stop="docker-compose down"
```

Running `my server.start` will execute docker-compose up.


## Features

- **Context-Aware Commands**: Executes commands based on the `.myCommands` file located in the current directory or its parent directories.
- **Scoped Command Aliases**: Each directory (or project) can define its own command aliases without impacting other directories.
- **Ease of Use**: A simple command `my <key>` is all you need to invoke the corresponding full command defined in the `.myCommands` file.
- **Recursive Lookup**: If a `.myCommands` file is not found in the current directory, the script searches parent directories until one is found.
- **Merged Configurations**: Reads `.myCommands` files from the root directory down to the present working directory, merging them to build a complete command set. If duplicates are found, the command closest to the current directory takes precedence.
- **Sectioned Commands**: Uses INI-style sections in `.myCommands` files to organize and access commands with dot-delimited syntax. This allows grouping related commands for better clarity and organization:
- **Positional Args**: Values within the `.myCommands` file can use positional argument references (ie $1, $2, ${3})
- **Default Variable Values**: Default values for variables may be set using the following syntax: `${1:-defaultValue}` or `${CONST:-defaultValue}`
- **Argument Passing**: Additional arguments provided after the command alias are passed directly to the underlying command. This enables dynamic behavior and flexible command usage.
- **Fallback to Shell**: If the requested alias is not found in the merged `.myCommands` configurations, the script will pass the command to the shell, allowing standard shell commands to work seamlessly with `my`.
- **Cross-Domain Commands with Variables**: Commands can reference variables set in different `.myCommands` files, allowing for reusable, high-level command configurations across directories. This feature is useful for defining generic commands in higher-level folders and reusing them in specific contexts within the workspace.
- **Include Files**: Other files can be included for re-use and/or keeping secret credentials in separate files


## Usage

### Basic Structure of `.myCommands` File

The `.myCommands` files uses INI-style sections to allow optional grouping, and key-value pairs where each key is an alias for a command, and the value is the corresponding command.

### Constants

Keys that are to be used internally to store reusable values in other commands (not commands to be executed) can be defined using all capital letters and the underscore character (`[A-Z_]`).
Keys that are fully uppercase are:
* Ignored by default by the `list` command (use `-a` flag to view)
* Cannot not be executed directly (ie. `my CONST`)
* Can be referenced in other commands using the following syntax: `build=pushd "$WORKSPACE_ROOT" && ...`

If you wish to view the evaluated value of a constant, you can use the dry-run flag (ie. `my -d CONST`).
Constants are also included in the output of the `definition` location action.

#### Importing other files

Other files may be included by using the `include <FILE>` syntax.
The path may be absolute or relative and should follow the same INI-style syntax.
If you want to include `.myCommands` in source control, it is recommended that you take advantage of this feature to store your credentials in a separate file.

#### Multi-line Commands

Values may span multiple lines by ending the line with a `\` char or using the `'''` heredoc style.
When using either of these continuation forms, any whitespace at the beginning of the consecutive line(s) will be preserved.

#### Magic/Built-In Constants

While most variables are not expanded until execution time (after all `.myCommands` files have been processed and merged), there are special variables that are expanded when parsing through `.myCommands` file entries.
These magic constants allow dynamically setting values based on the current details of the `.myCommands` file.

##### `__DIRECTORY__`

References to this magic constant will be replaced with the abolute path of the directory the current `.myCommands` file is stored (ie. `dirname .myCommands`).
This can be used to set a constant (like `WORKSPACE_ROOT`) inside a `.myCommands` file in the root of your project workspace, that can be used in command entries that need to be executed from the workspace root directory regardless of how deep in the workspace directory tree you may be.

#### Example `.myCommands` file

```ini
# Include other files
include credentials.secret

# Variables
LAST_CONTAINER="podman exec -it"
DB_CONTAINER="pod-db"

WORKSPACE_ROOT=__DIRECTORY__

# Commands
echo=echo "Custom Prefix: "
npm="$LAST_CONTAINER npm"

continuation=echo "This is a multi-line command \
that should be treated as a single command"

heredoc=echo -e '''
"This is a heredoc multiline value.
It will be included in the value with line wraps
    and indentation preserved."
'''

deploy=${WORKSPACE_ROOT}/vendor/bin/envoy run deploy

[db]
backup=podman exec --interactive --tty --rm $DB_CONTAINER mongodump
restore=podman exec --interactive --tty --rm $DB_CONTAINER mongorestore
```

### Running the my Script

Create a `.myCommands` file in the root of your project or any directory where you want to define custom commands.
Run the `my` script followed by the *alias* you want to execute, and any additional arguments you may want to pass.
For example, if you're in a directory with the previous `.myCommands` file:

```bash
# Usage:
#    my <alias>

~>$ my echo Hello World
Custom Prefix: Hello World

~>$ my db.backup --gzip
# Runs: podman exec --interactive --tty --rm pod-db mongodump --gzip
```

## Actions

The `my` script has the following internal commands.
These commands take priority over any keys or aliases of the same name that are defined in any `.myCommands` files, ***so consider them reserved keywords.***

### `help`

Don't worry if you forget the basics.
Simply type `my help` to view the usage details.

```shell
>$ my help

This script will search the current directory tree for a file named '.myCommands', containing
a key that matches the first argument.  If found, the value of that key will be used instead.
This can be used to allow local overriding of certain commands to point to a container
instead of the local installed command.

USAGE:
    my [OPTIONS] [help | version | set | list [-l] [-a] [PATTERN] | KEY [args...]] [?]

        <KEY> [...args]             The key of the command to run

        list [-l] [-a] [PATTERN]    List the available command keys.
                                    Include the '-l' arg to list one key per line.  Default is column view.
                                    Include the '-a' arg to include variables (uppercase)
                                    Include a PATTERN to filter the results.
                                        Use grep pattern syntax (e.g., \`my list prod\`)

        definition <key>            Identifies the file(s) the given key exist in.

        set <key> <command>         Adds or updates the 'key' to the '${MY_CUSTOM_FILE}' file in the current directory.
                                    The given command will be used whenever called from this level or a descendant.

        update [diff]               Update the script with the latest version.
                                    If 'diff' is given, then show the changes

        ?                           If the command ends with a '?' character, then dry-run mode will be enabled.
                                    This is a special syntax for dry-run mode that can be quickly used to check the command.
                                    Then use the UP arrow to recall the previous command and easily remove the dry-run syntax for execution.

        help                        Show usage
        version                     Show version number

    OPTIONS:
        -c      Run the command without sourcing the default shell rc file
        -v      Verbose Level (Multiple may be given to increase the verbosity)
        -d      Dry Run.  A trailing '?' may also be used as a special syntax to enable dry-run mode.


 By: Jerren Saunders
 Version: 26.2.25
```

### `version`:

Not sure if you have the latest version installed?
Run `my version` and compare against the latest version on [GitHub](https://github.com/jerrens/MyCE/releases).


### `set <cmd> <value>`:

> [!CAUTION]
> **Experimental!**

This command may be used to add a new value to the `.myCommands` file in the current directory.
The first argument is the key/alias, all remaining arguments will be treated as the value.
If the command should belong inside an INI section, then use a '.' to separate group from the key.
For example:

```bash
my set group.key echo "Hello World"
```

Will be stored as:

```ini
[group]
key=echo "Hello World"
```

### `list [-l] [-a] [PATTERN]`:

Can't remember what you used as the key?
Just enter `my list` to view the available commands.
If you don't like columns, add the `-l` option at the end to show one command per line.
If you want to view all definitions (including variables), add the `-a` option.

```shell
>$ my list
The following commands are available:
projA.env.backup                pod.log                         swap.on
projA.env.diff                  pod.ls                          swap.status
projA.env.view                  pod.replace                     test.dblpos1
projB.env.backup                pod.replace+                    test.dblpos2
projB.env.diff                  pod.run                         test.dblpos3
```

If you remember part of the command, add a grep pattern as an option filter the responses

```shell
>$ my list ^projB
The following commands are available:
projB.env.backup                projB.env.diff
```


### `definition <cmd>`:

It can be easy to forget which `.myCommands` file you added a definition especially if you're attempting to edit it.
To help locate which file(s) a certain command is defined, you can use the `definition` action to show it's references.

The output will contain the full file path, line number, command reference (section and command), and the value (no substitutions) given in that file.

```shell
 ~/code/MyCE/tests/projectB>$ my definition pod.ls
/home/jerren/.myCommand:91                       [pod]⇒ ls    podman ps --all --format "table  {{.Image}}  {{.RunningFor}}  {{.Status}}  {{.Names}}  "
/home/jerren/code/MyCE/.myCommands:94       [pod]⇒ ls    podman ps --all --format "table  {{.Image}}  {{.RunningFor}}  {{.Status}}  {{.Names}}  "
/home/jerren/code/MyCE/tests/.myCommands:7  [pod]⇒ ls    ${pod.CONTAINER_EXE} ps --all --format "table  {{.Image}}  {{.RunningFor}}  {{.Status}}  {{.Names}}  "
```


### `update [diff] [latest|released|head|main|<TAG>]`:

Easily pull down updates from the github repo.
The file will automatically update the MyCE script (typically `/usr/local/bin`) and the permissions set to 755.
This command needs to be run with root level privileges.
If not, it will attempt to elevate itself and prompt for a password if needed.

If you only want to view the changes (uses `sdiff`) between your local version and the latest version on GitHub, you can use `my update diff`.
You can also reference a version tag with the diff command.
If not specified, the latest released version will be assumed.

By default, the latest released version will be installed.
You can explicitly reference this with either `my
If you want to grab the latest version from the `main` branch, specify either `head` or `main`.

You may roll-back to a previously release version by specifying the tag.
To view all available tags, see [GitHub Repo Tags](https://github.com/jerrens/MyCE/tags).

```shell
my update diff
my update diff head
my update diff v26.2.13

my update head
my update v26.2.13
```


## Options

> [!IMPORTANT]
> Options for the `my` script should be added immediately following the `my` script call (before the key).

### `-v | -vv | -vvv`:
Log prints can be enabled for debugging by including the `-v` option.
Crank up the level by stacking more (`-vv`, `-vvv`).
Three levels is currently the most verbosity used in log prints, but if you get a little trigger happy with the `v` key, it will be ok :smiley:.

```shell
my -v build
my -vv build
my -vvv build
```

### `-d`:
Curious how your `.myCommands` entries will expand, but not brave enough to just try?
A dry run can be enabled by using the `-d` option.

> [!TIP]
> In dry run mode, the expanded command will be printed, but not executed

```shell
>$ my -d pod.con
---- THIS IS A DRYRUN! ----

CMD: podman exec -it my-container bash 
```

### `-c`:
Include this option if you don't want your shell rc file to expand for this execution.
To always disable sourcing the shell rc file, see [MYCE_RUNCOM](#myce_runcom).

```shell
my -c build
```

### `?`
A shorthand to preview the command that will be expanded, but not actually run the command is available by adding a trailing ` ?` on the command.
When a command that ends with `?` is detected, MyCE will interpret this as a request to print the final command to be executed (and will remove the '?' char).
This shorthand syntax makes it easy to question the command that will be executed, then if it is the command you want, you can:
1. Press UP-ARROW to recall the previous command from history
1. Press BACKSPACE to remove the '?' char
1. Press ENTER to execute the command

```shell
>$ my pod.con ?
---- THIS IS A DRYRUN! ----

CMD: podman exec -it my-container bash 
>$ my pod.con 
root@my-container:/var/www/html# 

```


## How it Works - Command Lookup Process

If you're reading this section, welcome fellow nerd :nerd_face:!

1. **Merging and Overriding**:
    The script starts with `~/.myCommands` file if it exists, then moves to the root directory and works down to the current directory (pwd), merging any `.myCommands` files found along the way.
    Any collisions with duplicate keys names will overwrite previous definition values.
    This means that commands defined in `.myCommands` files closer to the current directory override duplicates from higher-level directories.
    This makes the command engine adaptable for different projects, but also allows for globally defined aliases.
    It is important to note that the definitions are not processed during this step, so no variable substitutions will be performed.

2. **Sectioned Access**:
    Commands are referenced using `section.key` syntax if using INI-style sections.

3. **Fallback to Shell**:
    If no matching alias is found, the command is sent to the shell for evaluation.

### Handling Variables Across Directories

Variables can be set in `.myCommands` files at any directory level and accessed by commands in lower directories, allowing for flexible and reusable configurations.
To define a variable, use only uppercase letters, underscores, and dashes (ie `/[A-Z_-]/`).
Variables may be defined inside of a section if desired for better organization of your definitions.
These variables are excluded from the output the `list` subcommand by default unless the `-a` option is specified.

#### Example Hierarchy

```ini
# ~/code/.myCommands
UBUNTU_IMAGE=ubuntu:22.04

[pod]
CONTAINER_EXE=podman

ls=${pod.CONTAINER_EXE} ps --all --format "table  {{.Image}}  {{.RunningFor}}  {{.Status}}  {{.Names}}  "
dist=${pod.CONTAINER_EXE} run -it --rm ${UBUNTU_IMAGE} bash -c "cat /etc/lsb-release | grep DESCRIPTION"
terminal=${pod.CONTAINER_EXE} run -it --rm ${UBUNTU_IMAGE} bash
```

```ini
# ~/code/project_B/.myCommand
UBUNTU_IMAGE=ubuntu:20.04

[pod]
CONTAINER_EXE=docker
```

```bash
~/code/projectA>$ my pod.dist
# CMD: podman run -it --rm ubuntu:22.04 bash -c "grep DESCRIPTION /etc/lsb-release | cut -d'=' -f2"
"Ubuntu 22.04.5 LTS"

~/code/projectB>$ my pod.dist
# CMD: docker run -it --rm ubuntu:20.04 bash -c "grep DESCRIPTION /etc/lsb-release | cut -d'=' -f2"
"Ubuntu 20.04.6 LTS"
# Notice this used docker and Ubuntu 20.04 instead of podman and 22.04

~/code/projectC>$ my pod.dist
# CMD: podman run -it --rm ubuntu:22.04 bash -c "grep DESCRIPTION /etc/lsb-release | cut -d'=' -f2"
"Ubuntu 22.04.5 LTS"
```

### Include Files

Other files may be included by adding a `include <FILE>` line in a `.myCommands` file.
The key-values defined in the referenced file will be processed as soon as the line is detected.
This means that any definitions in the included file will overwrite any previously defined values and will be overwritten by any values processed later.

This feature is beneficial if you want to keep credentials and secrets in a separate file that is excluded from repositories, but you want the `.myCommands` file to be part of the version history for sharing with other developers.

#### Example Include

```ini
# File: ./.credentials.secret

[secret]
password1=$3cr3+

[toolA]
APIKey=0123456789ABCDEF
```

```ini
# File: ./.myCommands

# Relative paths are supported
# include ./tests/../credentials.secret

# Paths with environment variables are supported
# include $HOME/credentials.secret

# Absolute paths are supported
include ./.credentials.secret


[secret]
localcred=echo 'Password from PWD: "${secret.password1}"'

[toolA]
health=echo curl -s -H "Authorization: Bearer ${toolA.APIKey}" https://api.example.com/status
```

```bash
> my secret.localcred
Password from PWD: "$3cr3+"

> my toolA.health
curl -s -H Authorization: Bearer 0123456789ABCDEF https://api.example.com/status
```


## Installation

1. **Download the File**:
    Ensure the script file (`my`) is placed in a directory that is included in your system's $PATH.
    It is recommended to install at `/usr/local/bin/my`
    The permissions of the downloaded file will also need to be updated to allow for execution

    ```shell
    # Note: You may need to run with `sudo`
    curl -o /usr/local/sbin/my https://raw.githubusercontent.com/jerrens/MyCE/refs/heads/main/my
    chmod +x /usr/local/sbin/my
    ```


1. **Create `.myCommands` files**:
    Add a `.myCommands` file in the root directories of your projects.

    A sample is available at <https://github.com/jerrens/MyCE/blob/main/.myCommands.example>

**Optional**: You can add `my` to your `.bashrc` or `.zshrc` if you prefer:

```bash
alias my='/path/to/my'
```


## Environment Variables

Optional environment variables may be defined to override default values for MyCE.
These variables should be set for the current session by using `export <VARIABLE>=<VALUE>`
or permanently by defining in `.bashrc` or `.zshrc`.

### `MYCE_FILE_NAME`

By default, MyCE will load command definitions from `.myCommands` files in the current directory tree.
Set the value of this variable to the desired file name if you wish to override the file name used.

### `MYCE_COLUMN_WIDTH`

By default, the `list` action will use a column width of 120 when printing aliases.
Set the value of this variable to the desired width, or to `FULL` to use the full terminal width.

### `MYCE_RUNCOM`

By default, MyCE will source the shell's rc file (eg. `~/.bashrc`, `~/.zshrc`, `~/.kshrc`) to the subshell so that user customizations defined there can be used.
Set the value of this variable to an alternative path if the file you want sourced is different from the default shell path (eg. `export MYCE_RUNCOM=~/.profile`).
Set the value of this variable to `false` if you do not want to source any rc file

Related to the `-c` [command line option](#options)

To debug, either view verbose help (`my -vv help`) or search the output of a verbose command execution for the variable name (`my -vvv echo "Hello" | grep "MYCE_RUNCOM"`)



## Example Workflow

You have two repositories, Repo1 and Repo2, both with their own `.myCommands` files.

```ini
# Repo1's `.myCommands` file:
build="mvn clean package"
run="java -jar target/app.jar"
```

```ini
# Repo2's `.myCommands` file:

build="npm run build"
run="npm start"
```

When you are working in **Repo1**. To build and run the application:

```bash
my build   # Executes 'mvn clean package'
my run     # Executes 'java -jar target/app.jar'
```

You switch to **Repo2**. Now, running the same my build command:

```bash
my build   # Executes 'npm run build'
my run   # Executes 'npm start'
```

The command executed changes based on the directory you are in, as it reads the `.myCommands` file from that directory.


## Enable TAB Command Completion

The bash terminal offers a simple command completion feature using the TAB key while entering commands.
To take advantage of this feature with MyCE, if you already have the folder `/etc/bash_completion.d` you can run `my update` to download the latest release and install the auto-completion script.
You may need to run `exec bash` after the update for your shell to load the new feature
If you're using a different shell or location for your completion scripts, the manual installation instructions are:

1. Copy the bash-completion/my file from this repo to `/etc/bash_completion.d/my`
2. Enable the execute flag (`chmod +x`)

This can be done with the following commands (these will likely need to be run as `sudo`)

```bash
curl -o /etc/bash_completion.d/my https://raw.githubusercontent.com/jerrens/MyCE/refs/heads/main/bash-completion/my
chmod +x /etc/bash_completion.d/my
```

If you run `exec bash` after doing the above, your environment will be reloaded and you can check to see if the command completion is working by entering `my hel<TAB>`.
If working, it should auto complete to `my help`.
If it does not, you likely need to add one of the following to your `~/.bashrc` file to load the completion script when a session starts.

`source /etc/bash_completion.d/my`

to load the specific file, or to load all files in the `/etc/bash_completion.d` folder, you can add the line:

`for f in /etc/bash_completion.d/*; do source "/etc/bash_completion.d/$f"; done`

After adding one of those lines to `~/.bashrc`, save, then run `exec bash` and try again.


## Guide

If you'd like to learn more about MyCE, an article can be found at <https://medium.com/@jerren/introduction-my-command-engine-myce-42e15028364a> that goes into details and provides some examples.


## Troubleshooting

If you find a bug or have a suggestion on a feature to add to MyCE, please open a GitHub Issue, or better yet submit a PR for consideration.

The Discussions page has been enabled on the repo as well. This is a good area to gauge interest in a feature idea with the community and also to share the command keys you’ve come up with for your .myCommands files and help others kick-start their setup.




## License

MIT License
