#!/usr/bin/env python3

import json

import enum

class BinOpString(enum.Enum):
   Add = '+'
   Sub = '-'
   Mul = '*'
   Div = '/'
   Mod = '%'

class Node():
    def visit(self):
        pass
    def parse(self):
        pass

class Leveled_Node():
    pass


class Call(Node):
    def __init__(self, node):
        self.args = Sequence(node['args'])
        self.func = Name(node['func'])
    
    def visit(self):
        print("[CALL] visiting ...")
        return("{}({})".format(self.func.visit(),self.args.visit()))    

    def parse(self):
        print("[CALL] parsing ...")
        #Nothing to do here

class Name(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.id = node['id']
        self.type = node['ctx']['ast_type'] # Load / Store

    def visit(self):
        print("[NAME] visiting ...")
        return(self.id)

    def parse(self):
        print("[NAME] parsing ...")
        #TODO: what to do here ? 

class Str(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.value = node['s']

    def visit(self):
        print("[STR] visiting ...")
        return(self.value)

    def parse(self):
        print("[STR] parsing ...")
        #TODO: what to do here ?

class Num(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.node = int(node['n'])

    def visit(self):
        print("[NUM] visiting ...")
        return(self.node.visit())

    def parse(self):
        print("[NUM] parsing ...")
        #TODO: what to do here ? 
        
class int(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.n = node['n']
        self.n_str = node['n_str']

    def visit(self):
        print("[INT] visiting ...")
        return(self.n_str)

    def parse(self):
        print("[INT] parsing ...")
        #TODO: what to do here ? 

class Str(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.value = node['s']

    def visit(self):
        print("[STR] visiting ...")
        return(self.value)

    def parse(self):
        print("[STR] parsing ...")
        #TODO: what to do here ?

class Expr(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        print(node['value'])
        self.value = RightValue(node['value'])

    def visit(self):
        print("[EXPR] visiting ...")
        return(self.value.visit())

    def parse(self):
        print("[EXPR] parsing ...")
        print(self.value.visit())
        #TODO: what to do here ?


class RightValue(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.node = node
    
    def visit(self):
        print("[RIGHTVALUE] visiting ...")
        return(self.node.visit())

    def parse(self):
        print("[RIGHTVALUE] parsing ...")

        if self.node['ast_type'] == "BinOp":
            self.node = BinOp(self.node['left'],self.node['right'],self.node['op']['ast_type'])
            self.node.parse()
        elif self.node['ast_type'] == "Name":
            self.node = Name(self.node)
            self.node.parse()
        elif self.node['ast_type'] == "Str":
            self.node = Str(self.node)
            self.node.parse()
        elif self.node['ast_type'] == "Call":
            print('\n\nTWICE\n\n')
            self.node = Call(self.node)
            self.node.parse()
        elif self.node['ast_type'] == "Num":
            self.node = Num(self.node)
            self.node.parse()
        else:
            pass

class Assign(Node):
    #FIXME: python can have multiple values (i.e a,b = 2,3)
    def __init__(self, targets, value):
        self.targets = RightValue(targets[0]) 
        self.value = RightValue(value)
    
    def visit(self):
        print("[ASSIGN] visiting ...")
        return("{}={}".format(self.targets.visit(),self.value.visit()))    

    def parse(self):
        print("[ASSIGN] parsing ...")
        self.value.parse()
        self.targets.parse()

class BinOp(Node):
    def __init__(self, left, right, op):
        self.left = RightValue(left)
        self.right = RightValue(right)
        if op == 'Add':
            self.op = BinOpString.Add
        elif op == 'Mod':
            self.op = BinOpString.Mod
        else:
            pass
        #add more if needed

    def visit(self):
        print("[BINOP] visiting ...")
        self.left.visit()
        self.right.visit()
        return("{}{}{} ".format(self.left.visit(),self.op.value,self.right.visit()))

    def parse(self):
        print("[BINOP] parsing ...")
        self.left.parse()      
        self.right.parse()

class Sequence(Node):
    def __init__(self, nodes):
        self.nodes = nodes
        self.parsed_nodes = []  

    def visit(self):
        print("[SEQUENCE] visiting ...")
        st =[]
        for n in self.parsed_nodes:
            st.append(n.visit())
        print(st)
        return(", ".join(st))

    def parse(self):
        print("[SEQUENCE] parsing ...")
        
        for n in self.nodes:
            if n['ast_type'] == "Assign":
                assign_node = Assign(n['targets'], n['value'])
                assign_node.parse()
                self.parsed_nodes.append(assign_node)
            elif  n['ast_type'] == "Expr":
                expr_node = RightValue(n['value'])
                expr_node.parse()
                self.parsed_nodes.append(expr_node)
            elif  n['ast_type'] == "Name":
                name_node = Name(n)
                name_node.parse()
                self.parsed_nodes.append(name_node)
            else:
                print( n['ast_type'])
                pass
        

        


class Body(Node):
    def __init__(self, nodes):
        self.nodes = Sequence(nodes) 

    def visit(self):
        print("[BODY] visiting ...")
        self.nodes.visit()

    def parse(self):
        print("[BODY] parsing ...")
        self.nodes.parse()

class Module(Node):
    def __init__(self, ast):
        self.body = Body(ast['body'])
    
    def visit(self):
        print("[MODULE] visiting body...")
        self.body.visit()
    
    def parse(self):
        print("[MODULE] parsing body...")
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
    
    module.visit()

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