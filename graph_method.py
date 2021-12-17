# Sample input
# (x1 ∨ x2) ʌ (¬x1 ∨ x2) ʌ (x3 ∨ ¬x2) ʌ (¬x2 ∨ ¬x3) - Satisfiable
# (x1 ∨ x2) ʌ (¬x3 ∨ x4) - Unsatifiable

# This is only a sample. Anything in this format can be given and
# the program will work

from collections import defaultdict


class Graph:

    def __init__(self, vertex):
        self.v = vertex
        self.graph = defaultdict(list)

    # Adding edge into the graph
    def add_edge(self, _from, to):
        self.graph[_from].append(to)

    def fill_order(self, d, visited_vertex, stack):
        visited_vertex[d] = True
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)
        stack = stack.append(d)

    # transposing the matrix
    def transpose(self):
        g = Graph(self.v)

        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    def dfs(self, d, visited_vertex):
        global s
        visited_vertex[d] = True
        # print(str(d), end='')
        s += str(d)
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.dfs(i, visited_vertex)

    # Print strongly connected components
    def print_components(self):
        global s
        stack = []
        visited_vertex = [False] * self.v

        for i in range(self.v):
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)

        gr = self.transpose()

        visited_vertex = [False] * self.v

        while stack:
            i = stack.pop()
            if not visited_vertex[i]:
                gr.dfs(i, visited_vertex)

                # print("")
                s += '\n'


def accept():
    exp = input("input the CNF expression : ")
    exp = exp.replace(' ', '')
    var_no = 0
    for c in exp:
        if c.isdigit():
            if int(c) > var_no:
                var_no = int(c)

    notSymb = '¬~'
    andSymb = 'ʌ∧&*'
    orSymb = '∨+'
    if notSymb[0] in exp:
        exp = exp.replace(notSymb[0], notSymb[1])

    if andSymb[0] in exp:
        exp = exp.replace(andSymb[0], andSymb[3])
    elif andSymb[1] in exp:
        exp = exp.replace(andSymb[1], andSymb[3])
    elif andSymb[2] in exp:
        exp = exp.replace(andSymb[1], andSymb[3])

    if orSymb[0] in exp:
        exp = exp.replace(orSymb[0], orSymb[1])

    # making the literals
    literals = []
    for i in range(2 * var_no):
        literals.append('x' + str(int(i/2 + 1)))
        if not i % 2 == 0:
            literals[i] = '~' + literals[i]
    return exp, var_no, literals


s = ''


def main():
    exp, var_no, literals = accept()
    # var_no = 3
    # exp = '(x1+x2)*(~x2+~x1)*(x1+x3)*(~x3+x1)'
    # exp = '(~x1+x2)*(~x2+~x1)*(x1+x3)*(~x3+x1)'
    # literals = ['x1', '~x1', 'x2', '~x2', 'x3', '~x3']

    # print(literals)
    # print(exp)
    # print('0 - x1, 1 - ~x1, 2 - x2, 3 - ~x2, 4 - x3, 5 - ~x3')

    g = Graph(var_no * 2)

    clauses = exp.split('*')
    for i in range(len(clauses)):
        clauses[i] = clauses[i].replace('(', '', 1)
        clauses[i] = clauses[i].replace(')', '', 1)

    for clause in clauses:
        variables = clause.split('+', 1)
        var1 = int(variables[0][len(variables[0]) - 1]) - 1
        var2 = int(variables[1][len(variables[1]) - 1]) - 1

        pos1i = pos1f = 2 * var1
        pos2i = pos2f = 2 * var2

        if variables[0].find('~') >= 0:
            pos1f += 1
        else:
            pos1i += 1
        if variables[1].find('~') >= 0:
            pos2i += 1
        else:
            pos2f += 1

        g.add_edge(pos1i, pos2i)
        g.add_edge(pos2f, pos1f)

    global s
    print("Strongly Connected Components:")
    g.print_components()

    i = 0
    components = []

    j = 0
    while j < len(s):
        s2 = ''
        for i in range(2 * var_no):
            if not s[j] == '\n':  # new line character represents new component
                s2 += literals[int(s[j])] + ','
                j += 1
            else:
                j += 1
                break
        components.append(s2)
    if components.count('') > 0:
      components.remove('')

    print(components)

    satisfiable = True
    for component in components:
        for i in range(var_no):
            freq = component.count(literals[2*i])
            # print(freq)
            if freq == 2:
                satisfiable = False
                print('unsatisfiable')
                break
        if not satisfiable:
            break
    if satisfiable:
        print('satisfiable')


if __name__ == '__main__':
    main()
