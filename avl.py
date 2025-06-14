import matplotlib.pyplot as plt
import networkx as nx

# AVL-структура и алгоритм 
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Начальная высота нового узла

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def insert(self, root, value):
        if not root:
            return Node(value)
        if value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        # Обновляем высоту текущего узла
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Вычисляем баланс
        balance = self.balance(root)

        # 4 случая дисбаланса и соответствующие повороты
        if balance > 1 and value < root.left.value:       # Left-Left
            return self.right_rotate(root)
        if balance < -1 and value > root.right.value:     # Right-Right
            return self.left_rotate(root)
        if balance > 1 and value > root.left.value:       # Left-Right
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and value < root.right.value:     # Right-Left
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Выполняем поворот
        y.left = z
        z.right = T2

        # Обновляем высоты
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # Выполняем поворот
        y.right = z
        z.left = T3

        # Обновляем высоты
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def insert_value(self, value):
        self.root = self.insert(self.root, value)

    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.value, end=' ')
            self.inorder(node.right)

    # Новый метод поиска с возвратом найденного узла
    def search(self, root, value):
        if root is None or root.value == value:
            return root
        if value < root.value:
            return self.search(root.left, value)
        else:
            return self.search(root.right, value)

# Визуализация 

def build_graph(root):
    G = nx.DiGraph()
    pos = {}

    def add_edges(node, x=0, y=0, level=1):
        if not node:
            return
        G.add_node(node.value)
        pos[node.value] = (x, y)
        if node.left:
            G.add_edge(node.value, node.left.value)
            add_edges(node.left, x - 1 / level, y - 1, level + 1)
        if node.right:
            G.add_edge(node.value, node.right.value)
            add_edges(node.right, x + 1 / level, y - 1, level + 1)

    add_edges(root)
    return G, pos

def draw_tree(tree, highlight=None, delay=1):
    G, pos = build_graph(tree.root)
    plt.clf()
    colors = ['red' if node == highlight else 'lightblue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1000)
    plt.pause(delay)

def traced_insert(tree, value):
    print(f"Inserting {value}")
    tree.insert_value(value)
    draw_tree(tree, highlight=value)

# Новая функция визуализации поиска с подсветкой пройденных узлов
def traced_search(tree, value):
    G, pos = build_graph(tree.root)
    plt.ion()
    fig = plt.figure()
    visited = []

    def helper(node):
        if node is None:
            return None
        visited.append(node.value)
        plt.clf()
        colors = []
        for n in G.nodes():
            if n == value and n == node.value:
                colors.append('green')  # найденный узел
            elif n == node.value:
                colors.append('orange')  # текущий узел
            elif n in visited:
                colors.append('red')  # пройденные узлы
            else:
                colors.append('lightblue')
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1000)
        plt.pause(1)

        if node.value == value:
            return node
        elif value < node.value:
            return helper(node.left)
        else:
            return helper(node.right)

    print(f"Searching for {value}")
    result = helper(tree.root)
    plt.ioff()
    plt.show()
    if result:
        print(f"Value {value} found")
    else:
        print(f"Value {value} not found")
    return result

if __name__ == "__main__":
    plt.ion()
    tree = AVLTree()

    # Пошаговая вставка с визуализацией
    for val in [10, 20, 30, 25, 28, 27]:
        traced_insert(tree, val)

    print("\nIn-order traversal:")
    tree.inorder(tree.root)
    print()

    # Визуализация поиска
    traced_search(tree, 28)
    traced_search(tree, 39)

    plt.ioff()
    plt.show()
