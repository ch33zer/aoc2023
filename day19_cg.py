
import os
import sys
import collections
import operator
REG_MAPPING={
  "x": "X0",
  "m": "X1",
  "a": "X2",
  "s": "X3" 
}

class Goto:
  def __init__(self, dest):
    self.dest = dest
  def __repr__(self):
    return f"->{self.dest}"
  def asm(self):
    return f"""
  b {self.dest}0
    """

class Rule:
  def __init__(self, field, op_str, op, val, dest):
    self.field = field
    self.op_str = op_str
    self.op = op
    self.val = val
    self.dest = dest

  def __repr__(self):
    return f"{self.field}{self.op_str}{self.val}->{self.dest}"
  def asm(self):
    return f"""
  cmp {REG_MAPPING[self.field]}, #{self.val}
  {"bgt" if self.op_str == ">" else "blt"} {self.dest}0
    """

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
.text
.global _start
.align 4
_start:
  mov X0, #0 // will get incremented below
  mov X1, #1
  mov X2, #1
  mov X3, #1
  mov X4, #0
next:
  mov X6, #4001
  // x
  add X0, X0, #1
  udiv X5, X0, X6
  msub X0, X5, X6, X0
  cmp X0, #0
  bne in0
  add X0, X0, #1
  // m
  add X1, X1, #1
  udiv X5, X1, X6
  msub X1, X5, X6, X1
  cmp X1, #0
  bne in0
  add X1, X1, #1
  // a
  add X2, X2, #1
  udiv X5, X2, X6
  msub X2, X5, X6, X2
  cmp X2, #0
  bne in0
  add X2, X2, #1
  // s
  add X3, X3, #1
  udiv X5, X3, X6
  msub X3, X5, X6, X3
  cmp X3, #0
  bne in0
  add X3, X3, #1
  b exit
A0:
  add X4, X4, #1
  b next
R0:
  b next
exit:
  mov     X0, X4      // Use cnt as status code return code
  mov     X16, #1     // Service command code 1 terminates this program
  svc     0           // Call MacOS to terminate the program
  """)
  for rulename, rulelist in rules.items():
    for i, rule in enumerate(rulelist):
      out.append(f"""
{rulename}{i}:
{rule.asm()}
        """)
  return out

def readlines(filename):
  with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
  return lines

example_filename = "day19.test"
ex = readlines(example_filename)
print("Ex pt1", "\n".join(asmgen(ex)))
with open(example_filename + ".out", "w") as f:
  f.write("\n".join(asmgen(ex)))
#sys.exit(0)
main_filename = "day19.input"
m = readlines(main_filename)
print("Main pt1", "\n".join(asmgen(m)))
with open(main_filename + ".out", "w") as f:
  f.write("\n".join(asmgen(m)))

