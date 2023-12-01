with open("day1.input") as f:
  lines = f.readlines()

s = 0
for line in lines:
  digi = list(filter(lambda c: c.isdigit(), line))
  s += int(digi[0] + digi[-1])
print(s)

with open("day1pt2.input") as f:
  lines = f.readlines()

s = 0
mappings = {
  "one": 1,
  "two": 2,
  "three": 3,
  "four": 4,
  "five": 5,
  "six": 6,
  "seven": 7,
  "eight": 8,
  "nine": 9
}
import math
for line in lines:
  print(line)
  first = (math.inf, 0)
  last = (-math.inf, 0)
  def find(search, val):
    global first
    global last
    found = line.find(search)
    if found != -1 and found < first[0]:
      first = (found, val)
    found = line.rfind(search)
    if found != -1 and found > last[0]:
      last = (found, val)
  for frm, to in mappings.items():
    find(frm, to)
    find(str(to), to)
  print(first, last)
  s += first[1] * 10 + last[1]
print(s)
