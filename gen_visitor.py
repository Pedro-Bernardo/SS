import argparse

TEMPLATE = """class {}(Node):\n\tdef __init__(self, {}):\n\t\tpass\n\n\t def visit(self):\n\t\tpass\n\n\tdef parse(self):\n\t\tpass\n\n"""


parser = argparse.ArgumentParser(prog='get_nodes', description="get ast_type python nodes from documentation page",
                                     usage="python get_nodes <doc.html>")
parser.add_argument('filename', type=str)


if __name__ == '__main__':
    args = parser.parse_args()

    nodes = ""

    with open(args.filename, "r") as f:
        nodes = f.read()
    
    lines = nodes.split("\n")[:-1]
    # print lines
    i = 0
    for l in lines:
        arg_split = l.split("(")
        i += 1
        print TEMPLATE.format(arg_split[0], arg_split[1][:arg_split[1].index(")")])
