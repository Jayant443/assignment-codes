from collections import deque
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
DIRECTIONS = [(1, 0, "DOWN"), (0, 1, "RIGHT"), (-1, 0, "UP"), (0, -1, "LEFT")]
def pos(prompt, R, C): 
    while True:
        try:
            r, c = map(int, input(prompt).split())
            if 0 <= r < R and 0 <= c < C:return (r, c)
        except ValueError:pass
        print("  Enter a valid position: row column")
def show(maze):
    C = len(maze[0])
    print("      " + "".join(f"{c:^3}" for c in range(C)))
    print("     " + "-" * (C * 3 + 1))
    for r, row in enumerate(maze):print(f"  {r:2d} |" + "".join(f" {ch} " for ch in row))
    print()
def neighbours(maze, cell):
    R, C = len(maze), len(maze[0])
    r, c = cell
    for dr, dc, name in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] != "#": yield (nr, nc), name
def build_path(parent, goal):
    path, node = [], goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]
def dfs(maze, start, goal):
    stack = [(start, None, "START")]
    parent, moves, explored = {}, {}, []
    discovered = {start}
    while stack:
        cur, par, move = stack.pop()
        if cur in parent:continue
        parent[cur], moves[cur] = par, move
        explored.append(cur)
        if cur == goal:return build_path(parent, goal), explored, moves, discovered, parent
        for nxt, name in reversed(list(neighbours(maze, cur))):
            if nxt not in parent:
                discovered.add(nxt)
                stack.append((nxt, cur, name))
    return None, explored, moves, discovered, parent
def bfs(maze, start, goal):
    queue, parent = deque([start]), {start: None}
    explored = []
    while queue:
        cur = queue.popleft()
        explored.append(cur)
        if cur == goal:return build_path(parent, goal), explored, set(parent)
        for nxt, _ in neighbours(maze, cur):
            if nxt not in parent:
                parent[nxt] = cur
                queue.append(nxt)
    return None, explored, set(parent)
COLORS = {"open": "#FFFFFF", "wall": "#4B4D4E", "explored": "#FFE8CC","start": "#2A9D41", "goal": "#E63946", "path": "#6A4C93"}
def draw_panel(ax, maze, start, goal, explored, path, title):
    R, C = len(maze), len(maze[0])
    for r in range(R):
        for c in range(C):
            state, color = (r, c), COLORS["open"]
            if maze[r][c] == "#":color = COLORS["wall"]
            elif state in explored:color = COLORS["explored"]
            if state == start:color = COLORS["start"]
            if state == goal:color = COLORS["goal"]
            ax.add_patch(Rectangle((c, R - r - 1), 1, 1, facecolor=color, edgecolor="#9AA5AD", linewidth=.8))
    on_path = set(path or [])
    for i, (r, c) in enumerate(explored, 1):
        if (r, c) not in on_path:ax.text(c + .5, R - r - .5, str(i), ha="center", va="center",fontsize=9, color="#8A6D3B")
    if path:
        ax.plot([c + .5 for r, c in path], [R - r - .5 for r, c in path],color=COLORS["path"], linewidth=4, alpha=.9, zorder=2)
        for step, (r, c) in enumerate(path):
            if (r, c) not in (start, goal):
                ax.text(c + .5, R - r - .5, str(step), ha="center", va="center", fontsize=9, fontweight="bold", color="white", zorder=5,
                        bbox=dict(boxstyle="circle,pad=0.25", fc=COLORS["path"], ec="white", lw=1))
    for state, label in [(start, "S"), (goal, "G")]:
        ax.text(state[1] + .5, R - state[0] - .5, label, ha="center", va="center",fontsize=18, fontweight="bold", color="white", zorder=6)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xlim(0, C)
    ax.set_ylim(0, R)
    ax.set_aspect("equal")
    ax.axis("off")
