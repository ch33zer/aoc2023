with open("day3.input") as f:
	lines = f.read().splitlines()
def check(row, start, end):
	def issym(c):
		return (not c.isdigit()) and (c != '.')
	if row > 0:
		for c in lines[row-1][max(0, start - 1):min(len(lines[0]), end+2)]:
			if issym(c):
				return True
	if row < len(lines)-1:
		for c in lines[row+1][max(0, start - 1):min(len(lines[0]), end+2)]:
			if issym(c):
				return True
	if start > 0 and issym(lines[row][start-1]):
		return True
	if end < len(lines[0])-1 and issym(lines[row][end+1]):
		return True
	return False

s = 0
for li, line in enumerate(lines):
	inchar = False
	start = None
	for i, c in enumerate(line + "."):
		if c.isdigit():
			if not inchar:
				start = i
			inchar = True
		elif inchar:
			inchar = False
			end = i - 1
			if check(li, start, end):
				chars = line[start:end+1]
				ints = int(chars)
				s += ints
print(s)
# wrong: 546373
# wrong: 540324
# right 543867


def check2(row, start, end):
	def issym(c):
		return (not c.isdigit()) and (c == '*')
	out = []
	if row > 0:
		s = max(0, start - 1)
		for i, c in enumerate(lines[row-1][s:min(len(lines[0]), end+2)]):
			if issym(c):
				out.append((row-1, i + s))
	if row < len(lines)-1:
		s = max(0, start - 1)
		for i, c in enumerate(lines[row+1][s:min(len(lines[0]), end+2)]):
			if issym(c):
				out.append((row+1, i+s))
	if start > 0 and issym(lines[row][start-1]):
		out.append((row, start-1))
	if end < len(lines[0])-1 and issym(lines[row][end+1]):
		out.append((row, end+1))
	return out

import collections
gears = collections.defaultdict(list)
for li, line in enumerate(lines):
	inchar = False
	start = None
	for i, c in enumerate(line + "."):
		if c.isdigit():
			if not inchar:
				start = i
			inchar = True
		elif inchar:
			inchar = False
			end = i - 1
			nearby_gears = check2(li, start, end)
			ints = int(line[start:end+1])
			for coords in nearby_gears:
				gears[coords].append(ints)

s = 0
for coords, adj in gears.items():
	if len(adj) == 2:
		s+= adj[0] * adj[1]

print(s)