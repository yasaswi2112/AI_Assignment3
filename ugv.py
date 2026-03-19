import heapq
import random
import time

GRID_SIZE = 70

DENSITY_LEVELS = {
    1: ("Low", 0.10),
    2: ("Medium", 0.25),
    3: ("High", 0.40)
}

DIRECTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def generate_grid(size, density):
    grid = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.random() < density:
                grid[i][j] = 1
    return grid

def astar(grid, start, goal):
    start_time = time.time()

    pq = []
    heapq.heappush(pq, (0, start))

    came_from = {}
    g_cost = {start: 0}
    visited = 0

    while pq:
        _, current = heapq.heappop(pq)
        visited += 1

        if current == goal:
            break

        for dx, dy in DIRECTIONS:
            nx, ny = current[0] + dx, current[1] + dy

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] == 1:
                    continue

                new_cost = g_cost[current] + 1

                if (nx, ny) not in g_cost or new_cost < g_cost[(nx, ny)]:
                    g_cost[(nx, ny)] = new_cost
                    f_cost = new_cost + heuristic((nx, ny), goal)
                    heapq.heappush(pq, (f_cost, (nx, ny)))
                    came_from[(nx, ny)] = current

    end_time = time.time()

 
    path = []
    node = goal
    while node in came_from:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()

    return path, visited, end_time - start_time


def print_grid(grid, path, start, goal):
    path_set = set(path)

    for i in range(len(grid)):
        for j in range(len(grid)):
            if (i, j) == start:
                print("S", end=" ")
            elif (i, j) == goal:
                print("G", end=" ")
            elif (i, j) in path_set:
                print("*", end=" ")
            elif grid[i][j] == 1:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()



if __name__ == "__main__":

    print("\nEnter START position:")
    sr = int(input("  Row (0-69): "))
    sc = int(input("  Col (0-69): "))

    print("\nEnter GOAL position:")
    gr = int(input("  Row (0-69): "))
    gc = int(input("  Col (0-69): "))

    print("\nObstacle density:")
    print("  1. Low    (~10 %)")
    print("  2. Medium (~25 %)")
    print("  3. High   (~40 %)")
    choice = int(input("Choose [1-3]: "))

    density_name, density_value = DENSITY_LEVELS[choice]

    print(f"\nPlanning path from ({sr}, {sc}) to ({gr}, {gc}) with {density_name.lower()} obstacle density...")
    print(f"The battlefield environment is represented as a {GRID_SIZE} x {GRID_SIZE} grid map.\n")

    grid = generate_grid(GRID_SIZE, density_value)

    start = (sr, sc)
    goal = (gr, gc)


    grid[sr][sc] = 0
    grid[gr][gc] = 0

    path, visited, time_taken = astar(grid, start, goal)

    print("---")
    print(f"\nPath found  : {len(path)} steps  (cost = {len(path)-1})")
    print(f"Start -> Goal: ({sr}, {sc}) -> ({gr}, {gc})")
    print("\n---")

    show = input("\nDisplay grid (y/n): ").lower()

    if show == 'y':
        print()
        print_grid(grid, path, start, goal)

    print("\n Measures of Effectiveness ")
    print(f"Nodes explored : {visited}")
    print(f"Time taken     : {round(time_taken, 6)} seconds")
