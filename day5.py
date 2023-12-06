
import os
import sys
def main(lines):
  s = 0
  seeds = list(map(int, lines[0].split(" ")[1:]))
  new_seeds = []
  for line in lines[2:]:
    if "map" in line:
      continue
    elif not line:
      seeds = new_seeds + seeds
      new_seeds = []
      continue
    else:
      dest, src, length = map(int, line.split())
      remaining_seeds = []
      for seed in seeds:
        if seed >= src and seed < src + length:
          new_seeds.append(dest + seed - src)
        else:
          remaining_seeds.append(seed)
      seeds = remaining_seeds
  return min(seeds)

def main2(lines):
  ranges = []
  nums = list(map(int, lines[0].split(" ")[1:]))
  for start in range(0, len(nums), 2):
    ranges.append((nums[start], nums[start+1]))
  #print(ranges)
  new_ranges = []
  for line in lines[2:]:
    if "map" in line:
      #print("map")
      continue
    elif not line:
      #print(f"proc {new_ranges=} {ranges=}")
      ranges = new_ranges + ranges
      new_ranges = []
      continue
    else:
      dest, src, length = map(int, line.split())
      srcend = src + length
      #print(f"proc {dest=} {src=} {length=}")
      remaining_ranges = []
      for rstart, rlen in ranges:
        rend = rstart + rlen
        if rstart < srcend and rend > src:
          start = max(rstart, src)
          end = min(srcend, rend)
          width = end - start
          offset = dest - src
          new_ranges.append((start + offset, width))
          #print(f" mapping {(rstart, rend, rlen)} to {(start+offset, start+offset+width, width)}")
          if rend > srcend:
            remaining_ranges.append((srcend, rend - srcend))
          if rstart < src:
            remaining_ranges.append((rstart, src - rstart))
        else:
          remaining_ranges.append((rstart, rlen))
          #print(f" skipping {(rstart, rstart + rlen, rlen)}")
      ranges = remaining_ranges
  return min(ranges)[0]

def readlines(filename):
  with open(filename) as f:
    lines = [line[:-1] for line in f.readlines()]
  return lines

example_filename = "day5.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(0)
main_filename = "day5.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))

# high 1549152
