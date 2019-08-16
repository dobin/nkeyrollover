#!/bin/sh

~/.local/bin/pygount --suffix "py" | awk '{ print $1}' > temp/linecount.txt
awk '{s+=$1} END {print s}' temp/linecount.txt
