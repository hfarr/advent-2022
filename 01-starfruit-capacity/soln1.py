

puzzle_input = None
with open("input.txt") as f:
  puzzle_input = f.readlines()

max_calories = 0
current_total = 0 

for line in puzzle_input:
  if line == "\n":
    max_calories = max(max_calories, current_total)
    current_total = 0
  else:
    current_total += int(line)

# in case no newline at end
max_calories = max(max_calories, current_total)


print(max_calories)

# 70369


