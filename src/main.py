import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import sys


class Graph:
    def __init__(self):
        self.left_vertices = set()
        self.right_vertices = set()
        self.edges = []

    def add_vertex(self, vertex, is_left=True):
        if is_left:
            self.left_vertices.add(vertex)
        else:
            self.right_vertices.add(vertex)

    def remove_vertex(self, vertex):
        is_deleted = False
        if vertex in self.left_vertices:
            self.left_vertices.remove(vertex)
            is_deleted = True
        if vertex in self.right_vertices:
            self.right_vertices.remove(vertex)
            is_deleted = True
        self.edges = [(u, v) for u, v in self.edges if u != vertex and v != vertex]
        return is_deleted

    def add_edge(self, u, v):
        if (u and v) and ((u, v) not in self.edges):
            self.edges.append((u, v))
            self.left_vertices.add(u)
            self.right_vertices.add(v)
            return True
        return False

    def remove_edge(self, u, v):
        edge = (u, v)
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        return False

    def find_maximum_matching(self):

        def dfs(u, visited):
            curr_edges = self.edges[:]
            for edge in curr_edges:
                v = edge[1]
                if edge[0] == u and v not in visited:
                    visited.add(v)
                    if (v not in matching) or dfs(matching[v], visited):
                        matching[u] = v
                        matching[v] = u
                        curr_edges.remove(edge)
                        return True
            return False

        matching = {}
        for u in self.left_vertices:
            matching[u] = None

        for u in self.left_vertices:
            if matching[u] is None:
                visited = set()
                dfs(u, visited)

        matching_edges = [(u, matching[u]) for u in self.left_vertices if matching[u] is not None]
        return matching_edges

    def visualize_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.left_vertices, bipartite=0)
        graph.add_nodes_from(self.right_vertices, bipartite=1)
        graph.add_edges_from(self.edges)

        pos = nx.bipartite_layout(graph, self.left_vertices, aspect_ratio=5)

        plt.figure()
        nx.draw_networkx(graph, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
        plt.axis('off')
        plt.show()


class GraphGUI:
    def __init__(self):
        self.graph = Graph()
        self.root = tk.Tk()
        self.root.title("Graph GUI")

        self.vertex_location_var = tk.StringVar(value="left")
        self.label_vertex = tk.Label(self.root, text="Вершина:")
        self.entry_vertex = tk.Entry(self.root)
        self.radio_left = tk.Radiobutton(
            self.root, text="Левая доля", variable=self.vertex_location_var, value="left"
        )
        self.radio_right = tk.Radiobutton(
            self.root, text="Правая доля", variable=self.vertex_location_var, value="right"
        )
        self.button_add_vertex = tk.Button(self.root, text="Добавить вершину", command=self.add_vertex)

        self.button_remove_vertex = tk.Button(self.root, text="Удалить вершину", command=self.remove_vertex)

        self.label_edge = tk.Label(self.root, text="Ребро:")
        self.entry_edge_from = tk.Entry(self.root)
        self.entry_edge_to = tk.Entry(self.root)
        self.button_add_edge = tk.Button(self.root, text="Добавить ребро", command=self.add_edge)

        self.button_remove_edge = tk.Button(self.root, text="Удалить ребро", command=self.remove_edge)

        self.button_find_matching = tk.Button(
            self.root, text="Найти наибольшее паросочетание", command=self.find_matching
        )
        self.text_matching = tk.Text(self.root, height=10, width=30)

        self.figure = plt.figure(figsize=(8, 6))
        self.graph_ax = self.figure.add_subplot(111)
        self.graph_canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.graph_canvas.draw()

        self.update_graph()

    def add_vertex(self):
        vertex = self.entry_vertex.get()
        is_left = self.vertex_location_var.get() == "left"
        if vertex:
            self.graph.add_vertex(vertex, is_left)
            messagebox.showinfo("Добавление вершины", "Вершина успешно добавлена.")
            self.update_graph()
        else:
            messagebox.showwarning("Ошибка", "Введите значение вершины.")

    def remove_vertex(self):
        vertex = self.entry_vertex.get()
        is_deleted = self.graph.remove_vertex(vertex)
        if is_deleted:
            messagebox.showinfo("Удаление вершины", "Вершина успешно удалена.")
            self.update_graph()
        else:
            messagebox.showwarning("Ошибка", "Введите корректное значение вершины для удаления.")

    def add_edge(self):
        u = self.entry_edge_from.get()
        v = self.entry_edge_to.get()
        is_added = self.graph.add_edge(u, v)
        if is_added:
            messagebox.showinfo("Добавление ребра", "Ребро успешно добавлено.")
            self.update_graph()
        else:
            messagebox.showwarning("Ошибка", "Введите корректные значения вершин ребра.")

    def remove_edge(self):
        u = self.entry_edge_from.get()
        v = self.entry_edge_to.get()
        is_deleted = self.graph.remove_edge(u, v)

        if is_deleted:
            messagebox.showinfo("Удаление ребра", "Ребро успешно удалено.")
            self.update_graph()
        else:
            messagebox.showwarning("Ошибка", "Введите корректное значения вершин ребра.")

    def find_matching(self):
        matching = self.graph.find_maximum_matching()
        self.text_matching.delete("1.0", tk.END)
        if matching:
            for edge in matching:
                self.text_matching.insert(tk.END, f"{edge[0]} - {edge[1]}\n")
        else:
            self.text_matching.insert(tk.END, "Паросочетание не найдено.")

    def update_graph(self):
        self.graph_ax.clear()

        G = nx.Graph()
        G.add_nodes_from(self.graph.left_vertices, bipartite=0)
        G.add_nodes_from(self.graph.right_vertices, bipartite=1)
        G.add_edges_from(self.graph.edges)

        pos = nx.bipartite_layout(G, self.graph.left_vertices)

        nx.draw_networkx(
            G,
            pos=pos,
            ax=self.graph_ax,
            with_labels=True,
            node_color="lightblue",
            node_size=1000,
            edge_color="black",
            width=1,
        )

        self.graph_ax.axis("off")
        self.graph_canvas.draw()

    def run(self):
        self.label_vertex.grid(row=0, column=0, sticky="news")
        self.entry_vertex.grid(row=0, column=1, sticky="news")
        self.radio_left.grid(row=0, column=2, sticky="news")
        self.radio_right.grid(row=0, column=3, sticky="news")
        self.button_add_vertex.grid(row=0, column=4, sticky="news")

        self.button_remove_vertex.grid(row=0, column=5, sticky="news")
        self.label_edge.grid(row=1, column=0, sticky="news")
        self.entry_edge_from.grid(row=1, column=1, sticky="news")
        self.entry_edge_to.grid(row=1, column=2, sticky="news")
        self.button_add_edge.grid(row=1, column=3, sticky="news")
        self.button_remove_edge.grid(row=1, column=4, sticky="news")

        self.button_find_matching.grid(row=2, column=0, sticky="news")
        self.text_matching.grid(row=3, column=0, sticky="news")

        self.graph_canvas.get_tk_widget().grid(row=3, column=2, columnspan=4, sticky="news")

        # Растягивание элементов интерфейса
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        self.root.mainloop()


def run_tests():

    g = Graph()
    g.add_edge('A', 1)
    g.add_edge('B', 2)
    g.add_edge('C', 1)
    g.add_edge('C', 3)
    g.add_edge('D', 2)
    g.add_edge('E', 3)
    g.add_edge('F', 2)
    matching = g.find_maximum_matching()
    print("Наибольшее паросочетание:")
    for edge in matching:
        print(edge)
    g.visualize_graph()

    g = Graph()
    g.add_edge('A', 'X')
    g.add_edge('B', 'Y')
    g.add_edge('C', 'X')
    g.add_edge('D', 'Y')
    g.add_edge('E', 'Z')
    g.add_edge('F', 'Z')
    matching = g.find_maximum_matching()
    print("Наибольшее паросочетание:")
    for edge in matching:
        print(edge)
    g.visualize_graph()

    g = Graph()
    g.add_edge(1, 'A')
    g.add_edge(2, 'B')
    g.add_edge(3, 'C')
    g.add_edge(4, 'A')
    g.add_edge(5, 'B')
    g.add_edge(6, 'C')
    g.visualize_graph()
    matching = g.find_maximum_matching()
    print("Наибольшее паросочетание:")
    for edge in matching:
        print(edge)
    g.visualize_graph()

    g = Graph()
    # Создаем 10-20 вершин слева и справа
    num_left_vertices = random.randint(10, 20)
    num_right_vertices = random.randint(10, 20)
    left_vertices = [f'L{i}' for i in range(num_left_vertices)]
    right_vertices = [f'R{i}' for i in range(num_right_vertices)]
    # Создаем случайные ребра между левыми и правыми вершинами
    for u in left_vertices:
        for v in right_vertices:
            if random.random() < 0.5:
                g.add_edge(u, v)
    matching = g.find_maximum_matching()
    print("Наибольшее паросочетание:")
    for edge in matching:
        print(edge)
    g.visualize_graph()


is_dev = (len(sys.argv) > 1) and (str(sys.argv[1]) == "-test")
if is_dev:
    run_tests()
gui = GraphGUI()
gui.run()

