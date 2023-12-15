
import os
import sys

def HASH(seq):
  s = 0
  for c in seq.strip():
    s += ord(c)
    s *= 17
    s %= 256
  return s

def main(lines):
  s = 0
  for line in lines:
    for step in line.split(","):
      #print(f"({step})")
      s+= HASH(step)
  return s

def main2(lines):
  s = 0
  for line in lines:
    boxes = [[] for _ in range(256)]
    for step in line.split(","):
      if step[-1] == "-":
        label = step[:-1]
        box = HASH(label)
        box_contents = boxes[box]
        i = 0
        while i < len(box_contents):
          box_lens_label, _ = box_contents[i]
          if box_lens_label == label:
            del box_contents[i]
          else:
            i += 1
      else:
        label, num_str = step.split("=")
        num = int(num_str)
        box = HASH(label)
        box_contents = boxes[box]
        added = False
        for i in range(len(box_contents)):
          box_lens_label, _ = box_contents[i]
          if box_lens_label == label:
            added = True
            box_contents[i] = (label, num)
        if not added:
          box_contents.append((label, num))
    for i, box in enumerate(boxes):
      box_num = i + 1
      for j, (lens, focal_len) in enumerate(box):
        lens_num = j + 1
        s += box_num * lens_num * focal_len
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day15.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))

main_filename = "day15.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
