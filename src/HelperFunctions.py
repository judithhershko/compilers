from src.ast.AST import AST


def create_tree():
    expression_tree = AST()
    expression_tree.setRoot(None)
    return expression_tree
def getVariable(ctx):
    var=""
    found=False
    for i in ctx:
        if i=='=':
            found=True
        if not found:
            var+=i
    return var


