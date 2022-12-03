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

def lines(filename):
  with open(filename) as f:
    return f.readlines()

def main():
  filename = argv[1]
  part1(lines(filename))
  pass

if __name__ == "__main__":
  main()
