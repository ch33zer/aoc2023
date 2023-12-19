
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
  def asm(self):
    pass

def asmgen(lines):
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
  out = []
  # X: X0
  # M: X1
  # A: X2
  # S: X3
  # accepted_cnt: X4
  out.append("""
    .global _start
    .align 2
    main:

  """)
  for rule in rules:

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day19.test"
ex = readlines(example_filename)
print("Ex pt1", asmgen(ex))
#sys.exit(0)
main_filename = "day19.input"
m = readlines(main_filename)
print("Main pt1", asmgen(m))
