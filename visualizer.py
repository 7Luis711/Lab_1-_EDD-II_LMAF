from graphviz import Digraph

def draw_tree(root, filename="tree"):
    dot = Digraph()
    def add_nodes(node):
        if not node: return
        dot.node(node.iso3, f"{node.iso3}\n{round(node.mean,2)}")
        if node.left:
            dot.edge(node.iso3, node.left.iso3)
            add_nodes(node.left)
        if node.right:
            dot.edge(node.iso3, node.right.iso3)
            add_nodes(node.right)
    add_nodes(root)
    dot.render(filename, format="png", cleanup=True)
