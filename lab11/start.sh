#!/bin/bash

FILE=./.venv/bin/python
if test ! -f "$FILE"; then
    ./.venv/bin/python board.py
else
    python board.py
fi

echo "End"