#!/usr/bin/env python3

import json
import enum
import argparse

class Level(enum.Enum):
    Tainted = True
    Untainted = False

SYMTAB = {}
DEFAULT_LEVEL = Level.Untainted
CONFIG = ""

class BinOpString(enum.Enum):
    Add = '+'
    Sub = '-'
    Mul = '*'
    Div = '/'
    Mod = '%'

class UnaryOpString(enum.Enum):
    UAdd = '+'
    USub = '-'
    Not = 'not'
    Invert = '~'

class BoolOpString(enum.Enum):
    And = 'and'
    Or = 'or'
    Lt = '<'
    Gt = '>'
    Lte = '<='
    Gte = '>='
    Is = "is"
    In = 'in'
    NotIn = 'not in'
    Eq = '=='
    NotEq = '!='

# class ComparatorOpString(enum.Enum): #TODO: add the rest

def retNode(node): #TODO: Refactor this, no need to give the entire node as an argument 
    #FIXME: right value and sequence nodes can get different nodes 
    if node['ast_type'] == "Assign":
        node = Assign(node['targets'], node['value'])
    elif  node['ast_type'] == "Expr":
        node = RightValue(node['value'])
    elif  node['ast_type'] == "NameConstant":
        node = NameConstant(node['value'])
    elif node['ast_type'] == "BinOp":
        node = BinOp(node['left'],node['right'],node['op']['ast_type'])
    elif node['ast_type'] == "UnaryOp":
        node = UnaryOp(node['op']['ast_type'], node['operand'])
    elif node['ast_type'] == "Name":
        node = Name(node['id'], node['ctx'])
    elif node['ast_type'] == "Str":
        node = Str(node['s'])
    elif node['ast_type'] == "Call":
        node = Call(node['func'],node['args'])
    elif node['ast_type'] == "Num":
        node = Num(node['n'])
    elif node['ast_type'] == "If" :
        node = If(node['body'],node['orelse'],node['test'])  
    elif node['ast_type'] == "IfExp" :
        node = IfExp(node['body'],node['orelse'],node['test'])  
    elif node['ast_type'] == "While" :
        node = While(node['body'],node['orelse'],node['test'])  
    elif node['ast_type'] == "Tuple":
        node = Tuple(node['elts'], node['ctx'])
    elif node['ast_type'] == "Attribute":
        node = Attribute(node['value'], node['attr'], node['ctx'])
    elif node['ast_type'] == "Compare":
        node = Compare(node['left'],node['ops'],node['comparators'])
    else:
        print("SHOULD NEVER HAPPEN")
        print(node)
        pass

    return node

def getContext(ctx):
    return ctx['ast_type']
    
def getBoolopStr(op):
    if op == 'And':
        return(BoolOpString.And)
    elif op == 'Or':
        return(BoolOpString.Or)
    elif op == 'Lt':
        return(BoolOpString.Lt)
    elif op == 'Gt':
        return(BoolOpString.Gt)
    elif op == 'Lte':
        return(BoolOpString.Lte)
    elif op == 'Gte':
        return(BoolOpString.Gte)
    elif op == 'Is':
        return(BoolOpString.Is)
    elif op == 'In':
        return(BoolOpString.In)
    elif op == 'NotIn':
        return(BoolOpString.NotIn)
    elif op == 'Eq':
        return(BoolOpString.Eq)
    elif op == 'NotEq':
        return(BoolOpString.NotEq)
    else:
        pass

def getBinopStr(op): #add more if needed
    if op == 'Add':
        return(BinOpString.Add)
    elif op == 'Mod':
        return(BinOpString.Mod)
    else:
        pass

def getUnaryOpStr(op): #add more if needed
    if op == 'UAdd':
        return(UnaryOpString.UAdd)
    elif op == 'USub':
        return(UnaryOpString.USub)
    elif op == 'Invert':
        return(UnaryOpString.Invert)
    elif op == 'Not':
        return(UnaryOpString.Not)
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
    def print_node(self):
        pass
    def visit(self):
        pass
    def parse(self):
        pass

class Attribute(Node):
    def __init__(self, value, attr, ctx):
        print("HERE")
        self.value = retNode(value)
        self.attr = attr
        self.ctx = getContext(ctx)

    def print_node(self):
        return "{}.{}".format(self.value.print_node(), self.attr)

    def visit(self):
        pass

    def parse(self):
        pass

