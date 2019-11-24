import Node


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

