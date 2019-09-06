#!/bin/sh

~/.local/bin/pygount --folders-to-skip temp,ai --suffix "py" | awk '{ print $1}' > temp/linecount.txt
awk '{s+=$1} END {print s}' temp/linecount.txt
