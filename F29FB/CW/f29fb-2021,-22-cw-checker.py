#!/usr/bin/python3

# Copyright 2021, 2022 Heriot-Watt University.  All Rights Reserved.
#
# A HWU student enrolled in the course Foundations 2 (F29FB) in academic
# year 2021/2022 semester 2 is licensed to copy this and make derivative
# works and copy such derivative works, but only for the purposes of
# carrying out (e.g., preparing, submitting) their own HWU coursework
# and keeping copies of such coursework for their own personal study,
# and only when doing so in ways that take care to prevent copying or
# viewing by anyone else except persons or institutions authorized by
# HWU.  In addition to violating copyright, copying or allowing copying
# that does not follow these conditions might be academic misconduct
# that is subject to penalties.
#
# Author: Joe Wells

"""Checks the file turing-machine-action-table.txt.

This program is normally named “f29fb-2021,-22-cw-checker.py”.

This program reads, parses, and checks (for syntactic and semantic
correctness) a student's prepared turing-machine-action-table.txt file.
These checks are carried out:

1. Does a file named exactly “turing-machine-action-table.txt” exist in
   the current directory?

2. Does the file obey the required syntax specified in the coursework
   assignment?

3. Does the file contain a student ID comment on its first line?

4. Do the contents of the file denote a function (and therefore a Turing
   machine)?  (This means there must not be two distinct actions with
   the same current/old state and tape symbol.)

5. Does the Turing machine in the file have at least one action with q_0
   as the current/old state?

In addition, depending on the command-line arguments, the following
functionality is available:

6. Does the function g ∈ ℕ² → ℕ² that the Turing machine computes agree
   with the function rmoddiv specified in the coursework assignment for
   all inputs (x, y) ∈ { (x, y) ∈ ℕ × ℕ | 0 ≤ x ≤ 50 ∧ 0 ≤ y ≤ 50 }?

7. What does the Turing machine do on specific input numbers?

8. What does the Turing machine do on specific input tapes?

Run this program without any arguments to get instructions on what
arguments it takes.

This program has been tested with Python 3.5 and Python 3.9.  It is
extremely unlikely to work with Python 2.
"""

import math
import os
#import pprint
import re
import sys
import shutil
import textwrap

tty_width = shutil.get_terminal_size().columns

# old versions of argparse look at this environment variable rather than
# asking shutil.get_terminal_size.
if 'COLUMNS' not in os.environ:
    os.environ['COLUMNS'] = str(tty_width)
import argparse

def fill(t):
    return textwrap.fill(t, tty_width)


def machine_states(machine):
    from_states = set()
    to_states = set()
    for ((from_state, old_symbol),
         (to_state, new_symbol, move, move_num)) \
    in machine.items():
        from_states.add(from_state)
        to_states.add(to_state)
    return (from_states, to_states)


state_regexp = '[A-Za-z][-A-Za-z0-9_<>]*'
symbol_regexp = '[A-Z0-9^]'
move_regexp = '[LR0]'

action_regexp = ('''(?x)
\(
    \(
        (?P<current_state>{state_regexp})
      ,
        (?P<current_symbol>{symbol_regexp})
    \)
  ,
    \(
        (?P<new_state>{state_regexp})
      ,
        (?P<new_symbol>{symbol_regexp})
      ,
        (?P<move>{move_regexp})
    \)
\)
,
'''.format(**globals()))
# *** TODO compile regexp for speed

tape_arg_regexp = \
    (('(?:(?P<left_tape>{symbol_regexp}*)@)?'
      '(?P<right_tape>{symbol_regexp}*)')
     . format(**globals()))

move_delta = {'L' : - 1, '0' : 0, 'R' : 1}


