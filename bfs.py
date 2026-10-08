import heapq
import time
from collections import deque
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVES = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
OPPOSITE = {"UP": "down", "DOWN": "up", "LEFT": "right", "RIGHT": "left"}
def is_solvable(state):
    tiles = [t for t in state if t != 0]
    inversions = sum(a > b for i, a in enumerate(tiles) for b in tiles[i + 1:])
    return inversions % 2 == 0
def get_successors(state):
    blank = state.index(0)
    row, col = divmod(blank, 3)
    for move, (dr, dc) in MOVES.items():
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            target = r * 3 + c
            new = list(state)
            new[blank], new[target] = new[target], new[blank]
            yield move, tuple(new)
def bfs(start, goal=GOAL):
    stats = {"expanded": 0, "generated": 1, "max_frontier": 1, "per_depth": {}, "time": 0.0}
    t0 = time.perf_counter()
    parent = {start: (None, None, 0)}
    frontier = deque([start])
    found = start if start == goal else None
    while frontier and found is None:
        state = frontier.popleft()                       
        depth = parent[state][2]
        stats["expanded"] += 1
        stats["per_depth"][depth] = stats["per_depth"].get(depth, 0) + 1
        for move, nxt in get_successors(state):
            if nxt in parent:continue
            parent[nxt] = (state, move, depth + 1)
            stats["generated"] += 1
            if nxt == goal:                              
                found = nxt
                break
            frontier.append(nxt)
        stats["max_frontier"] = max(stats["max_frontier"], len(frontier))
    stats["time"] = time.perf_counter() - t0
    if found is None:return None, stats
    return rebuild(parent, found), stats
def manhattan(state, goal=GOAL):
    total = 0
    for idx, tile in enumerate(state):
        if tile:
            g = goal.index(tile)
            total += abs(idx // 3 - g // 3) + abs(idx % 3 - g % 3)
    return total
def rebuild(parent, found):
    path, state = [], found
    while state is not None:
        prev, move, _ = parent[state]
        path.append((move, state))
        state = prev
    return path[::-1]
def astar(start, goal=GOAL):
    stats = {"expanded": 0, "generated": 1, "max_frontier": 1, "per_depth": {}, "time": 0.0}
    t0 = time.perf_counter()
    parent = {start: (None, None, 0)}
    best_g = {start: 0}
    tie = 0                                              
    frontier = [(manhattan(start), 0, tie, start)]       
    found = None
    while frontier:
        f, g, _, state = heapq.heappop(frontier)         
        if g > best_g[state]:continue
        if state == goal:                                
            found = state
            break
        stats["expanded"] += 1
        stats["per_depth"][g] = stats["per_depth"].get(g, 0) + 1
        for move, nxt in get_successors(state):
            ng = g + 1
            if ng < best_g.get(nxt, float("inf")):
                best_g[nxt] = ng
                parent[nxt] = (state, move, ng)
                stats["generated"] += 1
                tie += 1
                heapq.heappush(frontier, (ng + manhattan(nxt), ng, tie, nxt))
        stats["max_frontier"] = max(stats["max_frontier"], len(frontier))
    stats["time"] = time.perf_counter() - t0
    return (rebuild(parent, found) if found else None), stats
def print_board(state, indent="    "):
    print(indent + "_____________")
    for i in range(3):
        cells = " | ".join(str(t) if t else " " for t in state[3 * i:3 * i + 3])
        print(indent + f"| {cells} |")
        if i < 2: print(indent + "|---|---|---|")
    print(indent + "|___|___|___|")
def print_solution(path):
    print("SOLUTION STEP BY STEP")
    print("Step 0: Initial state")
    print_board(path[0][1])
    for step, (move, state) in enumerate(path[1:], start=1):
        moved = path[step - 1][1][state.index(0)]        
        print(f"Step {step}: Slide tile {moved} {OPPOSITE[move]}" f"  (blank moves {move.lower()})")
        print_board(state)
    print("Goal reached!")
def print_stats(name, path, stats):
    print(f"SEARCH SUMMARY ({name})")
    print(f"Solution length (moves) : {len(path) - 1}")
    print(f"Nodes expanded          : {stats['expanded']}")
    print(f"Nodes generated         : {stats['generated']}")
    print(f"Max frontier size       : {stats['max_frontier']}")
    print(f"Time taken              : {stats['time']:.4f} s")
    print("Nodes expanded per depth level")
    for d, n in sorted(stats["per_depth"].items()):print(f"  depth {d:>2} | {n:>6} {'#' * max(1, n * 30 // max(stats['per_depth'].values()))}")
def print_comparison(path_b, st_b, path_a, st_a):
    rows = [("Solution length (moves)", len(path_b) - 1, len(path_a) - 1),
            ("Nodes expanded", st_b["expanded"], st_a["expanded"]),
            ("Nodes generated", st_b["generated"], st_a["generated"]),
            ("Max frontier size", st_b["max_frontier"], st_a["max_frontier"]),
            ("Time taken (s)", f"{st_b['time']:.4f}", f"{st_a['time']:.4f}")]
    print("COMPARISON: BFS vs A*")
    print(f"{'Metric':<26}{'BFS':>14}{'A*':>14}")
    print("-" * 56)
    for name, b, a in rows: print(f"{name:<26}{b:>14}{a:>14}")
    print("-" * 56)
    saved = 100 * (1 - st_a["expanded"] / st_b["expanded"])
    print(f"A* expanded {saved:.1f}% fewer nodes than BFS.")
def solve(start):
    print("INITIAL STATE")
    print_board(start)
    print("GOAL STATE")
    print_board(GOAL)
    if not is_solvable(start):
        print("This configuration is NOT solvable (odd number of inversions).")
        return
    path_b, st_b = bfs(start)
    path_a, st_a = astar(start)
    print_solution(path_b)                               
    print_stats("BFS", path_b, st_b)
    print_stats("A*", path_a, st_a)
    print_comparison(path_b, st_b, path_a, st_a)
def benchmark(cases):
    print("BENCHMARK ON HARDER PUZZLES")
    print(f"{'Start state':<30}{'Moves':>6} | {'BFS exp.':>9}{'A* exp.':>9} |" f" {'BFS s':>8}{'A* s':>8}")
    print("-" * 78)
    for start in cases:
        pb, sb = bfs(start)
        pa, sa = astar(start)
        assert len(pb) == len(pa)                        
        print(f"{str(start):<30}{len(pb) - 1:>6} | {sb['expanded']:>9}{sa['expanded']:>9} |" f" {sb['time']:>8.3f}{sa['time']:>8.3f}")
if __name__ == "__main__":
    start = (1, 2, 3, 0, 4, 6, 7, 5, 8)
    solve(start)
    benchmark([(1, 2, 3, 0, 4, 6, 7, 5, 8), (8, 1, 3, 4, 0, 2, 7, 6, 5), (8, 6, 7, 2, 5, 4, 3, 0, 1)])           
