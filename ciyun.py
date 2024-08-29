import pygame
import random
import collections
from config import WIDTH, HEIGHT, MAZE_WIDTH, MAZE_HEIGHT, TILE_SIZE, TOP_INFO_HEIGHT, WHITE, BLACK
from Image import food_image,monster_image,life_image_empty,life_image_full,game_pacman_images,select_pacman_images
from maze import generate_maze, draw_maze, find_food_positions

# 初始化 Pygame
pygame.init()

# 初始化游戏
max_lives = 3  # 定义玩家的最大生命值
lives = max_lives  # 初始化生命值为最大生命值
selected_pacman = None  # 当前选择的吃豆人（暂时未选）
game_pacman = None  # 当前游戏中使用的吃豆人图像
pacman_rect = None  # 吃豆人的矩形区域
running = True  # 游戏主循环运行状态
choosing = True  # 是否处于选择吃豆人界面
game_over = False  # 是否游戏结束
clock = pygame.time.Clock()  # 用于控制帧率的时钟对象
life_images = [life_image_full] * max_lives
# 定义屏幕大小和颜色
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("兔几吃豆子")



# 初始化游戏状态
def reset_game():
    global score, lives, maze, food_positions, pacman_rect, monster_rect, current_direction
    score = 0 #分数重置
    lives = max_lives  # 重新设置最大生命值
    update_life_images()
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT) # 生成迷宫
    food_positions = find_food_positions(maze, TILE_SIZE) # 计算路径的位置
    pacman_rect = game_pacman.get_rect(center=random.choice(food_positions)) # 生成玩家
    monster_rect = monster_image.get_rect(center=random.choice(food_positions)) # 生成怪物
    current_direction = (0, 0) # 初始方向


def draw_text(text, position, size=36, color=WHITE):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)
    return text_rect  # 返回文本的矩形边界

# 使用广度优先搜索 (BFS) 来寻找从怪物到玩家的最短路径
def bfs_find_path(maze, start, goal):
    queue = collections.deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        x, y = current
        for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            next_x, next_y = x + direction[0], y + direction[1]
            next_pos = (next_x, next_y)

            if 0 <= next_x < MAZE_WIDTH and 0 <= next_y < MAZE_HEIGHT:
                if maze[next_y][next_x] == 0 and next_pos not in came_from:
                    queue.append(next_pos)
                    came_from[next_pos] = current

    # 追溯路径
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path[1:]  # 返回从起始点到目标的路径，不包括起始点本身

