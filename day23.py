
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

invalid = {
  ">": (-1,0),
  "<": (1, 0),
  "^": (0, 1),
  "v": (0, -1)
}
def dfs(grid, start, end, shortcuts, visited):
  if start == end:
    return 0
  visited.add(start)
  x, y = start
  best = -math.inf
  for direction in ["L", "R", "U", "D"]:
    key = (start, direction)
    if key not in shortcuts:
      continue
    new, cost = shortcuts[key]
    if new in visited:
      continue
    best = max(dfs(grid, new, end, shortcuts, visited)+cost, best)
  visited.remove(start)
  return best

def find_all_directions(grid, start, end):
  visited = set()
  ret = {}
  # node, direction, cost
  frontier = [(start, None)]
  dist = 0
  while frontier:
    new_frontier = []
    for node, origin_direction in frontier:
      visited.add(node)
      x, y = node
      valid_directions = []
      for offx, offy, direction_str in [(-1, 0, "L"), (1, 0, "R"), (0, -1, "U"), (0, 1, "D")]:
        new = x + offx, y + offy
        newx, newy = new
        if in_bounds(grid, new):
          if new in visited:
            continue
          grid_val = grid[newy][newx]
          if grid_val == "#":
            continue
          valid_directions.append((new, direction_str))
      if dist > 0 and (len(valid_directions) > 1 or node == end):
        ret[(start, origin_direction)] = node, dist
      else:
        for valid_direction, new_direction in valid_directions:
          new_frontier.append((valid_direction, origin_direction if origin_direction else new_direction))
    frontier = new_frontier
    dist += 1
  return ret

def find_shortcuts(grid, start, end):
  total = {}
  visited = set()
  frontier = [start]
  while frontier:
    new_frontier = []
    for node in frontier:
      visited.add(node)
      all_dirs = find_all_directions(grid, node, end)
      for dest, _ in all_dirs.values():
        if dest not in visited:
          new_frontier.append(dest)
      total.update(all_dirs)
    frontier = new_frontier
  return total

def exit(grid, start, end, shortcuts, label=None):
  return dfs(grid, start, end, shortcuts, set())

def main(lines):
  s = 0
  grid = [list(line) for line in lines]
  start = (grid[0].index("."),0)
  end = (grid[-1].index("."), len(grid)-1)
  shortcuts = find_shortcuts(grid, start, end)
  return exit(grid, start, end, shortcuts)

def main2(lines):
  s = 0
  for line in lines:
    pass
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

sys.setrecursionlimit(sys.getrecursionlimit()*10)
example_filename = "day23.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
#print("Ex pt2", main2(ex))
#sys.exit(0)
main_filename = "day23.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