def visualize(maze, start, goal, explored, path, save_as=None):
    fig, ax = plt.subplots(figsize=(8, 7.4))
    draw_panel(ax, maze, start, goal, explored, path,"DFS FOR MAZE SOLVING" f"Path cost = {len(path) - 1}   |   States explored = {len(explored)}")
    ax.legend(handles=[Patch(color=COLORS["start"], label="Initial State (S)"), Patch(color=COLORS["goal"], label="Goal State (G)"),
                       Patch(color=COLORS["wall"], label="Wall (#)"), Patch(color=COLORS["explored"], label="Explored (number = visit order)"),
                       Patch(color=COLORS["path"], label="DFS path (number = step)")], loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=3, frameon=True)
    plt.tight_layout()
    if save_as:plt.savefig(save_as, dpi=130)
    else:plt.show()
print("STEP 1 : ENTER MAZE SIZE")
R = int(input("Enter number of rows    : "))
C = int(input("Enter number of columns : "))
print("STEP 2 : ENTER INITIAL STATE")
start = pos("Initial State (row column): ", R, C)
print("STEP 3 : ENTER GOAL / FINAL STATE")
while True:
    goal = pos("Goal State (row column)   : ", R, C)
    if goal != start:break
    print("Goal cannot equal Initial State.")
maze = [["." for _ in range(C)] for _ in range(R)]
print("STEP 4 : ENTER MAZE WALLS")
print("Enter positions as row column. Type 'done' when finished.")
while True:
    value = input("Wall position (or 'done'): ").strip()
    if value.lower() == "done":break
    try:
        r, c = map(int, value.split())
        if 0 <= r < R and 0 <= c < C:
            if (r, c) not in (start, goal):
                maze[r][c] = "#"
                print(f"  Wall added at ({r}, {c})")
            else:print("  Initial/Goal state cannot be a wall.")
        else:print("  Position is outside the maze.")
    except ValueError:print("  Enter position as: row column")
maze[start[0]][start[1]] = "S"
maze[goal[0]][goal[1]] = "G"
print("STEP 5 : USER-DEFINED INITIAL MAZE")
show(maze)
print("STEP 6 : EXECUTING DEPTH-FIRST SEARCH...")
path, explored, moves, discovered, parent = dfs(maze, start, goal)
for i, state in enumerate(explored, 1):
    note = ""
    if i > 1 and parent[state] != explored[i - 2]:note = f"   <- backtracked to {parent[state]}"
    print(f"  State {i:02d}    Current State : {state}{note}")
print("DFS RESULT")
if path:
    print("  STATUS               : SOLUTION FOUND")
    print(f"  Initial State        : {start}")
    print(f"  Goal State           : {goal}")
    print(f"  States Explored      : {len(explored)}")
    print(f"  Discovered States    : {len(discovered)}")
    print(f"  Dead-End States      : {len(explored) - len(path)}")
    print(f"  Path States          : {len(path)}")
    print(f"  Path Cost            : {len(path) - 1}")
    print("FINAL DFS PATH")
    for i, state in enumerate(path):print(f"  Step {i:02d}    State : {state}    Move : {moves[state]}")
    result = [row[:] for row in maze]
    for r, c in path:
        if result[r][c] not in ("S", "G"): result[r][c] = "*"
    print("SOLUTION MAZE")
    show(result)
    print("  S = Initial State")
    print("  G = Goal State")
    print("  # = Wall")
    print("  * = DFS Solution Path")
    b_path, b_explored, b_found = bfs(maze, start, goal)
    print("DFS vs BFS COMPARISON")
    print(f"  {'Metric':<22}{'DFS':>10}{'BFS':>10}")
    print(f"  {'Path Cost (moves)':<22}{len(path) - 1:>10}{len(b_path) - 1:>10}")
    print(f"  {'States Explored':<22}{len(explored):>10}{len(b_explored):>10}")
    print(f"  {'Discovered States':<22}{len(discovered):>10}{len(b_found):>10}")
    diff = len(path) - len(b_path)
    print("  " + ("DFS found a shortest path." if diff == 0 else f"DFS path is {diff} move(s) longer than the shortest path (BFS)."))
else:
    print("  STATUS               : NO SOLUTION FOUND")
    print(f"  Initial State        : {start}")
    print(f"  Goal State           : {goal}")
    print(f"  States Explored      : {len(explored)}")
print("GENERATING DFS VISUALIZATION")
if path:visualize(maze, start, goal, explored, path)
else:print("  No path to draw.")