def parse_machine_from_file(file):
    machine = {}
    parse_tm_stage = 0
    first_line = True
    with open(file, encoding='utf-8') as f:
        for line in f:
            # remove all whitespace:
            # *** TODO handle BOM
            line = line.translate(str.maketrans('', '', ' \t\n\r'))
            # print('line = [', line, ']', sep='')
            if (not line.startswith('#')
                and not re.fullmatch('[-{}(),A-Za-z0-9_<>^]*', line)
            ):
                raise RuntimeError(
                    'at least one illegal character on line: [{}]'
                    . format(line))
            if first_line:
                match = re.fullmatch('#(H00\d{6})', line)
                if match:
                    student_id = match.group(1)
                    first_line = False
                    continue
                raise RuntimeError('first line is not comment'
                                   ' containing only student ID')
            # ignore blank lines and comments
            if line == '' or line.startswith('#'):
                continue
            if line == '{':
                if parse_tm_stage == 0:
                    parse_tm_stage = 1
                    continue
                raise RuntimeError("seen two {'s")
            if line == '}':
                if parse_tm_stage == 1:
                    parse_tm_stage = 2
                    continue
                if parse_tm_stage == 0:
                    raise RuntimeError('} before {')
                if parse_tm_stage == 2:
                    raise RuntimeError("seen two }'s")
            if parse_tm_stage == 1:
                match = re.fullmatch(action_regexp, line)
                if match:
                    (current_state, current_symbol,
                     new_state, new_symbol, move) \
                        = match.group('current_state', 'current_symbol',
                                      'new_state', 'new_symbol', 'move')
                    key = (current_state, current_symbol)
                    if key in machine:
                        # *** TODO allow it and warn if RHS is same
                        raise RuntimeError(
                            'TM is not a function; two actions for {}'
                            . format(key))
                    move_num = move_delta[move]
                    # *** TODO intern states (and symbols?) for speed
                    machine[key] = (new_state, new_symbol, move,move_num)
                    continue
            raise RuntimeError('illegal line: [{}]'.format(line))
    if parse_tm_stage != 2:
        raise RuntimeError('there must be a { followed by a }')
    return (machine, student_id)


def print_tape(tape, head_offset):
    i = 0
    for o in tape:
        print(i == head_offset and '@' or ' ', chr(o), sep='', end='')
        i += 1


def run_tm(machine, max_state_len, tape_base, tape,
           max_steps, print_configs):
    #print('max_steps =', max_steps)
    assert isinstance(max_steps, int)
    state = 'q_0'
    step_count = 0
    extend_count = 0
    head_position = 0
    tape = tape.center(len(tape) + 6, b'^')
    tape_base -= 3
    while True:
        #print('tape =', tape)
        if (head_position <= tape_base
            or head_position >= tape_base + len(tape) - 1
        ):
            extend_amount = max(2**extend_count,
                                tape_base - head_position,
                                head_position - (tape_base + len(tape)),
                                5)
            tape = tape.center(len(tape) + 2 * extend_amount, b'^')
            tape_base = tape_base - extend_amount
            extend_count += 1
            # print('extend_count =', extend_count,
            #       'tape_base =', tape_base)
            #print('tape =', tape)
        head_offset = head_position - tape_base
        # print('head_position =', head_position,
        #       'head_offset =', head_offset)
        if print_configs:
            print(state.ljust(max_state_len), ':', tape_base, ':',end='')
            print_tape(tape, head_offset)
            print()
        old_symbol = chr(tape[head_offset])
        key = state, old_symbol
        if key not in machine:
            break
        if step_count >= max_steps:
            #print('step_count =', step_count, 'max_steps =', max_steps)
            return None
        state, new_symbol, move, move_num = machine[key]
        tape[head_offset] = ord(new_symbol)
        head_position += move_num
        step_count += 1
    return tape_base, tape, head_position, step_count


def grok_tape_arg(tape_arg):
    # print('tape_arg_regexp = [', tape_arg_regexp, ']',
    #       'tape_arg = [', tape_arg, ']', sep='')
    match = re.fullmatch(tape_arg_regexp, tape_arg)
    if not match:
        raise RuntimeError('illegal tape argument: [{}]'
                           . format(tape_arg))
        #raise RuntimeError('one or more illegal tape symbols')
    (left_tape, right_tape) = match.group('left_tape', 'right_tape')
    if left_tape == None:
        left_tape = ''
    tape_base = - len(left_tape)
    tape = bytearray(left_tape + right_tape, encoding='utf-8')
    return (tape_base, tape)


