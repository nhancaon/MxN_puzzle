from collections import deque
from queue import PriorityQueue
from queue import LifoQueue
from settings import *

def manhattan_distance(state):
    # Calculate the Manhattan distance heuristic for a given state
    distance = 0
    for i in range(GAME_SIZE_Y):
        for j in range(GAME_SIZE_X):
            if state[i][j] != 0:
                target_row = (state[i][j] - 1) // GAME_SIZE_Y
                target_col = (state[i][j] - 1) % GAME_SIZE_X
                distance += abs(i - target_row) + abs(j - target_col)
    return distance


def generate_successors(current_state):
    successors = []
    empty_row, empty_col = None, None
    # Find the position of the empty tile (0)
    for i in range(GAME_SIZE_Y):
        for j in range(GAME_SIZE_X):
            if current_state[i][j] == 0:
                empty_row, empty_col = i, j

    # Define possible moves (up, down, left, right)
    moves = [
        (-1, 0, "D"),
        (1, 0, "U"),
        (0, -1, "R"),
        (0, 1, "L")
    ]

    for dr, dc, move_direction in moves:
        new_row, new_col = empty_row + dr, empty_col + dc

        if 0 <= new_row < GAME_SIZE_Y and 0 <= new_col < GAME_SIZE_X:
            new_state = [list(row) for row in current_state]
            new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_row][empty_col]
            successors.append((new_state, move_direction))

    return successors


def bfs(initial_state, goal_state,searched_state_bfs):
    queue = deque([(initial_state, [])])
    explored = set()
    while queue:
        current_state, path = queue.popleft()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            searched_state_bfs[0] += 1
            if tuple(map(tuple, next_state)) not in explored:
                queue.append((next_state, path + [move_direction]))

    return None  # No solution found


def ucs(initial_state, goal_state, searched_state_ucs):
    open_set = PriorityQueue()
    open_set.put((0, initial_state, []))
    explored = set()

    while not open_set.empty():
        _, current_state, path = open_set.get()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            searched_state_ucs[0] += 1
            if tuple(map(tuple, next_state)) not in explored:
                priority = len(path)
                open_set.put(
                    (priority, next_state, path + [move_direction]))

    return None  # No solution found


def dfs(initial_state, goal_state, searched_state_dfs):
    stack = [(initial_state, [])]
    explored = set()

    while stack:
        current_state, path = stack.pop()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))
        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            searched_state_dfs[0] += 1
            if tuple(map(tuple, next_state)) not in explored:
                stack.append((next_state, path + [move_direction]))

    return None

def ids(initial_state, goal_state, searched_state_ids,max_depth=50):
    stack = [(initial_state, [])]
    explored = set()

    while stack:
        current_state, path = stack.pop()
        depth = len(path)

        if depth > max_depth:
            continue

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))
        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            searched_state_ids[0] += 1
            if tuple(map(tuple, next_state)) not in explored:
                stack.append((next_state, path + [move_direction]))

    return None

def greedy(initial_state, goal_state, searched_state_greedy):
    open_set = PriorityQueue()
    open_set.put((0, initial_state, []))
    explored = set()

    while not open_set.empty():
        _, current_state, path = open_set.get()

        if current_state == goal_state:
            return path

        explored.add(tuple(map(tuple, current_state)))

        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            searched_state_greedy[0] += 1
            if tuple(map(tuple, next_state)) not in explored:
                priority = manhattan_distance(next_state)
                open_set.put(
                    (priority, next_state, path + [move_direction]))

    return None  # No solution found


def a_star(initial_state, goal_state,searched_state_astar):
    open_set = PriorityQueue()
    open_set.put((0, initial_state, []))
    explored = set()
    while not open_set.empty():
        _, current_state, path = open_set.get()
        if current_state == goal_state:
            return path
        explored.add(tuple(map(tuple, current_state)))
        successors = generate_successors(current_state)

        for next_state, move_direction in successors:
            searched_state_astar[0] += 1
            if tuple(map(tuple, next_state)) not in explored:
                priority = len(path) + manhattan_distance(next_state)
                open_set.put((priority, next_state, path + [move_direction]))

    return None  # No solution found

def hill_climbing(initial_state, goal_state, searched_state_hill):
    path_explored = set()
    
    while 1==1:
        stack = [(initial_state, [])]
        explored = set()
        current_cnt_misplaced = float('inf')
        cnt = 0
        while 1==1 :
            current_state, path = stack.pop()

            if current_state == goal_state:
                return path

            explored.add(tuple(map(tuple, current_state)))
            
            if cnt==1 and len(explored) == 0:
                return None
            
            successors = generate_successors(current_state)

            best_state = None
            best_cnt_misplaced = float('inf')
            best_move = None
            
            for next_state, move_direction in successors:
                searched_state_hill[0] += 1
                if tuple(map(tuple, next_state)) not in explored:
                    if tuple(map(tuple, next_state)) not in path_explored:
                        new_cnt_misplaced = manhattan_distance(next_state)
                        if new_cnt_misplaced < best_cnt_misplaced:
                            best_state = next_state
                            best_cnt_misplaced = new_cnt_misplaced
                            best_move = move_direction
            if best_cnt_misplaced < current_cnt_misplaced:
                current_cnt_misplaced = best_cnt_misplaced
            if best_state is not None:
                stack.append((best_state, path + [best_move]))
                cnt = cnt+1
            else :
                break
    return None