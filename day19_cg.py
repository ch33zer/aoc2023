
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

  bl save_now

  mov X23, #0 // Valid accumulator
  mov X24, #4001 // Max part number (exclusive)
  mov X25, #0 // Invalid accumulator
  mov X26, #0 // ID

  mov X22, #1 // S
s_loop:
  mov X21, #1 // A
a_loop:
  mov X20, #1 // M
m_loop:
  mov X19, #1 // X
x_loop:
  b in0
next:
  add X26, X26, #1

  add X19, X19, #1
  cmp x19, x24
  blt x_loop

  add x20, x20, #1
  cmp x20, x24
  blt m_loop

  add x21, x21, #1
  cmp x21, x24
  blt a_loop

  add x22, x22, #1
  bl print_progress
  cmp x22, x24
  blt s_loop

  b exit

A0:
  add X23, X23, #1
  b next

R0:
  add X25, X25, #1
  b next

print_progress:
  stp FP, LR, [SP,#-16]!
  mov FP, SP

  sub SP, SP, #80 // 16 bit aligned?

  bl save_now
  sub X2, X0, X1

  adrp X0, last_processed@PAGE
  add X0, X0, last_processed@PAGEOFF
  ldr X1, [X0]
  str X26, [X0]
  sub X3, X26, X1
  udiv X4, X3, X2

  adrp X0, format@PAGE
  add X0, X0, format@PAGEOFF
  mov X1, SP
  str X19, [X1]
  str X20, [X1, #8]
  str X21, [X1, #16]
  str X22, [X1, #24]
  str X23, [X1, #32]
  str X25, [X1, #40]
  str X2,  [X1, #48]
  str X3,  [X1, #56]
  str X4,  [X1, #64]
  bl  _printf

  mov SP, FP
  ldp FP, LR, [SP], #16
  ret

save_now:
  stp FP, LR, [SP,#-16]!
  mov FP, SP

  mov X0, #0
  bl _time
  adrp X1, last_print_time@PAGE
  add X1, X1, last_print_time@PAGEOFF
  ldr X2, [X1]
  str X0, [X1]

  mov X1, X2

  mov SP, FP
  ldp FP, LR, [SP], #16
  ret

exit:
  mov X0, X23      // Use cnt as status code
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
  format: .asciz "\n\n\n\n\n\033[5Ax: %lld m: %lld a: %lld s: %lld\nvalid: %lld invalid: %lld\ntime %lld seconds elapsed\n%lld processed since last\n%lld combinations/sec\n\033[5A"
  last_print_time: .quad 0
  last_processed: .quad 0
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

