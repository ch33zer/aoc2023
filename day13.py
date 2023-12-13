
import os
import sys

def t(grid):
  new = [[] for _ in grid[0]]
  for row in grid:
    for i,c in enumerate(row):
      new[i].append(c)
  return new

def main(lines):
  s = 0
  grids = [[]]
  for line in lines:
    if line:
      grids[-1].append(line)
    else:
      grids.append([])
  for grid in grids:
    for split in range(len(grid) - 1):
      top = grid[:split+1]
      bottom = grid[split+1:]
      minwidth = min(len(top), len(bottom))
      top = top[-minwidth:]
      bottom = list(reversed(bottom[:minwidth]))
      if top == bottom:
        s += 100 * (split + 1)
  for grid in grids:
    grid = t(grid)
    for split in range(len(grid) - 1):
      top = grid[:split+1]
      bottom = grid[split+1:]
      minwidth = min(len(top), len(bottom))
      top = top[-minwidth:]
      bottom = list(reversed(bottom[:minwidth]))
      if top == bottom:
        s += (split + 1)


  return s

def compare(top, bottom):
  mismatches = []
  for i in range(len(top)):
    for j in range(len(top[i])):
      if top[i] == bottom[i]:
        continue
      else:
        mismatches.append((i,j))
  return mismatches

def rows_match(grid, ignore):
  for split in range(len(grid) - 1):
    top = grid[:split+1]
    bottom = grid[split+1:]
    minwidth = min(len(top), len(bottom))
    top = top[-minwidth:]
    bottom = list(reversed(bottom[:minwidth]))
    if top == bottom and ignore != split + 1:
      return split + 1
  return -1

def find_reflection(grid, ignore):
  rows = rows_match(grid, ignore[0] if ignore[1] == 0 else None)
  if rows != -1:
    return rows, 0
  return 0, rows_match(t(grid), ignore[1] if ignore[0] == 0 else None)

def main2(lines):
  s = 0
  grids = [[]]
  for line in lines:
    if line:
      grids[-1].append(list(line))
    else:
      grids.append([])
  for i, grid in enumerate(grids):
    #print("\n".join("".join(row) for row in grid))
    r = find_reflection(grid, (-1, -1))
    #print(r)
    used = set()
    for y in range(len(grid)):
      for x in range(len(grid[0])):
        grid[y][x] = "#" if grid[y][x] == "." else "."
        soln = find_reflection(grid, r)
        #print(y, x, soln)
        if soln[0] != -1 and soln[1] != -1 and soln != r and soln not in used:
          #print(y, x, soln, r)
          used.add(soln)
          s += 100*soln[0] if soln[1] == 0 else soln[1]
        grid[y][x] = "#" if grid[y][x] == "." else "."
    #if len(used) == 0:
      #print("no answer for grid:", grid)
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day13.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(1)
main_filename = "day13.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))

# 10700 low
# 11300 low