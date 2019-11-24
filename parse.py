#!/usr/bin/env python3

import json

import enum

class BinOpString(enum.Enum):
   Add = '+'
   Sub = '-'
   Mul = '*'
   Div = '/'
   Mod = '%'

class ComparatorOpString(enum.Enum): #TODO: add the rest
   Eq = '=='
   NotEq = '!='

def retNode(node): #TODO: Refactor this, no need to give the entire node as an argument 
    #FIXME: right value and sequence nodes can get different nodes 
    if node['ast_type'] == "Assign":
        node = Assign(node['targets'], node['value'])
    elif  node['ast_type'] == "Expr":
        node = RightValue(node['value'])
    elif node['ast_type'] == "BinOp":
        node = BinOp(node['left'],node['right'],node['op']['ast_type'])
    elif node['ast_type'] == "Name":
        node = Name(node)
    elif node['ast_type'] == "Str":
        node = Str(node)
    elif node['ast_type'] == "Call":
        node = Call(node)
    elif node['ast_type'] == "Num":
        node = Num(node)
    elif node['ast_type'] == "If" :
        node = If(node)  
    elif node['ast_type'] == "While":
        #node = While(node) #TODO: Not Implemented
        pass
    else:
        print("SHOULD NEVER HAPPEN")
        pass

    return node

def getBinopStr(op): #add more if needed
    if op == 'Add':
        return(BinOpString.Add)
    elif op == 'Mod':
        return(BinOpString.Mod)
    else:
        pass

def getComparatoropStr(op): #add more if needed
    if op == 'Eq':
        return(ComparatorOpString.Eq)
    elif op == 'NotEq':
        return(ComparatorOpString.NotEq)
    else:
        pass
   
class Node():
    def visit(self):
        pass
    def parse(self):
        pass

class Leveled_Node():
    pass


class Comparator(Node):
    def __init__(self, node):
        self.ops = getComparatoropStr(node['ops'][0]['ast_type']) #FIXME : hardcoded the index ... maybe sequence node?
        self.comparators = retNode(node['comparators'][0])
        self.left = Name(node['left']) #FIXME: only name???
    
    def visit(self):
        return("{}{}{}".format(self.left.visit(),self.ops.value, self.comparators.visit())) 
            

    def parse(self):
        #TODO: parse the test
        pass


class If(Node):
    def __init__(self, node):
        self.body = Sequence(node['body'])
        self.body.parse()

        self.orelse = Sequence(node['orelse'])
        self.orelse.parse()

        self.test = Comparator(node['test']) #FIXME: can be more than a compare node!
    
    def visit(self):

        return("if {}: {} else:{}".format(self.test.visit(),self.body.visit(), self.orelse.visit()))    

    def parse(self):
        #TODO: parse the test
        pass


class Call(Node):
    def __init__(self, node):
        self.args = Sequence(node['args'])
        self.args.parse()
        self.func = Name(node['func'])
    
    def visit(self):
        return("{}({})".format(self.func.visit(),self.args.visit()))    

    def parse(self):
        #Nothing to do here
        pass

class Name(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.id = node['id']
        self.type = node['ctx']['ast_type'] # Load / Store

    def visit(self):
        return(self.id)

    def parse(self):
        #TODO: what to do here ? 
        pass

class Str(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.value = node['s']

    def visit(self):
        return("{}".format(self.value))  

    def parse(self):
        #TODO: what to do here ?
        pass

class Num(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.node = int(node['n'])

    def visit(self):
        return(self.node.visit())

    def parse(self):
        #TODO: what to do here ? 
        pass
        
class int(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.n = node['n']
        self.n_str = node['n_str']

    def visit(self):
        return(self.n_str)

    def parse(self):
        #TODO: what to do here ? 
        pass

class Str(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.value = node['s']

    def visit(self):
        return(self.value)

    def parse(self):
        #TODO: what to do here ?
        pass

class RightValue(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.node = node
    
    def visit(self):
        return(self.node.visit())

    def parse(self):
        self.node = retNode(self.node)
        self.node.parse()

class Assign(Node):
    #FIXME: python can have multiple values (i.e a,b = 2,3)
    def __init__(self, targets, value):
        self.targets = RightValue(targets[0]) 
        self.value = RightValue(value)
    
    def visit(self):
        return("{}={}".format(self.targets.visit(),self.value.visit()))    

    def parse(self):
        self.value.parse()
        self.targets.parse()


class BinOp(Node):
    def __init__(self, left, right, op):
        self.left = RightValue(left)
        self.right = RightValue(right)
        self.op = getBinopStr(op)
        
    
    def visit(self):
        return("{}{}{} ".format(self.left.visit(),self.op.value,self.right.visit()))

    def parse(self):
        self.left.parse()      
        self.right.parse()

class Sequence(Node):
    def __init__(self, nodes):
        self.nodes = nodes
        self.parsed_nodes = []  

    def visit(self):
        st =[]
        for n in self.parsed_nodes:
            st.append(n.visit())
        return(", ".join(st))

    def parse(self):
        for n in self.nodes:
            node = retNode(n)
            node.parse()
            self.parsed_nodes.append(node)  

class Body(Node):
    def __init__(self, nodes):
        self.nodes = Sequence(nodes) 

    def visit(self):
        return(self.nodes.visit())

    def parse(self):
        self.nodes.parse()

class Module(Node):
    def __init__(self, ast):
        self.body = Body(ast['body'])
    
    def visit(self):
        return(self.body.visit())
    
    def parse(self):
        self.body.parse()

def parse(ast):
    if(ast['ast_type'] == "Module"):
        node = Module(ast['body'])
        node.parse()

def Main():
    ast = {}
    with open("proj-slices/slice7.json", "r") as f:
        ast = json.loads(f.read())
    
    module = Module(ast)
    module.parse()
    
    print(module.visit())

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