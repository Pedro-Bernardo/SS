#!/usr/bin/env python3
import json, enum, argparse, copy

class Level(enum.Enum):
    Tainted = True
    Untainted = False

SYMTAB = {}
IN_CALL = False
PATHS = []
DEFAULT_LEVEL = Level.Untainted
CONFIG = []
VULNERABILITY = {}

STACK = []
SOURCES = []
SANITIZERS = []
SINKS = []
BT = {}

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

def log_vulnerability():
    def recursive_log(current, depth):
        if current[-1].get('type',None) != None:
            if current[-1]['type'] != 'sanitizer':
                print(depth*"\t" + current[-1]['desc']) 
            else:
                print(depth*"\t" + current[-1]['desc'])
                recursive_log(current[:-1], depth)
        else:
            print(depth*"\t" + current[-1]['desc']) 
            if len(current[-1]['from']) > 1:
                for i in range(len(current[-1]['from'])):
                    if BT.get(current[-1]['from'][i], None) != None:
                        print("{}'{}' backtrace:".format("\t"*depth, current[-1]['from'][i]))
                        if BT[current[-1]['from'][i]] == current:
                            recursive_log(BT[current[-1]['from'][i]][:-1], depth+1)
                        else:
                            recursive_log(BT[current[-1]['from'][i]], depth+1)
                    else:
                        print("{}'{}' is a source of taintedness".format("\t"*depth, current[-1]['from'][i]))

            elif len(current[-1]['from']) == 1:
                if BT.get(current[-1]['from'][0], None) != None:
                    if BT[current[-1]['from'][0]] != current:
                        recursive_log(BT[current[-1]['from'][0]], depth)
                    elif len(current) > 1:
                        recursive_log(BT[current[-1]['from'][0]][:-1], depth)
                    

            
    
    global SINKS
    global VULNERABILITY
    global BT
    sink = SINKS[-1]
    vuln = VULNERABILITY

    # SINKS.append({'func': name, 'var':arg.id, 'lineno':self.lineno})
    if sink['vulnerable']:
        print("Vulnerability : {}\nStatus: vulnerable\nline {}: (SINK) call to '{}' with tainted value '{}'".format(vuln['vulnerability'], sink['lineno'], sink['func'], sink['var']))
    else:
        print("Vulnerability : {}\nStatus: probably safe\nline {}:(SINK) call to '{}' with safe value '{}'".format(vuln['vulnerability'], sink['lineno'], sink['func'], sink['var']))

    print("Backtrace:")
    
    recursive_log(BT[sink['var']], 1)
    print("=================================================================")


# class ComparatorOpString(enum.Enum): #TODO: add the rest
def is_stack_tainted():
    global STACK
    for s in STACK:
        if len(s) != 0:
            return True
    return False

def get_outter_test():
    for s in STACK[::-1]:
        if len(s) != 0:
            return s
    
    return None


def retNode(node): #TODO: Refactor this, no need to give the entire node as an argument 
    #FIXME: right value and sequence nodes can get different nodes 
    if node['ast_type'] == "Assign":
        node = Assign(node['targets'], node['value'], node['lineno'])
    elif  node['ast_type'] == "Expr":
        node = RightValue(node['value'])
    elif  node['ast_type'] == "NameConstant":
        node = NameConstant(node['value'])
    elif node['ast_type'] == "BinOp":
        node = BinOp(node['left'],node['right'],node['op']['ast_type'])
    elif node['ast_type'] == "BoolOp":
        node = BoolOp(node['op']['ast_type'], node['values'])
    elif node['ast_type'] == "UnaryOp":
        node = UnaryOp(node['op']['ast_type'], node['operand'])
    elif node['ast_type'] == "Name":
        node = Name(node['id'], node['ctx'], node['lineno'])
    elif node['ast_type'] == "Str":
        node = Str(node['s'])
    elif node['ast_type'] == "Call":
        node = Call(node['func'],node['args'], node['lineno'])
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

def is_source(name):
    return name in VULNERABILITY['sources']

def is_sanitizer(name):
    return name in VULNERABILITY['sanitizers']

def is_sink(name):
    return name in VULNERABILITY['sinks']

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
   
class Node():
    def print_node(self):
        pass
    def path_visit(self, G):
        pass

    
    def taint(self):
        pass

    def parse(self):
        pass

