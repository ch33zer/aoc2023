with open("day4.input") as f:
	lines = f.read().splitlines()

s = 0

for line in lines:
	winning, have = line.split(":")[1].split("|")
	winning = set(map(int, filter(None, winning.strip().split(" "))))
	have = list(map(int, filter(None, have.strip().split(" "))))
	score = 0
	for h in have:
		if h in winning:
			score += score if score else 1
	s += score
print(s)

cards = [1] * len(lines)

for i, line in enumerate(lines):
	winning, have = line.split(":")[1].split("|")
	winning = set(map(int, filter(None, winning.strip().split(" "))))
	have = list(map(int, filter(None, have.strip().split(" "))))
	matching = 0
	for h in have:
		if h in winning:
			matching += 1
	for reward in range(matching):
		cards[i + reward + 1] += cards[i]
print(cards)
print(sum(cards))