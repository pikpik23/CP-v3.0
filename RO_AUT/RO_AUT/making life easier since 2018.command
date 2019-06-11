#!/usr/bin/env bash

echo "THIS SCRIPT WILL NEED TO BE MODIFIED TO WORK"

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

cd "$BASEDIR"

PATH="${PATH}:$BASEDIR"
PYTHONPATH="${PYTHONPATH}:$BASEDIR"
export PYTHONPATH
export PATH

"$BASEDIR/venv/bin/python" -m ro_aut_main
open "$BASEDIR/test-output.docx"
osascript -e 'tell application "Microsoft Word" to activate'

echo "COMPLETE"
exit 0