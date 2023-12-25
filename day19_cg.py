
import os
import sys
import collections
import operator

REG_MAPPING={
  "x": "X19",
  "m": "X20",
  "a": "X21",
  "s": "X22" 
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
  # X: X19
  # M: X20
  # A: X21
  # S: X22
  # accepted_cnt: X23
  out.append("""
.text
.global _start
.align 4
_start:
  stp FP, LR, [SP,#-16]!
  mov FP, SP

  mov X19, #0 // will get incremented below
  mov X20, #1
  mov X21, #1
  mov X22, #1
  mov X23, #0
next:
  mov X24, #1001
x:
  add X19, X19, #1
  udiv X5, X19, X24
  msub X19, X5, X24, X19
  cmp X19, #0
  bne in0
  add X19, X19, #1
m:
  add X20, X20, #1
  udiv X5, X20, X24
  msub X20, X5, X24, X20
  cmp X20, #0
  bne in0
  add X20, X20, #1

a:
  add X21, X21, #1
  udiv X5, X21, X24
  msub X21, X5, X24, X21
  cmp X21, #0
  bne in0
  add X21, X21, #1

  bl print_progress

s:
  add X22, X22, #1
  udiv X5, X22, X24
  msub X22, X5, X24, X22
  cmp X22, #0
  bne in0
  add X22, X22, #1 // Doesn't matter
  b exit

A0:
  add X23, X23, #1
  b next

R0:
  b next

print_progress:
  stp FP, LR, [SP,#-16]!
  mov FP, SP

  sub SP, SP, #48 // 16 bit aligned?

  adrp X0, format@PAGE
  add X0, X0, format@PAGEOFF
  mov X1, FP
  str X19, [X1, #-48]
  str X20, [X1, #-40]
  str X21, [X1, #-32]
  str X22, [X1, #-24]
  str X23, [X1, #-16]
  bl  _printf

  mov SP, FP
  ldp FP, LR, [SP], #16
  ret

exit:
  mov X0, X23      // Use cnt as status code return code
  mov X16, #1     // Service command code 1 terminates this program
  svc 0           // Call MacOS to terminate the program
  // Never reached?
  mov SP, FP
  ldp FP, LR, [SP], #16
  ret
  """)
  for rulename, rulelist in rules.items():
    for i, rule in enumerate(rulelist):
      out.append(f"{rulename}{i}:{rule.asm()}")
  out.append(""".data
  format: .ascii "x: %lld m: %lld a: %lld s: %lld acc: %lld
\"
  last_printed_val: .double 0
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

