import Node

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