# 怪物的移动逻辑
def move_monster():
    global monster_rect
    pacman_pos = (pacman_rect.centerx // TILE_SIZE, (pacman_rect.centery - TOP_INFO_HEIGHT) // TILE_SIZE)
    monster_pos = (monster_rect.centerx // TILE_SIZE, (monster_rect.centery - TOP_INFO_HEIGHT) // TILE_SIZE)

    # 查找怪物到玩家的路径
    path = bfs_find_path(maze, monster_pos, pacman_pos)
    if path:  # 如果找到路径，按照路径移动怪物
        next_pos = path[0]
        target_x = next_pos[0] * TILE_SIZE + TILE_SIZE // 2
        target_y = next_pos[1] * TILE_SIZE + TILE_SIZE // 2 + TOP_INFO_HEIGHT  # 添加顶部信息区域的高度

        # 确保怪物不会移动到屏幕范围之外
        screen_rect = screen.get_rect()
        monster_rect.centerx = max(TILE_SIZE // 2, min(screen_rect.width - TILE_SIZE // 2, target_x))
        monster_rect.centery = max(60 + TILE_SIZE // 2, min(screen_rect.height - TILE_SIZE // 2, target_y))

# 移动玩家
def move_player():
    global pacman_rect

    # 计算目标位置
    target_x = pacman_rect.x + current_direction[0] * TILE_SIZE
    target_y = pacman_rect.y + current_direction[1] * TILE_SIZE

    # 计算目标位置在迷宫中的坐标
    maze_x = target_x // TILE_SIZE
    maze_y = (target_y - TOP_INFO_HEIGHT) // TILE_SIZE  # 减去顶部信息区域的高度

    # 确保目标位置在迷宫的范围内
    if 0 <= maze_x < MAZE_WIDTH and 0 <= maze_y < MAZE_HEIGHT:
        # 检查目标位置是否在迷宫路径上
        if maze[maze_y][maze_x] == 0:
            pacman_rect.x = target_x
            pacman_rect.y = target_y

    # 确保玩家不会移动到屏幕范围之外
    screen_rect = screen.get_rect()
    pacman_rect.left = max(0, pacman_rect.left)
    pacman_rect.right = min(screen_rect.width, pacman_rect.right)
    pacman_rect.top = max(60, pacman_rect.top)  # 顶部信息区域的高度
    pacman_rect.bottom = min(screen_rect.height, pacman_rect.bottom)
# 更新积分和生命
def update_game_state():
    global lives, game_over
    if pacman_rect.colliderect(monster_rect):
        lives -= 1
        update_life_images()  # 更新生命值图片并绘制
        reset_monster_position()
        if lives <= 0:
            game_over = True

    if not game_over:
        for pos in food_positions[:]:
            if pacman_rect.collidepoint(pos):
                food_positions.remove(pos)
                global score
                score += 10

# 重置怪物位置
def reset_monster_position():
    global monster_rect
    monster_rect.center = random.choice(food_positions)


#选择处理逻辑
def handle_pacman_selection(mouse_pos):
    global game_pacman, pacman_rect, choosing
    for i, rect in enumerate(pacman_rects):
        if rect.collidepoint(mouse_pos):
            game_pacman = game_pacman_images[i]
            choosing = False
            reset_game()


# 游戏结束处理逻辑
def handle_game_over(mouse_pos):
    global choosing, game_over, running
    restart_rect, quit_rect = show_game_over_screen()
    if restart_rect.collidepoint(mouse_pos):
        choosing = True
        game_over = False
    elif quit_rect.collidepoint(mouse_pos):
        running = False

# 绘制游戏内容
def draw_gameplay():

    # 绘制顶部信息
    draw_info()
    draw_life()

    # 绘制迷宫
    draw_maze(screen, maze, TILE_SIZE, 0, TOP_INFO_HEIGHT)  # 注意偏移量

    # 绘制食物
    draw_food()

    # 绘制角色
    screen.blit(monster_image, monster_rect)
    screen.blit(game_pacman, pacman_rect)

def draw_info():
    # 画顶部信息区域背景
    # pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 60))  # 背景区域

    # 绘制分数和生命信息
    draw_text(f"Score: {score}", (100, 30))
    draw_text("Lives:", (WIDTH - 200, 30))

def draw_life():
    # 计算生命值图标的起始 x 坐标，确保其与 "Lives:" 标签对齐
    start_x = WIDTH - 60  # 生命值图标的起始 x 坐标
    start_y = 20  # 生命值图标的起始 y 坐标

    # 绘制初始生命值图标
    for i in range(max_lives):
        screen.blit(life_images[i], (start_x - i * 30, start_y))



# 更新生命值图片列表
def update_life_images():
    global life_images
    life_images =  lives * [life_image_full] + (max_lives-lives) * [life_image_empty]


def draw_food():
    for pos in food_positions:
        # 计算食物的位置，考虑到顶部信息区域的偏移量
        screen.blit(food_image, (pos[0] - food_image.get_width() // 2, pos[1] - food_image.get_height() // 2))



# 选择界面文本绘制
def show_pacman_selection():
    draw_text("Choose your usaji", (WIDTH // 2, 100))
    for i, rect in enumerate(pacman_rects):
        screen.blit(select_pacman_images[i], rect)


# 结束界面文本绘制
def show_game_over_screen():
    draw_text("GAME OVER", (WIDTH // 2, HEIGHT // 2 - 50))
    restart_rect = draw_text("RESTART", (WIDTH // 2 - 200, HEIGHT // 2 + 50))
    quit_rect = draw_text("QUIT GAME", (WIDTH // 2 + 200, HEIGHT // 2 + 50))
    return restart_rect, quit_rect


# 处理方向键输入
def handle_key_input(key):
    global current_direction
    if key == pygame.K_LEFT:
        current_direction = (-1, 0)
    elif key == pygame.K_RIGHT:
        current_direction = (1, 0)
    elif key == pygame.K_UP:
        current_direction = (0, -1)
    elif key == pygame.K_DOWN:
        current_direction = (0, 1)


# 初始化选择界面
# 创建吃豆人的选择区域矩形，每个矩形用于检测点击
pacman_rects = [img.get_rect(topleft=(300 + i * 300, HEIGHT // 2 - 25)) for i, img in enumerate(select_pacman_images)]


# 主游戏循环
def game_loop():
    global running, choosing, game_over

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if choosing:
                    handle_pacman_selection(event.pos)
                elif game_over:
                    handle_game_over(event.pos)
            elif event.type == pygame.KEYDOWN and not (choosing or game_over):
                handle_key_input(event.key)

        if choosing:
            show_pacman_selection()
        elif game_over:
            show_game_over_screen()
        else:
            move_player()
            move_monster()
            update_game_state()
            draw_gameplay()

        pygame.display.flip()
        clock.tick(3)

# 开始游戏循环
game_loop()
pygame.quit()
