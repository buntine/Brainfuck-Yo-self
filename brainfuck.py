#! /usr/bin/env python

# A quick little wrapper script to execute a brainfuck program.

import sys
from lib.interpreter import BrainFuck

if len(sys.argv) != 2:
    print "Usage: ./brainfuck.py path/to/a/file.bf"
    sys.exit(1)

bf = BrainFuck(sys.argv[1])
bf.interpret()
print
