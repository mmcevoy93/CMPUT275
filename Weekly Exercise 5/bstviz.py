from graphviz import Digraph


def bstviz(tree, just_keys=False, padding=0.6):
    """
    Create a dot object to visualize a binary search tree.

    Assumes tree is a class that has a root member. This is a node
    of the tree. Also assumes each node has:
     - left: left child in the bst
     - right: right child in the bst
     - key: key of the node
     - item: item held at the key

    The returned dot object, say "treedot", can be viewed the usual way:
      treedot.render(view=True)
    """

    dot = Digraph()

    dot.attr("node", fontname="helvetica-bold", fontsize="20")

    if len(tree) == 0:
        dot.node("empty tree", style="dashed")
        return dot

    def gen_drawing(node, depth):
        nonlocal nodes_seen

        if node is None or node.key is None:
            return -1

        l_index = gen_drawing(node.left, depth+1)

        index = nodes_seen
        nodes_seen += 1
        pos_str = str(index*padding)+','+str(-depth)+'!'

        key_str = str(node.key)
        label = key_str
        if not just_keys:
            label += ','+str(node.item)
        dot.node(key_str, label, pos=pos_str)

        r_index = gen_drawing(node.right, depth+1)

        if l_index != -1:
            dot.edge(key_str, str(node.left.key))
        if r_index != -1:
            dot.edge(key_str, str(node.right.key))

        return index

    nodes_seen = 0
    root_id = gen_drawing(tree.root, 0)
    dot.node("__root", "root", pos=str(root_id*padding)+",1!", color="white")
    dot.edge("__root", str(tree.root.key))
    dot.engine = "neato"
    return dot
