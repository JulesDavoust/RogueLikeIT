import random
from windowParameters import WindowParameter

def generate_maze(width, height):
    # Initialize the grid with walls
    maze = [['W' for x in range(width)] for y in range(height)]
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]  # 4 directions to move in the maze

    # Start at a random point
    x, y = random.randint(0, width - 1) & ~1, random.randint(0, height - 1) & ~1  # ensure it is odd
    maze[y][x] = 'C'

    # List of available walls
    wall_list = [(x + dx[i], y + dy[i], i) for i in range(4)]

    #Check if deadlock happened
    previous_wall = None
    count = 0

    while wall_list:
        random_wall = random.choice(wall_list)
        if(previous_wall == random_wall):
            count += 1
        else:
            count = 0
        if(count >= 3):
            break

        wx, wy, direction = random_wall
        nx, ny = wx + dx[direction], wy + dy[direction]

        if 0 <= nx < width and 0 <= ny < height:
            if maze[ny][nx] == 'W':
                maze[wy][wx] = maze[ny][nx] = 'C'
                for i in range(4):
                    ax, ay = nx + dx[i], ny + dy[i]
                    if 0 <= ax < width and 0 <= ay < height and maze[ay][ax] == 'W':
                        wall_list.append((nx + dx[i], ny + dy[i], i))

            wall_list.remove(random_wall)
        previous_wall = random_wall
    for row in maze:
        print(' '.join(row))
    return maze


def delete_wall(maze, axis_x, axis_y):
    maze[axis_x][axis_y] = 'C'
    return maze

def detect_walls(maze):
    wall_list = []
    for y in range(0, len(maze)):
        for x in range(0, len(maze[y])):
            #print(maze[y][x])
            if(maze[y][x] == 'W'):
                #print(f"YES: Y:{y} X:{x}")
                wall_list.append([y,x])
    return wall_list

# Display the maze
# maze = generate_maze(WindowParameter.mapTileCol,WindowParameter.mapTileRow)
# wall_list = detect_walls(maze)

