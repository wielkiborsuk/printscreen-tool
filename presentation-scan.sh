#!/bin/bash

DIR="$(dirname "$(readlink -f "$0")")"

. "$DIR"/venv/bin/activate

cd "$DIR"

python print.py "$@"

