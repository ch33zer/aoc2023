
import os
import sys

def totup(grid):
  return tuple(tuple(row) for row in grid)
def rot(grid):
  new = [[None] * len(grid) for _ in grid[0]]
  for y in range(len(grid)):
    for x in range(len(grid[0])):
      new[x][len(grid[0]) - y - 1] = grid[y][x]
  return totup(new)

def tilt(grid):
  new = [[None] * len(row) for row in grid]
  for col in range(len(grid[0])):
    target = 0
    for row in range(len(grid)):
      char = grid[row][col]
      if char == ".":
        new[row][col] = char
      elif char == "#":
        new[row][col] = char
        target = row + 1
      else:
        new[target][col] = "O"
        if target != row:
          new[row][col] = "."
        target += 1
  return totup(new)

def score(grid):
  s = 0
  for rownum, row in enumerate(grid):
    score = len(grid) - rownum
    s += score * row.count("O")
  return s


def p(title, grid):
  print(title)
  print("\n".join("".join(row) for row in grid))

def main(lines):
  s = 0
  grids = [[]]
  for line in lines:
    if line:
      grids[-1].append(list(line))
    else:
      grids.append([])
  for grid in grids:
    s += score(tilt(grid))
  return s

def do_cycle(grid):
  return rot(tilt(rot(tilt(rot(tilt(rot(tilt(grid))))))))

CYCLES = 1000000000

def main2(lines):
  s = 0
  grids = [[]]
  for line in lines:
    if line:
      grids[-1].append(tuple(line))
    else:
      grids.append([])
  for i in range(len(grids)):
    grids[i] = totup(grids[i])
  seen = {}
  for grid in grids:
    cycle = 0
    while cycle < CYCLES:
      #p("BEFORE", grid)
      was = hash(grid)
      grid = do_cycle(grid)
      print(cycle, "was", was, "now", hash(grid), "score", score(grid))
      #p("AFTER", grid)
      if grid in seen:
        first_seen = seen[grid]
        period = cycle - first_seen
        new_cycle = period * ((CYCLES - first_seen) // period) + first_seen
        print(f"Cycle with len({cycle}) found! Forwarding to {new_cycle}")
        cycle = new_cycle
        seen = {}
      seen[grid] = cycle
      cycle += 1
    s += score(grid)
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day14.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(0)
main_filename = "day14.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
