#!/bin/bash



usage() {
    echo >&2 "This tool scans a /24 subnet, only.
Syntax: $0 1.2.3"
}

if [ "$1" = "" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ] || \
    [[ ! $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    usage
    exit 1
fi

subnet="$1"

for ip in `seq 1 254`; do
    ping -c 1 -W 1 "$subnet.$ip" 2>/dev/null | grep -e '64 bytes' | cut -d ' ' -f 4 | tr -d ':' &
done

# wait for ping finish
sleep 2
