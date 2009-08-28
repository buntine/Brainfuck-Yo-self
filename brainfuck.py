#! /usr/bin/env python

from lib.interpreter import BrainFuck

bf = BrainFuck("./examples/addition.bf")
bf.interpret()
