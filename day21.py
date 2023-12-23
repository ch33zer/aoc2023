
import os
import sys
import math
def p(grid, frontier):
  for y in range(len(grid)):
    s = ""
    for x in range(len(grid[0])):
      if (x,y) in frontier:
        c = "O"
      else:
        c = grid[y][x]
      s += c
    print(s)

def in_bounds(grid, point):
  return 0 <= point[0] < len(grid[0]) and 0 <= point[1] < len(grid) 

def sim(grid, start, steps, label=None):
  frontier = set([start])
  for _ in range(steps):
    new_frontier = set()
    for x, y in frontier:
      for offx, offy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new = x + offx, y + offy
        newx, newy = new
        if in_bounds(grid, new) and grid[new[1]][new[0]] != "#":
          new_frontier.add(new)
    frontier = new_frontier
  if label:
    print(f"{label} starting from {start} for {steps}:")
    p(grid, frontier)
  return len(frontier)

def main(lines):
  s = 0
  grid = []
  for line in lines:
    grid.append(list(line))
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      if grid[y][x] == "S":
        start = (x, y)
        break
  return sim(grid, start, 64)

def main2(lines):
  s = 0
  grid = []
  for line in lines:
    grid.append(list(line))
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      if grid[y][x] == "S":
        start = (x, y)
        break
  assert len(grid) == len(grid[0])
  assert len(grid) % 2 == 1
  assert start[0] == (len(grid)-1) // 2 and start[1] == (len(grid)-1) // 2
  # Mostly from https://www.reddit.com/r/adventofcode/comments/18o4y0m/2023_day_21_part_2_algebraic_solution_using_only/
  STEPS = 26501365
  w = h = len(grid)
  #import pdb; pdb.set_trace()
  N = (STEPS - (start[0])) // w
  even = sim(grid, start, 3 * w, "even")
  odd = sim(grid, start, (3 * w) + 1, "odd")
  bottom = w - 1
  big_corner_steps = ((3*w) - 3) // 2
  big_corners = (sim(grid, (0, 0), big_corner_steps, "Big corner") + sim(grid, (0, bottom), big_corner_steps, "Big corner") +
    sim(grid, (bottom, 0), big_corner_steps, "Big corner") + sim(grid, (bottom, bottom), big_corner_steps, "Big corner"))
  small_corners_steps = (w-3) // 2
  small_corners = (sim(grid, (0, 0), small_corners_steps, "Small corner") + sim(grid, (0, bottom), small_corners_steps, "Small corner") +
    sim(grid, (bottom, 0), small_corners_steps, "Small corner") + sim(grid, (bottom, bottom), small_corners_steps, "Small corner"))
  tips = sim(grid, (0, start[1]), w, "Tips") + sim(grid, (start[0], 0), w, "Tips") + sim(grid, (bottom, start[1]), w, "Tips") + sim(grid, (start[0], bottom), w, "Tips")
  return tips + small_corners * N + big_corners * (N-1) + N * N * even + (N-1) * (N-1) * odd

# 305983606156910 -> too low
# 599108270050506 -> wrong
def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day21.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
#print("Ex pt2", main2(ex))

main_filename = "day21.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
