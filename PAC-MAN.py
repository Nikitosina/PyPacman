import pygame
import sys
import os

pygame.init()
size = WIDTH, HEIGHT = 650, 750
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Field:
    def __init__(self, field):
        self.field = field

    def cell(self, x, y):
        return int(x / tile_width), int(y / tile_height)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

        self.tile_type = tile_type


class PacMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (tile_width - 2, tile_height - 2))
        self.img = self.image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 1, tile_height * pos_y + 1)

        self.speed = 3
        self.cur_dir = None
        self.next_dir = None

    def move(self, dir):
        global x, y
        check_pos = list(tiles_group)[(field.cell(self.rect.x, self.rect.y)[1]) * (x + 1):(field.cell(self.rect.x, self.rect.y)[1] + 2) * (x + 1)]
        if dir == 'r':
            self.rect.x += self.speed
            for s in check_pos:
                if s.tile_type == 'wall' and pygame.sprite.collide_rect(self, s):
                    self.rect.x -= self.speed
                    return False
            self.rect.x -= self.speed
            self.image = self.img
            self.rect = self.rect.move(self.speed, 0)
        if dir == 'l':
            self.rect.x -= self.speed
            for s in check_pos:
                if s.tile_type == 'wall' and pygame.sprite.collide_rect(self, s):
                    self.rect.x += self.speed
                    return False
            self.rect.x += self.speed
            self.image = pygame.transform.rotate(self.img, 180)
            self.rect = self.rect.move(-self.speed, 0)
        if dir == 'u':
            self.rect.y -= self.speed
            for s in list(tiles_group)[(field.cell(self.rect.x, self.rect.y)[1]) * (x + 1):(field.cell(self.rect.x, self.rect.y)[1] + 2) * (x + 1)]:
                if s.tile_type == 'wall' and pygame.sprite.collide_rect(self, s):
                    self.rect.y += self.speed
                    return False
            self.rect.y += self.speed
            self.image = pygame.transform.rotate(self.img, 90)
            self.rect = self.rect.move(0, -self.speed)
        if dir == 'd':
            self.rect.y += self.speed
            for s in check_pos:
                if s.tile_type == 'wall' and pygame.sprite.collide_rect(self, s):
                    self.rect.y -= self.speed
                    return False
            self.rect.y -= self.speed
            self.image = pygame.transform.rotate(self.img, -90)
            self.rect = self.rect.move(0, self.speed)
        if dir is not None:
            return True

    def update(self):
        global x, y
        map_x, map_y = field.cell(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2)
        if self.move(self.next_dir):
            self.cur_dir, self.next_dir = self.next_dir, None
        self.move(self.cur_dir)
        tile = list(tiles_group)[map_y * (x + 1) + map_x]
        if tile.tile_type == 'tile_point':
            tile.tile_type = 'tile_empty'
            tile.image = pygame.transform.scale(tile_images[tile.tile_type], (tile_width, tile_height))
        # print(field.cell(self.rect.x, self.rect.y))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('tile_point', x, y)
            elif level[y][x] == 'O':
                Tile('tile_point_big', x, y)
            elif level[y][x] == '_':
                Tile('tile_empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('tile_empty', x, y)
                new_player = PacMan(x, y)
    return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # max_width = max(map(len, level_map))
    max_width = WIDTH // tile_width
    for _ in range(HEIGHT // tile_height - len(level_map)):
        level_map.append('.')

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# print(load_level('map.txt'))

running = True
FPS = 40
tile_width = tile_height = 23
clock = pygame.time.Clock()

tile_images = {
    'wall': load_image('block.png'),
    'tile_empty': load_image('ground1.png'),
    'tile_point': load_image('ground_point.png'),
    'tile_point_big': load_image('ground_point_big.png')
}
player_image = load_image('pacman.png')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

m = load_level('map_classic.txt')
field = Field(m)
pacman, x, y = generate_level(m)
print(len(list(tiles_group)), x, y)


def start_screen():
    intro_text = ["ZASTAVKA"]

    fon = pygame.transform.scale(load_image('bg_start_screen.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


while running:
    screen.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        if event.type == pygame.KEYDOWN:
            dir = None
            if event.key == pygame.K_LEFT:
                dir = 'l'
            if event.key == pygame.K_RIGHT:
                dir = 'r'
            if event.key == pygame.K_UP:
                dir = 'u'
            if event.key == pygame.K_DOWN:
                dir = 'd'
            pacman.next_dir = dir
            # pacman.move(dir)

    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
