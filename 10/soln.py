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
      # print("Parsed an add with value", value, "parsed to int as", instructions[-1][1])
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
    print(f" Cycle {cycle:3} register x has", register_x, end="")
    # increment before or after we take a signal measurement?
    cycle += 1
    if (cycle - 20) % 40 == 0:
      # print("ADDING STRENGTH at cycle", cycle)
      strengths.append(cycle * register_x)
      print(". Strength", cycle * register_x)
    else:
      print()

  while len(instructions) > 0:
    instr, maybe_val = instructions.pop(0)
    if instr == "noop":
      print("noop    ", end="")
      cycle_incr()
    elif instr == "addx":
      print(f"addx {maybe_val:3}", end="")
      cycle_incr()
      print("   |    ", end="")
      cycle_incr()
      # we simulate the side effect of "addx" taking effect (updating the value)
      # happening after the cycle changes. So during the two cycles of an add, the effect is non present
      # print("Adding", maybe_val)
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
  return sum(signals)


def main():
  lines = [ l.strip() for l in open(argv[1]).readlines() ]
  instructions = parse_instructions(lines)
  answer_1 = part_1(compute(instructions))
  print("Part 1", answer_1) # 2580, which is too low
  # attempt 2, 10380. still too low. I was reading instructions backwards in part 1 (needed to pop from beginning)
  # attempt 3, 14060. I was adding in values at the wrong time, ugh. it's wrong but they won't tell me too low or too high :(
    # but it is correct for someone else

if __name__ == "__main__":
  main()