# FEM - Filip's Evil Machine

FEM is a programming language. Programs in FEM consist of instructions placed in a two-dimensional *grid*. Each instruction has an *opcode*, a *parameter* and a continuation *arrow*. A program can have a number of inputs and outputs. The machine has 26 integer registers and an integer accumulator.

## Program execution
The *instruction pointer* starts on the top left instruction in the grid. The program loop executes one instruction, pointed to by the *instruction pointer*, and then moves the *pointer* to the next instruction in the direction of the *arrow*, except for special cases of instructions `case`, `reverse` and `stop` (see below).

The program stops if it executes the instruction `stop`, or if it executes instruction `input` when there is no more input left.

When the *instruction pointer*, transitioning to the next instruction, crosses the edge of the program *grid*, it wraps around.

For example:

* if the *pointer* is in the leftmost column and the *arrow* points left, the *pointer* jumps to the rightmost column of the same row of the *grid*.
* If the *pointer* is in the bottom row and rightmost column and the *arrow* points bottom right, the *pointer* jumps to the top row and leftmost column of the *grid*.

Cells of the program *grid* can also be left blank. If a program steps onto a blank cell, it doesn't execute any instruction, and moves the *instruction pointer* one step in the same direction as the previous step. In the special case when the first instruction of a program (the top left cell of the *grid*) is blank, the *instruction pointer* will move to the right.

## Registers
The machine has 26 registers, labelled `A` through `Z`. It also has a single accumulator, denoted `acc`, which is the source or target of most instructions. All registers and the `acc` can hold signed integer values. The range of applicable values and behavior in case of overflow/underflow are yet to be specified.

All registers as well as `acc` start initialized as `0` at the beginning of the program.

## Instructions

* `[L] load <R>` - load value from register `<R>` to `acc`
* `[S] store <R>` - store value from `acc` to register `<R>`
* `[I] input <I>` - load value from input number `<I>` to `acc`
* `[O] output <O>` - store value from `acc` to output `<O>`
* `[+] add <R>` - add value of register `<R>` to `acc`
* `[-] sub <R>` - subtract value of register `<R>` from `acc`
* `[*] mul <R>` - miltiply `acc` with value of register `<R>`
* `[.] noop` - do nothing
* `[C] case`
     * This instruction doesn't have any *arrow*. The movement of the *instruction pointer* is determined by the value of `acc` and the *reverse* mode.
     * If value of `acc` is less than 0, instruction pointer moves up.
     * If value of `acc` is equal to 0, instruction pointer moves to the right.
     * If value of `acc` is greater than 0, instruction pointer moves down.
     * In the *reverse* mode, all the directions are exactly opposite (`acc < 0` - down, `acc = 0` - left, `acc > 0` - up).
* `[x] stop` - stop the program
* `[V] imm <V>` - load immediate value `<V>` into `acc`. The value can be an integer from 0 to 9 (inclusive)
* `[R] reverse`
     * Toggle *reverse* mode.
     * The program starts with *reverse* mode off.
     * When in *reverse* mode, all *arrows* are are inverted. For example, if an instruction has an *arrow* pointing to left up, the instruction pointer will move down and right in *reverse* mode.

## Program representation

Programs are written in a plaintext file. Each line is one row of the program grid. Line endings are either \r, \n or both and line ending at the end of the file is optional.

If there is a blank line in the program file, it denotes end of the program grid. Everything after the blank line is ignored (subject to future extensions).

Each instruction is represented as 3 characters. Instructions on the row are separated by a single space. There can be optional blank spaces at the end of each line.

The 3 characters of each instruction are representing, in order:
* *opcode*
     * opcode of each instruction is specified in brackets [] in the *Instructions* section.
* *parameter*
     * For a register parameter, this is the letter `A` through `Z`.
     * For a value parameter (including `input`, `output` instruction parameters), this is a digit `0` through `9`.
     * If an instruction doesn't use parameter, this is a blank space `' '`.
* *arrow*
     * 0 - up
     * 1 - right
     * 2 - down
     * 3 - left
     * 4 - right up
     * 5 - right down
     * 6 - left down
     * 7 - left up
     * If an instruction doesn't have an arrow, this is a blank space.

Blank cell is represented as 3 spaces.

## Example programs

### Factorial of n

`n` is provided as input 0

```
I01 SB6 SO2 LC2     SE3 +O3 LE3 O01 x
V11 SC4 SE4 *E1 SC1 LE1 -B1 C   LC0
```

(grid size 10 x 2)

### Odd or even

A list of numbers if provided on input 0. For each of them, the program will put on output 0 either `0` if the value is even, or `1` if it is odd.

```
I01 . 1 SA1 V12
R 0 -A2 V03 SB3
    -B1 +B1 R 4
O02 V01 C   V11
    R 4 +B1
```

(grid size 4 x 5)

## Extension Ideas
* Add stacks (at least 2), and instructions push/pop
* Interpreter flags determine the size of registers
     * Also allow to work with characters instead of int
     * Add a line to the end of the program file with the interpreter flags
* (?) Division, modulo, bitwise logical operators