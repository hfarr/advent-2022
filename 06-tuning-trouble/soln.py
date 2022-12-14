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



def find_sequence_distinct(buffer, length):
  
  position = length

  while position + length < len(buffer):
    chars = set(buffer[position-length:position])
    if len(chars) == length:
      return position
    position += 1
  
  # no marker, shouldn't happen
  pass
def part_1(buffer):
  return find_sequence_distinct(buffer, 4)

def part_2(buffer):
  return find_sequence_distinct(buffer, 14)

def main():
  buffer = None
  with open(argv[1]) as f:
    buffer = f.read().strip()

  result_1 = part_1(buffer)
  print(result_1)
  print(part_2(buffer))


if __name__ == "__main__":
  main()