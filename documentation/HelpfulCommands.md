# Commands

## Git

```ini
REPO_ROOT=$(git rev-parse --show-toplevel)

[git]
dir=echo "${REPO_ROOT}"
stash.staged=git stash push --staged
stash.unstaged=git stash push --keep-index
stash.unstaged+=git stash push --keep-index --include-untracked
dir.recon=for dir in */; do [ -d "${dir}.git" ] && (cd "$dir"; echo "${dir%/} $(git rev-parse --abbrev-ref HEAD) $(git rev-parse --short HEAD) $(git branch --format='%(refname:short)' | paste -sd, )"; cd ..); done | column --table --output-separator "    " --table-columns "DIRECTORY,ACTIVE BRANCH,REVISION,LOCAL BRANCHES"
```

## User Prompts

```ini
confirm=read -rp "Are you sure? [Y/n] " -n 1 && echo && [[ $REPLY =~ ^[Yy]$ ]];

# Example use of confirm
[test]
confirm={ $confirm } && echo "Confirmed" || echo "Rejected"
```

## File
```ini
[file]
backup=echo cp "$1" "$1--$(date +%Y%m%d_%H%M%S).bkp"
```

## Find
```ini
[find]
# Search the current directory and below for a file with the given pattern
name=find ${PWD} -name "$1" 2>/dev/null

# Search for the 10 largest files
largest=find / -type f -exec du -h {} + 2>/dev/null | sort -rh | head -10
# Biggest directory in the current directory
bigdir=du -h --max-depth=1 ${PWD} 2>/dev/null | sort -hr

# Most CPU intensive processes
proc=ps -eo pcpu,pid:10,comm --sort=-pcpu | grep -v 'my$' | head -10
# Most Memory intensive processes
mem=ps -eo pmem,pid:10,comm --sort=-pmem | head -10
```

## Date/Time

```ini
time=TZ="${TIMEZONE:-America/New_York}" date +"%F %X"
```

## Session
```ini
# Keeps an SSH session from closing
hold=echo -ne "Holding the session open since\n  $(my date)\n  Press 'q' to resume...\n\n"; while true; do read -t 1 -n 1 -s keypress; if [[ $keypress == "q" ]]; then echo -e "\r\e[5A\e[J"; break; fi; ec$

recon=uname -a; whoami; id; my ip;
```

## Services
```ini
# Service
[service]
start=systemctl start
stop=systemctl stop
restart=systemctl restart
status=systemctl status
list=systemctl list-unit-files --type=service -all
alive=systemctl list-units --type=service --state=running
dead=systemctl list-units --type=service --state=exited
find=${service.list} | grep .*$1.*
```

## Metrics/Utilization
```ini
[size]
disk=df -h
disk.color=df -h | awk 'NR==1; NR>1 {if ($5+0 > 90) print "\033[0;31m" $0 "\033[0m"; else if ($5+0 > 75) print "\033[33m" $0 "\033[0m"; else if ($5+0 > 50) print "\033[1;33m" $0 "\033[0m"; else print $0}'dir=du -sh *
dir=du -sh -- $(find . -mindepth 1 -maxdepth 1 -type d) 2>/dev/null
dir.sort=${size.dir} | sort -rh | head -10
mem=command -v free &> /dev/null && free -h || lsmem
cpu=command -v mpstat &> /dev/null && mpstat -P ALL | lscpu -e
```

## Network
```ini
ip=ip -brief a

[port]
who=ss -ltpn --no-header 'sport = :$1' | awk '{print \$6}'
open=lsof -i -P -n | grep LISTEN
probe=nc -z localhost $1 && echo "port open" || echo "port closed"
ping=nc -zv $1 $2 2>&1 | grep "Connect"
```

## Podman (Docker)
```ini
# These may be defined/overwritten in other directories
POD_YAML=pod.yaml
WORKSPACE_ROOT=$(dirname ${POD_YAML})

WEB_CONTAINER=dev-pod-web
MONGO_CONTAINER=dev-pod-mongodb

[pod]
attach=podman exec -ti $1 bash
up=pushd "$WORKSPACE_ROOT" > /dev/null && podman play kube "${POD_YAML}" && popd > /dev/null
up+=${pod.up} && sleep 3 && ${pod.ls}
down=pushd "$WORKSPACE_ROOT" > /dev/null && podman play kube "${POD_YAML}" --down && popd > /dev/null
down+=${pod.down} && sleep 3 && ${pod.ls}
replace=pushd "$WORKSPACE_ROOT" > /dev/null && podman play kube "${POD_YAML}" --replace && popd > /dev/null
replace+=${pod.replace} && sleep 3 && ${pod.ls}
stats=podman stats --no-stream
link=ln -sfn $(realpath --relative-to="${HOME}/code/podman" ${REPO_ROOT}) ~/code/podman/repo-name
checklink=ls -l ~/code/podman | awk '{if ($1 ~ /^l/) print $9 " -> " $11}'

# Different forms of showing containers (simple, simple combo, verbose combo)
ls=podman ps --all --format "table  {{.Image}}  {{.RunningFor}}  {{.Status}}  {{.Names}}  "
vol.ls=podman volume ls --format "table  {{.Driver}}  {{.Mountpoint}} {{.Name}}"
ll=echo -e "Containters:\n-----------------------------------------" && ${pod.ls} && echo -e "\nVolumes:\n-----------------------------------------" && ${pod.vol.ls}
la=echo -e "Containters:\n-----------------------------------------" && podman ps --all && echo -e "\nVolumes:\n-----------------------------------------" && ${pod.vol.ls}

# Generic form (define in ~/)
log=podman logs --follow --tail=50

# Specific form (override in repo directory)
log=podman logs $WEB_CONTAINER
log+=podman logs --tail 100 --follow $WEB_CONTAINER


# Interact with containers
con=podman exec -it $WEB_CONTAINER bash
xdebug.log=${pod.con} -c "tail --follow --lines=25 /tmp/xdebug.log"
web.restart=podman restart $WEB_CONTAINER

[pod.mongo]
con=podman exec -it $MONGO_CONTAINER bash
sh=podman exec --tty --interactive $MONGO_CONTAINER mongosh -u adminuser --port 27017


# Launch Utilitie in a Container
[mongo]
con=podman run --rm --tty --interactive --volume $(pwd):/mnt/host --workdir "/mnt/host" docker.io/alpine/mongosh bash
sh=podman run --rm --tty --interactive --volume $(pwd):/mnt/host --workdir "/mnt/host" docker.io/alpine/mongosh mongosh
export=podman run --rm --tty --interactive --volume $(pwd):/mnt/host --workdir "/mnt/host" docker.io/alpine/mongosh mongoexport
restore=podman run --rm --tty --interactive --volume $(pwd):/mnt/host --workdir "/mnt/host" docker.io/alpine/mongosh mongorestore
dump=podman run --rm --tty --interactive --volume $(pwd):/mnt/host --workdir "/mnt/host" docker.io/alpine/mongosh mongodump
```

## Python
```ini
[python]
venv.create=python -m venv .venv && source .venv/bin/activate
```
