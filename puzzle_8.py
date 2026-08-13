import random
import heapq

class Node:
    def __init__(self, state, parent=None, g_n=0):
        self.state = state
        self.parent = parent
        self.g_n = g_n
        self.h_n = 0
        self.f_n = 0
    def __lt__(self, other):
        return self.f_n < other.f_n


class AStarSearch:
    def __init__(self, start_state, goal_state):
        self.goal_state = goal_state
        self.start = Node(start_state)
        self.goal_pos = self.calculate_goal_positions()

    def get_neighbors(self, tile):
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for di, dj in directions:
            new_i = tile[0] + di
            new_j = tile[1] + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3: neighbors.append((new_i, new_j))
        return neighbors
    
    def get_next_possible_states(self, node: Node):
        state = node.state
        next_nodes, blank= [], None
        for i in range(3):
            for j in range(3):
                if state[i][j] is None:
                    blank = (i, j)
                    break
            if blank:
                break
        for new_i, new_j in self.get_neighbors(blank):
            new_state = [row[:] for row in state]
            new_state[blank[0]][blank[1]], new_state[new_i][new_j] = (new_state[new_i][new_j], new_state[blank[0]][blank[1]])
            child = Node(state=new_state, parent=node, g_n=node.g_n + 1)
            child.h_n, child.f_n = self.calculate_heuristic(child.state), child.g_n + child.h_n
            next_nodes.append(child)
        return next_nodes

    def calculate_heuristic(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value is None:
                    continue
                goal_x, goal_y = self.goal_pos[value]
                distance += abs(i - goal_x) + abs(j - goal_y)
        return distance
    
    def is_goal(self, state):
        return state == self.goal_state
    
    def state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)
    
    def reconstruct_path(self, node):
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path
    
    def solve(self):
        self.start.g_n = 0
        self.start.h_n = self.calculate_heuristic(self.start.state)
        self.start.f_n = self.start.g_n + self.start.h_n
        open_list = []
        closed_set = set()
        heapq.heappush(open_list, self.start)
        while open_list:
            current = heapq.heappop(open_list)
            if self.is_goal(current.state):
                return self.reconstruct_path(current)
            closed_set.add(self.state_to_tuple(current.state))
            children = self.get_next_possible_states(current)
            for child in children:
                state_key = self.state_to_tuple(child.state)
                if state_key in closed_set:
                    continue
                child.g_n = current.g_n + 1
                child.h_n = self.calculate_heuristic(child.state)
                child.f_n = child.g_n + child.h_n
                heapq.heappush(open_list, child)
        return None

    def calculate_goal_positions(self):
        goal_pos = {}
        for i in range(len(self.goal_state)):
            for j in range(len(self.goal_state[0])):
                value = self.goal_state[i][j]
                if value is not None:
                    goal_pos[value] = (i, j)
        return goal_pos

    def print_board(self, state):
        print("------------")
        for row in state:
            print("|", end="")
            for value in row: print(f" {value if value is not None else ' '} |", end="")
            print()
            print("------------")

def create_board():
    state = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
    nums = [1, 2, 3, 4, 5, 6, 7, 8, None]
    for i in range(3):
        for j in range(3):
            num = random.choice(nums)
            nums.pop(nums.index(num))
            state[i][j] = num
    return state

goal_state = [
    [1, 2, 3],
    [8, None, 4],
    [7, 6, 5]
]

search = AStarSearch(create_board(), goal_state)
print("Initial board:")
search.print_board(search.start.state)
solution = search.solve()
if solution is None:
    print("No solution found.")

else:
    print(f"Solved in {len(solution)-1} moves.")
    for state in solution:
        search.print_board(state)
