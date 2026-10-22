# MyCE Security Review

## Scope

This report documents the security concerns identified in the reviewed `my` script, proposed mitigations, and remediation status. Finding 4 has been addressed in the current working tree; the other findings remain open.

The referenced locations correspond to the current [`my`](../../my) script. Command definitions are shell programs by design, so `.myCommands` files should be treated as executable code and trusted accordingly. The findings below focus on cases where runtime arguments, configuration paths, or elevated update operations can cross that trust boundary.

## Findings and mitigations

### 1. Runtime arguments can become shell code

**Severity: High**

Positional arguments are substituted into a command-template string without shell-quoting them at [`my`, line 703](../../my#L703). That string is then executed with `eval` at [`my`, line 1056](../../my#L1056). An argument containing shell syntax, such as a command substitution, can therefore execute as code when passed to an alias that references that argument. This is especially relevant when automation or other callers supply values they do not control.

**Mitigation proposal**

- Preserve the existing command-definition syntax, including intentional shell operators, pipes, and redirections.
- Treat values supplied at invocation time as data: shell-quote each argument before inserting it into a command template. Preserve argument boundaries for positional references and `$@`-style placeholders.
- Replace the nested-argument `eval` at [`my`, line 868](../../my#L868) with a parser/tokenizer for the quoting and tokenization features that nested invocations officially support.
- Add regression tests for spaces, quotes, glob characters, semicolons, command-substitution syntax, and multiple arguments. Tests should confirm intended shell syntax in definitions still works while shell syntax supplied as an argument is not evaluated.

### 2. Include paths are evaluated as shell input

**Severity: High**

The config parser expands an `include` path using `eval echo` at [`my`, line 1421](../../my#L1421). Shell substitutions and other shell constructs in the path may execute while MyCE parses the configuration. Since configuration loading is also used for operations such as listing definitions, this may execute code even when the user did not request that particular alias.

**Mitigation proposal**

- Replace shell evaluation with explicit expansion for supported path forms, such as leading `~` and environment-variable references.
- Reject command substitutions and unsupported shell syntax in include paths.
- Continue resolving relative include paths against the including file's directory.
- Test supported path expansions, relative paths, missing includes, and paths containing spaces; verify that shell metacharacters are treated as path data and are never executed.

### 3. A privileged update may source user-controlled startup code

**Severity: High, conditional on environment and sudo policy**

`runCMD` sources the configured run-command file before running a command at [`my`, lines 998–1001](../../my#L998). The update process re-invokes MyCE with `sudo -E` at [`my`, line 2705](../../my#L2705). If the environment and sudo policy preserve a user-controlled `HOME` or `MYCE_RUNCOM`, a later `runCMD` in the elevated process may source that file with root privileges.

This is conditional: sudo commonly filters environment variables, and policy may reject or restrict `-E`. The relevant risk exists when the effective environment retains a startup-file path controlled by the invoking user.

**Mitigation proposal**

- Do not source user shell startup files during privileged update operations.
- Use a minimal, explicitly constructed environment for the elevated process rather than preserving the full environment with `sudo -E`.
- Ignore `MYCE_RUNCOM` when running as root, or accept it only when the file is owned by root and not writable by untrusted users.
- If aliases are needed to perform an update, resolve them before elevation or use a narrowly scoped, trusted root configuration.
- Test under the supported sudo policies and verify that user-controlled `HOME`, `MYCE_RUNCOM`, and shell-marker variables cannot influence privileged startup behavior.

### 4. Predictable temporary path in the privileged update flow

**Severity: Medium, platform-dependent**

The update archive was downloaded to a predictable path under `/tmp`, derived from the application name and release tag, and `wget` wrote directly to that path. The update may proceed with elevated privileges after re-execution. In a shared temporary directory, a pre-created path or race could redirect or interfere with privileged file operations, depending on operating-system protections and permissions.

**Mitigation proposal**

- Create a private temporary directory with `mktemp -d` and restrictive permissions; place both the downloaded archive and extracted files inside it.
- Ensure extraction is confined to that directory and only expected files are installed.
- Validate the release tag before using it in URLs or filesystem paths.
- Treat download or extraction failure as fatal, and verify that required files exist before installation.
- Clean up the private directory with a trap on success, failure, and interruption.
- For stronger supply-chain assurance, verify a trusted release signature or checksum before installing the downloaded content.

**Status: Addressed in the current working tree**

- Both update and diff operations create a private temporary directory with `mktemp -d` and mode `700`; an exit trap removes it on completion or interruption ([`my`, lines 18–25](../../my#L18)).
- Release tags are validated before they are used in archive URLs or paths. The downloaded archive is listed and the updater extracts only the expected script and shell-completion files into the private directory ([`my`, lines 2484–2575](../../my#L2484)).
- Download, archive inspection, and required-script extraction failures stop the update rather than continuing with incomplete files ([`my`, lines 2540–2580](../../my#L2540)).
- Signature or checksum verification has not been implemented; this remains a separate supply-chain hardening opportunity.

## Design and trust-boundary note

Executing command definitions with `eval` at [`my`, line 1056](../../my#L1056) supports MyCE's shell-command alias behavior. Removing it outright could break intentional shell syntax. The practical near-term boundary is to keep definitions trusted executable configuration while ensuring that untrusted runtime arguments and paths cannot be reinterpreted as shell source.

A longer-term design could parse command definitions into command/argument structures and represent pipelines or other shell expressions explicitly. That is a broader compatibility change and should be approached with a documented grammar and comprehensive regression tests.

## Suggested remediation order

1. Prevent runtime arguments and nested invocation arguments from becoming executable shell syntax.
2. Remove `eval` from include-path expansion.
3. Ensure privileged update execution cannot source user-controlled startup files.
4. Use a private update workspace and validate archive contents. **Implemented.** Trusted signature or checksum verification remains open.
