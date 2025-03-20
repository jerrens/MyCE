# Commands

## Git

```ini
REPO_ROOT=$(git rev-parse --show-toplevel)

[git]
dir=echo "${REPO_ROOT}"
stash.staged=git stash push --staged
stash.unstaged=git stash push --keep-index
stash.unstaged+=git stash push --keep-index --include-untracked
```

## Terminal

```ini
confirm=read -rp "Are you sure? [Y/n] " -n 1 && echo && [[ $REPLY =~ ^[Yy]$ ]];

# Example use of confirm
[test]
confirm={ $confirm } && echo "Confirmed" || echo "Rejected"
```

```ini
find=find ${PWD} -name "$1" 2>/dev/null
```

```ini
date=TZ="${TIMEZONE:-America/New_York}" date +"%F %X"
```

```ini
# Keeps an SSH session from closing
hold=echo -ne "Holding the session open since\n  $(my date)\n  Press 'q' to resume...\n\n"; while true; do read -t 1 -n 1 -s keypress; if [[ $keypress == "q" ]]; then echo -e "\r\e[5A\e[J"; break; fi; ec$
```

```ini
# Service
[service]
start=systemctl start
stop=systemctl stop
restart=systemctl restart
status=systemctl status
list=systemctl list-unit-files --type=service -all
find=${service.list} | grep .*$1.*
```

```ini
[size]
disk=df -h
disk.color=df -h | awk 'NR==1; NR>1 {if ($5+0 > 90) print "\033[0;31m" $0 "\033[0m"; else if ($5+0 > 75) print "\033[33m" $0 "\033[0m"; else if ($5+0 > 50) print "\033[1;33m" $0 "\033[0m"; else print $0}'dir=du -sh *
mem=command -v free &> /dev/null && free -h || lsmem
cpu=command -v mpstat &> /dev/null && mpstat -P ALL | lscpu -e
```

```ini
[port]
who=ss -ltpn --no-header 'sport = :$1' | awk '{print \$6}'
probe=nc -z localhost $1 && echo "port open" || echo "port closed"
```