class NameConstant(Node):
    def __init__(self, value):
        self.value = value
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        return self.value
    
    def visit(self):
        pass

    def parse(self):
        pass

class Tuple(Node):
    def __init__(self, elts, ctx):
        self.elts = Sequence(elts)
        self.elts.parse()
        self.ctx = getContext(ctx) # Load / Store
        self.level = DEFAULT_LEVEL

    def print_node(self):
        return ("({})".format(self.elts.print_node()))

    def visit(self):
        pass
    def parse(self):
        pass

class Compare(Node):
    def __init__(self, left, ops, comparators):
        self.left = RightValue(left)
        self.ops = [ getBoolopStr(op['ast_type']) for op in ops ]
        self.comparators = Sequence(comparators)
        self.comparators.parse()

    def print_node(self):
        comparators = self.comparators.print_node().split(",")

        return "{} {}".format(self.left.print_node(), " ".join([op.value + " " + comp.strip() for op, comp in zip(self.ops, comparators)]))

    def visit(self):
        pass
    def parse(self):
        pass

class IfExp(Node):
    def __init__(self, body, orelse, test):
        self.body = RightValue(body)
        self.body.parse()

        self.orelse = RightValue(orelse)
        self.orelse.parse()

        self.test = retNode(test) #FIXME: can be more than a compare node!
    
    def print_node(self):

        return("{} if {} else: {}".format(self.body.print_node(), self.test.print_node(), self.orelse.print_node()))    

    def visit(self):
        pass
    def parse(self):
        #TODO: parse the test
        pass


class If(Node):
    def __init__(self, body, orelse, test):
        self.body = Sequence(body)
        self.body.parse()

        self.orelse = Sequence(orelse)
        self.orelse.parse()

        self.test = retNode(test) #FIXME: can be more than a compare node!
    
    def print_node(self):

        return("if {}: {} else:{}".format(self.test.print_node(),self.body.print_node(), self.orelse.print_node()))    

    def visit(self):
        pass
    def parse(self):
        #TODO: parse the test
        pass

class While(Node):
    def __init__(self, body, orelse, test):
        self.body = Sequence(body)
        self.body.parse()

        self.orelse = Sequence(orelse)
        self.orelse.parse()

        self.test = retNode(test) #FIXME: can be more than a compare node!
    
    def print_node(self):

        return("while {}: {} else:{}".format(self.test.print_node(),self.body.print_node(), self.orelse.print_node()))    

    def visit(self):
        pass
    def parse(self):
        #TODO: parse the test
        pass

class Call(Node):
    def __init__(self, func, args):
        self.args = Sequence(args)
        self.args.parse()
        self.func = retNode(func)   # Name(func['id'], func['ctx'])
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        return("(level:{}) {}({})".format(self.level, self.func.print_node(),self.args.print_node()))    

    def visit(self):
        self.args.visit()
        print(self.args)
        for arg in self.args.parsed_nodes:
            if arg.level == Level.Tainted:
                self.level = Level.Tainted

    def parse(self):
        #Nothing to do here
        pass

class Name(Node):
    #FIXME: needs a level 
    def __init__(self, idd, ctx):
        self.id = idd
        self.type = getContext(ctx) # Load / Store
        self.level = self.level = DEFAULT_LEVEL
        # TODO: Optimize!
        

    def print_node(self):
        # return("{} (level: {})".format(self.id, self.level)) 
        return("{}".format(self.id)) 

    def visit(self):
        if self.type == "Load" and self.id not in SYMTAB:
            # set level to tainted
            self.level = Level.Tainted

        if self.id not in SYMTAB:
            SYMTAB[self.id] = self
        
    
    def parse(self):
        #TODO: what to do here ? 
        pass

class Str(Node):
    #FIXME: needs a level 
    def __init__(self, s):
        self.value = s
        self.level = DEFAULT_LEVEL

    def print_node(self):
        return("\"{}\"".format(self.value))  

    def visit(self):
        pass
    def parse(self):
        #TODO: what to do here ?
        pass

