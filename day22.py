
import os
import sys
import math
import collections

def intersects(occupied, prism):
  first, second, _ = prism
  for x in range(first[0], second[0] + 1):
    for y in range(first[1], second[1] + 1):
      for z in range(first[2], second[2] + 1):
        if (x,y,z) in occupied:
          return True
  return False
def track(prism, occupied):
  first, second, ident = prism
  for x in range(first[0], second[0] + 1):
    for y in range(first[1], second[1] + 1):
      for z in range(first[2], second[2] + 1):
        occupied[(x,y,z)] = ident
def p(occupied, prisms):
  print(occupied)
  print(prisms)
  minx, miny, minz, maxx, maxy, maxz = math.inf, math.inf, 1, -math.inf, -math.inf, -math.inf
  for (fx, fy, fz), (sx, sy, sz), ident in prisms:
    minx = min(fx, minx)
    miny = min(fy, miny)
    maxx = max(sx, maxx)
    maxy = max(sy, maxy)
    maxz = max(sz, maxz)
  print(minx, miny, minz, maxx, maxy, maxz)
  print(" " * ((maxx - minx) // 2), "x")
  print(" ".join(map(str, range(minx, maxx+1))))
  for z in range(maxz, minz-1, -1):
    row = ""
    for x in range(minx, maxx + 1):
      y_chr = "."
      for y in range(miny, maxy+1):
        if (x,y,z) in occupied:
          y_chr = occupied[(x,y,z)]
          break
      row += y_chr + " "
    row += f"{z}"
    print(row)

  print()
  print(" " * ((maxy - miny) // 2), "y")
  print(" ".join(map(str, range(miny, maxy+1))))
  for z in range(maxz, minz-1, -1):
    row = ""
    for y in range(miny, maxy + 1):
      x_chr = ". "
      for x in range(minx, maxx+1):
        if (x,y,z) in occupied:
          x_chr = str(occupied[(x,y,z)]) + " "
          break
      row += x_chr
    row += f"{z}"
    print(row)

def main(lines):
  s = 0
  prisms = []
  ident = 65
  for line in lines:
    first, second = line.split("~")
    first = tuple(map(int, first.split(",")))
    second = tuple(map(int, second.split(",")))
    prisms.append((first, second, chr(ident)))
    ident += 1
  prisms.sort(key=lambda el: el[0][2])
  while True:
    new_prisms = []
    occupied = {}
    for prism in prisms:
      (fx, fy, fz), (sx, sy, sz), ident = prism
      if sz == 1 or intersects(occupied, ((fx, fy, fz - 1), (sx, sy, fz-1), ident)):
        new_prisms.append(prism)
        track(prism, occupied)
      else:
        new_prism = (fx, fy, fz -1), (sx, sy, sz-1), ident
        new_prisms.append(new_prism)
    if new_prisms == prisms:
      prisms = new_prisms
      break
    prisms = new_prisms
  unsafe = set()
  for prism in prisms:
    below = set()
    (fx, fy, fz), (sx, sy, sz), ident = prism
    if fz == 1:
      continue
    for x in range(fx, sx + 1):
      for y in range(fy, sy + 1):
        if (x,y, fz - 1) in occupied:
          below.add(occupied[(x,y,fz-1)])
    if len(below) == 1:
      unsafe.add(list(below)[0])
  return len(prisms) - len(unsafe)

def main2(lines):
  s = 0
  prisms = []
  ident = 65
  for line in lines:
    first, second = line.split("~")
    first = tuple(map(int, first.split(",")))
    second = tuple(map(int, second.split(",")))
    prisms.append((first, second, ident))
    ident += 1
  prisms.sort(key=lambda el: el[0][2])
  while True:
    new_prisms = []
    occupied = {}
    for prism in prisms:
      (fx, fy, fz), (sx, sy, sz), ident = prism
      if sz == 1 or intersects(occupied, ((fx, fy, fz - 1), (sx, sy, fz-1), ident)):
        new_prisms.append(prism)
        track(prism, occupied)
      else:
        new_prism = (fx, fy, fz -1), (sx, sy, sz-1), ident
        new_prisms.append(new_prism)
    if new_prisms == prisms:
      prisms = new_prisms
      break
    prisms = new_prisms
  dependees = collections.defaultdict(list)
  depends_on = collections.defaultdict(list)
  for prism in prisms:
    below = set()
    (fx, fy, fz), (sx, sy, sz), ident = prism
    if fz == 1:
      continue
    for x in range(fx, sx + 1):
      for y in range(fy, sy + 1):
        if (x,y, fz - 1) in occupied:
          occupier = occupied[(x,y,fz-1)]
          dependees[occupier].append(ident)
          depends_on[ident].append(occupier)
  for i, prism in enumerate(prisms):
    _, _, ident = prism
    frontier = set([ident])
    fallen = set([ident])
    while frontier:
      new_frontier = set()
      for ident in frontier:
        for dependee in dependees[ident]:
          all_dependents_fell = True
          for dependee_depends_on in depends_on[dependee]:
            if dependee_depends_on not in fallen:
              all_dependents_fell = False
              break
          if all_dependents_fell:
            new_frontier.add(dependee)
            fallen.add(dependee)
      frontier = new_frontier
    s += len(fallen) - 1
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day22.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(0)
main_filename = "day22.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
