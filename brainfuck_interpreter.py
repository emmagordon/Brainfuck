#!/usr/bin/env python

import sys


MEMORY_SIZE = 30000


class SegmentationFault(Exception):
    pass


class InvalidBrainfuck(Exception):
    pass


class Break(Exception):
    pass


class Continue(Exception):
    pass


def _increment_data_pointer():
    global memory_index
    memory_index += 1
    if memory_index >= MEMORY_SIZE:
        raise SegmentationFault


def _decrement_data_pointer():
    global memory_index
    memory_index -= 1
    if memory_index < 0:
        raise SegmentationFault


def _increment_byte():
    memory[memory_index] = (memory[memory_index] + 1) % 256


def _decrement_byte():
    memory[memory_index] = (memory[memory_index] - 1) % 256


def _output_byte():
    sys.stdout.write(chr(memory[memory_index]))


def _input_byte():
    while True:
        user_input = raw_input("Enter a single character:")
        if len(user_input) == 1:
            memory[memory_index] = ord(user_input)
            break


def _while_byte():
    if memory[memory_index] == 0:
        raise Break


def _end_while():
    if memory[memory_index] != 0:
        raise Continue


COMMANDS = {">": _increment_data_pointer,
            "<": _decrement_data_pointer,
            "+": _increment_byte,
            "-": _decrement_byte,
            ".": _output_byte,
            ",": _input_byte,
            "[": _while_byte,
            "]": _end_while}


def _find_braces(program_string):
    find_opening_brace = {}
    find_closing_brace = {}

    opening_braces = []
    for (position, character) in enumerate(program_string):
        if character == "[":
            opening_braces.append(position)

        elif character == "]":
            try:
                opening_brace_position = opening_braces.pop()

            except IndexError:
                raise InvalidBrainfuck

            find_closing_brace[opening_brace_position] = position
            find_opening_brace[position] = opening_brace_position

    if len(opening_braces) != 0:
        raise InvalidBrainfuck

    return find_opening_brace, find_closing_brace


def _initialise_memory():
    global memory, memory_index
    memory = [0] * MEMORY_SIZE
    memory_index = 0


def main(program_string):
    _initialise_memory()

    find_opening_brace, find_closing_brace = _find_braces(program_string)

    program_position = 0
    while True:
        try:
            instruction = program_string[program_position]
        except IndexError:
            break

        try:
            COMMANDS[instruction]()
        except KeyError:
            pass
        except Break:
            program_position = find_closing_brace[program_position]
        except Continue:
            program_position = find_opening_brace[program_position]

        program_position += 1


if __name__ == "__main__":
    main(sys.argv[1])

