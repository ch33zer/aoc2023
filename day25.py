
import os
import sys
import math
import collections
import random
import graphviz

class Node:
  def __init__(self, name, edges):
    self.name = name
    self.edges = edges
  def __repr__(self):
    return f"Node({self.name}, {self.edges})"
def kargers_one_iter(edges):
  node_mapping = {frm: Node(frm, {to: [(frm, to)] for to in tos}) for frm, tos in edges.items()}
  vertices_cnt = len(edges)
  while vertices_cnt > 2:
    frm = random.choice(list(node_mapping.keys()))
    frm_node = node_mapping[frm]
    frm_edges = frm_node.edges
    to = random.choice(list(frm_edges.keys()))
    to_node = node_mapping[to]
    to_edges = to_node.edges
    #print(vertices_cnt, "Merge", frm, to, frm_node, to_node)
    del frm_edges[to]
    del to_edges[frm]
    for k, v in to_edges.items():
      dependent_edges = node_mapping[k].edges
      dependent_edges[frm] = dependent_edges.get(frm, []) + dependent_edges[to]
      del dependent_edges[to]
      frm_edges[k] = frm_edges.get(k, []) + v
    del node_mapping[to]
    vertices_cnt -= 1
  return list(node_mapping[frm].edges.values())[0]

def kargers(edges):
  best, el = math.inf, None
  for _ in range(len(edges)):
    cut = kargers_one_iter(edges)
    if len(cut) < best:
      el = cut
      best = len(cut)
    if best == 3:
      continue
  return el

def reachable(edges, start):
  visited = set([start])
  frontier = [start]
  while frontier:
    new_frontier = []
    for node in frontier:
      visited.add(node)
      for edge in edges[node]:
        if edge not in visited:
          new_frontier.append(edge)
    frontier = new_frontier
  return len(visited)


# ('plt', 'mgb'), ('jxm', 'qns'), ('dbt', 'tjd')
def main(lines):
  s = 0
  edges = collections.defaultdict(set)
  for line in lines:
    src, dests = line.split(":")
    for d in dests.split():
      d = d.strip()
      edges[src].add(d)
      edges[d].add(src)

  # graph = graphviz.Graph()
  # for frm, tos in edges.items():
  #   graph.node(frm, frm)
  #   for to in tos:
  #     graph.edge(frm, to)
  # graph.view()
  cut = kargers(edges)
  assert len(cut) == 3
  for frm, to in cut:
    edges[frm].remove(to)
    edges[to].remove(frm)
  return reachable(edges, cut[0][0]) * reachable(edges, cut[0][1])


def main2(lines):
  s = 0
  for line in lines:
    pass
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day25.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))

main_filename = "day25.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
