
import os
import sys
import re
import functools
def main(lines):
  s = 0
  def gen(line, pos):
    if pos >= len(line):
      yield ""
    elif line[pos] == "?":
      for suffix in gen(line, pos+1):
        yield "." + suffix
        yield "#" + suffix
    else:
      for suffix in gen(line, pos+1):
        yield line[pos] + suffix
    return
  def valid(line, spec):
    ingroup = False
    group_cnt = 0
    spec_pointer = 0
    for c in line + ".":
      if c == "#":
        if ingroup:
          group_cnt += 1
        else:
          ingroup = True
          group_cnt = 1
      else:
        if ingroup:
          if spec_pointer >= len(spec):
            return False
          if group_cnt != spec[spec_pointer]:
            return False
          group_cnt = 0
          spec_pointer += 1
          ingroup = False
        else:
          pass
    if spec_pointer != len(spec):
      return False
    return True

  for line in lines:
    chars, spec = line.split(" ")
    spec = list(map(int, spec.split(",")))
    for pos in gen(chars, 0):
      if valid(pos, spec):
        s+= 1
  return s

def find(pattern, string):

  @functools.cache
  def scan(pattern_pos, string_pos):
    initial_pattern_pos = pattern_pos
    initial_string_pos = string_pos
    if pattern_pos == len(pattern) and string_pos == len(string):
      return 1
    if pattern_pos == len(pattern):
      return 0
    # Open bracket
    pattern_pos += 1
    valid_c = set()
    # valid chars
    while (p := pattern[pattern_pos]) != "]":
      valid_c.add(p)
      pattern_pos += 1
    # Close bracket
    pattern_pos += 1
    p = pattern[pattern_pos]
    # start of specifier
    pattern_pos += 1
    tot = 0
    if p == "*":
      # Allow this pattern to match no characters or infinite characters
      tot += scan(pattern_pos, string_pos)
      for c_i in range(string_pos, len(string)):
        if string[c_i] in valid_c:
          tot += scan(pattern_pos, c_i+1)
        else:
          break
    elif p == "+":
      # This pattern must match at least one character
      for c_i in range(string_pos, len(string)):
        if string[c_i] in valid_c:
          tot += scan(pattern_pos, c_i+1)
        else:
          break
    else:
      # This pattern must match exactly the number specified
      num_str = ""
      while (p := pattern[pattern_pos]) != "}":
        num_str += p
        pattern_pos += 1
      num = int(num_str)
      pattern_pos += 1
      taken = 0
      for c_i in range(string_pos, min(len(string), string_pos + num)):
        if string[c_i] in valid_c:
          taken += 1
        else:
          break
      if taken == num:
        tot += scan(pattern_pos, string_pos + num)
    return tot

  return scan(0, 0)

DOT = "[?.]"
def main2(lines):
  s = 0
  for line in lines:
    chars, spec = line.split(" ")
    chars = "?".join([chars] * 5)
    spec = list(map(int, spec.split(",")))
    spec = spec * 5
    regex = [f"[#?]{{{cnt}}}" for cnt in spec]
    full = f"{DOT}*" + f"{DOT}+".join(regex) + f"{DOT}*"
    s += find(full, chars)
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day12.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(1)
main_filename = "day12.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
