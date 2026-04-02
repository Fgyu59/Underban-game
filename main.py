import pygame
import random
import math
import sys
import os

# Инициализация
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
PURPLE = (200, 0, 255)
GRAY = (40, 40, 40)
ORANGE = (255, 150, 0)

# Пути
base_path = os.path.dirname(os.path.abspath(__file__))

def load_img(name, size):
    path = os.path.join(base_path, name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except: return None

boss_img = load_img("_face.png", (350, 350))
dusha_img = load_img("dusha.png", (30, 30))

# Параметры боя
box_w, box_h = 650, 450
box_rect = pygame.Rect(WIDTH//2 - box_w//2, HEIGHT//2 - 50, box_w, box_h)
player_rect = pygame.Rect(box_rect.centerx, box_rect.centery, 30, 30)

# Статы игрока
hp = 92.0
is_blue_mode = False # Режим гравитации
vel_y = 0
on_ground = False
shake_amount = 0

# Списки объектов
blasters = []
platforms = []
bones = [] # Новая быстрая атака

class Blaster:
    def __init__(self):
        self.side = random.choice(['L', 'R', 'T', 'B'])
        self.timer = 0
        self.active = False
        pos_map = {
            'L': [box_rect.left - 80, random.randint(box_rect.top, box_rect.bottom-60)],
            'R': [box_rect.right + 20, random.randint(box_rect.top, box_rect.bottom-60)],
            'T': [random.randint(box_rect.left, box_rect.right-60), box_rect.top - 80],
            'B': [random.randint(box_rect.left, box_rect.right-60), box_rect.bottom + 20]
        }
        self.r = pygame.Rect(pos_map[self.side][0], pos_map[self.side][1], 60, 60)

    def draw(self, surf):
        self.timer += 1
        color = PURPLE if self.timer > 15 else WHITE
        pygame.draw.rect(surf, color, self.r, 4)
        if self.timer > 20: # Быстрый выстрел
            self.active = True
            beam_color = BLUE if is_blue_mode else WHITE
            if self.side == 'L': beam = pygame.Rect(self.r.right, self.r.y+10, box_w, 40)
            elif self.side == 'R': beam = pygame.Rect(self.r.left-box_w, self.r.y+10, box_w, 40)
            elif self.side == 'T': beam = pygame.Rect(self.r.x+10, self.r.bottom, 40, box_h)
            else: beam = pygame.Rect(self.r.x+10, self.r.top-box_h, 40, box_h)
            pygame.draw.rect(surf, beam_color, beam)
            if beam.colliderect(player_rect): return True
        return False

class Bone:
    def __init__(self):
        self.w = 20
        self.h = random.randint(100, 250)
        self.rect = pygame.Rect(box_rect.right, box_rect.bottom - self.h, self.w, self.h)
        self.speed = random.randint(10, 16)
    def update(self):
        self.rect.x -= self.speed
        return self.rect.right < box_rect.left

# Джойстик
joy_center = (200, HEIGHT - 200)
joy_radius = 100
stick_pos = list(joy_center)
is_dragging = False

clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 45, bold=True)

mode_timer = 0

while True:
    # Тряска экрана
    offset_x = random.randint(-shake_amount, shake_amount)
    offset_y = random.randint(-shake_amount, shake_amount)
    if shake_amount > 0: shake_amount -= 1
    
    screen.fill(BLACK)
    render_surf = pygame.Surface((WIDTH, HEIGHT)) # Слой для тряски
    render_surf.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_AC_BACK:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot(event.pos[0]-joy_center[0], event.pos[1]-joy_center[1]) < joy_radius:
                is_dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            is_dragging = False
            stick_pos = list(joy_center)

    # Логика смены режима
    mode_timer += 1
    if mode_timer > 400: # Каждые ~7 секунд режим меняется
        is_blue_mode = not is_blue_mode
        mode_timer = 0
        shake_amount = 15

    # Управление
    mx, my = 0, 0
    if is_dragging:
        p = pygame.mouse.get_pos()
        dx, dy = p[0]-joy_center[0], p[1]-joy_center[1]
        dist = math.hypot(dx, dy)
        limit = min(dist, joy_radius)
        angle = math.atan2(dy, dx)
        stick_pos = [joy_center[0] + math.cos(angle)*limit, joy_center[1] + math.sin(angle)*limit]
        mx, my = math.cos(angle)*(limit/joy_radius), math.sin(angle)*(limit/joy_radius)

    # Физика Души
    if not is_blue_mode:
        player_rect.x += mx * 10
        player_rect.y += my * 10
    else:
        # Синий режим (Гравитация)
        player_rect.x += mx * 10
        if my < -0.5 and on_ground: # Прыжок
            vel_y = -18
            on_ground = False
        vel_y += 1 # Сила тяжести
        player_rect.y += vel_y
        
    # Коллизии с полом
    if player_rect.bottom > box_rect.bottom:
        player_rect.bottom = box_rect.bottom
        vel_y = 0
        on_ground = True
    player_rect.clamp_ip(box_rect)

    # Спавн Атак (Адская частота)
    if random.random() < 0.06: blasters.append(Blaster())
    if random.random() < 0.05: bones.append(Bone())
    if random.random() < 0.04: 
        platforms.append(type('Obj', (object,), {'rect': pygame.Rect(box_rect.left-120, random.randint(box_rect.top+50, box_rect.bottom-50), 120, 15), 'speed': random.randint(5, 12)})())

    # Отрисовка
    if boss_img: render_surf.blit(boss_img, (WIDTH//2 - 175, box_rect.top - 330))
    pygame.draw.rect(render_surf, WHITE, box_rect, 6)

    # Платформы
    for p in platforms[:]:
        pygame.draw.rect(render_surf, WHITE, p.rect)
        p.rect.x += p.speed
        if p.rect.colliderect(player_rect):
            player_rect.x += p.speed
            if is_blue_mode and vel_y > 0:
                player_rect.bottom = p.rect.top
                vel_y = 0
                on_ground = True
        if p.rect.left > box_rect.right: platforms.remove(p)

    # Кости
    for b in bones[:]:
        pygame.draw.rect(render_surf, WHITE, b.rect)
        if b.update(): bones.remove(b)
        if b.rect.colliderect(player_rect): hp -= 0.5

    # Бластеры
    for bl in blasters[:]:
        if bl.draw(render_surf): 
            hp -= 0.8
            shake_amount = 5
        if bl.timer > 45: blasters.remove(bl)

    # Душа
    d_color = BLUE if is_blue_mode else RED
    if dusha_img: 
        render_surf.blit(dusha_img, player_rect)
        if is_blue_mode: pygame.draw.rect(render_surf, BLUE, player_rect, 2) # Подсветка в синем режиме
    else: pygame.draw.rect(render_surf, d_color, player_rect)

    # UI
    pygame.draw.circle(render_surf, GRAY, joy_center, joy_radius, 4)
    pygame.draw.circle(render_surf, WHITE, (int(stick_pos[0]), int(stick_pos[1])), 45)
    
    hp_col = RED if hp < 20 else (255, 255, 0)
    hp_text = font.render(f"HP: {int(hp)}", True, hp_col)
    render_surf.blit(hp_text, (WIDTH//2 - 60, box_rect.bottom + 30))
    
    if is_blue_mode:
        warn = font.render("GRAVITY MODE", True, BLUE)
        render_surf.blit(warn, (WIDTH//2 - 130, 50))

    if hp <= 0:
        hp = 92
        blasters, bones, platforms = [], [], []
        is_blue_mode = False

    screen.blit(render_surf, (offset_x, offset_y))
    pygame.display.flip()
    clock.tick(60)
