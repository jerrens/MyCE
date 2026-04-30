#compdef my

# Toggle logging - set DEBUG=1 to enable
DEBUG=${DEBUG:-0}

# Prints log messages to a file if DEBUG is enabled
function log() {
    local log_file="/tmp/zsh-my-debug.log"
    [[ "$DEBUG" == "1" ]] && echo "$@" >> "$log_file"
}

_my() {
    log "---- NEW INVOCATION ----"
    log "words: $words"

    # Remove banner + trim whitespace in one go
    cmds=("${(@f)$(my list | tail -n +2)}")
    cmds=("${cmds[@]//(#s)[[:space:]]##/}")

    local curcontext="$curcontext" state line
    typeset -A opt_args

    _arguments -C \
        '1:firstarg:->first' \
        '2:subcmd:->second' \
        '*::args:->args'

    log "state: $state"

    case $state in
        first)
            local -a actions
            actions=(definition list help version update set)
            log "Offering: ${actions[@]} ${cmds[@]}"
            compadd -- "${actions[@]}" "${cmds[@]}"
            return
            ;;
        second)
            local firstarg="$words[2]"
            case "$firstarg" in
                update)
                    log "update opts"
                    compadd -- diff main head latest release
                    ;;
                definition)
                    local -a all_cmds
                    all_cmds=("${(@f)$(my list -a | tail -n +2)}")
                    all_cmds=("${all_cmds[@]//(#s)[[:space:]]##/}")
                    log "definition completions: ${all_cmds[@]}"
                    compadd -- "${all_cmds[@]}"
                    ;;
                list)
                    log "list opts"
                    compadd -- -l -a -d
                    ;;
            esac
            return
            ;;
        args)
            local firstarg="$words[2]"
            log "firstarg: $firstarg"

            if [[ "$firstarg" == "-d" ]]; then
                firstarg="$words[3]"
                log "shifted firstarg: $firstarg"
            fi

            case "$firstarg" in
                *)
                    log "default cmds: ${cmds[@]}"
                    compadd -- "${cmds[@]}"
                    return
                    ;;
            esac
            ;;
    esac
}