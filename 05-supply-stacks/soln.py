
from sys import argv
from typing import Tuple, List, Union
import re
import itertools
import functools

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
      offset += 3
    elif current[offset] == NEWLINE:
      offset = 0
      tokens.append(ENDROW)
      current = lines.pop(0)
    elif current[offset:offset+3] == BLANK:
      tokens.append(None)
      offset += 3
    elif current[offset] == GAP:
      offset += 1
    else: # number. the BLANK/GAP machinery would work to consume the last line but we don't want None tokens
      tokens.append(current[offset])
      offset += 4 # last line so we are just chewing through numbers

  return tokens, lines

def parse_crates(tokens):
  tok = tokens.pop(0)
  while tok != '1': # start of the numeral row
    pass
  
def parse_instruction(line: str):
  return Instruction(*map(int, instruction_matcher.match(line).groups()))

def part_1(scenario):
  pass

def lines(filename):
  with open(filename) as f:
    # return list(map(str.strip, f.readlines()))
    return f.readlines()

def main():
  toks, rest = tokenize(lines(argv[1]))
  print(toks)
  pass

if __name__ == "__main__":
  main()