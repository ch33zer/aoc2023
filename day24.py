
import os
import sys
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

REGION_MIN = 200000000000000
REGION_MAX = 400000000000000
def main(lines):
  s = 0
  particles = []
  for line in lines:
    pos, vel = line.split("@")
    x, y, z = map(int, pos.split(","))
    xvel, yvel, zvel = map(int, vel.split(","))
    particles.append(((x,y,z), (xvel,yvel,zvel)))
  for i, first in enumerate(particles):
    ((x,y,z), (xv,yv,zv)) = first
    for j in range(i+1, len(particles)):
      second = particles[j]
      (x2,y2,z2), (xv2,yv2,zv2) = second
      if ((xv2/xv)-(yv2/yv)) == 0:
        print(i,j, "Div by 0")
        continue
      t2 = (((y2-y)/(yv))-((x2-x)/(xv)))/((xv2/xv)-(yv2/yv))
      t1 = (yv2*t2 +y2 - y) / yv
      x_col = xv*t1+x
      y_col = yv*t1+y
      print(i,j,x_col, y_col, t1, t2)
      if t1 > 0 and t2 > 0 and REGION_MIN <= x_col <= REGION_MAX and REGION_MIN <= y_col <= REGION_MAX:
        print(" match")
        s += 1
  return s

def sim(first, second, third, stone):
  fx,fv = first
  sx,sv = second
  tx,tv = third
  sx,sv = stone

def draw(particles):
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')
  def scale(l):
    return [100 * ((el - REGION_MIN) / (REGION_MAX - REGION_MIN)) for el in l]
  def get_avg(l):
    return sum(l) / len(l)
  def update(frame):
    nonlocal particles
    SPEED=1000000000
    new_particles = []
    for pos, speed in particles:
      new_particles.append(((pos[0] + SPEED * speed[0], pos[1] +  SPEED * speed[1], pos[2] + SPEED*speed[2]), speed))
    particles = new_particles
    xs,ys,zs = (
      scale([pos[0] for pos, _ in particles]),
      scale([pos[1] for pos, _ in particles]),
      scale([pos[2] for pos, _ in particles]))
    scat._offsets3d =(xs,ys,zs)
    avg = [get_avg(xs)], [get_avg(ys)], [get_avg(zs)]
    avg_point._offsets3d = avg
    title.set_text(f"Frame {frame+1}")
  xs,ys,zs = (
    scale([pos[0] for pos, _ in particles]),
    scale([pos[1] for pos, _ in particles]),
    scale([pos[2] for pos, _ in particles]))
  avg = get_avg(xs), get_avg(ys), get_avg(zs)
  scat = ax.scatter(xs,ys,zs, marker=".")
  avg_point = ax.scatter(*avg, marker="1")
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  title = ax.set_title("Frame 0")

  anim = animation.FuncAnimation(fig, update, cache_frame_data=False, blit=False)

  plt.show()

def main2(lines):
  s = 0
  particles = []
  for line in lines:
    pos, vel = line.split("@")
    x, y, z = map(int, pos.split(","))
    xvel, yvel, zvel = map(int, vel.split(","))
    particles.append(((x,y,z), (xvel,yvel,zvel)))
  draw(particles)
  mid = ((REGION_MAX-REGION_MIN)//2) + REGION_MIN
  stone = ((mid,mid,mid), (1,1,1))
  (xs,ys,zs),(vxs,vys,vzs) = stone
  for first in particles[:3]:
    for second in particles[:3]:
      for third in particles[:3]:
        if first == second or second == third or first == third:
          continue
        (x1,y1,z1), (vx1,vy1,vz1) = first
        (x2,y2,z2), (vx2,vy2,vz2) = second
        (x3,y3,z3), (vx3,vy3,vz3) = third
        sim((x1,vx1), (x2,vx2), (x3,vx3), (xs,vxs))


def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day24.test"
ex = readlines(example_filename)
#print("Ex pt1", main(ex))
#print("Ex pt2", main2(ex))
#sys.exit(1)
main_filename = "day24.input"
m = readlines(main_filename)
#print("Main pt1", main(m))
print("Main pt2", main2(m))
