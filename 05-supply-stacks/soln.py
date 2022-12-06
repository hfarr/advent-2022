
from sys import argv
from typing import Tuple, List, Union
import re
import itertools
import functools

import copy

def compose(*f):
  def binary_compose(f,g):
    def of(x):
      return f(g(x))
    return of
  identity = lambda x: x
  return functools.reduce(binary_compose, f, identity)

def curry(f):
  return lambda a: lambda b: f(a,b)

from collections import namedtuple
# instruction_matcher = re.compile("[^\d]*(\d*)[^\d]*(\d*)[^\d]*(\d*)")
instruction_matcher = re.compile("^move (\d*) from (\d*) to (\d*)$")

Instruction = namedtuple('Instruction', ['amount','source','dest'])
Row = List[Union[str, None]]

BLANK="   "
GAP=" "
LBRACE = "["
RBRACE = "]"
NEWLINE = "\n"
ENDROW = "x"

# lazy parsing
def tokenize(lines: List[str]):
  current = lines.pop(0)
  tokens = []
  stop_line = 1
  offset = 0
  while current != NEWLINE:
    if offset >= len(current):
      current = lines.pop(0)
      offset = 0
      tokens.append(ENDROW)
      continue

    if current[offset] == LBRACE:
      tokens.append(current[offset+1])
      offset += 4
    elif current[offset] == NEWLINE:
      offset = 0
      tokens.append(ENDROW)
      current = lines.pop(0)
    elif current[offset:offset+3] == BLANK:
      tokens.append(None)
      offset += 4
    elif current[offset] == GAP:
      # only really happens once, probably don't need blanks detection
      offset += 1
    else: # number. the BLANK/GAP machinery would work to consume the last line but we don't want None tokens
      # actually we are done
      lines.pop(0)
      return tokens, lines 
      tokens.append(current[offset])
      offset += 4 # last line so we are just chewing through numbers

  return tokens, lines

def parse_crates(tokens):
  rows = []
  current_row = []
  while len(tokens) > 0:
    tok = tokens.pop(0)
    if tok == ENDROW:
      rows.insert(0, current_row)
      current_row = []
      continue
    current_row.append(tok)
  
  # convert rows -> columns (transpose via zip)
  # remove the "None"s
  # convert tuples to lists
  return list(map(compose(list, curry(filter)(lambda x: x)), zip(*rows)))

def parse_instruction(line: str):
  amt, src, dst = tuple(map(int, instruction_matcher.match(line).groups()))
  return Instruction(amt, src - 1, dst - 1)

def parse_instructions(lines):
  return list(map(parse_instruction, lines))

# mutates creates
def part1_execute(crates: List[List[str]], instructions: List[Instruction]):
  count = 0
  for op in instructions:
    count += 1
    # print("instruction", count)
    # print(crates)
    # print(count,instructions[count-1])
    for _ in range(op.amount):
      try:
        crate = crates[op.source].pop()
        crates[op.dest].append(crate)
      except Exception as e:
        print("oop", instructions[count-1])

def part2_execute(crates: List[List[str]], instructions: List[Instruction]):
  for op in instructions:
    crates_in_motion = crates[op.source][-op.amount:]
    crates[op.source] = crates[op.source][:-op.amount]
    crates[op.dest].extend(crates_in_motion)

# Display (queries on crates)
def top_crates(crates: List[List[str]]):
  return [ stack[-1] for stack in crates ]

def lines(filename):
  with open(filename) as f:
    # return list(map(str.strip, f.readlines()))
    return f.readlines()

def main():
  toks, rest = tokenize(lines(argv[1]))
  crate_stacks = parse_crates(toks)
  instructions = parse_instructions(rest)
  
  # print(crate_stacks)
  part1_values = copy.deepcopy(crate_stacks)
  part1_execute(part1_values, instructions)
  # print(crate_stacks)
  part2_values = copy.deepcopy(crate_stacks)
  part2_execute(part2_values, instructions)

  print("Part1", ''.join(top_crates(part1_values)))
  print("Part2", ''.join(top_crates(part2_values)))

if __name__ == "__main__":
  main()