def read_numbers_from_final_tape(tape_base, tape, head_position):
    head_offset = head_position - tape_base
    tape_len = len(tape)
    blank = b'^'[0]
    one = b'1'[0]
    valid_symbols = [blank, one]
    offset = 0
    while (offset < tape_len and tape[offset] == blank
           and offset < head_offset):
        offset += 1
    if offset < head_offset:
        return ('non-blank symbol to left of final head position: '
                + chr(tape[offset]))
    numbers = []
    left_ones = 0
    while offset < tape_len and tape[offset] in valid_symbols:
        if tape[offset] == one:
            left_ones += 1
        elif tape[offset] == blank:
            numbers.append(left_ones)
            left_ones = 0
        else:
            raise RuntimeError('impossible ⦃VLhrau@4P_⦄')
        offset += 1
    if offset == tape_len:
        return numbers
    if tape[offset] not in valid_symbols:
        return ('symbol other than blank or 1 on final tape: '
                + chr(tape[offset]))
    raise RuntimeError('impossible ⦃gJ.Vzx-VeD⦄')


def write_tape_from_numbers(numbers):
    #print('numbers = ', numbers)
    def number_to_unary(n):
        if n < 0:
            die(fill("Can't write a negative number on tape: " + str(n)))
        return b'1' * n + b'^'
    return bytearray(b''.join(map(number_to_unary, numbers)))


def cblog(k):
    try:
        l = math.log2(k)
    except ValueError:
        return None
    return [math.ceil(l)]


cblog_test_range = 101


def good_test_range_for_cblog(x):
    # *** TODO add command-line option for testing range
    if x is None:
        x = cblog_test_range
    test_range = set(range(x))
    for x in range(0, 12):
        for y in range(-3, 4):
            z = 2**x + y
            if z >= 0:
                test_range.add(z)
    return map(list, sorted(test_range))


def rmoddiv(x, y):
    if x == 0:
        return None
    [q, r] = divmod(y, x)
    return [r, q]


rmoddiv_test_range = 51


def good_test_range_for_rmoddiv(x):
    if x is None:
        x = rmoddiv_test_range
    # *** TODO add command-line option for testing range
    r = range(x)
    return ((x, y) for x in r for y in r)


expected_number_of_output_numbers = 2


def comprehensively_test_machine(machine, max_state_len, max_steps,
                                 test_range, student_id):
    count = 0
    correct_count = 0
    max_steps_used = 0
    for numbers in good_test_range_for_rmoddiv(test_range):
        tape = write_tape_from_numbers(numbers)
        result = run_tm(machine, max_state_len, 0, tape, max_steps,False)
        # print('result =', result)
        if not result:
            result = 'exceeded step limit'
        else:
            [tape_base, tape, head_position, step_count] = result
            max_steps_used = max(max_steps_used, step_count)
            result = read_numbers_from_final_tape(tape_base, tape,
                                                  head_position)
            if type(result) == list:
                #print('result =', repr(result))
                while len(result) < expected_number_of_output_numbers:
                    result.append(0)
                while (len(result) > expected_number_of_output_numbers
                       and result[-1] == 0):
                    del result[-1]
                if len(result) > expected_number_of_output_numbers:
                    if (set(result[expected_number_of_output_numbers :])
                        != {0}
                    ):
                        result = (
                            'final tape has more than '
                            + str(expected_number_of_output_numbers)
                            + ' two non-zero numbers written on it: '
                            + ' '.join(map(repr, result)))
                    else:
                        result = (
                            result[: expected_number_of_output_numbers])
        correct = rmoddiv(*numbers)
        if (result != correct
            and not (correct == None and isinstance(result, str))
        ):
            print('input = ', numbers, '; correct result = ', correct,
                  '; result calculated by TM = ', result,
                  '; steps used = ', step_count, sep='')
            pass
        else:
            #print('input =', k)
            correct_count += 1
        count += 1
    print(count, 'computation sequences run.')
    print(correct_count, 'computation sequences had correct results.')
    print('maximum number of steps in any computation sequence:',
          step_count)
    print('{} percent correct = {:.1%}'
          . format(student_id, correct_count / count))


