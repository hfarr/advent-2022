from sys import argv
from typing import Tuple, List

import itertools
import functools



def compose(*f):
  def binary_compose(f,g):
    def of(x):
      return f(g(x))
    return of
  identity = lambda x: x
  return functools.reduce(binary_compose, f, identity)

def flip(f):
  return lambda a, b: f(b, a)

def curry(f):
  return lambda a: lambda b: f(a,b)

def delimit(delimiter):
  return curry(flip(str.split))(delimiter)

def isnot(predicate):
  return lambda x: not predicate(x)

# inclusive bound range of integers
class Range():
  __slots__ = ["lb", "rb"]
  def __init__(self, left_bound, right_bound):
    # invariant: self.lb <= self.rb
    self.lb = left_bound
    self.rb = right_bound

  def __repr__(self) -> str:
    return f"Range:[{self.lb}, {self.rb}]"

  @classmethod
  def from_str_list(cls: 'Range', vals: List[str]):
    # its cheating (not really but in that "this is not the responsibility of Range, Im just doing this for ease" way) 
    # a bit to do the int parsing here but oh well
    return cls(int(vals[0]), int(vals[1]))

    # could do something like return "BadRange" if lb > rb but we will assume good inputs for this challenge
  
  def contains(self,other: 'Range'):
    return all(map( lambda x: x in range(self.lb, self.rb + 1), (other.lb, other.rb)))

  def overlaps(self, other: 'Range'):
    return other.lb in self or other.rb in self or self.lb in other or self.rb in other

  def __contains__(self, elem):
    return elem in range(self.lb, self.rb + 1)

def print_range_pairs(tups):
  for tup in tups:
    print(tup)

def parse_range(string):
  # would need applicatives to encode the 'flatten' behavior I want, here we have to flatten manually.
  # that is we'd convert all functions to ones that operate on, in this case, lists and get that behavior
  # by default. for now though...
  # I want to express as: compose(delimit("-"), delimit(",")) 
  # but the result of the first delimit is a list not a string and we'd need to build in the pipelining
  # for that using ~functional shenanigans~ which I won't do (at least not yet). instead,
  f = compose(tuple, curry(map)(compose(Range.from_str_list, delimit("-"))), delimit(","))
  return f(string)
  # okay it's getting silly but I like it

def part_1(assignment_pairs: List[Tuple[Range, Range]]):

  contained_ranges_among_pairs = 0
  # print(assignment_pairs[0])
  for r1, r2 in assignment_pairs:
    if r1.contains(r2) or r2.contains(r1):
      contained_ranges_among_pairs += 1
  
  print(f"Fully container partners {contained_ranges_among_pairs}")
  pass

def part_2(assignment_pairs: List[Tuple[Range, Range]]):
  def overlaps(tup: Tuple[Range,Range]):
    r1, r2 = tup
    return r1.overlaps(r2)
  num_overlapping = len(list(filter(overlaps, assignment_pairs)))
  non_overlapping = list(filter(isnot(overlaps), assignment_pairs))
  print(f"Not overlapping {len(non_overlapping)}")
  # print_range_pairs(non_overlapping)
  print(f"Overlapping {num_overlapping}")


# now that we have a couple puzzles using this, a library is starting to make sense!
def lines(filename):
  with open(filename) as f:
    return list(map(str.strip, f.readlines()))

def main():
  scenario = lines(argv[1])
  part_1(list(map(parse_range, scenario)))
  part_2(list(map(parse_range, scenario)))

  
if __name__ == "__main__":

  main()
