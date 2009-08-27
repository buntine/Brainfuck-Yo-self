import sys

class BrainFuck:
    '''A simple interpreter for the Brainfuck esotoric programming
       language. Originally designed by Urban Muller in 1993.'''

    def __init__(self, filepath, array_size=30000):
        self.filepath = filepath
        self.data_pointer = 0
        self.cells = [0] * array_size

    def interpret(self):
        '''Main interpreter loop. Reads in the file and blindly interprets
           it as a Brainfuck program. Output is pushed directly to STDOUT,
           so this method will either return None, or raise an exception.'''

        stream = self.__open_stream()

        byte = stream.read(1)
        while byte:
            method = self.__fetch_handler(byte)
            if method: method()

            byte = stream.read(1)

        self.__close_stream(stream)

    def __open_stream(self):
        '''Opens a file for reading and returns it.'''
        try:
            file = open(self.filepath, "r", 0)
        except IOError:
            raise IOError("File '%s' cannot be read. Are you sure it exists?" % self.filepath)

        return file

    def __close_stream(self, file):
        file.close()
        return file.closed

    def __fetch_handler(self, command):
        '''Maps program commands to appropriate handler methods. Returns
           the actual function or None if nothing can be found.'''
        handlers = {
          '>': self.__increment_pointer,
          '<': self.__decrement_pointer,
          '+': self.__increment_data,
          '-': self.__decrement_data,
          '.': self.__write_data,
          ',': self.__read_data,
          '[': self.__future_jump,
          ']': self.__history_jump
        }

        return handlers.get(command)

    def __increment_pointer(self):
        print ">"

    def __decrement_pointer(self):
        print "<"

    def __increment_data(self):
        print "+"

    def __decrement_data(self):
        print "-"

    def __write_data(self):
        print "."

    def __read_data(self):
        print ","

    def __future_jump(self):
        print "["

    def __history_jump(self):
        print "]"
