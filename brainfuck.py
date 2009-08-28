#! /usr/bin/env python

from lib.interpreter import BrainFuck

bf = BrainFuck("./examples/hello_world.bf")
bf.interpret()
