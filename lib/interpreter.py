import sys

class BrainFuck:
    '''A simple interpreter for the Brainfuck esotoric programming
     language. Originally designed by Urban Muller in 1993.'''

    HANDLERS = {
        '>': 'increment_pointer',
        '<': 'decrement_pointer',
        '+': 'increment_data',
        '-': 'decrement_data',
        '.': 'write_data',
        ',': 'read_data',
        '[': 'future_jump',
        ']': 'history_jump'
    }

    def __init__(self, filepath, array_size=30000):
        self.filepath = filepath
        self.cells = self.__init_cells(array_size)
        self.data_pointer = 0

    def interpret(self):
        '''Main interpreter loop. Reads in the file and blindly interprets
         it as a Brainfuck program. Output is pushed directly to STDOUT,
         so this method will either return None, or raise an exception.'''

        stream = self.__open_stream()

        byte = stream.read(1)
        while byte:
            print byte
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

    def __init_cells(self, array_size):
        return [0] * array_size