# class Attribute(Node):
#     def __init__(self, value, attr, ctx):
#         self.value = retNode(value)
#         self.attr = attr
#         self.ctx = getContext(ctx)
#         self.level = DEFAULT_LEVEL
#         self.name = ""

#     def print_node(self):
#         return "{}.{}".format(self.value.print_node(), self.attr)

#     def taint(self):
#         # get the name
#         if not name:
#             name = self.value.id

#         if self.value.level == Level.Tainted:
#             self.level = Level.Tainted

#         self.name = "{}.{}".format(name, self.attr)
#         return self.name

#     def parse(self):
#         pass

class Attribute(Node):
    def __init__(self, value, attr, ctx):
        self.value = retNode(value)
        self.attr = attr
        self.ctx = getContext(ctx)
        self.level = DEFAULT_LEVEL

    def print_node(self):
        return "{}.{}".format(self.value.print_node(), self.attr)

    def path_visit(self, G):
        pass

    def taint(self):
        self.value.taint()
        self.level = self.value.level

    def parse(self):
        pass


class NameConstant(Node):
    def __init__(self, value):
        self.value = value
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        return self.value
    
    def path_visit(self, G):
        pass


    
    def taint(self):
        pass

    def parse(self):
        pass

class Tuple(Node):
    def __init__(self, elts, ctx):
        self.elts = Sequence(elts)
        self.ctx = getContext(ctx) # Load / Store
        self.level = DEFAULT_LEVEL

    def print_node(self):
        return ("({})".format(self.elts.print_node()))

    def path_visit(self, G):
        pass

    
    def taint(self):
        self.elts.taint()
        for el in self.elts.nodes:
            if el.level == Level.Tainted:
                self.level = Level.Tainted
                return
        

    def parse(self):
        self.elts.parse()

class Compare(Node):
    def __init__(self, left, ops, comparators):
        self.left = RightValue(left)
        self.ops = [ getBoolopStr(op['ast_type']) for op in ops ]
        self.comparators = Sequence(comparators)
        self.level = DEFAULT_LEVEL

    def print_node(self):
        comparators = self.comparators.print_node().split(",")
        return "{} {}".format(self.left.print_node(), " ".join([op.value + " " + comp.strip() for op, comp in zip(self.ops, comparators)]))

    def path_visit(self, G):
        pass


    def taint(self):
        self.left.taint()
        self.comparators.taint()
        tainters = []

        if self.left.level == Level.Tainted:
            self.level = Level.Tainted
            tainters.append(self.left.node)

        for c in self.comparators.nodes:
            if c.level == Level.Tainted:
                self.level = Level.Tainted
                tainters.append(c)
        
        return tainters

    def parse(self):
        self.comparators.parse()

class IfExp(Node):
    def __init__(self, body, orelse, test):
        self.body = RightValue(body)
        self.orelse = RightValue(orelse)
        self.test = retNode(test) #FIXME: can be more than a compare node!
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        return("{} if {} else: {}".format(self.body.print_node(), self.test.print_node(), self.orelse.print_node()))    
        

    def path_visit(self, G):
        L = []
        R = []
        self.body.path_visit(L) 
        self.orelse.path_visit(R)
        # insert test
        L.insert(0, self)
        R.insert(0, self)

        G.append([L, R])

    
    def taint(self):
        global STACK
        ret = self.test.taint()
        STACK.insert(0, ret)

    def parse(self):
        #TODO: parse the test
        self.body.parse()
        self.orelse.parse()


class If(Node):
    def __init__(self, body, orelse, test):
        self.body = Sequence(body)
        self.orelse = Sequence(orelse)
        self.test = retNode(test) #FIXME: can be more than a compare node!
    
    def print_node(self):
        return("if {}: {} else:{}".format(self.test.print_node(),self.body.print_node(), self.orelse.print_node()))    

    def path_visit(self, G):
        L = []
        R = []
        self.body.path_visit(L) 
        self.orelse.path_visit(R)
        # insert test
        L.insert(0, self)
        R.insert(0, self)

        G.append([L, R])
    
    def taint(self):
        global STACK
        ret = self.test.taint()
        STACK.insert(0, ret)

    def parse(self):
        #TODO: parse the test
        self.body.parse()
        self.orelse.parse()

