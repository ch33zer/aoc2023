
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
def kargers(edges):
  node_mapping = {frm: Node(frm, {to: 1 for to in tos}) for frm, tos in edges.items()}
  vertices_cnt = len(edges)
  while vertices_cnt > 2:
    print(node_mapping)
    frm = random.choice(list(node_mapping.keys()))
    frm_node = node_mapping[frm]
    frm_edges = frm_node.edges
    to = random.choice(list(frm_edges.keys()))
    to_node = node_mapping[to]
    print(vertices_cnt, "Merge", frm, to)
    del frm_edges[to]
    to_edges = to_node.edges
    del to_edges[frm_node.name]
    for k, v in to_edges.items():
      frm_edges[k] = frm_edges.get(k, 0) + v
    node_mapping[to_node.name] = frm_node
    vertices_cnt -= 1
  return node_mapping[frm].edges.items()[0][1]

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
  return kargers(edges)

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
