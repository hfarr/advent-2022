

puzzle_input = None
with open("input.txt") as f:
  puzzle_input = f.readlines()

# Part 1

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


print("Part 1:", max_calories)

# Part 1 answer 70369

# Part 2:
top_three = [0, 0, 0]

def insert(new_calories):
  index = 0
  while index < 3 and new_calories < top_three[index]:
    index += 1
  if index < 3:
    top_three.insert(index, new_calories)

current_total = 0
for line in puzzle_input:
  if line == "\n":
    insert(current_total)
    current_total = 0
  else:
    current_total += int(line)

if current_total > 0:
  insert(current_total)

print("Top three,", top_three[:3])
print("Total", sum(top_three[:3]))


