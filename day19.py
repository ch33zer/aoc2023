
import os
import sys
import collections
import operator
class Part:
  def __init__(self):
    self.x = None
    self.m = None
    self.a = None
    self.s = None
  def val(self):
    return self.x + self.m + self.a + self.s
  def __repr__(self):
    return f"{{{self.x=} {self.m=} {self.a=} {self.s=}}}"

class PnRange:
  def __init__(self, x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000)):
    self.x = x
    self.m = m
    self.a = a
    self.s = s
  def split(self, field, val):
    lower_bound, upper_bound = getattr(self, field)
    if lower_bound == upper_bound or val <= lower_bound or val > upper_bound:
      return [self]
    lower = PnRange(self.x, self.m, self.a, self.s)
    upper = PnRange(self.x, self.m, self.a, self.s)
    setattr(lower, field, (lower_bound, val-1))
    setattr(upper, field, (val, upper_bound))
    return [lower, upper]
  def size(self):
    acc = 1
    for field in [self.x, self.m, self.a, self.s]:
      acc *= field[1] - field[0] + 1
    return acc
  def __repr__(self):
    return f"{{{self.x=} {self.m=} {self.a=} {self.s=}}}"

class Goto:
  def __init__(self, dest):
    self.dest = dest
  def eval(self, _):
    return self.dest
  def __repr__(self):
    return f"->{self.dest}"
  def eval_range(self, rng):
    return [(rng, self.dest)]

class Rule:
  def __init__(self, field, op_str, op, val, dest):
    self.field = field
    self.op_str = op_str
    self.op = op
    self.val = val
    self.dest = dest
  def eval(self, part):
    if self.op(getattr(part, self.field), self.val):
      return self.dest
    return None
  def eval_range(self, rng):
    new_rngs = rng.split(self.field, self.val+1 if self.op_str == ">" else (self.val))
    ret = []
    for rng in new_rngs:
      target = self.dest if self.op(getattr(rng, self.field)[0], self.val) else None
      ret.append((rng, target))
    return ret

  def __repr__(self):
    return f"{self.field}{self.op_str}{self.val}->{self.dest}"
def main(lines):
  rules = collections.defaultdict(list)
  parts = []
  phase = "R"
  for line in lines:
    if not line:
      phase = "P"
    elif phase == "R":
      name, steps = line.replace("}", "").split("{")
      for step in steps.split(","):
        if ":" in step:
          check, dest = step.split(":")
          if "<" in check:
            field, val = check.split("<")
            val = int(val)
            op = operator.lt
            op_str = "<"
          else:
            field, val = check.split(">")
            val = int(val)
            op = operator.gt
            op_str = ">"
          rules[name].append(Rule(field, op_str, op, val, dest))
        else:
          rules[name].append(Goto(step))
    else:
      line = line[1:-1]
      part = Part()
      for defn in line.split(","):
        field, val = defn.split("=")
        val = int(val)
        setattr(part, field, val)
      parts.append(part)
  s = 0
  for part in parts:
    print(part)
    ruleset = "in"
    while ruleset != "A" and ruleset != "R":
      print(f" {ruleset=} {rules[ruleset]}")
      for rule in rules[ruleset]:
        print(f"  {rule=}")
        res = rule.eval(part)
        print(f"   {res=}")
        if res:
          ruleset = res
          break
        else:
          continue
    if ruleset == "A":
      print("Accept", part)
      s += part.val()
  return s

def main2(lines):
  rules = collections.defaultdict(list)
  phase = "R"
  for line in lines:
    if not line:
      break
    name, steps = line.replace("}", "").split("{")
    for step in steps.split(","):
      if ":" in step:
        check, dest = step.split(":")
        if "<" in check:
          field, val = check.split("<")
          val = int(val)
          op = operator.lt
          op_str = "<"
        else:
          field, val = check.split(">")
          val = int(val)
          op = operator.gt
          op_str = ">"
        rules[name].append(Rule(field, op_str, op, val, dest))
      else:
        rules[name].append(Goto(step))
  s = 0
  frontier = [(PnRange(), "in", 0)]
  while frontier:
    print(frontier)
    new_frontier = []
    for rng, ruleset, rule_index in frontier:
      print(" ", rng, ruleset, rule_index, rules[ruleset][rule_index])
      new_explorations = rules[ruleset][rule_index].eval_range(rng)
      for new_rng, new_target in new_explorations:
        print("   ", new_rng, new_target)
        if new_target == "A":
          s += new_rng.size()
        elif new_target == "R":
          continue
        elif new_target:
          new_frontier.append((new_rng, new_target, 0))
        else:
          new_frontier.append((new_rng, ruleset, rule_index+1))
    frontier = new_frontier
  return s

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day19.test"
ex = readlines(example_filename)
print("Ex pt1", main(ex))
print("Ex pt2", main2(ex))
#sys.exit(0)
main_filename = "day19.input"
m = readlines(main_filename)
print("Main pt1", main(m))
print("Main pt2", main2(m))
