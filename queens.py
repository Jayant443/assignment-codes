import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
N = 8
def is_safe(board, row, col):
    for c in range(col):
        r = board[c]
        if r == row or abs(r - row) == abs(c - col): return False
    return True
def backtrack(board, col, stats):
    if col == N: return True
    for row in range(N):
        if is_safe(board, row, col):
            board[col] = row
            if backtrack(board, col + 1, stats): return True
            board[col] = -1
            stats[0] += 1
    return False
def solve_one():
    board = [-1] * N
    stats = [0]
    result = board if backtrack(board, 0, stats) else None
    return result, stats[0]
def backtrack_all(board, col, solutions):
    if col == N:
        solutions.append(board.copy())
        return
    for row in range(N):
        if is_safe(board, row, col):
            board[col] = row
            backtrack_all(board, col + 1, solutions)
            board[col] = -1
def solve_all():
    solutions = []
    backtrack_all([-1] * N, 0, solutions)
    return solutions
def draw_board(ax, board, n=N):
    light, dark = "#F0D9B5", "#B58863"
    for row in range(n):
        for col in range(n):
            color = light if (row + col) % 2 == 0 else dark
            ax.add_patch(plt.Rectangle((col, n - 1 - row), 1, 1, facecolor=color, edgecolor="none"))
    for col, row in enumerate(board):
        ax.text(col + 0.5, n - 1 - row + 0.5, "♛", ha="center", va="center", fontsize=30, color="#1a1a1a",
                path_effects=[path_effects.withStroke(linewidth=3, foreground="white")])
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect("equal")
    ax.set_xticks([i + 0.5 for i in range(n)])
    ax.set_yticks([i + 0.5 for i in range(n)])
    ax.set_xticklabels([chr(ord("a") + i) for i in range(n)])
    ax.set_yticklabels([str(n - i) for i in range(n)])
    ax.tick_params(length=0, pad=5)
    for spine in ax.spines.values():
        spine.set_edgecolor("#5A3E1B")
        spine.set_linewidth(2)
    ax.set_title(f"8-Queens Solution  •  {board}", fontsize=12, fontweight="bold", pad=12)
def save_solution_image(board, total, backtracks, save_path="queens_solution.png"):
    import os
    fig = plt.figure(figsize=(11, 6.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1.7], wspace=0.08)
    ax_board = fig.add_subplot(gs[0, 0])
    ax_info = fig.add_subplot(gs[0, 1])
    draw_board(ax_board, board)
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.axis("off")
    ax_info.add_patch(plt.Rectangle((0.02, 0.02), 0.96, 0.96, facecolor="#FAF7F0", edgecolor="#5A3E1B", linewidth=2))
    queens = ", ".join(f"{chr(ord('a') + c)}{N - r}" for c, r in enumerate(board))
    details = [
        ("8-Queens CSP", 16, True), ("Backtracking search", 11, False), (f"One solution of {total}", 12, True), ("board[col] = row:", 10, True),
        (str(board), 10, False), ("Queen positions:", 10, True), (queens, 9, False), (f"Total solutions: {total}", 11, False),
        (f"Backtracks: {backtracks}", 11, False), ("Queens placed: 8 / 8", 11, False), ("Constraints:", 10, True), ("No shared row, column, or diagonal", 9, False),
    ]
    y = 0.94
    for text, size, bold in details:
        ax_info.text(0.10, y, text, fontsize=size, fontweight="bold" if bold else "normal", style="italic" if text == "Backtracking search" else "normal",
                     va="top", ha="left", color="#3B2A17" if bold else "#333333", wrap=True)
        y -= 0.085 if size >= 12 else 0.075
    fig.suptitle("8-Queens • CSP + Backtracking", fontsize=14, fontweight="bold")
    fig.subplots_adjust(left=0.05, right=0.95, top=0.88, bottom=0.05, wspace=0.15)
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
def main():
    solution, backtracks = solve_one()
    solutions = solve_all()
    print(f"Backtracks: {backtracks}")
    save_solution_image(solution, len(solutions), backtracks)
if __name__ == "__main__":
    main()