class While(Node):
    def __init__(self, body, orelse, test):
        self.body = Sequence(body)
        self.orelse = Sequence(orelse)
        self.test = retNode(test) #FIXME: can be more than a compare node!
    
    def print_node(self):
        return("while {}: {} else:{}".format(self.test.print_node(),self.body.print_node(), self.orelse.print_node()))    

    def path_visit(self, G):
        L = []
        R = []
        self.body.path_visit(L) 
        self.orelse.path_visit(R)
        # insert test
        L.insert(0, self)
        R.insert(0, self)

        G.append([L, R])

    def taint(self):
        global STACK
        ret = self.test.taint()
        STACK.insert(0, ret)

    def parse(self):
        self.body.parse()
        self.orelse.parse()

class Call(Node):
    def __init__(self, func, args, lineno):
        global IN_CALL
        self.args = Sequence(args)
        IN_CALL = True
        self.func = retNode(func)   # Name(func['id'], func['ctx'])
        IN_CALL = False
        self.lineno = lineno
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        # return("({}) {}({})".format(self.level, self.func.print_node(),self.args.print_node()))    
        return("{}({})".format(self.func.print_node(),self.args.print_node()))    

    def path_visit(self, G):
        G.append(self)

    
    def taint(self):
        global SANITIZERS
        global SINKS
        
        self.func.taint()
        tainters = self.args.taint()

        name = self.func.id if isinstance(self.func, Name) else self.func.attr

        if is_source(name):
            self.level = Level.Tainted
            return [{'type': "SOURCE", 'lineno': self.lineno, 'func': name }]

        # true if not sanitizer
        if is_sanitizer(name):
            self.level = Level.Tainted
            # return outter-most tainted test
            tainters = []
            for t in get_outter_test():
                if isinstance(t, dict):
                    tainters.append(t['func'])
                else:
                    tainters.append(t.id)

            for arg in self.args.nodes:
                name = ""
                
                if isinstance(arg, Name) and SYMTAB[arg.id].level == Level.Tainted:
                    name = arg.id

                bt_entry = {'lineno': self.lineno, 'from':tainters, 'desc': "line {}: '{}' tainted for being sanitized in the scope of branch with a tainted guard ('{}')".format(self.lineno, name, "' or '".join(tainters))}

                if BT.get(name, None) != None:
                    BT[name].append(bt_entry)
                else:
                    BT[name] = [bt_entry]
            return


            for arg in self.args.nodes:
                if isinstance(arg, Name) and SYMTAB[arg.id].level == Level.Tainted:
                    SYMTAB[arg.id].level = Level.Untainted
                    SANITIZERS.append({'func': name, 'var':arg.id, 'lineno':self.lineno })
                    if BT.get(arg.id, None) != None:
                        BT[arg.id].append({'type':'sanitizer', 'lineno':self.lineno, 'from':[name], 'desc': "line {}: '{}' sanitized by call to '{}'".format(self.lineno, arg.id, name)})
                    else:
                        BT[arg.id] = {'type':'sanitizer', 'lineno':self.lineno, 'from':[name], 'desc': "line {}: '{}' sanitized by call to '{}'".format(self.lineno, arg.id, name)}
        
        elif is_sink(name):
            for arg in self.args.nodes:
                if isinstance(arg, Name) or len(SANITIZERS) > 0:
                    if SYMTAB[arg.id].level == Level.Tainted:
                        self.level = Level.Tainted
                        SINKS.append({'func': name, 'var':arg.id, 'lineno':self.lineno, 'vulnerable':True})
                    else: 
                        SINKS.append({'func': name, 'var':arg.id, 'lineno':self.lineno, 'vulnerable':False})
                        
                    log_vulnerability()



        else:
            # tainters = []
            # for arg in self.args.nodes:
            #     if arg.level == Level.Tainted:
            #         tainters.append(arg)
            final_tainters = []
            for t in tainters:
                if isinstance(t, list):
                    final_tainters += t
                else:
                    final_tainters.append(t)

            if len(final_tainters) > 0:
                self.level = Level.Tainted
            
            return final_tainters

    def parse(self):
        #Nothing to do here
        self.args.parse()
        pass

