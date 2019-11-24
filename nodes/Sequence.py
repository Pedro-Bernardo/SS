import Node
import retNode

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