
import os
import collections
import math

Point = collections.namedtuple("Point", ["x", "y"])

Beam = collections.namedtuple("Beam", ["point", "direction"])

RIGHT = Point(1, 0)
LEFT = Point(-1, 0)
UP = Point(0, -1)
DOWN = Point(0, 1)

NEXT = {
  (RIGHT, "/"): [UP],
  (LEFT, "/"): [DOWN],
  (UP, "/"): [RIGHT],
  (DOWN, "/"): [LEFT],
  (RIGHT, "\\"): [DOWN],
  (LEFT, "\\"): [UP],
  (UP, "\\"): [LEFT],
  (DOWN, "\\"): [RIGHT],
  (RIGHT, "|"): [UP, DOWN],
  (LEFT, "|"): [UP, DOWN],
  (UP, "|"): [UP],
  (DOWN, "|"): [DOWN],
  (RIGHT, "-"): [RIGHT],
  (LEFT, "-"): [LEFT],
  (UP, "-"): [LEFT, RIGHT],
  (DOWN, "-"): [LEFT, RIGHT],
  (RIGHT, "."): [RIGHT],
  (LEFT, "."): [LEFT],
  (UP, "."): [UP],
  (DOWN, "."): [DOWN],
}

def in_bounds(grid, loc):
  return loc.x >= 0 and loc.x < len(grid[0]) and loc.y >= 0 and loc.y < len(grid)

def next_beams(grid, beam):
  next_point = Point(beam.point.x + beam.direction.x, beam.point.y + beam.direction.y)
  if not in_bounds(grid, next_point):
    return []
  new_dirs = NEXT[(beam.direction, grid[next_point.y][next_point.x])]
  return [Beam(next_point, new_dir) for new_dir in new_dirs]

def sim(grid, start_beam):
  frontier = [start_beam]
  seen = set()
  while frontier:
    new_frontier = []
    for beam in frontier:
      new_beams = next_beams(grid, beam)
      for new_beam in new_beams:
        if new_beam not in seen:
          new_frontier.append(new_beam)
          seen.add(new_beam)
    frontier = new_frontier
  return len({beam.point for beam in seen})

def main(lines):
  grid = []
  for line in lines:
    grid.append(line)
  return sim(grid, Beam(Point(-1, 0), RIGHT))

def main2(lines):
  grid = []
  for line in lines:
    grid.append(line)
  best = -math.inf
  for col in range(len(grid[0])):
    best = max(best, sim(grid, Beam(Point(col, -1), DOWN)))
    best = max(best, sim(grid, Beam(Point(col, len(grid)), UP)))
  for row in range(len(grid)):
    best = max(best, sim(grid, Beam(Point(-1, row), RIGHT)))
    best = max(best, sim(grid, Beam(Point(len(grid[0]), row), LEFT)))
  return best

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day16.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))

main_filename = "day16.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))