def die(message):
    print(message, file=sys.stderr)
    sys.exit(1)


# def fill_text(text, width, indent):
#     import textwrap
#     lines = text.splitlines(keepends=True)
#     new_lines = []
#     for line in lines:
#         #print('A line =', repr(line))
#         line = textwrap.fill(line, width, initial_indent=indent, subsequent_indent=indent) + '\n'
#         #print('B line =', repr(line))
#         new_lines.append(line)
#     result = ''.join(new_lines)
#     #print('result =', repr(result))
#     return result
# def get_formatter(self):
#     formatter = self.formatter_class(prog=self.prog)
#     #formatter._whitespace_matcher = re.compile('R-MHXsfyN_JDe7FLVDvW')
#     formatter._fill_text = fill_text
#     return formatter
# argparse.ArgumentParser._get_formatter = get_formatter


class MyArgParseHelpFormatter(argparse.HelpFormatter):

    def _fill_text(self, text, width, indent):
        # print('C', repr(text))
        lines = text.splitlines()
        new_lines = []
        for line in lines:
            #print('A line =', repr(line))
            line = (textwrap.fill(line, width, initial_indent=indent,
                                  subsequent_indent=indent,
                                  replace_whitespace=False)
                    + '\n')
            #print('B line =', repr(line))
            new_lines.append(line)
        result = ''.join(new_lines)
        #print('result =', repr(result))
        return result

    def _split_lines(self, text, width):
        # print('D', repr(text))
        return textwrap.wrap(text, width)


