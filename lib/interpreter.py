from __future__ import with_statement
import sys

class BrainFuck:
    '''A simple interpreter for the Brainfuck esoteric programming
       language. Originally designed by Urban Muller in 1993.'''

    def __init__(self, filepath, array_size=30000):
        self.stream = self.__open_stream(filepath)
        self.data_pointer = 0
        self.instruction_pointer = 0
        self.cells = [0] * array_size

    def interpret(self):
        '''Main interpreter loop. Reads in the file and blindly interprets
           it as a Brainfuck program. Output is pushed directly to STDOUT,
           so this method will either return None, or raise an exception.'''
        with self.stream as s:
            byte = s.read(1)
            while byte:
                method = self.__fetch_handler(byte)
                if method: method()

                # Seek to the instruction pointer explicitely, as the 
                # command may have updated it.
                self.instruction_pointer += 1
                s.seek(self.instruction_pointer, 0)
                byte = s.read(1)

    def __open_stream(self, filepath):
        '''Opens a file for reading and returns it.'''
        try:
            file = open(filepath, "r", 0)
        except IOError:
            raise IOError("File '%s' cannot be read. Are you sure it exists?" % filepath)

        return file

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
        '''Increment the data pointer (one cell to the right).'''
        self.data_pointer += 1

        # If we run out of space, just increase memory! This is an
        # easy way of achieving Turing Completeness.
        if self.data_pointer == len(self.cells):
            self.cells.append(0)

    def __decrement_pointer(self):
        '''Decrement the data pointer (one cell to the left).'''
        self.data_pointer -= 1

    def __increment_data(self):
        '''Increment the value (by one) of the cell at the data pointer.'''
        self.cells[self.data_pointer] += 1

    def __decrement_data(self):
        '''Decrement the value (by one) of the cell at the data pointer.'''
        self.cells[self.data_pointer] -= 1

    def __write_data(self):
        '''Outputs the value of the cell at the data pointer.'''
        sys.stdout.write(chr(self.cells[self.data_pointer]))

    def __read_data(self):
        '''Reads a value from STDIN and stores it at the data pointer. A
           newline acts as EOF.'''
        try:
            input = raw_input()
            if len(input) == 0:
                data = 0
            else:
                data = ord(input[0])
        except:
            raise ValueError("WTF did you type?!")

        self.cells[self.data_pointer] = data

    def __future_jump(self):
        '''If the value at the data pointer is zero, jump it forward to
           the command after the matching ] command.'''
        if self.cells[self.data_pointer] == 0:
            position = self.stream.tell()
            byte = self.stream.read(1)
            nest_count = 0

            # Contine reading the file until we find the matching
            # command, or just die with syntax error.
            while byte:
                if byte == "[":
                    nest_count += 1
                elif byte == "]":
                    if nest_count == 0:
                        break
                    else:
                        nest_count -= 1

                byte = self.stream.read(1)
            else:
                raise SyntaxError("No closing brace was found for command at position %d" % position)

            self.instruction_pointer = self.stream.tell()

    def __history_jump(self):
        '''If the byte at the data pointer is nonzero, jump it back to
           the command after the matching [ command.'''
        if self.cells[self.data_pointer] != 0:
            position = self.stream.tell()
            nest_count = 0

            # Contine reading the file backwards until we find the
            # matching command, or just die with syntax error.
            while self.stream.tell() > 1:
                self.stream.seek(-2, 1)
                byte = self.stream.read(1)
                if byte == "]":
                    nest_count += 1
                elif byte == "[":
                    if nest_count == 0:
                        break
                    else:
                        nest_count -= 1
            else:
                raise SyntaxError("No opening brace was found for command at position %d" % position)

            self.instruction_pointer = self.stream.tell() - 1
