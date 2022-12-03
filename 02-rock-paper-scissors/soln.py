# https://adventofcode.com/2022/day/2

from sys import argv

def as_lines(filename):

  with open(filename) as f:
    return f.readlines()

ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissors'


choice_points = {
  ROCK: 1,
  PAPER: 2,
  SCISSORS: 3,
}

def decode(encoded_choice):

  if encoded_choice in ('A', 'X'): 
    return ROCK
  if encoded_choice in ('B', 'Y'): 
    return PAPER
  if encoded_choice in ('C', 'Z'): 
    return SCISSORS

def parse_choices(line):
  return map(decode, line.split())
  # opponent, mine = line.split()
  # return decode(opponent), decode(mine)

def score_game(opponent_choice, my_choice):
  LOSE_SCORE = 0
  TIE_SCORE = 3
  WIN_SCORE = 6
  if opponent_choice == my_choice:
    return TIE_SCORE

  win_scenarios = [
    (ROCK, PAPER),
    (PAPER, SCISSORS),
    (SCISSORS, ROCK)
  ]

  if (opponent_choice, my_choice) in win_scenarios:
    return WIN_SCORE
  
  return LOSE_SCORE

def points_for_choice(choice):
  return choice_points[choice]

def score_round(opponent_choice, my_choice):
  return score_game(opponent_choice, my_choice) + points_for_choice(my_choice)

def part_1(lines):
  rounds = map(parse_choices, lines)
  total = sum([ score_round(*choices) for choices in rounds ])
  print(f"Total {total}")


def determine_choice(opponent_choice, instruction):
  # Lose cycle:
  # ROCK -> SCISSORS -> PAPER
  # X lose: offset 1
  # Y tie: offset 0
  # Z win: offset 2
  instruction_offset = { 'X': 1, 'Y': 0, 'Z': 2 }
  choices = [ ROCK, SCISSORS, PAPER ]

  index = choices.index(opponent_choice)
  my_choice_index = (index + instruction_offset[instruction]) % len(choices)
  return choices[my_choice_index]

def apply_strategy(line):
  choice_code, instruction = line.split()
  opponent_choice = decode(choice_code)
  print("opponent", opponent_choice, " me", determine_choice(opponent_choice, instruction))
  return score_round( opponent_choice, determine_choice(opponent_choice, instruction))

def part_2(lines):
  total = sum(map(apply_strategy, lines))
  print(f"Total {total}")


def main():
  if len(argv) < 2:
    print("enter filename")
    exit(1)
  filename = argv[1]
  lines = as_lines(filename)
  part_1(lines)
  part_2(lines)

print(apply_strategy("B X"))

if __name__ == "__main__":
  pass
  main()

