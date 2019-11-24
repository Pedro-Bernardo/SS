import Node

class Module(Node):
    def __init__(self, ast):
        self.body = Body(ast['body'])
    
    def visit(self):
        return(self.body.visit())
    
    def parse(self):
        self.body.parse()