class Num(Node):
    #FIXME: needs a level 
    def __init__(self, n):
        self.node = int(n['n'], n['n_str'])
        self.level = DEFAULT_LEVEL

    def print_node(self):
        return(self.node.print_node())

    def visit(self):
        pass
    def parse(self):
        #TODO: what to do here ? 
        pass
        
class int(Node):
    #FIXME: needs a level 
    def __init__(self, n, n_str):
        self.n = n
        self.n_str = n_str

    def print_node(self):
        return(self.n_str)

    def visit(self):
        pass
    def parse(self):
        #TODO: what to do here ? 
        pass


class RightValue(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.level = DEFAULT_LEVEL
        self.node = retNode(node)
        self.node.parse()
    
    def print_node(self):
        return(self.node.print_node())

    def visit(self):
        self.node.visit()
        self.level = self.node.level

    def parse(self):
        pass

class Assign(Node):
    #TODO : FINISH 
    #FIXME: python can have multiple values (i.e a,b = 2,3)
    def __init__(self, targets, value):
        self.targets = RightValue(targets[0]) 
        # self.value = RightValue(value)
        self.value = RightValue(value)
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        self.visit()
        return("(level: {}) {}={}".format(self.level, self.targets.print_node(),self.value.print_node()))    

    def visit(self):
        if isinstance(self.targets.node, Tuple):
            pass # logo se ve
        else:
            self.value.visit()
            self.targets.visit()
            self.level = self.value.level 
            SYMTAB[self.targets.node.id].level = self.level 

    def parse(self):
        self.value.parse()
        self.targets.parse()


class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = getUnaryOpStr(op)
        self.operand = RightValue(operand)
    
    def print_node(self):
        return "{} {}".format(self.op.value, self.operand.print_node())

    def visit(self):
        pass

    def parse(self):
        pass


class BinOp(Node):
    def __init__(self, left, right, op):
        self.left = RightValue(left)
        self.right = RightValue(right)
        self.op = getBinopStr(op)
        
    
    def print_node(self):
        return("{}{}{} ".format(self.left.print_node(),self.op.value,self.right.print_node()))

    def visit(self):
        pass
    def parse(self):
        self.left.parse()      
        self.right.parse()

class BoolOp(Node):
    def __init__(self, left, right, op):
        self.left = RightValue(left)
        self.right = RightValue(right)
        self.op = getBoolopStr(op)
        
    
    def print_node(self):
        return("{}{}{} ".format(self.left.print_node(),self.op.value,self.right.print_node()))

    def visit(self):
        pass
    def parse(self):
        self.left.parse()      
        self.right.parse()

class Sequence(Node):
    def __init__(self, nodes):
        self.nodes = nodes
        self.parsed_nodes = []  

    def print_node(self):
        st =[]
        for n in self.parsed_nodes:
            st.append(n.print_node())
        return(", ".join(st))

    def visit(self):
        pass
    def parse(self):
        i = 0
        for n in self.nodes:
            # print("{} : {}".format(i, n))
            # i += 1
            node = retNode(n)
            self.parsed_nodes.append(node)  

class Body(Node):
    def __init__(self, nodes):
        self.nodes = Sequence(nodes) 

    def print_node(self):
        return(self.nodes.print_node())

    def visit(self):
        pass
    def parse(self):
        self.nodes.parse()

class Module(Node):
    def __init__(self, ast):
        self.body = Body(ast['body'])
    
    def print_node(self):
        return(self.body.print_node())
    
    def visit(self):
        pass
    def parse(self):
        self.body.parse()

def parse(ast):
    if(ast['ast_type'] == "Module"):
        node = Module(ast['body'])
        node.parse()


def Main(filename, config_file):
    ast = {}

    with open(config_file, "r") as f:
        CONFIG = json.loads(f.read())

    with open(filename, "r") as f:
    # with open(filename, "r") as f:
        ast = json.loads(f.read())
    
    module = Module(ast)
    module.parse()
    print(module.print_node())

parser = argparse.ArgumentParser(prog='parse', description="to be continued", 
            usage="python parse slice.json")
parser.add_argument('filename', type=str)
parser.add_argument('--config', type=str, default="config.json")

if __name__ == '__main__':
    args = parser.parse_args()
    Main(args.filename, args.config)