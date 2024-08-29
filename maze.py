import random
from Image import wall_image
from config import TOP_INFO_HEIGHT,TILE_SIZE

def generate_maze(width, height):
    assert width % 2 == 1 and height % 2 == 1, "宽度和高度必须为奇数。"

    # 初始化迷宫，全为墙
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # 设置中心3x3区域
    center_x, center_y = width // 2, height // 2
    for y in range(center_y - 1, center_y + 2):
        for x in range(center_x - 1, center_x + 2):
            maze[y][x] = 1
    maze[center_y][center_x] = 0  # 中心设为路

    # 设置3x3区域外一圈为路径
    for y in range(center_y - 2, center_y + 3):
        for x in range(center_x - 2, center_x + 3):
            if (x < center_x - 1 or x > center_x + 1 or y < center_y - 1 or y > center_y + 1):
                maze[y][x] = 0

    def carve_passages(x, y):
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
                if not (center_x - 2 <= nx <= center_x + 2 and center_y - 2 <= ny <= center_y + 2):  # 避免中心区域及其外围
                    maze[ny - dy // 2][nx - dx // 2] = 0
                    maze[ny][nx] = 0
                    carve_passages(nx, ny)

    # 从随机点开始雕刻路径，但不能是中心区域或其外围
    start_x, start_y = random.randrange(1, width - 1, 2), random.randrange(1, height - 1, 2)
    while center_x - 2 <= start_x <= center_x + 2 and center_y - 2 <= start_y <= center_y + 2:
        start_x, start_y = random.randrange(1, width - 1, 2), random.randrange(1, height - 1, 2)

    maze[start_y][start_x] = 0
    carve_passages(start_x, start_y)

    # 连通死路，而不是删除死路
    def connect_dead_ends():
        dead_ends = True
        while dead_ends:
            dead_ends = False
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    if maze[y][x] == 0:
                        exits = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if
                                 maze[y + dy][x + dx] == 0]
                        if len(exits) == 1:  # 找到死路
                            dead_ends = True
                            neighbors = [(x + dx * 2, y + dy * 2) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if
                                         0 <= x + dx * 2 < width and 0 <= y + dy * 2 < height and maze[y + dy * 2][
                                             x + dx * 2] == 0]
                            if neighbors:
                                # 连接到一个随机的邻居
                                nx, ny = random.choice(neighbors)
                                maze[(y + ny) // 2][(x + nx) // 2] = 0

    # 连接死路直到所有死路都被连接
    connect_dead_ends()
    # 确定inuji位置
    hostage_position = (center_x * TILE_SIZE, center_y * TILE_SIZE + TOP_INFO_HEIGHT)

    return maze, hostage_position

def draw_maze(screen, maze, tile_size, top_left_x, top_left_y):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                screen.blit(wall_image, (top_left_x + col * tile_size, top_left_y + row * tile_size))

def find_food_positions(maze, tile_size):
    return [(col * tile_size + tile_size // 2, row * tile_size + tile_size // 2 + TOP_INFO_HEIGHT)
            for row in range(len(maze))
            for col in range(len(maze[0]))
            if maze[row][col] == 0]