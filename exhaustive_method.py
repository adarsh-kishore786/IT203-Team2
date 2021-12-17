# Sample input
# (x1 ∨ x2) ʌ (¬x1 ∨ x2) ʌ (x3 ∨ ¬x2) ʌ (¬x2 ∨ ¬x3) - Satisfiable
# (x1 ∨ x2) ʌ (¬x3 ∨ x4) - Unsatifiable

# This is only a sample. Anything in this format can be given and
# the program will work

import re

def evaluate(exp, val):
    res = True
    for pair in exp:
        x1 = val[pair[0]]
        x2 = val[pair[1]]
        res &= (x1 | x2)
        if res == False:
            return False
    return res

def solve(exp, n):
    i = 0
    res = False
    while (not res) and (i < 2**n):
        val = [0 for i in range(2 * n + 1)]
        # val = [0, 1, 2, 3, -3, -2, -1]
        for j in range(n-1, -1, -1):
            if (i & (1 << j) > 0):
                val[j+1] = True
                val[-j-1] = False
            else:
                val[j+1] = False
                val[-j-1] = True

        res = evaluate(exp, val)
        i += 1

    return (res, i-1)

def parseExpression(exp):
    notSymb = '¬!~'
    andSymb= "ʌ|\*|&|\^"
    orSymb = "∨|\+|v"
    expression = []
    n = 0
    exp = re.split(andSymb, exp)
    for pair in exp:
        pair = pair.strip()
        var = re.split(orSymb, pair)
        clause = []
        for atom in var:
            atom = atom.strip().lstrip('(').rstrip(')')
            num = int(atom[-1])
            if (num > n): n = num
            if (atom[0] in notSymb):
                num = -num
            clause.append(num)
        expression.append(clause)
    return (expression, n)

def prn(res, soln, n):
  if not res:
    print('Not Satisfiable')
  else:
    print('Satisfiable with')
    for i in range(n):
      print('x'+str(i+1), '=', (soln & (1 << i) > 0))
  pass


def main():
    exp = input("Enter expression in CNF form: ")
    expression, n = parseExpression(exp)
    res, soln = solve(expression, n)
    prn(res, soln, n)


if __name__ == "__main__":
    main()
