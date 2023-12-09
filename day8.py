
import os
import functools
import math

def infiniter(iter, start=0):
  yield from iter[start:]
  while True:
    yield from iter

def main(lines):
  lrs = lines[0]
  print(f"'{lrs}'")

  m = {}
  for l in lines[2:]:

    key, val = l.split("=")
    key = key.strip()
    val = val.strip()
    l, r = val.split(",")
    l = l.strip().strip("(")
    r = r.strip().strip(")")
    m[key] = (l, r)
  @functools.cache
  def sim(i, start):
    curr = start
    steps = 0
    for lr in infiniter(lrs, i):
      curr = m[curr][0 if lr == "L" else 1]
      steps += 1
      if curr.endswith("Z"):
        break
    return curr, steps
  frontier = [(k, 0) for k in m.keys() if k.endswith("A")]
  print(frontier)
  furthest_z = -1
  while True:
    new_frontier = []
    advanced = math.inf
    DEBUG = []
    new_furthest_z = furthest_z
    for curr, curr_steps in frontier:
      if furthest_z == -1 or curr_steps < furthest_z:
        nextz, additional_steps = sim(curr_steps % len(lrs), curr)
        possible_steps = (furthest_z - curr_steps) // additional_steps
        if furthest_z != -1 and nextz == curr and possible_steps != 0:
          additional_steps *= possible_steps
        advanced = min(advanced, additional_steps)
        new_pos = additional_steps + curr_steps
        new_frontier.append((nextz, new_pos))
        new_furthest_z = max(new_pos, new_furthest_z)
        DEBUG.append(("NEW", curr, curr_steps, nextz, new_pos, additional_steps))
      else:
        new_frontier.append((curr, curr_steps))
        DEBUG.append(("OLD", curr, curr_steps, curr, curr_steps, 0))
    print(f"UPD {furthest_z=} {new_furthest_z=} {advanced=}\n ", "\n  ".join(str(e) for e in DEBUG))
    #print(frontier, new_frontier, furthest_z, advanced)
    frontier = new_frontier
    furthest_z = new_furthest_z
    if advanced == math.inf:
      break
    #if frontier[0][1] > 100000:
    #  break
  return frontier[0][1]

def main2(lines):
  s = 0
  for line in lines:
    pass
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day8.test"
ex = readlines(example_filename)
#print("Ex pt1", main(ex))
#print("Ex pt2", main2(ex))
#import sys; sys.exit(0)
main_filename = "day8.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
