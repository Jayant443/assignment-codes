import tkinter as tk
from tkinter import ttk
import random, math

class Node:
    def __init__(self, name, depth, is_max):
        self.name, self.depth, self.is_max = name, depth, is_max
        self.children, self.value = [], None
        self.alpha, self.beta = -math.inf, math.inf
        self.current_value = -math.inf if is_max else math.inf
        self.x = self.y = 0
        self.pruned = False
        self.state = "unvisited"

class AlphaBetaApp:
    LEGEND = [("Max Node (Circle)", "#bdc3c7", "oval"), ("Min Node (Square)", "#bdc3c7", "rect"),
              ("Current", "#f1c40f", "oval"), ("Evaluated", "#2ecc71", "oval"), ("Pruned", "#e74c3c", "oval")]
    STATE_COLOR = {"current": "#f1c40f", "evaluated": "#2ecc71", "pruned": "#e74c3c"}

    def __init__(self, root):
        self.root = root
        root.title("Alpha-Beta Pruning Visualizer")
        root.geometry("1200x800")
        root.configure(bg="#2c3e50")
        try:
            import ctypes; ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.setup_ui()
        self.node_counter = 0
        self.tree_root = None
        self.generator = None
        self.is_running = False
        self.nodes_dict = {}
        root.after(100, self.generate_tree)

    def setup_ui(self):
        ctrl = tk.Frame(self.root, bg="#34495e", pady=10)
        ctrl.pack(fill=tk.X)
        ttk.Button(ctrl, text="Generate Random Tree", command=self.generate_tree).pack(side=tk.LEFT, padx=10)
        ttk.Button(ctrl, text="Start Search", command=self.start_search).pack(side=tk.LEFT, padx=10)
        self.speed_scale = tk.Scale(ctrl, from_=50, to=2000, orient=tk.HORIZONTAL, label="Animation Delay (ms)",
                                     bg="#34495e", fg="white", highlightthickness=0, length=200)
        self.speed_scale.set(600)
        self.speed_scale.pack(side=tk.RIGHT, padx=20)
        self.lbl_status = tk.Label(ctrl, text="Ready", fg="#f1c40f", bg="#34495e", font=("Segoe UI", 12, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=20)

        legend_canvas = tk.Canvas(self.root, bg="#2c3e50", height=40, highlightthickness=0)
        legend_canvas.pack(fill=tk.X, padx=10, pady=5)
        x = 20
        for text, color, shape in self.LEGEND:
            draw = legend_canvas.create_oval if shape == "oval" else legend_canvas.create_rectangle
            draw(x, 10, x + 20, 30, fill=color, outline="#2c3e50")
            legend_canvas.create_text(x + 25, 20, text=text, fill="white", anchor=tk.W, font=("Segoe UI", 10))
            x += 160

        self.canvas = tk.Canvas(self.root, bg="#1a252f", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def create_tree(self, depth, is_max, max_depth):
        node = Node(f"N{self.node_counter}", depth, is_max)
        self.nodes_dict[node.name] = node
        self.node_counter += 1
        if depth == max_depth:
            node.value = random.randint(1, 99)
        else:
            node.children = [self.create_tree(depth + 1, not is_max, max_depth)
                              for _ in range(random.randint(2, 3))]
        return node

    def layout_tree(self, node, x_min, x_max, y, y_step):
        node.x, node.y = (x_min + x_max) / 2, y
        if node.children:
            width = (x_max - x_min) / len(node.children)
            for i, child in enumerate(node.children):
                self.layout_tree(child, x_min + i * width, x_min + (i + 1) * width, y + y_step, y_step)

    def generate_tree(self):
        self.is_running = False
        self.node_counter, self.nodes_dict = 0, {}
        self.tree_root = self.create_tree(0, True, 4)
        self.canvas.update()
        width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 1200
        self.layout_tree(self.tree_root, 0, width, 50, 140)
        self.draw_tree()
        self.lbl_status.config(text="New tree generated. Ready to search.")

    def draw_tree(self):
        self.canvas.delete("all")
        self.draw_edges(self.tree_root)
        self.draw_nodes(self.tree_root)

    def draw_edges(self, node):
        for child in node.children:
            color, dash = ("#e74c3c", (4, 4)) if child.pruned else ("#7f8c8d", ())
            self.canvas.create_line(node.x, node.y, child.x, child.y, fill=color, dash=dash, width=2)
            self.draw_edges(child)

    def draw_nodes(self, node):
        r = 22
        fill = self.STATE_COLOR.get(node.state, "#bdc3c7")
        shape = self.canvas.create_oval if node.is_max else self.canvas.create_rectangle
        shape(node.x - r, node.y - r, node.x + r, node.y + r, fill=fill, outline="#2c3e50", width=2)

        if node.value is not None:
            val_text = str(node.value)
        elif node.current_value not in (-math.inf, math.inf):
            val_text = str(node.current_value)
        else:
            val_text = "?"
        self.canvas.create_text(node.x, node.y, text=val_text, font=("Segoe UI", 11, "bold"))

        if not node.pruned and node.children:
            ab = f"α: {self.format_inf(node.alpha)}\nβ: {self.format_inf(node.beta)}"
            self.canvas.create_text(node.x + 35, node.y, text=ab, font=("Segoe UI", 9),
                                     fill="#ecf0f1", justify=tk.LEFT)
        for child in node.children:
            self.draw_nodes(child)

    @staticmethod
    def format_inf(val):
        return "∞" if val == math.inf else "-∞" if val == -math.inf else str(val)

    def start_search(self):
        if self.is_running:
            return
        self.is_running = True
        for node in self.nodes_dict.values():
            node.state = "unvisited"
            node.alpha, node.beta = -math.inf, math.inf
            node.current_value = -math.inf if node.is_max else math.inf
            node.pruned = False
        self.draw_tree()
        self.generator = self.alpha_beta_gen(self.tree_root, -math.inf, math.inf, True)
        self.step_search()

    def step_search(self):
        if not self.is_running:
            return
        try:
            action, node, *args = next(self.generator)

            for n in self.nodes_dict.values():
                if n.state == "current":
                    n.state = "evaluated" if (n.value is not None or
                                               n.current_value not in (-math.inf, math.inf)) else "unvisited"
            node.state = "current"

            if action == "visit":
                node.alpha, node.beta = args
                self.lbl_status.config(text=f"Visiting {node.name}. Traversing down...")
            elif action == "eval_leaf":
                node.state = "evaluated"
                self.lbl_status.config(text=f"Evaluating leaf {node.name}: Value = {node.value}")
            elif action == "update":
                val, alpha, beta = args
                node.current_value, node.alpha, node.beta = val, alpha, beta
                kind = "MAX" if node.is_max else "MIN"
                self.lbl_status.config(
                    text=f"Updated {kind} {node.name}: Val={val}, α={self.format_inf(alpha)}, β={self.format_inf(beta)}")
            elif action == "prune":
                self.lbl_status.config(
                    text=f"Pruning at {node.name}! β ({self.format_inf(node.beta)}) <= α ({self.format_inf(node.alpha)})")
                for pc in args[0]:
                    self.mark_pruned(pc)
            elif action == "return":
                node.value = args[0]
                node.state = "evaluated"
                self.lbl_status.config(text=f"Returning value {args[0]} from {node.name} upwards.")

            self.draw_tree()
            self.root.after(self.speed_scale.get(), self.step_search)
        except StopIteration:
            self.is_running = False
            self.tree_root.state = "evaluated"
            self.draw_tree()
            self.lbl_status.config(text=f"Search Complete! Optimal Value = {self.tree_root.value}")

    def mark_pruned(self, node):
        node.pruned = True
        node.state = "pruned"
        for child in node.children:
            self.mark_pruned(child)

    def alpha_beta_gen(self, node, alpha, beta, is_max):
        yield ("visit", node, alpha, beta)
        if not node.children:
            yield ("eval_leaf", node)
            return node.value

        value = -math.inf if is_max else math.inf
        for i, child in enumerate(node.children):
            val = yield from self.alpha_beta_gen(child, alpha, beta, not is_max)
            value = max(value, val) if is_max else min(value, val)
            if is_max:
                alpha = max(alpha, value)
            else:
                beta = min(beta, value)
            yield ("update", node, value, alpha, beta)

            if (is_max and value >= beta) or (not is_max and value <= alpha):
                pruned = node.children[i + 1:]
                if pruned:
                    yield ("prune", node, pruned)
                break
        yield ("return", node, value)
        return value

if __name__ == "__main__":
    root = tk.Tk()
    AlphaBetaApp(root)
    root.mainloop()