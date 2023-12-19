
import os
import sys
import collections
STEPS = {
  "L": (-1, 0),
  "R": (1, 0),
  "U": (0, -1),
  "D": (0, 1)
}
def p(grid, minx, maxx, miny, maxy):
  for y in range(miny, maxy+1):
    r = ""
    for x in range(minx, maxx+1):
      r+=grid[(x,y)] if (x,y) in grid else "."
    print(r)

CORNERS = {
  ("U", "R"): "╔",
  ("U", "L"): "╗",
  ("D", "R"): "╚",
  ("D", "L"): "╝",
  ("L", "U"): "╚",
  ("L", "D"): "╔",
  ("R", "U"): "╝",
  ("R", "D"): "╗",
}

def main(lines):
  s = 0
  curr = (0,0)
  grid = {curr: None}
  prev_dir = lines[-1].split(" ")[0]
  for line in lines:
    direction, dist, color = line.split(" ")
    dist = int(dist)
    step = STEPS[direction]
    grid[curr] = CORNERS[(prev_dir, direction)]
    prev_dir = direction
    for _ in range(dist):
      nxt = (curr[0] + step[0], curr[1] + step[1])
      if nxt != (0,0):
        grid[nxt] = direction
      curr = nxt
  minx, maxx, miny, maxy = (0, 0, 0, 0)
  for x, y in grid:
    minx = min(minx, x)
    maxx = max(maxx, x)
    miny = min(miny, y)
    maxy = max(maxy, y)
  print((minx, miny), (maxx, maxy))
  p(grid, minx, maxx, miny, maxy)
  for y in range(miny, maxy+1):
    inside = False
    for x in range(minx, maxx+1):
      if (x,y) in grid and grid[(x,y)] in {"U", "D", "╔", "╗"}:
        inside = not inside
      elif inside and (x,y) not in grid:
        grid[(x,y)] = "F"
  print()
  p(grid, minx, maxx, miny, maxy)
  return len(grid)

# 93240: high

def n2dir(direction):
  return {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U"
  }[direction]
def main2(lines):
  s = 0
  curr = (0,0)
  prev_dir = lines[-1].split(" ")[0]
  transitions = collections.defaultdict(list)
  for i, line in enumerate(lines):
    _, _, color = line.split(" ")
    color = color.replace(")", "").replace("(", "")
    direction = n2dir(color[-1])
    dist = "0x" + color[1:-1]
    dist = int(dist, 16)
    step = STEPS[direction]
    corner = CORNERS[(prev_dir, direction)]
    next_corner = CORNERS[(direction, n2dir(lines[(i+1) % len(lines)][-2]))]
    prev_dir = direction
    step = (step[0] * dist, step[1]*dist)
    end = (curr[0] + step[0], curr[1] + step[1])
    print(line, direction, dist, step, curr, end)
    if direction in {"U", "D"}:
      ymin = min(end[1], curr[1])
      ymax = max(end[1], curr[1])
      for y in range(ymin, ymax+1):
        transitions[y].append((curr[0], direction))
      transitions[curr[1]][-1] = (curr[0], corner)
      transitions[end[1]][-1] = (end[0], next_corner)
    curr = end
  prev_transitions = None
  for y, transitions in transitions.items():
    inside = False
    border = False
    transitions.sort()
    start = None
    accum = []
    for x, direction in transitions:
      if direction in {"U", "D", "╔", "╗"}:
        inside = not inside
      if direction in {"╔", "╚"}:
        border = not border
      if direction in {"╝", "╗"}:
        border = not border
      if inside or border:
        if start is None:
          start = x
      elif start is not None:
        s += x - start +1
        accum.append(x-start + 1)
        start = None
    if transitions != prev_transitions:
      print(y, transitions)
      print(y, accum)
      prev_transitions = transitions

  print()
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day18.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(1)
main_filename = "day18.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
