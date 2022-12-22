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


"""
say we measure on 5, 10, 15
measure             |              |              |
cycle   1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
instr   n  a  -  a  -

5 is at the second cycle of an ADD instruction which means the ADD hasn't finished computing yet
I don't think it matters if we check before or after incrementing, because the increment+check
operation is 'atomic' with respect to cycle changes. the only thing that matters would be updating
the cycle correctly, that is, before the side effect of the add takes place
"""

def compute(instructions: List[Tuple[str, int]]):
  register_x = 1
  cycle = 1
  strengths = []

  def cycle_incr():
    nonlocal cycle
    # increment before or after we take a signal measurement?
    cycle += 1
    if (cycle - 20) % 40 == 0:
      strengths.append(cycle * register_x)

  while len(instructions) > 0:
    if (cycle - 20) % 40 == 0:
      strengths.append(cycle * register_x)
    instr, maybe_val = instructions.pop()
    if instr == "noop":
      cycle_incr()
    elif instr == "addx":
      cycle_incr()
      cycle_incr()
      # we simulate the side effect of "addx" taking effect (updating the value)
      # happening after the cycle changes. So during the two cycles of an add, the effect is non present
      register_x += maybe_val
  
  print(strengths)
  return strengths


  # modeling multi-cycle clock instructions... where we take a measurement everytime the cycle increments.
  # well, create a hook on cycle increment, as one approach

  # we measure at for non-negative integers n, cycles 20 + 40n
  # for instr, maybe_val in instructions:
  #   if (cycle - 20) % 40 == 0:
  #     strengths.append(cycle * register_x)
  #   if instr == "addx":
  #     pass

def part_1(signals):
  return sum(signals[:6])


def main():
  lines = [ l.strip() for l in open(argv[1]).readlines() ]
  instructions = parse_instructions(lines)
  answer_1 = part_1(compute(instructions))
  print("Part 1", answer_1) # 2580, which is too low

if __name__ == "__main__":
  main()