data = open('day21.input').read().split('\n')

    
w, h = len(data[0]), len(data)
deltas = [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]
steps = 26501365
# go 65 steps within the start square before you leave it
bigsteps = steps - 65
# how many blocks of 131 you go after leaving the start square
grids = bigsteps // 131

space = {}
for j in range(h):
    for i in range(w):
        space[complex(i,j)] = data[j][i]
        if data[j][i] == 'S':
            start = complex(i,j)
            space[complex(i,j)] = '.'
center = start.real            

# function to compute flood fill distances     
   
def neighs(z, s, b):
    # go each cardinal direction and only keep new points
    nexts = [z+d for d in deltas if z + d in space and space[z + d] != '#' and z + d not in dists[b]]
    for y in nexts:
        # record the distance to this node
        dists[b][y] = s     
    return nexts

#directions from s = start grid are indexed as follows:    
#ul u ur
#l  s r
#dl l dr

#points we will enter each type of grid at first after analyzing the problem
beginnings = {'s': [start],'l': [complex(w - 1, center)], 'd': [complex(center,0)], 'r': [complex(0,center)], 'u': [complex(center, h - 1)], 'dl' : [complex(w - 1, 0)], 'ul' : [complex(w - 1, h - 1)], 'dr': [complex(0, 0)], 'ur': [complex(0, h - 1)] }

# store how many steps to each legal space from the start space for each grid type
dists = {key: {} for key in beginnings}

#do the floodfill for all the grid types
for b in beginnings:
    frontier = beginnings[b]
    for z in frontier:
        dists[b][z] = 0
    while  True:
        newfront = []
        for n in frontier:
            newfront += [z for z in neighs(n, dists[b][n] + 1, b) if z not in newfront]
        if len(newfront) == 0:
            break
        else:
            frontier = newfront.copy()

# S should be off at the end (parity check 1), because we have an odd number of total steps
# parity to use if we want the actual parity in that direction in the same parity as the original grid
parity_equal_s = {'s': 1, 'u': 0, 'r': 0, 'd': 0, 'l': 0, 'ur': 1, 'dr': 1, 'dl': 1, 'ul': 1}
    
# parity to use if we want the actual parity in that direction in the opposite parity as the original grid
parity_opp_s = {key: (parity_equal_s[key] + 1) % 2 for key in parity_equal_s}

# record how man points are "on" in equal and opposite parity in a full grid
parity_nums = {'equals' : len([z for z in dists['s'] if dists['s'][z] % 2 == parity_equal_s['s']]), 'opposite' : len([z for z in dists['s'] if dists['s'][z] % 2 == parity_opp_s['s']])}

# count all the points in the reached space at the correct number of steps
total = 0
# Count the correct number of opposite and equal parity full squares (relative to S square)

# equal parity to start for the correct number of entire grids.  
# Can calculate this by looking at the pattern of expanding grids every 131 steps, and finding a closed formula for summing N.2 odd numbers   
total += (1 + 4 * (((grids - 1) // 2) ** 2 + (grids - 1) // 2)) * parity_nums['equals']
# opposite parity to start for the correct number of entire grids.  
# Can calculate this by looking at the pattern of expanding grids every 131 steps, and finding a closed formula for summing N/2 even numbers  
total += 4 * (((grids) // 2) ** 2) * parity_nums['opposite']

# count top, right, bottom, and left points on partial grids at the very ends of the diamond "ball"
# num grids is even, so these match parity of original grid
parity = parity_equal_s['u']
for key in ['u','r','d','l']:
    #walk out 130 steps into these to finish the final 131 steps (1 step to get from previous square to this one)
    total += sum([1 for z in dists[key] if dists[key][z] <= 130 and dists[key][z] % 2 == parity])
    
#triangles and trapezoids along diagonal borders:

# even number of grids, so traps match parity of S and triangles are opposite parity from S
parity_trap = parity_equal_s['ur']
parity_tri = parity_opp_s['ur']

for key in ['ur','dr','dl','ul']:
    # on trapezoids you need to go out 130 + half the length to fill that shape.   You get (grids - 1) trapezoidal shapes
    total += (grids - 1) * sum([1 for z in dists[key] if dists[key][z] <= (130 + 65) and dists[key][z] % 2 == parity_trap])
    # on small triangles you need to go out 64 units to fill in that shape.  You get (grids) number of triangle shapes
    total += grids * sum([1 for z in dists[key] if dists[key][z] <= 64 and dists[key][z] % 2 == parity_tri])
print(total)