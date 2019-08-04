#!/usr/bin/env python3

import sys
import Machine
from typing import List

class ProgramParser:
    @staticmethod
    def load(fname: str) -> Machine.Program:
        code: List[List[Machine.Instruction]] = []
        wid = 0

        with open(fname, 'rt') as f:
            for l in f.readlines():
                code += [ProgramParser.parse_line(l)]
                wid = max(wid, len(code[-1]))
        
        hei = len(code)
        for i in range(hei):
            code[i] += [Machine.Instruction(
                opcode=' ', param=' ', arrow=None
            )] * (wid - len(code[i]))

        return Machine.Program(
            width=wid, height=hei, code=code
        )


    @staticmethod
    def parse_line(line: str) -> List[Machine.Instruction]:
        res: List[Machine.Instruction] = []
        for i in range(0, len(line), 4):
            #assert(len(line) <= i+3 or line[i+3] == ' ')

            opcode = line[i]
            param = line[i+1] if len(line) > i+1 else ' '
            arrow_c = line[i+2] if len(line) > i+2 else ' '
            if arrow_c == ' ':
                arrow = None
            else:
                assert(arrow_c >= '0' and arrow_c <= '9')
                arrow={
                    0: Machine.Direction.Up,
                    1: Machine.Direction.Right,
                    2: Machine.Direction.Down,
                    3: Machine.Direction.Left,
                    4: Machine.Direction.RightUp,
                    5: Machine.Direction.RightDown,
                    6: Machine.Direction.LeftDown,
                    7: Machine.Direction.LeftUp
                }[ord(arrow_c) - ord('0')]

            res += [Machine.Instruction(
                opcode=opcode,
                param=param,
                arrow=arrow
            )]
        return res


def input(i: int) -> int:
    return 11

def output(i: int, val: int):
    print('Output {}: {}'.format(i, val))

def main():
    prog = ProgramParser.load('factorial.fem')
    mach = Machine.Machine()
    mach.reset(prog, input, output)
    mach.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())