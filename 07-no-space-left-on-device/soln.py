from sys import argv
from typing import Tuple, List, Union, Dict
import re
import itertools
import functools
import math

class DirFile:

  def __init__(self, name, parent, size):
    self.name: str = name
    self.filesize: int = size
    self.parent: Dir = parent
  
  def size(self):
    return self.filesize
  
  def __contains__(self, element):
    return False

  def __repr__(self) -> str:
    return f"- {self.name} (file, size={self.filesize})"

  def traverse(self, base, rec, depth = 0):
    return [ base(self, depth) ]

class Dir(DirFile):
  def __init__(self, name, parent):
    super().__init__(name, parent, 0)
    self.__memosize = None
    self.name = name
    self.files: Dict[str, DirFile] = dict()

  def add_files(self, files: List[DirFile]):
    for f in files:
      self.files[f.name] = f
      f.parent = self
  
  def add_file(self, file: DirFile):
    if file not in self:
      self.files[file.name] = file
      file.parent = self

  def size(self):
    
    # anticipates the directory doesn't change after creation
    if not self.__memosize:
      self.__memosize = sum([ f.size() for f in self.files.values() ])
    return self.__memosize

  def __contains__(self, element: DirFile):
    return element.name in self.files

  # pre order traversal
  def traverse(self, base, rec, depth = 0):
    results = [ f.traverse(base, rec, depth + 1) for f in self.files.values() ]
    concatted = []
    for r in results:
      concatted.extend(r)

    # there's probably an iterable way to flatmap
    # return [ rec(self, depth) ] + [ f.traverse(base, rec, depth + 1) for f in self.files.values() ]

    return [ rec(self, depth) ] + concatted

  def __str__(self):
    return repr(self)
  
  def __repr__(self) -> str:
    return f"{self.name} (dir, {self.size()})"

  def pretty_print(self) -> str:
    # def rec(f: DirFile, depth):
    #   return f"{'  '*depth}- {f.name} (dir)"
    def rec(f: DirFile, depth):
      return f"{'  '*depth}- {f.name} (dir, size={f.size()})"

    def base(f: DirFile, depth):
      return f"{'  '*depth}{str(f)}"

    contents = self.traverse(base, rec)
    return "\n".join(contents)
  
CMD_START = "$"
CD = "cd"

def parse_fs_tree(lines):

  # root = Dir("/")
  # current_dir = root
  # I debated not having it default but python typing is not helpful when things aren't bound
  root: Dir = Dir("/", None)
  current_dir: Dir = root
  
  # Except for root, we assume that the dir passed already exists. that is, it's been found after interrogating another dir.
  def change_dir(fname):
    nonlocal root, current_dir
    if fname == "/":  # special case for root
      current_dir = root
    elif fname == "..":
      current_dir = current_dir.parent
    else:
      current_dir = current_dir.files[fname]

  for line in lines:
    [ first, second, *rest ] = line.split()

    # I need to install python 3.10 or higher omg
    if first == CMD_START:
      if second == CD:
        change_dir(rest[0])
      # LS- we will not do anything special here, the files will naturally be added
    else: # output line from LS
      if first == "dir":  # directory
        current_dir.add_file(Dir(second, current_dir))  # redundantly setting current dir here and in add_file
      else: # file
        current_dir.add_file(DirFile(second, current_dir, int(first)))
  
  return root

def collect_dirs(structure: DirFile):
  dirs: List[Dir] = list()
  base = lambda _, __: 0
  def rec(f: Dir, _):
    dirs.append(f)
    return 0
  # executed for side effect
  structure.traverse(base, rec)
  return dirs

# small dir sums
def part_1(structure: DirFile):
  dirs = collect_dirs(structure)

  # print(dirs)
  # small_dirs = filter( lambda d: d.size() <= 100000, dirs)
  result = sum([ d.size() for d in dirs if d.size() <= 100000])
  return result
  
def part_2(structure: DirFile):
  dirs = collect_dirs(structure)
  dirs.sort(key=lambda dir: dir.size(), reverse=True)
  TOTAL_SPACE = 70_000_000
  # USED_SPACE = TOTAL_SPACE - structure.size() # this actually computes FREE SPACE. free_space + deleted would be our answer.
  USED_SPACE = structure.size()
  FREE_SPACE = TOTAL_SPACE - USED_SPACE
  SPACE_NEEDS = 30_000_000
  can_free = lambda dir: FREE_SPACE + dir.size() >= SPACE_NEEDS

  # can do a bsearch lmao (that is, increase index exponentially rather than linearly)
  # it's kind of a bsearch. I guess technically a bsearch would be continually taking midpoints,
  # but it's a similar idea. can probably compare the runtimes.
  champion = None # smallest dir we can delete
  idx = 0
  increment = 1
  # invariant: idx always points to a valid dir, one that satisfies the predicate, supposing at least one satisfies the predicate
  while increment > 0 and idx < len(dirs):
    while idx + increment >= len(dirs):
      increment //= 2

    if can_free(dirs[idx + increment]):
      # because we sorted,  this file will always be at least as good as a choice as the champion, so we replace it
      champion = dirs[idx + increment] 
      idx += increment
      increment *= 2
    else:
      increment //= 2
  
  # print(FREE_SPACE + champion.size())
  # print(FREE_SPACE + dirs[idx + 1].size())
  return champion.size()

def main():
  lines = open(argv[1]).readlines()
  structure = parse_fs_tree(lines)

  print(structure.pretty_print())
  print()
  # print(str(structure))
  print("Sum of sizes of dirs less than 100000")
  print(part_1(structure))
  print()
  print("(size of) Best directory to delete")
  print(part_2(structure))
  print()


if __name__ == "__main__":
  main()
