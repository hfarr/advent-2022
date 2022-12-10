from sys import argv
from typing import Tuple, List, Union, Dict
import re
import itertools
import functools


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
    return sum([ f.size() for f in self.files ])

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
    def rec(f: DirFile, depth):
      return f"{'  '*depth}- {f.name} (dir)"

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
        current_dir.add_file(DirFile(second, current_dir, first))
  
  return root

def main():
  lines = open(argv[1]).readlines()
  structure = parse_fs_tree(lines)

  print(structure)
  # print(str(structure))

if __name__ == "__main__":
  main()