class Name(Node):
    #FIXME: needs a level 
    def __init__(self, idd, ctx, lineno):
        self.id = idd
        self.type = getContext(ctx) # Load / Store
        self.level = self.level = DEFAULT_LEVEL
        self.lineno = lineno
        self.in_call = IN_CALL
        # TODO: Optimize!

    def print_node(self):
        return("{}".format(self.id)) 
        # return("({}) {}".format(self.level, self.id)) 

    def path_visit(self, G):
        # return("{} (level: {})".format(self.id, self.level)) 
        pass

    def taint(self):
        if not self.in_call:
            if self.id not in SYMTAB:
                SYMTAB[self.id] = self

                if self.type == "Load":
                    # set level to tainted
                    self.level = Level.Tainted
                    BT[self.id] = [{'type':'unknown', 'lineno': self.lineno, 'from': None , 'desc': 'line {}: {} not initialized'.format(self.lineno, self.id)}]

            self.level = SYMTAB[self.id].level
        
        return [self]
        

        # print("({}) {}".format(self.level, self.id))

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

    def path_visit(self, G):
        pass


    
    def taint(self):
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

    def path_visit(self, G):
        pass


    
    def taint(self):
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

    def path_visit(self, G):
        pass


    
    def taint(self):
        pass

    def parse(self):
        #TODO: what to do here ? 
        pass


class RightValue(Node):
    #FIXME: needs a level 
    def __init__(self, node):
        self.level = DEFAULT_LEVEL
        self.node = retNode(node)
    
    def print_node(self):
        return(self.node.print_node())

    def path_visit(self, G):
        return(self.node.path_visit(G))


    def taint(self):
        ret = self.node.taint()
        self.level = self.node.level
        return ret

    def parse(self):
        self.node.parse()

class Assign(Node):
    #TODO : FINISH 
    #FIXME: python can have multiple values (i.e a,b = 2,3)
    def __init__(self, targets, value, lineno):
        self.targets = RightValue(targets[0]) 
        # self.value = RightValue(value)
        self.value = RightValue(value)
        self.level = DEFAULT_LEVEL
        self.lineno = lineno
    
    def print_node(self):
        # return("(level: {}) {}={}".format(self.level, self.targets.print_node(),self.value.print_node()))    
        return("{}={}".format(self.targets.print_node(),self.value.print_node()))    

    def path_visit(self, G):
        G.append(self)

    
    def taint(self):
        global SOURCES
        global SANITIZERS
        global SINKS

        self.targets.taint()
        ret = self.value.taint()

        if is_stack_tainted():
            self.level = Level.Tainted
            self.targets.level = Level.Tainted
            # return outter-most tainted test
            tainters = []
            for t in get_outter_test():
                if isinstance(t, dict):
                    tainters.append(t['func'])
                else:
                    tainters.append(t.id)

            bt_entry = {'lineno': self.lineno, 'from':tainters, 'desc': "line {}: '{}' tainted for being in the scope of branch with a tainted guard ('{}')".format(self.lineno, self.targets.node.id, "' or '".join(tainters))}

            if BT.get(self.targets.node.id, None) != None:
                BT[self.targets.node.id].append(bt_entry)
            else:
                BT[self.targets.node.id] = [bt_entry]
            return


            
            # if BT.get(self.targets.node.id, None) != None:
            #     BT[self.targets.node.id].append({'lineno': self.lineno, 'from':[get_], 'desc': "line {}: {} tainted by call to source '{}'".format(ret['lineno'], self.targets.node.id, ret['func'])})

        else:
            if self.value.level == Level.Tainted:
                    # SOURCES.append({'var': self.targets.node.id, 'lineno': ret['lineno'], 'func': ret['func']})
                if isinstance(ret, list):
                    if len(ret) == 1 and isinstance(ret[0], dict): # tainted by a source
                        ret = ret[0]
                        if BT.get(self.targets.node.id, None) != None:
                            BT[self.targets.node.id].append({'type':'source', 'lineno': ret['lineno'], 'from':[ret['func']], 'desc': "line {}: {} tainted by call to source '{}'".format(ret['lineno'], self.targets.node.id, ret['func'])})
                        else:
                            BT[self.targets.node.id] = [{'lineno': ret['lineno'], 'from':[], 'desc': "line {}: {} tainted by call to source '{}'".format(ret['lineno'], self.targets.node.id, ret['func'])}]
                    else:
                        bt_entry = {'lineno': self.lineno, 'from':[], 'desc': "line {}: '{}' tainted by contact with '{}'"}
                        for t in ret:
                            if isinstance(t, dict):
                                bt_entry['from'].append(t['func'])
                            else:
                                bt_entry['from'].append(t.id)

                        bt_entry['desc'] = bt_entry['desc'].format(bt_entry['lineno'], self.targets.node.id, "' or '".join([name for name in bt_entry['from']]))  

                        if BT.get(self.targets.node.id, None) != None:
                            BT[self.targets.node.id].append(bt_entry)
                        else:
                            BT[self.targets.node.id] = [bt_entry]
            else:
                name = ""
                if isinstance(self.value.node, Name):
                    name = self.value.node.id
                    desc = "line {}: {} untainted by an assignment to '{}'".format(self.lineno, self.targets.node.id, self.value.node.id)
                elif isinstance(self.value.node, Call):
                    name = self.value.node.func.id if isinstance(self.value.node.func, Name) else self.value.node.func.attr
                    desc = "line {}: {} untainted by safe call to '{}'".format(self.lineno, self.targets.node.id, name)
                else:
                    name = "assignment to a constant"
                    desc = "line {}: {} untainted by safe call to a constant".format(self.lineno, self.targets.node.id)

                if BT.get(self.targets.node.id, None) != None:
                    BT[self.targets.node.id].append({'lineno': self.lineno, 'from':[name], 'desc': desc})
                else:
                    BT[self.targets.node.id] = [{'lineno': self.lineno, 'from':[name], 'desc': desc}]

            self.level = self.value.level 

        SYMTAB[self.targets.node.id].level = self.level 
        

    def parse(self):
        self.value.parse()
        self.targets.parse()


