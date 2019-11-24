from nodes.Node import Node

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