def main(argv):
    # global parser
    # global group
    # global args
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        formatter_class=MyArgParseHelpFormatter,
        # announce that these are instructions for how to use the
        # program (some students are baffled)
        description=(
            'The above “usage:” line(s) illustrates the possible'
            ' command-line arguments that can be used with this program.'
            '\n\n'
            'IMPORTANT NOTE: This is the help text for this program.'
            '\n\n'
            "This program can perform various tests on the student's"
            ' Turing machine.'
            '  By default it uses the Turing machine specified in the'
            ' file turing-machine-action-table.txt in the current'
            ' directory.'
            '\n\n'
            'Of the options described below, exactly one marked with'
            ' “[ACTION]” must be used or you will just get this help'
            ' text or an error message.'))
    # *** TODO check if add_mutually_exclusive_group ever gains the
    # separate help text grouping feature of add_argument_group (looks
    # like this will be complicated to add)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--test-without-running', action='store_true',
        help=('[ACTION] Do all tests that can be done without running'
              ' the Turing machine.'))
    group.add_argument(
        '--comprehensive-test', action='store_true',
        help=('[ACTION] Run the Turing machine on a lot of tapes each'
              ' generated from two natural numbers.'
              '  Do not show any configurations.'
              '  If the answer for a particular number pair of number X'
              ' and Y does not match rmoddiv(X, Y),'
              ' print a comparison between the correct and actual'
              ' outcomes.'
              '  Print overall percent correct.'))
    group.add_argument(
        '--run-on-numbers', type=int, nargs='*', metavar='NUM',
        # *** TODO figure out whether action='append' (or
        # action='extend', not available until python 3.8) would make
        # sense here
        help=('[ACTION] Run the Turing machine with initial tape'
              ' containing natural numbers %(metavar)s written in unary'
              ' notation starting at position 0 and going to the right.'
              '  Show all configurations.'))
    group.add_argument(
        '--run-on-tape',
        metavar='TAPE',
        help=('[ACTION] Run the Turing machine with initial tape'
              ' specified by %(metavar)s.'
              '  Show all configurations.'
              '  If you want the leftmost position in %(metavar)s to be'
              ' other than position 0, you must put @ between your'
              ' desired position -1 and your desired position 0.'))
    # parser.add_argument('--start-state')
    parser.add_argument(
        '--max-steps', type=int, metavar='MAX',
        help=('Force the Turing machine to halt whenever %(metavar)s'
              ' steps have already been carried out, even if the'
              ' configuration is not halted.'))
    parser.add_argument(
        '--test-range', type=int, metavar='RANGE',
        help=('Set the upper bound of the range of numbers that is used'
              ' when generating test cases for comprehensive testing.'))
    parser.add_argument(
        '--turing-machine-file', metavar='FILE',
        help=('Load the Turing machine from %(metavar)s instead of from'
              ' turing-machine-action-table.txt.'))
    if not argv:
        argv = ['--help']
    #pprint.pprint(parser)
    # pprint.pprint(parser.__dict__)
    args = parser.parse_args(argv)
    # pprint.pprint(args)
    #args = parser.parse_args(['--help'])
    #sys.exit(1)
    file='turing-machine-action-table.txt'
    if args.turing_machine_file != None:
        file=args.turing_machine_file
    if (args.run_on_tape != None or args.run_on_numbers != None
        or args.comprehensive_test != None
    ):
        if args.max_steps != None:
            max_steps = args.max_steps
        else:
            max_steps = 10000000
    elif args.max_steps != None:
        die(fill('Option --max-steps only valid with --run-on-tape or'
                 ' --run-on-number or --comprehensive-test.'))
    if args.comprehensive_test != None:
        if args.test_range != None:
            test_range = args.test_range
        else:
            test_range = None
    elif args.test_range != None:
        die(fill('Option --test-range only valid with'
                 ' --comprehensive-test.'))
    try:
        r = parse_machine_from_file(file)
    except RuntimeError as e:
        die('failed while loading Turing machine: '+ str(e.args[0]))
    except Exception as e:
        die('failed while loading Turing machine: '+ str(e))
    (machine, student_id) = r
    (from_states, to_states) = machine_states(machine)
    if 'q_0' not in from_states:
        die(fill('Useless Turing machine has no actions in state q_0.'))
    max_state_len = max(map(len, from_states | to_states))
    # print('machine =', end='')
    # pprint.pprint(machine, width=200)
    if args.run_on_tape != None or args.run_on_numbers != None:
        if args.run_on_tape != None:
            [tape_base, tape] = grok_tape_arg(args.run_on_tape)
        elif args.run_on_numbers != None:
            tape = write_tape_from_numbers(args.run_on_numbers)
            tape_base = 0
        result = run_tm(machine, max_state_len, tape_base, tape,
                        max_steps, True)
        if not result:
            numbers = 'exceeded step limit'
        else:
            [tape_base, tape, head_position, step_count] = result
            numbers = read_numbers_from_final_tape(tape_base, tape,
                                                   head_position)
        if type(numbers) == list:
            print('Numbers read from final tape:', *numbers)
        elif type(numbers) == str:
            print('No numbers could be read from final tape because:',
                  numbers)
        else:
            raise RuntimeError('impossible ⦃cHbE8e6AFP⦄')
        print('Number of steps:', step_count)
    elif args.comprehensive_test:
        comprehensively_test_machine(machine, max_state_len, max_steps,
                                     test_range, student_id)
    elif args.test_without_running:
        print('\n',
              fill('Your Turing machine is probably legal if this'
                   ' message is printed, because this program should'
                   ' have aborted otherwise.'),
              '\n', sep='')
    else:
        print('\n', fill('You failed to specify what to do.'), '\n',
              sep='', file=sys.stderr)
        parser.parse_args(['--help'])


if __name__ == '__main__':
    main(sys.argv[1:])

# The following comments customize the Emacs programmer's editor.
#
# Local variables:
# fill-column: 72
# tab-always-indent: t
# end:
