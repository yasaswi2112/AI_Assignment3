import heapq
import random


GRID_SIZE = int(input("Enter grid size (e.g., 20 or 70): "))

print("\nEnter START position:")
sr = int(input(f"Row (0-{GRID_SIZE-1}): "))
sc = int(input(f"Col (0-{GRID_SIZE-1}): "))

print("\nEnter GOAL position:")
gr = int(input(f"Row (0-{GRID_SIZE-1}): "))
gc = int(input(f"Col (0-{GRID_SIZE-1}): "))

start = (sr, sc)
goal = (gr, gc)

print("\nDynamic obstacle density:")
print("1. Low (~1%)")
print("2. Medium (~2%)")
print("3. High (~5%)")
choice = int(input("Choose [1-3]: "))

density_map = {
    1: 0.01,
    2: 0.02,
    3: 0.05
}

probability = density_map.get(choice, 0.02)

DIRECTIONS = [(0,1),(1,0),(0,-1),(-1,0)]



def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    pq = [(0, start)]
    came_from = {}
    g = {start: 0}

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            break

        for dx, dy in DIRECTIONS:
            nx, ny = current[0]+dx, current[1]+dy

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] == 1:
                    continue

                new_cost = g[current] + 1

                if (nx, ny) not in g or new_cost < g[(nx, ny)]:
                    g[(nx, ny)] = new_cost
                    f = new_cost + heuristic((nx, ny), goal)
                    heapq.heappush(pq, (f, (nx, ny)))
                    came_from[(nx, ny)] = current

    path = []
    node = goal
    while node in came_from:
        path.append(node)
        node = came_from[node]

    path.append(start)
    path.reverse()

    return path


def add_dynamic_obstacles(grid, current, goal, probability):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

           
            if (i, j) == current or (i, j) == goal:
                continue

            if random.random() < probability:
                grid[i][j] = 1


def simulate_dynamic(grid, start, goal):
    current = start
    full_path = [current]
    steps = 0

    print("\nPlanning in dynamic environment...\n")

    while current != goal:
        path = astar(grid, current, goal)

        if len(path) <= 1:
            print("❌ No path available!")
            return

        current = path[1]
        full_path.append(current)
        steps += 1

        print(f"Step {steps}: Moving to {current}")

        
        add_dynamic_obstacles(grid, current, goal, probability)

   
        grid[current[0]][current[1]] = 0
        grid[goal[0]][goal[1]] = 0

    print("\n✅ Goal reached!")
    print(f"Total steps: {steps}")
    print("Path:", full_path)




grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]


grid[start[0]][start[1]] = 0
grid[goal[0]][goal[1]] = 0

simulate_dynamic(grid, start, goal)
