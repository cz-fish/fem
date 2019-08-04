from typing import NamedTuple, List, Callable, Dict, Optional
from enum import Enum

class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3
    RightUp = 4
    RightDown = 5
    LeftDown = 6
    LeftUp = 7

InstructionPointer = NamedTuple('IP', [('row', int), ('col', int)])
Instruction = NamedTuple('Instruction',
    [('opcode', str), ('param', str), ('arrow', Optional[Direction])]
)

Program = NamedTuple('Program',
    [('width', int),
    ('height', int),
    ('code', List[List[Instruction]])]
)


class Machine:
    def __init__(self) -> None:
        self.instrmap = {
            'L': self._i_load,
            'S': self._i_store,
            'I': self._i_input,
            'O': self._i_output,
            '+': self._i_add,
            '-': self._i_sub,
            '*': self._i_mul,
            '.': self._i_noop,
            'C': self._i_case,
            'x': self._i_stop,
            'V': self._i_imm,
            'R': self._i_reverse
        }

    def reset(self,
              program: Program,
              input: Callable[[int], int],
              output: Callable[[int, int], None]) -> None:

        self.ip = InstructionPointer(row=0, col=0)
        self.acc = 0
        self.reverse = False
        self.reg: Dict[str, int] = {}
        for i in range(26):
            self.reg[chr(ord('A') + i)] = 0
        self.program = program
        self.input = input
        self.output = output
        self.last_dir = Direction.Right

    def _i_load(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= 'A' and instr.param <= 'Z')
        self.acc = self.reg[instr.param]
        return instr.arrow

    def _i_store(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= 'A' and instr.param <= 'Z')
        self.reg[instr.param] = self.acc
        return instr.arrow
    
    def _i_input(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= '0' and instr.param <= '9')
        self.acc = self.input(ord(instr.param) - ord('0'))
        return instr.arrow

    def _i_output(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= '0' and instr.param <= '9')
        self.output(ord(instr.param) - ord('0'), self.acc)
        return instr.arrow

    def _i_add(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= 'A' and instr.param <= 'Z')
        self.acc += self.reg[instr.param]
        return instr.arrow

    def _i_sub(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= 'A' and instr.param <= 'Z')
        self.acc -= self.reg[instr.param]
        return instr.arrow

    def _i_mul(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= 'A' and instr.param <= 'Z')
        self.acc *= self.reg[instr.param]
        return instr.arrow

    def _i_noop(self, instr: Instruction) -> Optional[Direction]:
        return instr.arrow

    def _i_case(self, instr: Instruction) -> Optional[Direction]:
        if self.acc < 0:
            return Direction.Up
        elif self.acc == 0:
            return Direction.Right
        else:
            return Direction.Down

    def _i_stop(self, instr: Instruction) -> Optional[Direction]:
        return None

    def _i_imm(self, instr: Instruction) -> Optional[Direction]:
        assert(instr.param >= '0' and instr.param <= '9')
        self.acc = ord(instr.param) - ord('0')
        return instr.arrow

    def _i_reverse(self, instr: Instruction) -> Optional[Direction]:
        self.reverse = not self.reverse
        return instr.arrow


    def step(self, instr: Instruction) -> Optional[Direction]:
        if instr.opcode == ' ':
            return self.last_dir

        assert(instr.opcode in self.instrmap)
        d = self.instrmap[instr.opcode](instr)
        if d is None:
            return None
        
        if self.reverse:
            d = {
                Direction.Left: Direction.Right,
                Direction.Up: Direction.Down,
                Direction.Right: Direction.Left,
                Direction.Down: Direction.Up,
                Direction.LeftUp: Direction.RightDown,
                Direction.RightUp: Direction.LeftDown,
                Direction.LeftDown: Direction.RightUp,
                Direction.RightDown: Direction.LeftUp
            }[d]
        
        self.last_dir = d
        return d

    def run(self) -> None:
        self.reset(self.program, self.input, self.output)
        while True:
            i = self.program.code[self.ip.row][self.ip.col]
            d = self.step(i)
            if d is None:
                break
            move = {
                Direction.Left: InstructionPointer(row=0, col=-1),
                Direction.Up: InstructionPointer(row=-1, col=0),
                Direction.Right: InstructionPointer(row=0, col=1),
                Direction.Down: InstructionPointer(row=1, col=0),
                Direction.RightUp: InstructionPointer(row=-1, col=1),
                Direction.RightDown: InstructionPointer(row=1, col=1),
                Direction.LeftUp: InstructionPointer(row=-1, col=-1),
                Direction.LeftDown: InstructionPointer(row=1, col=-1)
            }[d]
            self.ip = InstructionPointer(
                row = (self.ip.row + move.row) % self.program.height,
                col = (self.ip.col + move.col) % self.program.width
            )