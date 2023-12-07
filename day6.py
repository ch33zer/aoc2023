import math
import os

def main(lines):
  acc = 1
  times = list(map(int, lines[0].split(":")[1].split()))
  dists = (map(int, lines[1].split(":")[1].split()))
  for time, dist in zip(times, dists):
    tot = time
    rec = dist + 1
    lower = (-tot + math.sqrt(tot**2 - 4 * rec)) / -2
    upper = (-tot - math.sqrt(tot**2 - 4 * rec)) / -2
    r = math.floor(upper) - math.ceil(lower) + 1
    acc *= r
  return acc

def main2(lines):
  acc = 1
  times = [int(lines[0].split(":")[1].replace(" ", ""))]
  dists = [int(lines[1].split(":")[1].replace(" ", ""))]
  for time, dist in zip(times, dists):
    tot = time
    rec = dist + 1
    lower = (-tot + math.sqrt(tot**2 - 4 * rec)) / -2
    upper = (-tot - math.sqrt(tot**2 - 4 * rec)) / -2
    r = math.floor(upper) - math.ceil(lower) + 1
    acc *= r
  return acc

def readlines(filename):
  with open(filename) as f:
    lines = [line[:-1] for line in f.readlines()]
  return lines

example_filename = "day6.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))

main_filename = "day6.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
