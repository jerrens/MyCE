---
name: myce
description: "Use MyCE (`my`) to discover and run hierarchical `.myCommands` aliases, preview or inspect definitions, manage aliases, or handle development-tool commands. MyCE falls back to the shell when no alias matches."
argument-hint: 'Optional: provide the command you want rewritten or validated with MyCE'
user-invocable: true
metadata:
	version: "26.10.21"
---

# MyCE Command Scope

## When to Use
- The user mentions MyCE, `.myCommands`, command aliases, or `my` behavior.
- The user asks to run, generate, or verify shell commands for development tooling.
- The project has `.myCommands` files or the user asks about project command shortcuts.
- Commands involve PHP, Laravel, Composer, JavaScript tooling, test runners, or build scripts.

## How MyCE Resolves Commands
- MyCE loads the user's `$HOME/.myCommands` and all `.myCommands` found while traversing the current directory's ancestry from the root.
- Definitions are merged, with the nearest directory's definition taking precedence.
- Suffixed files such as `.myCommands.local` can override or add definitions.
- When the first argument matches a configured key, MyCE runs that key's command with the supplied arguments.
- When no key matches, MyCE passes the command to the shell.
- MyCE is an alias resolver, not a container boundary or sandbox; `my php artisan test` runs PHP in the current shell environment unless a `php` alias is configured.
- MyCE sources the detected shell's rc file by default; `-c` or `MYCE_RUNCOM=false` disables that behavior.

## Policy
1. Prefer a project-defined MyCE alias when the user intends to use a project command or execution environment.
2. Do not assume that prefixing a raw tool command with `my` selects a container or avoids host execution.
3. Before a command that must run in a container or another specific environment, discover and inspect the matching alias; if no suitable alias exists, follow the project's documented command or ask before running it in a different environment.
4. Preserve the command's arguments and flags exactly when translating it to a MyCE alias.
5. Prefer an existing semantic alias over reconstructing its underlying command.
6. Treat aliases as executable commands that may have side effects; inspect or preview them when behavior is uncertain.
7. Do not update the MyCE script unless the user requests that action.

## Command Families and Alias Conventions
- Common tooling includes `php`, `artisan`, `composer`, `pest`, `phpunit`, `npm`, `npx`, `node`, `pnpm`, `yarn`, and `vite`.
- Project aliases may use namespaces such as `pod.*`, `test.*`, `spell.*`, `envoy.*`, `cache.*`, or `ide.*`; names and behavior are defined by each project's configuration.
- Dot notation commonly groups aliases, and a `+` suffix is an ordinary part of an alias name whose meaning is project-defined.

## Procedure
1. Identify whether the request needs a configured project alias, a raw shell command, or a particular execution environment.
2. Find likely aliases with `my list <pattern>` or show their descriptions with `my list -d <pattern>`.
3. Inspect where an alias is defined with `my definition <alias>` or the `my <alias> @` shorthand.
4. Preview its expanded command with `my -d <alias>` or the trailing `?` shorthand before executing an uncertain command.
5. Run the chosen alias with the original arguments, or use a raw command through MyCE only when execution in the current shell environment is intended.
6. Honor explicit requests for host execution and state the execution environment when it matters.

## Discovery and Verification Shortcuts
- `my help`, and `my version` show the installed CLI usage and version.
- `my list <pattern>` filters aliases; `my list -d <pattern>` includes descriptions.
- `my list -v <pattern>` shows alias values; `my list -vv <pattern>` fully expands nested referenced aliases in those values.
- `-vv` before the action, as in `my -vv list`, enables diagnostic verbosity rather than expanded list values.
- `my definition <alias>` and `my <alias> @` show definition locations.
- `my -d <alias>` previews an expanded command without running it; in zsh, escape the suffix as `\?` when using `my <alias> ?`.
- `my set <key> <command>` writes to the current directory's MyCE command file; use it only when the user asks to add or change an alias.
- `my update [diff] [latest|released|head|main|<TAG>]` downloads or installs MyCE updates and may require network access and elevated privileges; do not run it unless explicitly requested.
- `my update agent-skill` installs or updates this skill in `~/.agents/skills/myce/SKILL.md`, using a local copy when available and otherwise downloading it from GitHub; network access is only needed for the download fallback, and elevated privileges are not required.

## Examples
- `my test.report.main` is an example of a project-specific test alias; verify that it exists before use.
- `my pod.log+` is an example of a project-specific log alias; its exact behavior depends on its definition.
- For a configured PHP alias named `php`, `my php artisan test --filter SomeTest` runs the alias with the supplied arguments.
- Without that alias, `my php artisan test --filter SomeTest` falls back to running `php artisan test --filter SomeTest` in the current shell environment.

## Completion Checks
- Confirm that the selected alias exists and is appropriate for the requested environment.
- Preserve all original flags and arguments, with no duplicate `my` prefix.
- Do not claim container execution unless the selected alias or command explicitly provides it.
- For raw command fallback, confirm that execution in the current shell environment is intended.
