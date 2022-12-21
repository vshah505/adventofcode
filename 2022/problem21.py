import utils
import sympy


class TreeNode:
    def __init__(self, name, left, right, operator, value):
        self.name = name
        self.lname = left
        self.rname = right
        self.operator = operator
        self.value = value


def get_input():
    nodes = dict()
    with utils.get_input_fd(__file__) as f:
        for line in f.read().split("\n"):
            name, operation = line.split(":")
            if operation.lstrip().isnumeric():
                nodes[name] = TreeNode(
                    name=name, left=None, right=None, operator=None, value=operation
                )
            else:
                lname, operator, rname = operation.lstrip().split(" ")
                nodes[name] = TreeNode(
                    name=name, left=lname, right=rname, operator=operator, value=None
                )

    return nodes


def get_equation(nodes, mistranslation=False):
    root = nodes["root"]

    def dfs(node):
        if node.lname:
            left_val = dfs(nodes[node.lname])
        if node.rname:
            right_val = dfs(nodes[node.rname])

        if node.value:
            return node.value

        if node.operator:
            return f"({left_val} {node.operator} {right_val})"

    equation = dfs(root)
    if mistranslation:
        x = sympy.symbols("x")
        l, r = equation[1:-1].split(" = ")
        return (eval(l) / int(eval(r))) - 1

    return eval(equation)


def part1():
    nodes = get_input()
    return get_equation(nodes)


def part2():
    nodes = get_input()
    nodes["humn"].value = "x"
    nodes["root"].operator = "="
    return sympy.solve(get_equation(nodes, mistranslation=True))[0]


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
