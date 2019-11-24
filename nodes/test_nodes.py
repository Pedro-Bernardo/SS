        
class Node():
    def visit(self):
        pass
    def parse(self):
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
        if op == 'Add':
            self.op = BinOpString.Add
        elif op == 'Mod':
            self.op = BinOpString.Mod
        else:
            pass
        #add more if needed

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

class FormattedValue(Node):
	def __init__(self, value, conversion, format_spec):
		pass

	def visit(self):
		pass

	def parse(self):
		pass

class JoinedStr(Node):
	def __init__(self, values):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Bytes(Node):
	def __init__(self, s):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class List(Node):
	def __init__(self, elts, ctx):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Tuple(Node):
	def __init__(self, elts, ctx):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Set(Node):
	def __init__(self, elts):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Dict(Node):
	def __init__(self, keys, values):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Ellipsis(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class NameConstant(Node):
	def __init__(self, value):
		pass

	def visit(self):
		pass

	def parse(self):
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
		pass
        #TODO: w


class Load(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Store(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Del(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Starred(Node):
	def __init__(self, value, ctx):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Expr(Node):
	def __init__(self, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class UnaryOp(Node):
	def __init__(self, op, operand):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class UAdd(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class USub(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Not(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Invert(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class BinOp(Node):
	def __init__(self, left, op, right):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Add(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Sub(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Mult(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Div(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class FloorDiv(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Mod(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Pow(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class LShift(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class RShift(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class BitOr(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class BitXor(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class BitAnd(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class MatMult(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class BoolOp(Node):
	def __init__(self, op, values):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class And(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Or(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Compare(Node):
	def __init__(self, left, ops, comparators):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Eq(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class NotEq(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Lt(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class LtE(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Gt(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class GtE(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Is(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class IsNot(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class In(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class NotIn(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class keyword(Node):
	def __init__(self, arg, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class IfExp(Node):
	def __init__(self, test, body, orelse):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Attribute(Node):
	def __init__(self, value, attr, ctx):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Subscript(Node):
	def __init__(self, value, slice, ctx):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Index(Node):
	def __init__(self, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Slice(Node):
	def __init__(self, lower, upper, step):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class ExtSlice(Node):
	def __init__(self, dims):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class ListComp(Node):
	def __init__(self, elt, generators):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class SetComp(Node):
	def __init__(self, elt, generators):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class GeneratorExp(Node):
	def __init__(self, elt, generators):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class DictComp(Node):
	def __init__(self, key, value, generators):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class comprehension(Node):
	def __init__(self, target, iter, ifs, is_async):
		pass

	def visit(self):
		pass

	def parse(self):
		pass



class AnnAssign(Node):
	def __init__(self, target, annotation, value, simple):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class AugAssign(Node):
	def __init__(self, target, op, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Print(Node):
	def __init__(self, dest, values, nl):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Raise(Node):
	def __init__(self, exc, cause):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Assert(Node):
	def __init__(self, test, msg):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Delete(Node):
	def __init__(self, targets):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Pass(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Import(Node):
	def __init__(self, names):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class ImportFrom(Node):
	def __init__(self, module, names, level):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class alias(Node):
	def __init__(self, name, asname):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class If(Node):
	def __init__(self, test, body, orelse):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class For(Node):
	def __init__(self, target, iter, body, orelse):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class While(Node):
	def __init__(self, test, body, orelse):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Break(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Continue(Node):
	def __init__(self, ):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Try(Node):
	def __init__(self, body, handlers, orelse, finalbody):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class TryFinally(Node):
	def __init__(self, body, finalbody):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class TryExcept(Node):
	def __init__(self, body, handlers, orelse):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class ExceptHandler(Node):
	def __init__(self, type, name, body):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class With(Node):
	def __init__(self, items, body):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class withitem(Node):
	def __init__(self, context_expr, optional_vars):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class FunctionDef(Node):
	def __init__(self, name, args, body, decorator_list, returns):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Lambda(Node):
	def __init__(self, args, body):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class arguments(Node):
	def __init__(self, args, vararg, kwonlyargs, kwarg, defaults, kw_defaults):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class arg(Node):
	def __init__(self, arg, annotation):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Return(Node):
	def __init__(self, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Yield(Node):
	def __init__(self, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class YieldFrom(Node):
	def __init__(self, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Global(Node):
	def __init__(self, names):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Nonlocal(Node):
	def __init__(self, names):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class ClassDef(Node):
	def __init__(self, name, bases, keywords, starargs, kwargs, body, decorator_list):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class AsyncFunctionDef(Node):
	def __init__(self, name, args, body, decorator_list, returns):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class Await(Node):
	def __init__(self, value):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class AsyncFor(Node):
	def __init__(self, target, iter, body, orelse):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


class AsyncWith(Node):
	def __init__(self, items, body):
		pass

	def visit(self):
		pass

	def parse(self):
		pass


