<!-- markdownlint-configure-file {
    "no-inline-html": {
        "allowed_elements": [ "div" ]
    },
    "no-multiple-blanks": {
        "maximum": 4
    }
}
-->
<div align="center"><img style="max-width: 450px;" src="./logo/Myce - Blue.png" alt="MyCE Logo"></div>

# My Command Engine (MyCE)


## Overview

My Command Engine or MyCE (as in "Mice") is a powerful, context-aware command-line tool, written intirely in bash, and designed to streamline project workflows by utilizing custom command definitions stored in `.myCommand` files within the directory tree.
It searches for `.myCommand` files from the root down to the current directory, merging commands to create a localized and context-sensitive command set.
The `~/.myCommand` file will always be processed first, even if not executed within your $HOME directory
This tool is ideal for developers who frequently switch between projects or environments and need specific commands scoped to each context.



## Features

- **Context-Aware Commands**: Executes commands based on the `.myCommand` file located in the current directory or its parent directories.
- **Scoped Command Aliases**: Each directory (or project) can define its own command aliases without impacting other directories.
- **Ease of Use**: A simple command `my <key>` is all you need to invoke the corresponding full command defined in the `.myCommand` file.
- **Recursive Lookup**: If a `.myCommand` file is not found in the current directory, the script searches parent directories until one is found.
- **Merged Configurations**: Reads `.myCommand` files from the root directory down to the present working directory, merging them to build a complete command set. If duplicates are found, the command closest to the current directory takes precedence.
- **Sectioned Commands**: Uses INI-style sections in `.myCommand` files to organize and access commands with dot-delimited syntax. This allows grouping related commands for better clarity and organization:
- **Positional Args**: Values within the `.myCommand` file can use positional argument references (ie $1, $2, ${3})

```ini
[server]
start="docker-compose up"
stop="docker-compose down"
```

Running `my server.start` will execute docker-compose up.

- **Argument Passing**: Additional arguments provided after the command alias are passed directly to the underlying command. This enables dynamic behavior and flexible command usage.
- **Fallback to Shell**: If the requested alias is not found in the merged `.myCommand` configurations, the script will pass the command to the shell, allowing standard shell commands to work seamlessly with `my`.
- **Cross-Domain Commands with Variables**: Commands can reference variables set in different `.myCommand` files, allowing for reusable, high-level command configurations across directories. This feature is useful for defining generic commands in higher-level folders and reusing them in specific contexts within the workspace.



## Usage

### Basic Structure of `.myCommand` File

The `.myCommand` files uses INI-style sections to allow optional grouping, and key-value pairs where each key is an alias for a command, and the value is the corresponding command.

Example `.myCommand` file:

```ini
# Variables
LAST_CONTAINER="podman exec -it"
DB_CONTAINER="pod-db"

# Commands
echo=echo "Custom Prefix: "
npm="$LAST_CONTAINER npm"

[db]
backup=podman exec --interactive --tty --rm $DB_CONTAINER mongodump
restore=podman exec --interactive --tty --rm $DB_CONTAINER mongorestore
```

### Running the my Script

Create a `.myCommand` file in the root of your project or any directory where you want to define custom commands.
Run the `my` script followed by the *alias* you want to execute, and any additional arguments you may want to pass.
For example, if you're in a directory with the previous `.myCommand` file:

```bash
# Usage:
#    my <alias>

my echo Hello World
#> Custom Prefix: Hello World

my db.backup --gzip 
# Runs: podman exec --interactive --tty --rm pod-db mongodump --gzip
```

### Arguments

The `my` script has the following internal commands.
These commands take priority over any keys or aliases of the same name that are defined in any `.myCommand` files, ***so consider them reserved keywords.***

`help`:
Don't worry if you forget the basics.  
Simply type `my help` to view the usage details.

`version`:
Not sure if you have the latest version installed?  
Just run `my version` and compare against the latest version on [GitHub](https://github.com/jerrens/MyCE)

`set <cmd> <value>`:
**Experimental!**
This command may be used to add a new value to the `.myCommand` file in the current directory.
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

`list [-l]`:
Can't remember what you used as the key?
Just enter `my list` to view the available commands.
If you don't like columns, add the `-l` option at the end to show one command per line

`update [diff]`:
Easily pull down the latest version from the github repo.
The file will be downloaded into `/usr/local/bin` and the permissions set to 755.
This command needs to be run with root level privileges.
If not, it will attempt to elevate itself and prompt for a password if needed.

If you only want to view the changes (uses `sdiff`) between your local version and the latest version on GitHub, you can use `my update diff`

> ***NOTE:***
>
> This pulls down the latest checked-in version and **not** the latest release.
> It may contain bugs.


### Options

Options for the `my` script should be added immediately following the `my` script call (before the key).

`-v | -vv | -vvv`:
Log prints can be enabled for debugging by including the `-v` option.
Crank up the level by stacking more (`-vv`, `-vvv`).
Three levels is currently the most verbosity used in log prints, but if you get a little trigger happy with the `v` key, it will be ok.

Example: `my -vv build`

`-d`:
Curious how your `.myCommand` entries will expand, but not brave enough to just try?
A dry run can be enabled by using the `-d` option.
In dry run mode, the expanded command will be printed, but not executed

Example: `my -d build`


## Command Lookup Process

1. **Merging and Overriding**:
    The script starts at the root directory, working down to the current directory (pwd), merging any `.myCommand` files found along the way.
    Commands defined in `.myCommand` files closer to the current directory override duplicates from higher-level directories.
    This makes the command engine adaptable for different projects without the need for globally defined aliases.

2. **Sectioned Access**:
    Commands are referenced using `section.key` syntax if using INI-style sections.

3. **Fallback to Shell**:
    If no matching alias is found, the command is sent to the shell for evaluation.

### Handling Variables Across Directories

Variables can be set in `.myCommand` files at any directory level and accessed by commands in lower directories, allowing for flexible and reusable configurations.



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


1. **Create `.myCommand` files**:
    Add a `.myCommand` file in the root directories of your projects.

    A sample is available at <https://github.com/jerrens/MyCE/blob/main/.myCommand.example>

**Optional**: You can add my to your .bashrc or .zshrc if you prefer:

```bash
alias my='/path/to/my'
```


## Example Workflow

You have two repositories, Repo1 and Repo2, both with their own `.myCommand` files.

```ini
# Repo1's `.myCommand` file:
build="mvn clean package"
run="java -jar target/app.jar"
```

```ini
# Repo2's `.myCommand` file:

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

The command executed changes based on the directory you are in, as it reads the `.myCommand` file from that directory.



## Troubleshooting


License
MIT License

This README provides a comprehensive guide for users to install, configure, and use My Command Engine. For further assistance or contributions, feel free to open an issue or submit a pull request.
