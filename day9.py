
import os
import sys

def main(lines):
  s = 0
  for line in lines:
    line = list(map(int, line.split()))
    deltas = [line]
    while any(map(lambda el: el != 0, deltas[-1])):
      prev = None
      new_delta = []
      for el in deltas[-1]:
        if prev is not None:
          new_delta.append(el - prev)
        prev = el
      deltas.append(new_delta)
    last = 0
    for delta in reversed(deltas):
      delta.append(delta[-1] + last)
      last = delta[-1]
    s += deltas[0][-1]
  return s

def main2(lines):
  s = 0
  for line in lines:
    line = list(map(int, line.split()))
    deltas = [line]
    while any(map(lambda el: el != 0, deltas[-1])):
      prev = None
      new_delta = []
      for el in deltas[-1]:
        if prev is not None:
          new_delta.append(el - prev)
        prev = el
      deltas.append(new_delta)
    last = 0
    for delta in reversed(deltas):
      delta.append(delta[0] - last)
      last = delta[-1]
    s += deltas[0][-1]
    #print(deltas)
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day9.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
main_filename = "day9.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
