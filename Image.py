import pygame
from config import TILE_SIZE, PM_SIZE

# 加载墙、萝卜、怪物，inuji的图片
wall_image = pygame.transform.scale(pygame.image.load('wall.png'), (TILE_SIZE, TILE_SIZE))
food_image = pygame.transform.scale(pygame.image.load('luobei.jpg'), (TILE_SIZE // 2, TILE_SIZE // 2))
monster_image = pygame.transform.scale(pygame.image.load('monster.jpg'), (PM_SIZE, PM_SIZE))
inuji_image = pygame.transform.scale(pygame.image.load('monster.jpg'), (PM_SIZE, PM_SIZE))
# 生命值图片配置
life_image_full = pygame.transform.scale(pygame.image.load('heart_1.png'), (20, 20))  # 代表一个生命值
life_image_empty = pygame.transform.scale(pygame.image.load('heart_6.png'), (20, 20))  # 代表没有生命值
# 选择界面玩家图片
select_pacman_images = [
    pygame.transform.scale(pygame.image.load('tuji.jpg'), (200, 200)),
    pygame.transform.scale(pygame.image.load('pangpang.jpg'), (200, 200))
]
# 玩家图片
game_pacman_images = [
    pygame.transform.scale(pygame.image.load('tuji.jpg'), (PM_SIZE, PM_SIZE)),
    pygame.transform.scale(pygame.image.load('pangpang.jpg'), (PM_SIZE, PM_SIZE))
]