class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = getUnaryOpStr(op)
        self.operand = RightValue(operand)
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        return "{} {}".format(self.op.value, self.operand.print_node())

    def path_visit(self, G):
        pass

    def taint(self):
        self.operand.taint()
        self.level = self.operand.level() #just updates if the operand level changes

    def parse(self):
        pass


class BinOp(Node):
    def __init__(self, left, right, op):
        self.left = RightValue(left)
        self.right = RightValue(right)
        self.op = getBinopStr(op)
        self.level = DEFAULT_LEVEL
        
    def print_node(self):
        return("{}{}{} ".format(self.left.print_node(),self.op.value,self.right.print_node()))

    def path_visit(self, G):
        pass

    
    def taint(self):
        self.left.taint()
        self.right.taint()
        if self.left.level == Level.Tainted or self.right.level == Level.Tainted:
            self.level = Level.Tainted
        
        tainters = []
        if self.left.level == Level.Tainted:
            tainters.append(self.left.node)
        if self.right.level == Level.Tainted:
            tainters.append(self.right.node)
        
        return tainters

        
    def parse(self):
        self.left.parse()      
        self.right.parse()

class BoolOp(Node):
    def __init__(self, op, values):
        self.values = Sequence(values)
        self.op = getBoolopStr(op)
        self.level = DEFAULT_LEVEL
    
    def print_node(self):
        return("{}{}{} ".format(self.left.print_node(),self.op.value,self.right.print_node()))

    def path_visit(self, G):
        pass

    def taint(self):
        # self.right.taint()
        # if self.left.level == Level.Tainted or self.right.level == Level.Tainted:
        #     self.level = Level.Tainted
        
        # tainters = []
        # if self.left.level == Level.Tainted:
        #     tainters.append(self.left.node)
        # if self.right.level == Level.Tainted:
        #     tainters.append(self.right.node)
        
        return self.values.taint()

    def parse(self):
        self.left.parse()      
        self.right.parse()

class Sequence(Node):
    def __init__(self, nodes):
        self.level = DEFAULT_LEVEL
        self.nodes = []
        for n in nodes:
            self.nodes.append(retNode(n))

    def print_node(self):
        st =[]
        for n in self.nodes:
            st.append(n.print_node())
        return(", ".join(st))

    def path_visit(self, G):
        for n in self.nodes:
            n.path_visit(G)
            
    
    def taint(self):
        tainters = []
        for n in self.nodes:
            tainted_args = n.taint()
            if tainted_args != None:
                for t in tainted_args:
                    if isinstance(t, dict) and t.level == Level.Tainted:
                        tainters += tainted_args
                    elif isinstance(t, Name):
                        tainters.append(t)
                    
            # else:
            #     if n.level == Level.Tainted:
            #         tainters.append(n)
            # if isinstance(n,Name) and n.level == Level.Tainted:

        if len(tainters) > 0:
            self.level = Level.Tainted

        return tainters

    def parse(self):
        for n in self.nodes:
            n.parse()

