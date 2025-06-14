import random
import time
import networkx as nx
import matplotlib.pyplot as plt

# Вершина Декартового дерева
class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(0, 99)
        self.left = None
        self.right = None

# T1, T2 и T3 - это поддеревья дерева с корнем y
#               y                             x
#              / \     правый поворот         /  \
#             x   T3   – – – – – – – >       T1   y
#            / \       < - - - - - - -            / \
#          T1  T2     левый поворот             T2  T3

# Вспомогательная функция для правого поворота поддерева с корнем y
def rightRotate(y):
    x = y.left
    T2 = x.right
    
    # Выполняем поворот
    x.right = y
    y.left = T2
    
    # Возвращаем новый корень
    return x
    
def leftRotate(x):
    y = x.right
    T2 = y.left
    
    # Выполняем поворот
    y.left = x
    x.right = T2
    
    # Возвращаем новый корень
    return y

def insert(root, key):
    # Если корень None, создаём новый узел и возвращаем его
    if not root:
        return TreapNode(key)
    
    # Если ключ меньше либо равен корню
    if key <= root.key:
        # Вставляем в левое поддерево
        root.left = insert(root.left, key)
        
        # Восстанавливаем свойство кучи при необходимости
        if root.left.priority > root.priority:
            root = rightRotate(root)
    else:
        # Вставляем в правое поддерево
        root.right = insert(root.right, key)
        
        # Восстанавливаем свойство кучи при необходимости
        if root.right.priority > root.priority:
            root = leftRotate(root)
    return root

def deleteNode(root, key):
    if not root:
        return root
    
    if key < root.key:
        root.left = deleteNode(root.left, key)
    elif key > root.key:
        root.right = deleteNode(root.right, key)
    else:
        # Если поле left равно None
        if not root.left:
            temp = root.right
            root = None
            return temp

        # Если поле right равно None
        elif not root.right:
            temp = root.left
            root = None
            return temp
        
        # Если нужно слиять с помощью поворота
        elif root.left.priority < root.right.priority:
            root = leftRotate(root)
            root.left = deleteNode(root.left, key)
        else:
            root = rightRotate(root)
            root.right = deleteNode(root.right, key)

    return root

def search(root, key):
    if not root or root.key == key:
        return root
    
    if root.key < key:
        return search(root.right, key)
    return search(root.left, key)

def inorder(root):
    if root:
        inorder(root.left)
        print("ключ:", root.key, "| приоритет:", root.priority, end="")
        if root.left:
            print(" | левый ребенок :", root.left.key, end="")
        if root.right:
            print(" | правый ребенок :", root.right.key, end="")
        print()
        inorder(root.right)



def draw_treap(ax, root, highlight=None, found=False):
    ax.clear()
    G = nx.DiGraph()
    labels = {}
    pos = {}
    colors = {}

    def add_edges(node, x=0, y=0, dx=1.5):
        if not node:
            return
        node_id = id(node)
        G.add_node(node_id)
        labels[node_id] = f"{node.key}({node.priority})"
        pos[node_id] = (x, -y)
        colors[node_id] = (
            'green' if found and highlight == node else
            'yellow' if highlight == node else
            'lightblue'
        )
        if node.left:
            G.add_edge(node_id, id(node.left))
            add_edges(node.left, x - dx, y + 1, dx / 1.5)
        if node.right:
            G.add_edge(node_id, id(node.right))
            add_edges(node.right, x + dx, y + 1, dx / 1.5)

    add_edges(root)
    node_colors = [colors[n] for n in G.nodes()]
    nx.draw(G, pos, ax=ax, with_labels=True, labels=labels, arrows=True,
            node_size=2000, node_color=node_colors, font_size=10, font_weight='bold')
    ax.set_title("Визуализация поиска")
    ax.axis('off')
    plt.pause(0.8)

def search_visual(root, key, ax):
    current = root
    while current:
        draw_treap(ax, root, highlight=current, found=False)
        if current.key == key:
            print(f"Ключ {key} найден.")
            draw_treap(ax, root, highlight=current, found=True)
            return current
        elif key < current.key:
            current = current.left
        else:
            current = current.right
    print(f"Ключ {key} не найден.")
    draw_treap(ax, root, highlight=None, found=False)
    return None


if __name__ == "__main__":
    keys = [50, 30, 70, 20, 40, 60, 80]
    root = None
    for key in keys:
        root = insert(root, key)

    search_keys = [60, 25]

    fig, ax = plt.subplots()
    plt.ion()  

    for key in search_keys:
        print(f"Поиск ключа {key}")
        search_visual(root, key, ax)
        time.sleep(1)

    plt.ioff() 
    plt.show()