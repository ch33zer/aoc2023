
import os
import sys
import collections
Point = collections.namedtuple('Point', ['x', 'y'])

CONNECTS = {
  "UP": {"|", "L", "J"},
  "DOWN": {"|", "7", "F"},
  "LEFT": {"-", "7", "J"},
  "RIGHT": {"-", "F", "L"}
}
def main(lines):
  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      if c == "S":
        start = Point(x, y)
        break
  start = start # if this fails we don't have start, and something is wrong
  def connects(start, nxt):
    assert (abs(start.x - nxt.x) == 1) ^ (abs(start.y - nxt.y) == 1), f"Must be called on adjacent points {start=} {nxt=}"
    if nxt.x - start.x == 1 and nxt.x <= len(lines[0]) - 1:
      return lines[start.y][start.x] in CONNECTS["RIGHT"] | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["LEFT"]
    elif nxt.x - start.x == -1 and nxt.x >= 0:
      return lines[start.y][start.x] in CONNECTS["LEFT"]  | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["RIGHT"]
    elif nxt.y - start.y == 1 and nxt.y <= len(lines) - 1:
      return lines[start.y][start.x] in CONNECTS["DOWN"] | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["UP"]
    elif nxt.y - start.y == -1 and nxt.y >= 0:
      return lines[start.y][start.x] in CONNECTS["UP"] | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["DOWN"]
    return False
  frontier = [(start, None)]
  steps = 0
  while len(frontier) == 1 or frontier[0][0] != frontier[1][0]:
    #print(steps, "PRE FRONTIER:", frontier)
    new_frontier = []
    for (point, prev) in frontier:
      #print("F point", point, f"({lines[point.y][point.x]})", prev)
      for offx, offy, direction in [(-1, 0, "LEFT"), (1, 0, "RIGHT"), (0, -1, "UP"), (0, 1, "DOWN")]:
        nxt = Point(point.x + offx, point.y + offy)
        #print(" nxt:", nxt)
        if connects(point, nxt) and prev != nxt:
          #print("  add", nxt, direction, f"({lines[nxt.y][nxt.x]})")
          new_frontier.append((nxt, point))
    frontier = new_frontier
    #print("POST FRONTIER:", new_frontier)
    #print()
    steps += 1
  return steps

def up(point, grid):
  if point.y > 0:
    return Point(point.x, point.y-1)
  return None
def down(point, grid):
  if point.y < len(grid) - 1:
    return Point(point.x, point.y+1)
  return None
def left(point, grid):
  if point.x > 0:
    return Point(point.x-1, point.y)
  return None
def right(point, grid):
  if point.x < len(grid[0]) - 1:
    return Point(point.x+1, point.y)
  return None

def main2(lines):
  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      if c == "S":
        start = Point(x, y)
        break
  start = start # if this fails we don't have start, and something is wrong
  def connects(start, nxt):
    assert (abs(start.x - nxt.x) == 1) ^ (abs(start.y - nxt.y) == 1), f"Must be called on adjacent points {start=} {nxt=}"
    if nxt.x - start.x == 1 and nxt.x <= len(lines[0]) - 1:
      return lines[start.y][start.x] in CONNECTS["RIGHT"] | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["LEFT"] | {"S"}
    elif nxt.x - start.x == -1 and nxt.x >= 0:
      return lines[start.y][start.x] in CONNECTS["LEFT"]  | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["RIGHT"] | {"S"}
    elif nxt.y - start.y == 1 and nxt.y <= len(lines) - 1:
      return lines[start.y][start.x] in CONNECTS["DOWN"] | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["UP"] | {"S"}
    elif nxt.y - start.y == -1 and nxt.y >= 0:
      return lines[start.y][start.x] in CONNECTS["UP"] | {"S"} and lines[nxt.y][nxt.x] in CONNECTS["DOWN"] | {"S"}
    return False
  visited = set()
  lefts = set()
  rights = set()
  frontier = [(start, None)]
  steps = 0
  while steps == 0 or lines[frontier[0][0].y][frontier[0][0].x] != "S":
    #print(steps, "PRE FRONTIER:", frontier)
    new_frontier = []
    for (point, prev) in frontier:
      #print("F point", point, f"({lines[point.y][point.x]})", prev)
      for offx, offy, direction in [(-1, 0, "LEFT"), (1, 0, "RIGHT"), (0, -1, "UP"), (0, 1, "DOWN")]:
        nxt = Point(point.x + offx, point.y + offy)
        #print(" nxt:", nxt)
        if connects(point, nxt) and prev != nxt:
          #print("  add", nxt, direction, f"({lines[nxt.y][nxt.x]})")
          new_frontier.append((nxt, point))
          if direction == "LEFT":
            if down(nxt, lines):
              lefts.add(down(nxt, lines))
              lefts.add(down(point, lines))
            if up(nxt, lines):
              rights.add(up(nxt, lines))
              rights.add(up(point, lines))
          elif direction == "RIGHT":
            if down(nxt, lines):
              rights.add(down(nxt, lines))
              rights.add(down(point, lines))
            if up(nxt, lines):
              lefts.add(up(nxt, lines))
              lefts.add(up(point, lines))
          elif direction == "UP":
            if left(nxt, lines):
              lefts.add(left(nxt, lines))
              lefts.add(left(point, lines))
            if right(nxt, lines):
              rights.add(right(nxt, lines))
              rights.add(right(point, lines))
          elif direction == "DOWN":
            if left(nxt, lines):
              rights.add(left(nxt, lines))
              rights.add(left(point, lines))
            if right(nxt, lines):
              lefts.add(right(nxt, lines))
              lefts.add(right(point, lines))
          break
    frontier = new_frontier
    visited.update(el[0] for el in new_frontier)
    #print("POST FRONTIER:", new_frontier)
    #print()
    steps += 1
  def floodfill(mask, path):
    frontier = list(mask)
    visited = set(path)
    new_mask = set()
    while frontier:
      new_frontier = []
      for f in frontier:
        if f in visited:
          continue
        new_mask.add(f)
        visited.add(f)
        if up(f, lines):
          new_frontier.append(up(f, lines))
        if down(f, lines):
          new_frontier.append(down(f, lines))
        if left(f, lines):
          new_frontier.append(left(f, lines))
        if right(f, lines):
          new_frontier.append(right(f, lines))
      frontier = new_frontier
    return new_mask
  def mask(title, mask, orig = False):
    graph = [["." for _ in line] for line in lines]
    for seen in mask:
      graph[seen.y][seen.x] = lines[seen.y][seen.x] if orig else "#"
    print(title, len(mask))
    for row in graph:
      print("".join(row))
  def all():
    ret = set()
    for y, line in enumerate(lines):
      for x, _ in enumerate(line):
        ret.add(Point(x, y))
    return ret
  mask("VISITED", visited, True)
  all_left = floodfill(lefts - visited, visited)
  mask("LEFT", all_left)
  all_right = floodfill(rights - visited, visited)
  mask("RIGHT", all_right)
  print(f"{len(visited) + len(all_right) + len(all_left)} calculated vs {len(lines) * len(lines[0])}")
  mask("REMAINDER", all() - visited - all_left - all_right)
  return steps


def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day10.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(0)
main_filename = "day10.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))

# 294: too low
# 296: wrong
# 298: too high
# 302: too high