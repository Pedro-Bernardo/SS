# Copyright (c) 2011, Jay Conrod.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Jay Conrod nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JAY CONROD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from equality import *

class Monitor():
    def __init__(self):
        self.level_stack = []

    def step(self, label):
        print label
        print self.level_stack
        print "H" in self.level_stack
        if label['kind'] == 'if':
            self.level_stack.append(label['test_lvl'])
            return True
        if label['kind'] == 'exit':
            self.level_stack.pop()
            return True

        elif label['kind'] == 'assign':
            var = VarAexp(label['var'])
            
            if "H" in self.level_stack:
                print var.level()
                if var.level() == "L":
                    raise RuntimeError("implicit leak")
            
            elif var.level() == "L" and label['exp_lvl'] == "H":
                raise RuntimeError("explicit leak")
            else:
                return True

        



class Statement(Equality):
    pass

class Aexp(Equality):
    pass

class Bexp(Equality):
    pass

# x := a => level of x and a
class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp
        

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)

    def level(self):
        if len(self.name) != 0 and self.name[0] == 'h':
            return "H"
        else:
            return "L"

    # if self.level() == "L" and self.aexp.level() == 'H':
    #         raise Exception("Illegal flow")

    # def eval(self, env, mon):
    #     value = self.aexp.eval(env, mon)
    #     env[self.name] = value
    
    def eval(self, env, mon):
        # monitor
        if mon.step({'kind':'assign', 'var':self.name, 'exp_lvl':self.aexp.level()}):
            value = self.aexp.eval(env, mon)
            env[self.name] = value

class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env, mon):
        self.first.eval(env, mon)
        self.second.eval(env, mon)

class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env, mon):
        if mon.step({'kind':'if', 'test_lvl': self.condition.level()}):
            condition_value = self.condition.eval(env, mon)
            if condition_value:
                self.true_stmt.eval(env, mon)
            else:
                if self.false_stmt:
                    self.false_stmt.eval(env, mon)
        mon.step({'kind':'exit'})

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env, mon):
        condition_value = self.condition.eval(env, mon)
        while condition_value:
            self.body.eval(env, mon)
            condition_value = self.condition.eval(env, mon)

class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def level(self):
        return "L"
    
    def eval(self, env, mon):
        return self.i

class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name
    
    def level(self):
        if len(self.name) != 0 and self.name[0] == 'h':
            return "H"
        else:
            return "L"

    def eval(self, env, mon):
        if self.name in env:
            return env[self.name]
        else:
            return 0

# TODO: level of Binop expression
class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def level(self):
        if self.left.level() == "H" or self.right.level() == "H":
            return "H"
        else:
            return "L"

    def eval(self, env, mon):
        left_value = self.left.eval(env, mon)
        right_value = self.right.eval(env, mon)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.op, self.left, self.right)


    def level(self):
        if self.left.level() == "H" or self.right.level() == "H":
            return "H"
        else:
            return "L"

    def eval(self, env, mon):
        left_value = self.left.eval(env, mon)
        right_value = self.right.eval(env, mon)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)


    def level(self):
        if self.left.level() == "H" or self.right.level() == "H":
            return "H"
        else:
            return "L"

    def eval(self, env, mon):
        left_value = self.left.eval(env, mon)
        right_value = self.right.eval(env, mon)
        return left_value and right_value

class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

    def level(self):
        if self.left.level() == "H" or self.right.level() == "H":
            return "H"
        else:
            return "L"

    def eval(self, env, mon):
        left_value = self.left.eval(env, mon)
        right_value = self.right.eval(env, mon)
        return left_value or right_value

class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBexp(%s)' % self.exp

    def level(self):
        return self.exp.level()

    def eval(self, env, mon):
        value = self.exp.eval(env, mon)
        return not value
