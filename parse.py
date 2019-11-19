#!/usr/bin/env python3

import json

class Node():
    def visit(self):
        pass
    def parse(self):
        pass

class Leveled_Node():
    pass

class Assign(Node):
    def __init__(self, targets, value):
        self.targets = targets
        self.value = value
    
    def visit(self):
        # visit all targets
        # visit value
        print(self.targets)
        print(self.value)

    def parse(self):
        print("target = {}".format(self.targets))
        print("value = {}".format(self.value))



class Body(Node):
    def __init__(self, nodes):
        self.nodes = nodes
        self.parsed_nodes = []  

    def visit(self):
        # print(self.nodes)
        for n in self.nodes:
            self.nodes.visit()

    def parse(self):
        for n in self.nodes:
            if n['ast_type'] == "Assign":
                assign_node = Assign(n['targets'], n['value'])
                assign_node.parse()
                self.parsed_nodes.append(assign_node)
            else:
                node = Node()
                self.parsed_nodes.append(node)

class Module(Node):
    def __init__(self, ast):
        self.body = Body(ast['body'])
    
    def visit(self):
        self.body.visit()
    
    def parse(self):
        self.body.parse()

def parse(ast):
    if(ast['ast_type'] == "Module"):
        node = Module(ast['body'])
        node.parse()



def Main():
    ast = {}
    with open("proj-slices/slice1.json", "r") as f:
        ast = json.loads(f.read())
    
    module = Module(ast)
    module.parse()

    print(module.body.parsed_nodes)

    


if __name__ == '__main__':
    Main()

# def stmt(Node):
#     return assign_stmt() | \
#            if_stmt()     | \
#            while_stmt()

# def assign_stmt():
#     def process(parsed):
#         ((name, _), exp) = parsed
#         return AssignStatement(name, exp)
#     return id + keyword(':=') + aexp() ^ process

# def if_stmt():
#     def process(parsed):
#         (((((_, condition), _), true_stmt), false_parsed), _) = parsed
#         if false_parsed:
#             (_, false_stmt) = false_parsed
#         else:
#             false_stmt = None
#         return IfStatement(condition, true_stmt, false_stmt)
#     return keyword('if') + bexp() + \
#            keyword('then') + Lazy(stmt_list) + \
#            Opt(keyword('else') + Lazy(stmt_list)) + \
#            keyword('end') ^ process

# def while_stmt():
#     def process(parsed):
#         ((((_, condition), _), body), _) = parsed
#         return WhileStatement(condition, body)
#     return keyword('while') + bexp() + \
#            keyword('do') + Lazy(stmt_list) + \
#            keyword('end') ^ process

# # Boolean expressions
# def bexp():
#     return precedence(bexp_term(),
#                       bexp_precedence_levels,
#                       process_logic)

# def bexp_term():
#     return bexp_not()   | \
#            bexp_relop() | \
#            bexp_group()

# def bexp_not():
#     return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

# def bexp_relop():
#     relops = ['<', '<=', '>', '>=', '=', '!=']
#     return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

# def bexp_group():
#     return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

# # Arithmetic expressions
# def aexp():
#     return precedence(aexp_term(),
#                       aexp_precedence_levels,
#                       process_binop)

# def aexp_term():
#     return aexp_value() | aexp_group()

# def aexp_group():
#     return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group
           
# def aexp_value():
#     return (num ^ (lambda i: IntAexp(i))) | \
#            (id  ^ (lambda v: VarAexp(v)))

# # An IMP-specific combinator for binary operator expressions (aexp and bexp)
# def precedence(value_parser, precedence_levels, combine):
#     def op_parser(precedence_level):
#         return any_operator_in_list(precedence_level) ^ combine
#     parser = value_parser * op_parser(precedence_levels[0])
#     for precedence_level in precedence_levels[1:]:
#         parser = parser * op_parser(precedence_level)
#     return parser

# # Miscellaneous functions for binary and relational operators
# def process_binop(op):
#     return lambda l, r: BinopAexp(op, l, r)

# def process_relop(parsed):
#     ((left, op), right) = parsed
#     return RelopBexp(op, left, right)

# def process_logic(op):
#     if op == 'and':
#         return lambda l, r: AndBexp(l, r)
#     elif op == 'or':
#         return lambda l, r: OrBexp(l, r)
#     else:
#         raise RuntimeError('unknown logic operator: ' + op)

# def process_group(parsed):
#     ((_, p), _) = parsed
#     return p

# def any_operator_in_list(ops):
#     op_parsers = [keyword(op) for op in ops]
#     parser = reduce(lambda l, r: l | r, op_parsers)
#     return parser

# # Operator keywords and precedence levels
# aexp_precedence_levels = [
#     ['*', '/'],
#     ['+', '-'],
# ]

# bexp_precedence_levels = [
#     ['and'],
#     ['or'],
# ]