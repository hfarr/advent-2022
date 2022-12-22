from __future__ import annotations
from enum import unique
from itertools import accumulate

from sys import argv
from typing import List

# unknown max dimensions of the grid ahead of time 
# so we model with vectors offset from (0,0)

def abs(number):
  return number if number >= 0 else -number

class Vec2D:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.coords = (x,y)

  # hmm, I want to say, like, defining __add__ let's us override "+"
  # but I don't have internet and I am not sure I want to experiment
  # silly goose of course I'll experiment
  # yeah it is __add__
  def __add__(self, other):
    return Vec2D(self.x + other.x, self.y + other.y)

  # ditto this could be a "__sub__" right?
  def __sub__(self, other):
    return Vec2D(self.x - other.x, self.y - other.y)

  def __hash__(self) -> int:
      return hash(self.coords)

  # without this we will get "false negative" hash collisions- that is,
  # two will collide, and it will treat them differently e.g negatively
  # reporting they're different, since after a hash matches python will
  # check equality.
  def __eq__(self, other: Vec2D) -> bool:
    return self.coords == other.coords

  # not really a "taxi" normalization. I mean it is a norm, right? 
  # there are proper definitions. hm. I need to brush up on linear algebra
  # here it's just a kind of cheap trick to resolve the "diagonal" steps
  # into a "unit" step
  def taxi_normal(self):
    newX = abs(self.x) // self.x if self.x != 0 else 0
    newY = abs(self.y) // self.y if self.y != 0 else 0
    return Vec2D(newX, newY)

  # "taxi distance" again not really correct per "taxi" definition.
  # I'm kinda making up my own norm, where instead of sum(distx, disty)
  # its max(distx, disty). which may or may not be a well defined norm.
  # i would have to crack open my notes. hmm. I may have notes on my laptop.
  def distance(self, other):
    # should be same as "length(diff(self, other))"
    distX = abs(self.x - other.x)
    distY = abs(self.y - other.y)
    return max(distX, distY)

  def __str__(self):
    return str(self.coords)
  
  def __repr__(self):
    return str(self)

UNITS = {
  "R": Vec2D(1,0),
  "U": Vec2D(0,1),
  "L": Vec2D(-1,0),
  "D": Vec2D(0,-1),
}

def accumulate_unique_tail_positions(steps: List[Vec2D]):
  head = tail = origin = Vec2D(0,0)

  unique_positions = { tail }

  count = 0
  unique_count = 0

  for step in steps:
    count += 1
    # print(head, "+", step, "=", head+step)
    head += step
    # it's probably fine if this is just an 'if', it should NEVER be more than 2 after all

    while head.distance(tail) > 1:

      # Step "tail" towards "head" one 'unit' at a time
      # unit being a step in a cardinal or diagonal direction
      diff = (head - tail)
      tail += diff.taxi_normal()  # The metric/norm is not taxicab, I'm pretty sure. what I consider one unit diagonally taxi would have as 2, but I can't think of a name at the moment

      # if tail not in unique_positions:
      #   print(tail)
      # if tail not in unique_positions:
      #   unique_count += 1
      unique_positions.add(tail)

  # print(unique_positions)
  # print(len(unique_positions), unique_count)
  return len(unique_positions)

def accumulute_unique_long_rope(knots: int, steps: List[Vec2D]):
  # origin = Vec2D(0,0)
  # I mean... linked list, yeah? doubly so? mer
  rope = [ Vec2D(0,0) for _ in range(knots) ]
  unique_positions = { rope[-1] }

  for step in steps:
    rope[0] += step
    for i in range(1, len(rope)):  # see a doubly linked list.. we could visit node.parent instead of rope[i-1]
      if rope[i - 1].distance(rope[i]) > 1:
        diff = rope[i - 1] - rope[i]
        rope[i] += diff.taxi_normal()

    unique_positions.add(rope[-1])  # only the tail
  
  return len(unique_positions)

part_1 = accumulate_unique_tail_positions
part_2 = accumulute_unique_long_rope

def parse_step_from_line(line: str):
  direction, amount = line.split()
  return [ UNITS[direction] ] * int(amount)

def parse_steps(lines: List[str]):
  steps = []
  for line in lines:
    steps.extend(parse_step_from_line(line))
  return steps

def main():
  lines = open(argv[1]).readlines()
  steps = parse_steps(lines)
  print(len(steps), "steps to execute")

  answer_1 = part_1(steps) # currently 8922, which is too high
  # wait it's correct now with 6190... oh because I was missing __eq__ in Vec2D
  print("Part 1", answer_1, "unique positions")

  test_1 = part_2(2, steps) # should match answer_1
  vecspect(answer_1, test_1)

  answer_2 = part_2(10, steps)
  print("Part 2", answer_2, "unique positions") # 2516, correct


def vecspect(expected, actual, iter=None):
  if iter:
    print("Iteration", iter, end=": ")

  if actual != expected:
    print("expected", expected, "but got", actual)

# test compute diff of horizontal step
def test1():
  for i in range(10):
    tail = Vec2D(0+i,0)
    head = Vec2D(2+i,0)

    expect = Vec2D(1,0)

    # code duplication, not exactly best testing we got
    diff = (head - tail)
    actual = diff.taxi_normal()
    # tail += diff.taxi_normal()
    vecspect(expect, actual)

def test2():
  # I'd rather test like, a "move head" function, then test that the tail moves to the expected spot, but I opted not to program like
  # that, and for the moment I will try to avoid refactoring for that. although maybe I should
  """
  . h .  ->  . t h
  t . .      . . .
  """
  tail = Vec2D(0,0)
  head = Vec2D(2,1)
  expect_pos = Vec2D(1,1)
  actual = tail + (head - tail).taxi_normal()
  vecspect(expect_pos, actual)

def test3():
  tail = Vec2D(3,3)
  head = tail
  vecspect(0, head.distance(tail))

def tests():
  test1()
  test2()
  test3()

if __name__ == "__main__":
  main()
  # tests()