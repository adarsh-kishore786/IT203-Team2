# Sample input
# (x1 ∨ x2) ʌ (¬x1 ∨ x2) ʌ (x3 ∨ ¬x2) ʌ (¬x2 ∨ ¬x3) - Satisfiable
# (x1 ∨ x2) ʌ (¬x3 ∨ x4) - Unsatifiable

# This is only a sample. Anything in this format can be given and
# the program will work

from copy import deepcopy
import re

class Node:
    def __init__(self, data, depth):
        self.left = None
        self.right = None
        self.data = data
        self.depth = depth

    def __str__(self):
        s = str(self.depth) + ": " + str(self.data)
        if self.left is not None:
            s += '\n' + str(self.left)
        if self.right is not None:
            s += '\n' + str(self.right)
        return s

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

def createTree(truthVal, n, max):
    if (n > max):
        return
    node = Node(truthVal, n)
    node.left = createTree(True, n+1, max)
    node.right = createTree(False, n+1, max)
    return node

def evaluate(expList):
    temp = deepcopy(expList)
    result = True
    for (i, el) in enumerate(temp):
        if isinstance(el[0], bool) and isinstance(el[1], bool) and el[0] == False and el[1] == False:
            return False
        elif (isinstance(el[0], bool) and el[0] == True) or (isinstance(el[1], bool) and el[1] == True):
            temp[i] = True
        if not (isinstance(temp[i], bool) and temp[i] == True):
            result = False
    if result:
        return True
    return temp

def expTree(tree, expList, diction):
    temp = deepcopy(expList)
    tempDict = deepcopy(diction)
    if tree is None:
        return (None, False)
    tempDict['x{}'.format(tree.depth)] = tree.data
    for el in temp:
        if tree.depth == abs(el[0]) and isinstance(el[0], int):
            el[0] = tree.data if el[0] > 0 else not tree.data
        if tree.depth == abs(el[1]) and isinstance(el[1], int):
            el[1] = tree.data if el[1] > 0 else not tree.data
    val = evaluate(temp)
    if isinstance(val, bool) and val == True:
        del tempDict['x0']
        print("Satisfiable with values {}".format(tempDict))
        exit()
    elif isinstance(val, bool) and val == False:
        return
    expTree(tree.left, temp, tempDict)
    expTree(tree.right, temp, tempDict)

def isSatisfiable(expNum):
    expList = expNum[0]
    n = expNum[1]
    tree = createTree(True, 0, n)
    expTree(tree, expList, {})
    print("Not satisfiable")

if __name__ == "__main__":
    exp = input("Enter expression: ")
    isSatisfiable(parseExpression(exp))
