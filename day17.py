
import os
import sys
import collections
import math
def get_next(grid, start, prev_dir, cnt):
  nxt = []
  for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    moved = (start[0] + direction[0], start[1] + direction[1])
    if 0 <= moved[0] < len(grid[0]) and 0 <= moved[1] < len(grid):
      nxt_cnt = cnt + 1 if dir == prev_dir else 1
      if nxt_cnt <= 3:
        nxt.append((moved, direction, nxt_cnt))
  return nxt
def min_path(grid, start):
  # cost, point, dir, cnt
  frontier = [(0, start, None, 0)]
  curr = frontier[0]
  visited = collections.defaultdict(lambda: math.inf)
  while frontier:
    #print(frontier)
    #print(visited)
    #input()
    cost, point, direction, cnt = curr
      for nxt_point, nxt_direction, nxt_cnt in get_next(grid, point, direction, cnt):
        grid_cost = grid[nxt_point[1]][nxt_point[0]]
        nxt_cost = grid_cost + cost
        if nxt_cost >= visited[(nxt_point, nxt_direction, nxt_cnt)]:
          continue
        visited[(nxt_point, nxt_direction, nxt_cnt)] = nxt_cost
        new_frontier.append((nxt_point, nxt_direction, nxt_cnt, cost + grid[nxt_point[1]][nxt_point[0]]))
    frontier = new_frontier
  if True:
    for row in range(len(grid)):
      r = ""
      for col in range(len(grid[0])):
        best = math.inf
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
          for cnt in range(4):
            best = min(best, visited[((col, row), direction, cnt)])
        r += f" {best:3}"
      print(r)
  return min(val for (point, _, _), val in visited.items() if point == (len(grid[0]) - 1, len(grid) - 1))

def main(lines):
  grid = []
  for line in lines:
    grid.append(list(map(int, line)))
  return min_path(grid, (0, 0))


def main2(lines):
  s = 0
  for line in lines:
    pass
  return s

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
print("Main pt1", main(m))
print("Main pt2", main2(m))