import sys

class BrainFuck:
    '''A simple interpreter for the Brainfuck esotoric programming
       language. Originally designed by Urban Muller in 1993.'''

    def __init__(self, filepath, array_size=30000):
        self.filepath = filepath
        self.data_pointer = 0
        self.instruction_pointer = 0
        self.cells = [0] * array_size

    def interpret(self):
        '''Main interpreter loop. Reads in the file and blindly interprets
           it as a Brainfuck program. Output is pushed directly to STDOUT,
           so this method will either return None, or raise an exception.'''

        stream = self.__open_stream()

        byte = stream.read(1)
        while byte:
            method = self.__fetch_handler(byte)
            if method: method(stream)

            self.instruction_pointer += 1
            stream.seek(self.instruction_pointer)
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

    def __increment_pointer(self, *rest):
        '''Increment the data pointer (one cell to the right).'''
        if self.data_pointer < len(self.cells):
            self.data_pointer += 1

    def __decrement_pointer(self, *rest):
        '''Decrement the data pointer (one cell to the left).'''
        if self.data_pointer > 0:
            self.data_pointer -= 1

    def __increment_data(self, *rest):
        '''Increment the value (by one) of the cell at the data pointer.'''
        self.cells[self.data_pointer] += 1

    def __decrement_data(self, *rest):
        '''Decrement the value (by one) of the cell at the data pointer.'''
        self.cells[self.data_pointer] -= 1

    def __write_data(self, *rest):
        '''Outputs the value of the cell at the data pointer.'''
        sys.stdout.write(chr(self.cells[self.data_pointer]))

    def __read_data(self, *rest):
        '''Reads a value from STDIN and stores it at the data pointer.'''
        data = raw_input()
        self.cells[self.data_pointer] = data

    def __future_jump(self, stream):
        if self.cells[self.data_pointer] == 0:
            self.instruction_pointer = 41

    def __history_jump(self, stream):
        if self.cells[self.data_pointer] > 0:
            self.instruction_pointer = 10
