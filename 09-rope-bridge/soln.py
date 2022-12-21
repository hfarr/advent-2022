
# unknown max dimensions of the grid ahead of time 
# so we model with vectors offset from (0,0)

def abs(number):
  return number if number >= 0 else -number

class Vec2D:

  def __init__(self, x, y):
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

  # not really a "taxi" normalization. I mean it is a norm, right? 
  # there are proper definitions. hm. I need to brush up on linear algebra
  # here it's just a kind of cheap trick to resolve the "diagonal" steps
  # into a "unit" step
  def taxi_normal(self):
    newX = 1 if self.x > 0 else 0
    newY = 1 if self.y > 0 else 0
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

  

