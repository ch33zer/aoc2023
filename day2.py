import collections
with open("day2.input") as f:
  lines = f.readlines()
maxes = {"red": 12, "green":13, "blue": 14}
s = 0
for line in lines:
  doable = True
  game, reveals = line.split(":")
  game_id = int(game.replace("Game ", ""))
  for reveal in reveals.split(";"):
    cnt = collections.Counter()
    for cube in reveal.split(","):
      num, color = cube.strip().split()
      num = int(num)
      cnt[color] += num
    if len(cnt) > len(maxes):
      doable = False
    for c, num in maxes.items():
      if cnt[c] > num:
        doable = False
  if doable:
    s+= game_id
print(s)

with open("day2.input") as f:
  lines = f.readlines()

s = 0
for line in lines:
  game, reveals = line.split(":")
  game_id = int(game.replace("Game ", ""))
  cnt = collections.Counter()
  for reveal in reveals.split(";"):
    for cube in reveal.split(","):
      num, color = cube.strip().split()
      num = int(num)
      if cnt[color] < num:
        cnt[color] = num
  power = 1
  for num in cnt.values():
    power *= num
  s+= power
print(s)
