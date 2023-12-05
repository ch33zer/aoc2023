import sys
import requests
import os

TEMPLATE = """
import os

def main(lines):
  s = 0
  for line in lines:
    pass
  return s

def main2(lines):
  s = 0
  for line in lines:
    pass
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line[:-1] for line in f.readlines()]
  return lines

example_filename = "day{DAY}.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))

main_filename = "day{DAY}.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
"""

YEAR = 2023
INPUT_URL = "https://adventofcode.com/{YEAR}/day/{DAY}/input"
def main(day, session):
  print(f"Running for day {day} year {YEAR}")
  populated = INPUT_URL.format(YEAR=YEAR, DAY=day)
  h ={"Cookie":f"session={session}"}
  try:
    r = requests.get(populated, headers=h)
    r.raise_for_status()
    with open(f"day{day}.input", "w") as f:
      f.write(r.text)
  except Exception:
    print("Failed to get input. Wrong/missing/expired session?", file=sys.stderr)
    with open(f"day{day}.input", "w") as f:
      pass
  with open(f"day{day}.test", "w") as f:
    pass
  with open(f"day{day}.py", "w") as f:
    f.write(TEMPLATE.format(DAY=day, YEAR=YEAR))

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Provide day!", file=sys.stderr)
    sys.exit(1)
  day = int(sys.argv[1])
  with open("session") as f:
    session = f.read().strip()
  main(day, session)