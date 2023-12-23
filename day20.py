
import os
import sys
import collections
import graphviz

HIGH = "HIGH"
LOW = "LOW"
DOTSEP = ";\n"
def distribute(dests, pulse, src):
  return [(dest, pulse, src) for dest in dests]

def gen_dot(module, shape, fillcolor, signals):
  s = f"""
    {module.name} [shape={shape}{f', style=filled, fillcolor={fillcolor}' if fillcolor else ''}];
    """
  for dest in module.dests:
    had_signal = False
    for signal_dest, signal_type, signal_src in signals:
      if signal_dest == dest and signal_src is module:
        had_signal = True
        break
    if had_signal:
      s += f"    {module.name} -> {dest} [label={signal_type}];\n"
    else:
      s += f"    {module.name} -> {dest};\n"
  return s

class Broadcast:
  def __init__(self, name, dests):
    self.name = name
    self.dests = dests
  def handle(self, _, signal):
    return distribute(self.dests, signal, self)
  def add_input(self, _):
    pass
  def __repr__(self):
    return f"Broadcast({self.name}, {self.dests})"
  def dot(self, signals):
    return gen_dot(self, 'triangle', None, signals)

class FlipFlop:
  def __init__(self, name, dests):
    self.name = name
    self.dests = dests
    self.on = False
  def handle(self, _, signal):
    if signal == LOW:
      self.on = not self.on
      return distribute(self.dests, HIGH if self.on else LOW, self)
    return []
  def add_input(self, _):
    pass
  def __repr__(self):
    return f"FlipFlop({self.name}, {self.dests}, {self.on})"
  def dot(self, signals):
    return gen_dot(self, 'ellipse', 'blue' if self.on else 'red', signals)


class Conj:
  def __init__(self, name, dests):
    self.name = name
    self.dests = dests
    self.inputs = {}
  def on(self):
    return all(map(lambda el: el == HIGH, self.inputs.values()))
  def handle(self, src, signal):
    self.inputs[src.name] = signal
    return distribute(self.dests, LOW if self.on() else HIGH, self)
  def add_input(self, src):
    self.inputs[src] = LOW
  def __repr__(self):
    return f"Conj({self.name}, {self.dests}, {','.join(':'.join(tup) for tup in self.inputs.items())})"
  def dot(self, signals):
    return gen_dot(self, 'box', 'blue' if self.on() else 'red', signals)

def main(lines):
  s = 0
  modules = {}
  incoming = collections.defaultdict(list)
  for line in lines:
    name, dests = line.split("->")
    name = name.strip()
    typ = name[0] if name[0] in {"%", "&"} else "B"
    name = name[1:] if typ in {"%", "&"} else name
    dests = dests.strip()
    dests = dests.split(",")
    dests = list(map(lambda s: s.strip(), dests))
    for dest in dests:
      incoming[dest].append(name)
    if typ == "B":
      mod = Broadcast(name, dests)
    elif typ == "%":
      mod = FlipFlop(name, dests)
    elif typ == "&":
      mod = Conj(name, dests)
    modules[name] = mod
  for dest, incoming_items in incoming.items():
    for incoming_item in incoming_items:
      if dest in modules:
        modules[dest].add_input(incoming_item)
  high, low = 0, 0
  for i in range(1000):
    #print("i", i, low, high)
    frontier = [("broadcaster", LOW, None)]
    low += 1 # button
    while frontier:
      #print(" ", frontier)
      new_frontier = []
      for dest, sig, src in frontier:
        new_signals = modules[dest].handle(src, sig) if dest in modules else []
        #print("  ", new_signals)
        for _, new_sig, _ in new_signals:
          if new_sig == HIGH:
            high += 1
          else:
            low += 1
        new_frontier.extend(new_signals)
      frontier = new_frontier
  #print(low, high)
  return high * low

def dot(modules, signals):
  s = "digraph g {\n      node [shape=star];\n"
  for _, mod in modules.items():
    s += mod.dot(signals)
  s += "\n}"
  return s
def show_dot(modules, signals):
  text = dot(modules, signals)
  src = graphviz.Source(text)
  src.view()
  input("Press any key to continue")

def main2(lines):
  s = 0
  modules = {}
  incoming = collections.defaultdict(list)
  for line in lines:
    name, dests = line.split("->")
    name = name.strip()
    typ = name[0] if name[0] in {"%", "&"} else "B"
    name = name[1:] if typ in {"%", "&"} else name
    dests = dests.strip()
    dests = dests.split(",")
    dests = list(map(lambda s: s.strip(), dests))
    for dest in dests:
      incoming[dest].append(name)
    if typ == "B":
      mod = Broadcast(name, dests)
    elif typ == "%":
      mod = FlipFlop(name, dests)
    elif typ == "&":
      mod = Conj(name, dests)
    modules[name] = mod
  for dest, incoming_items in incoming.items():
    for incoming_item in incoming_items:
      if dest in modules:
        modules[dest].add_input(incoming_item)
  i = 1
  while True:
    #print(i)
    frontier = [("broadcaster", LOW, None)]
    while frontier:
      #print(" ", frontier)
      new_frontier = []
      for dest, sig, src in frontier:
        #print("  ", f"'{dest}'", sig, src)
        if src and src.name in {"zp", "sj", "rg", "pp"} and sig == LOW:
          print(src, i)
        new_signals = modules[dest].handle(src, sig) if dest in modules else []
        #print("   ", new_signals)
        new_frontier.extend(new_signals)
      frontier = new_frontier
    if i%100000 == 0:
      show_dot(modules, [])
    if not modules['xl'].on() or not modules['xp'].on() or not modules['gp'].on() or not modules['ln'].on():
      print(f"xl: {modules['xl'].on()} xp: {modules['xp'].on()} gp: {modules['gp'].on()} ln: {modules['ln'].on()}")
    i += 1
 # 251051863665515 -> too low
 # 251051863665516 -> too low
def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day20.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
#print("Ex pt2", main2(ex))
#sys.exit(1)
main_filename = "day20.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