class Body(Node):
    def __init__(self, nodes):
        self.nodes = Sequence(nodes) 

    def print_node(self):
        return(self.nodes.print_node())

        
    def path_visit(self, G):
        return(self.nodes.path_visit(G))

    def taint(self):
        pass

    def parse(self):
        self.nodes.parse()

class Module(Node):
    def __init__(self, ast):
        self.body = Body(ast['body'])

    
    def print_node(self):
        return(self.body.print_node())
    
    def path_visit(self, G):
        pass


    def path_visit(self):
        G = []
        self.body.path_visit(G)
        return G
    
    def taint(self):
        pass

    def parse(self):
        self.body.parse()

def parse(ast):
    if(ast['ast_type'] == "Module"):
        node = Module(ast['body'])
        node.parse()



def dfs(graph, visited, paths):
    if len(graph) == 0:
        paths += [visited]
        return visited

    if isinstance(graph[0], list):
        dfs(graph[0][0] + ["POP"] + graph[1:], visited, paths)
        dfs(graph[0][1] + ["POP"] + graph[1:], visited, paths)
    
    else:
        # use a deepcopy to make every path independant of eachother
        return dfs(graph[1:], visited + [copy.deepcopy(graph[0])], paths)


def Main(filename, config_file):
    global SYMTAB
    global CONFIG
    global STACK
    global SOURCES
    global SANITIZERS
    global SINKS
    global VULNERABILITY
    ast = {}

    with open(config_file, "r") as f:
        CONFIG = json.loads(f.read())

    with open(filename, "r") as f:
        ast = json.loads(f.read())
    
    module = Module(ast)
    # build objects
    module.parse()

    # build the call graph
    G = module.path_visit()

    dfs(G, [], PATHS)
    
    # for a in PATHS:
    #     print("{} steps - {}".format(len(a), a))

    # search one vulnerability at a time
    for vuln in CONFIG:
        VULNERABILITY = vuln
        for path in PATHS:
            for node in path:
                if node == "POP":
                    STACK = STACK[1:]
                else:
                    node.taint()
            
            # print("============ SYMTAB ===============")
            # for s in SYMTAB:
            #     print("{} : {}".format(SYMTAB[s].id, SYMTAB[s].level))
            # print("===================================")

            # TODO: Maybe log porpagations?
            # TODO: No sinks but sanitizers
            # TODO: No sources but sinks (undeclared variables)
            # TODO: Move RightValue to retNode
            # TODO: Check if sinks is empty, if not check for sanitizers and log them


            # clear state for next iteration
            SYMTAB = {}
            STACK = []
            SOURCES = []
            SANITIZERS = []
            SINKS = []


parser = argparse.ArgumentParser(prog='parse', description="to be continued", 
            usage="python parse slice.json < --config config.json >")
parser.add_argument('filename', type=str)
parser.add_argument('--config', type=str, default="config.json")

if __name__ == '__main__':
    args = parser.parse_args()
    Main(args.filename, args.config)



# for source in SOURCES:
#         print("================================================")
#         if len(SANITIZERS) > 0:
#             for sanitizer in SANITIZERS:
#                 for sink in SINKS:
#                     print("line {}: (SOURCE) variable '{}' tainted by call to '{}'".format(source['lineno'], source['var'], source['func']))
#                     print("line {}: (SANITIZER) varialbe '{}' sanitized by call to '{}'".format(sanitizer['lineno'], sanitizer['var'], sanitizer['func']))
#                     print("line {}: (SINK) call to '{}' with tainted variable '{}'".format(sink['lineno'], sink['func'], sink['var']))
#         else:
#             for sink in SINKS:
#                 print("line {}: (SOURCE) variable '{}' tainted by call to '{}'".format(source['lineno'], source['var'], source['func']))
#                 print("line {}: (SINK) call to '{}' with tainted variable '{}'".format(sink['lineno'], sink['func'], sink['var']))
