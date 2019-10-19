#!/bin/sh

~/.local/bin/pygount --suffix "py" | grep -vE "temp|esper|asciimatics|asciimatics.git|stackfsm" | awk '{ print $1}' > temp/linecount.txt
awk '{s+=$1} END {print s}' temp/linecount.txt
