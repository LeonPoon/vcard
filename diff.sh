#!/bin/bash
PREFIX="$(dirname "$0")"
f1="$1"
shift
f2="$1"
shift
exec "$PREFIX/.venv/bin/python3" -m vcard.diff <("$PREFIX/.venv/bin/python3" -m vcard.sort "$@" < "$f1") <("$PREFIX/.venv/bin/python3" -m vcard.sort "$@" < "$f2") "$@"
