import matplotlib.pyplot as plt
import networkx as nx

# Вспомогательная функция для построения графа
def build_graph(root):
    G = nx.DiGraph()
    pos = {}

    def add_edges(node, x=0, y=0, level=1):
        if node is None:
            return
        G.add_node(node.key)
        pos[node.key] = (x, y)
        if node.left:
            G.add_edge(node.key, node.left.key)
            add_edges(node.left, x - 1 / level, y - 1, level + 1)
        if node.right:
            G.add_edge(node.key, node.right.key)
            add_edges(node.right, x + 1 / level, y - 1, level + 1)

    add_edges(root)
    return G, pos

# Визуализация каждого шага поиска
def visualize_search_step(G, pos, visited, current_key=None, found=False):
    plt.clf()
    colors = []
    for node in G.nodes():
        if node == current_key and found:
            colors.append('green')
        elif node == current_key:
            colors.append('orange')
        elif node in visited:
            colors.append('red')
        else:
            colors.append('lightblue')
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1000, arrows=False)
    plt.pause(1)

# Обёртка вокруг search() для визуализации
def traced_search(root, key):
    G, pos = build_graph(root)
    plt.ion()
    fig = plt.figure()
    visited = []

    def helper(node):
        if node is None:
            return None
        visited.append(node.key)
        visualize_search_step(G, pos, visited, node.key)
        if node.key == key:
            visualize_search_step(G, pos, visited, node.key, found=True)
            return node
        if node.key < key:
            return helper(node.right)
        else:
            return helper(node.left)

    result = helper(root)
    plt.ioff()
    plt.show()
    return result



# Реализация BST
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

#Функция для поиска ключа в BST
def search(root, key):
  
    # Стандартный случай: root это null или клюс 
    if root is None or root.key == key:
        return root
    
    # Клюс больше чем ключ родителя
    if root.key < key:
        return search(root.right, key)
    
    # Клюс меньше чем ключ родителя
    return search(root.left, key)


# Создаем дерево хардкодингом, чтобы скоратить длинну кода из-за большго кол-ва деревьев
root = Node(50)
root.left = Node(30)
root.right = Node(70)
root.left.left = Node(20)
root.left.right = Node(40)
root.right.left = Node(60)
root.right.right = Node(80)

# Ищем ключи
print("Найдено" if traced_search(root, 80) else "Не найдено")
print("Найдено" if traced_search(root, 19) else "Не найдено")