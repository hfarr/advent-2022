from sys import argv
from typing import List, Tuple


def parse_instructions(lines: List[str]):

  instructions = []
  for line in lines:
    if line == "noop":
      instructions.append( ("noop", None ) )
    else: # addx
      _, value = line.split()
      instructions.append( ("addx", int(value)) )
  return instructions

  # return [ line.split() for line in lines ]

def compute(instructions: List[Tuple[str, int]]):
  register_x = 1
  cycle = 1
  strengths = []

  while len(instructions) > 0:
    if (cycle - 20) % 40 == 0:
      strengths.append(cycle * register_x)
    instr, maybe_val = instructions.pop()

    cycle += 1

  # modeling multi-cycle clock instructions... where we take a measurement everytime the cycle increments.
  # well, create a hook on cycle increment

  # we measure at for non-negative integers n, cycles 20 + 40n
  for instr, maybe_val in instructions:
    if (cycle - 20) % 40 == 0:
      strengths.append(cycle * register_x)
    if instr == "addx":
      pass


def main():
  lines = open(argv[1]).readlines()
  instructions = parse_instructions(lines)

if __name__ == "__main__":
  main()