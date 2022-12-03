from sys import argv


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

def part1(lines):

  print(shared_letter(lines[0]))
  pass


def lines(filename):
  with open(filename) as f:
    return f.readlines()


def main():
  filename = argv[1]
  part1(lines(filename))
  pass

if __name__ == "__main__":
  main()
