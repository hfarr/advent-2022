
from sys import argv
from typing import Tuple, List, Union, Dict
import re
import itertools
import functools
import math

from collections import namedtuple, defaultdict
from enum import Enum

TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3

Comparison = namedtuple('Comparison', ['current', 'pos', 'coordinate'])

def print_grid(grid):
  for i in range(len(grid)):
    for j in range(len(grid)):
      print(grid[i][j],end="")
    print()

def print_grid_dict(length, grid):
  for i in range(length):
    for j in range(length):
      if grid[(i,j)] == -1:
        print("-",end="")
      else:
        print(grid[(i,j)],end="")
    print()

def print_tallest_froms(grid, tallest_from):

  for idx in TOP, BOTTOM, LEFT, RIGHT:

    for i in range(len(grid)):
      for j in range(len(grid)):
        if tallest_from[(i,j)][idx] == -1:
          print("-",end='')
          continue
        print(tallest_from[(i,j)][idx], end='')
      print()
    print()

def abs(number):
  return number if number >= 0 else -number

# slightly better than brute I think
def compute_tallest_from(grid: List[List[int]]):

  tallest_from_top = grid[1]
  grid_dict = defaultdict(lambda: -1)
  for i in range(len(grid)):  
    for j in range(len(grid)):
      # maybe something from itertools could help here, it's a "zip"ish move, somewhat
      grid_dict[(i,j)] = grid[i][j]

  tallest_from = defaultdict(lambda: [-1]*4)
  # sight_block_from = defaultdict(lambda: [None]*4)  # maps a coord to coords, in all directions, of tree blocking LOS
  sight_block_from = defaultdict(lambda: [0]*4)  # maps a coord to distance of the tree blocking LOS in that direction
  # grid is a square
  LAST_IDX = len(grid) - 1

  # print_grid(grid)
  # print()
  # print_grid_dict(len(grid), grid_dict)

  #                         row         column
  hoz_opp = lambda coord: (coord[0], len(grid) - 1 - coord[1])
  ver_opp = lambda coord: (len(grid) - 1 - coord[0], coord[1])

  #         direction, offset func
  top =     TOP,    lambda coord, amt=1: (coord[0] - amt, coord[1]), 0
  bottom =  BOTTOM, lambda coord, amt=1: (coord[0] + amt, coord[1]), 0
  left =    LEFT,   lambda coord, amt=1: (coord[0], coord[1] - amt), 1
  right =   RIGHT,  lambda coord, amt=1: (coord[0], coord[1] + amt), 1

  # def find_blocking

  for row_idx in range(0, len(grid)):
    for col_idx in range(0, len(grid)):
      coord = (row_idx, col_idx)
      # eight settings to perform
      # each comp is done twice when we only need them done once. 
      # e.g on hoz axis, as column moves, only one needs the "top" op, because it will sweep and pick up the other.
      #     on ver axis, as row moves, only one needs left
      # in fact it applies for all. when we cross the half way point in either case we end up with dups.
      # and since it does corners, while one is sweeping left -> right, it's hoz opposites are sweeping right -> left
      # and need the opposite opps. might be a bit painstaking but we could filter out the opps.
      comp = [
        (coord, top),
        (coord, left),
        (hoz_opp(coord), top),
        (hoz_opp(coord), right),
        (ver_opp(coord), bottom),
        (ver_opp(coord), left),
        (ver_opp(hoz_opp(coord)), bottom),
        (ver_opp(hoz_opp(coord)), right),
      ]

      # print(coord)
      for coordinate, (dir, offset, coord_idx)  in comp:
        neighbor = offset(coordinate)
        # print("  ", coordinate, tallest_from[neighbor], grid_dict[neighbor])
        tallest_from[coordinate][dir] = max( tallest_from[neighbor][dir], grid_dict[neighbor] )

        if neighbor[coord_idx] in (-1,len(grid)): 
          # this tree is on the edge and the direction we're looking in has no trees, so continue on
          continue

        distance = 1
        cur_blocking = offset(coordinate)

        # for our scenario, the tallest tree is never more than 9, which is an upper bound on the number
        # of iterations this can go through.
        # if we extend the problem to trees of arbitrary positive heights the asymptotics go to
        # O(n*m * min(max(n,m), tallest_tree_size))
        # at least, pretty sure part 1 on its own is n*m. a high constant factor but we do it one one pass
        # through the full array.
        # part 2 is still O(n*m) if we consider the bounded max height of trees.
        # though maybe we shouldn't consider that bound as making this loop constant, big-o algorithm
        # analysis has some red herrings
        while grid_dict[coordinate] > grid_dict[cur_blocking]:
          candidate_distance = sight_block_from[cur_blocking][dir]

          if candidate_distance == 0:
            # the candidate is on the edge and shorter than us, no more trees to review.
            sight_block_from[coordinate][dir] = distance
            break

          # essentially chaining/accumulating distances till the end
          distance += candidate_distance
          cur_blocking = offset(cur_blocking, candidate_distance)
          # could also be offset(coordinate, distance), but the above makes the "chaining" explicit

        
        # print("  ", sight_block_from[coordinate], distance)
        sight_block_from[coordinate][dir] = distance
  
  return grid_dict, tallest_from, sight_block_from

def get_best_scenic(sight_block_from):

  # scenic_scores = defaultdict(lambda: 0)

  best_scenic = 0
  for view_distances in sight_block_from.values():
    product = math.prod(view_distances)
    if product > best_scenic:
      best_scenic= product
  return best_scenic

def count_visible(grid: List[List[int]]):
  grid_dict, tallest_from, sight_block_from = compute_tallest_from(grid)

  # print_tallest_froms(grid, sight_block_from)
  # return 0
  print_tallest_froms(grid, tallest_from)

  visible = defaultdict(lambda: False)
  pretty_visible = defaultdict(lambda: '.')

  dirs = TOP, BOTTOM, LEFT, RIGHT

  def is_visible(coord):
    nonlocal dirs
    # A tree is visible if it is taller than the tallest tree looking out to all directions
    # no silly.. a tree is visible if it is taller than at least one of the trees looking out to all directions
    return any( [ grid_dict[coord] > tallest_from[coord][dir] for dir in dirs ] )

  for coord in grid_dict:
    visible[coord] = is_visible(coord)
    pretty_visible[coord] = 'x' if is_visible(coord) else '.'

  print_grid_dict(len(grid), pretty_visible)

  # could, and maybe should, split these into separate functions
  num_visible = sum(filter(lambda x: x, visible.values()))
  best_scenic = get_best_scenic(sight_block_from)

  return num_visible, best_scenic


def parse_input(lines):
  return [ [ int(c) for c in line.strip() ] for line in lines ]

def main():
  lines = open(argv[1]).readlines()
  grid = parse_input(lines)
  visible_trees, best_scenic_score = count_visible(grid)
  
  print("Part 1: visible_trees")
  print(visible_trees)
  print()

  print("Part 2: scenic score")
  print(best_scenic_score)
  print()

if __name__ == "__main__":
  main()