
import os
import sys
import collections
import math
DEBUG = True
def get_next(grid, start, prev_dir, cnt):
  nxt = []
  for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    # Disallow reversing
    if prev_dir and direction == (-prev_dir[0], -prev_dir[1]):
      continue
    moved = (start[0] + direction[0], start[1] + direction[1])
    if 0 <= moved[0] < len(grid[0]) and 0 <= moved[1] < len(grid):
      nxt_cnt = cnt + 1 if direction == prev_dir else 1
      if nxt_cnt <= 3:
        nxt.append((moved, direction, nxt_cnt))
  return nxt

def min_path(grid, start, nxt_func, min_travel_dist, max_travel_dist):
  # point, dir, cnt, cost
  frontier = [(start, None, 0, 0)]
  visited = collections.defaultdict(lambda: math.inf)
  while frontier:
    #print(frontier)
    #input()
    new_frontier = []
    for point, direction, cnt, cost in frontier:
      for nxt_point, nxt_direction, nxt_cnt in nxt_func(grid, point, direction, cnt):
        grid_cost = grid[nxt_point[1]][nxt_point[0]]
        nxt_cost = grid_cost + cost
        if nxt_cost >= visited[(nxt_point, nxt_direction, nxt_cnt)]:
          continue
        visited[(nxt_point, nxt_direction, nxt_cnt)] = nxt_cost
        new_frontier.append((nxt_point, nxt_direction, nxt_cnt, nxt_cost))
    frontier = new_frontier
  if DEBUG:
    for row in range(len(grid)):
      r = ""
      for col in range(len(grid[0])):
        r += f" {grid[row][col]:3}"
      print(r)
    print()
    for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      for cnt in range(1, max_travel_dist + 1):
        print(f"{direction=} {cnt=}")
        for row in range(len(grid)):
          r = ""
          for col in range(len(grid[0])):
            r += f" {visited[(col,row), direction, cnt]:3}"
          print(r)
        print()
  return min(val for (p, _, cnt), val in visited.items() if p == (len(grid[0])-1, len(grid)-1) and cnt >= min_travel_dist)
def main(lines):
  grid = []
  for line in lines:
    grid.append(list(map(int, line)))
  return min_path(grid, (0, 0), get_next, 0, 3)


def get_next2(grid, start, prev_dir, cnt):
  nxt = []
  for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    # Disallow reversing
    if prev_dir and direction == (-prev_dir[0], -prev_dir[1]):
      continue
    if prev_dir and cnt < 4 and direction != prev_dir:
      continue
    moved = (start[0] + direction[0], start[1] + direction[1])
    if 0 <= moved[0] < len(grid[0]) and 0 <= moved[1] < len(grid):
      nxt_cnt = cnt + 1 if direction == prev_dir else 1
      if nxt_cnt <= 10:
        nxt.append((moved, direction, nxt_cnt))
  return nxt

def main2(lines):
  grid = []
  for line in lines:
    grid.append(list(map(int, line)))
  return min_path(grid, (0, 0), get_next2, 4, 10)

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day17.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(1)
main_filename = "day17.input"
m = readlines(main_filename)
#print("Main pt1", main(m))
print("Main pt2", main2(m))