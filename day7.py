
import os
import collections

MAPPING = {
card: i for i, card in enumerate([
  "A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"])}
def jokerify(cnt):
  if "J" not in cnt:
    return cnt
  if cnt["J"] == 5:
    return cnt
  jcnt = cnt["J"]
  del cnt["J"]
  most_common = cnt.most_common(1)[0][0]
  cnt[most_common] += jcnt
  return cnt

def rank(hand):
  cnt = jokerify(collections.Counter(hand))
  vals = sorted(cnt.values(), reverse=True)
  if len(cnt) == 1:
    score = 1
  elif len(cnt) == 2 and vals[0] == 4:
    score = 2
  elif len(cnt) == 2 and vals[0] == 3:
    score = 3
  elif len(cnt) == 3 and vals[0] == 3:
    score = 4
  elif len(cnt) == 3 and vals[0] == 2 and vals[1] == 2:
    score = 5
  elif len(cnt) == 4:
    score = 6
  else:
    score = 7
  tiebreak = tuple(map(MAPPING.get, hand))
  return (score,) + tiebreak

def main(lines):
  ranks = []
  for line in lines:
    hand, bet = line.split()
    bet = int(bet)
    ranks.append((rank(hand), bet))
  ranks.sort(reverse=True)
  return sum((pos + 1) * bid for pos, (_, bid) in enumerate(ranks))

def main2(lines):
  s = 0
  for line in lines:
    pass
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day7.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))

main_filename = "day7.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
