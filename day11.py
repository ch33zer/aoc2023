
import os
import sys

def draw(map):
  for row in map:
    print("".join(row))
def main(lines):
  s = 0
  initial = lines
  expanded_rows = []
  for row in initial:
    if row.count(".") == len(row):
      expanded_rows.append(row)
    expanded_rows.append(row)
  expanded_cols = [[] for _ in range(len(expanded_rows))]
  for col in range(len(expanded_rows[0])):
    if all(map(lambda el: el == ".", [row[col] for row in expanded_rows])):
      for row in range(len(expanded_rows)):
        expanded_cols[row].append(expanded_rows[row][col])
    for row in range(len(expanded_rows)):
      expanded_cols[row].append(expanded_rows[row][col])
  #draw(expanded_cols)
  galaxies = []
  for r, row in enumerate(expanded_cols):
    for c, char in enumerate(row):
      if char == "#":
        galaxies.append((r, c))
  for start, g1 in enumerate(galaxies):
    for g2 in galaxies[start+1:]:
      s+= abs(g2[1] - g1[1]) + abs(g2[0] - g1[0])




  return s

EXPANSION = 1000000
def main2(lines):
  s = 0
  initial = lines
  expanded_rows = set()
  for r, row in enumerate(initial):
    if row.count(".") == len(row):
      expanded_rows.add(r)
  expanded_cols = set()
  for col in range(len(initial[0])):
    if all(map(lambda el: el == ".", [row[col] for row in initial])):
      expanded_cols.add(col)
  #draw(expanded_cols)
  galaxies = []
  for r, row in enumerate(initial):
    for c, char in enumerate(row):
      if char == "#":
        galaxies.append((r, c))
  for start, g1 in enumerate(galaxies):
    for g2 in galaxies[start+1:]:
      startx = min(g1[1], g2[1])
      endx = max(g1[1], g2[1])
      starty = min(g1[0], g2[0])
      endy = max(g1[0], g2[0])
      for col in range(startx, endx):
        s += EXPANSION if col in expanded_cols else 1
      for row in range(starty, endy):
        s += EXPANSION if row in expanded_rows else 1
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day11.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))

main_filename = "day11.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
