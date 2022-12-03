from sys import argv
import itertools

# compute the letter that is in both the first half and second half of the string
def shared_letter(line):
  length = len(line)
  # first_half = line[:length // 2]
  first_half = set(line[:length // 2])
  second_half = line[length // 2:]
  for c in second_half:
    if c in first_half:
      return c
  print("issue, not found", line)

def priority(letter):
  ordinal = ord(letter)
  if ordinal >= ord('a'):
    return ordinal - ord('a') + 1
  return ordinal - ord('A') + 27

def part1(lines):

  total = sum([ priority(shared_letter(line)) for line in lines ])
  print(f"total {total}")


def find_common(first_line, *lines):

  intersection = set(first_line)
  for line in lines:
    intersection.intersection_update(set(line))

  # print(len(intersection), list(intersection)) # 1

  return list(intersection)[0]


def group(iterable, group_size):
  return zip( *([iter(iterable)] * 3) )

def part2(lines):
  groups = group(lines, 3)
  total = sum([ priority(find_common(*group)) for group in groups ])
  print(f"total {total}")

def lines(filename):
  with open(filename) as f:
    return list(map(str.strip, f.readlines()))

def main():
  # filename = argv[1]
  scenario = lines(argv[1])

  part1(scenario)
  part2(scenario)
  pass

if __name__ == "__main__":
  main()
