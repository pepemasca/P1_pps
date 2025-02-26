#!/usr/bin/env python3
import pygame
import random
import sys
import time

# ---------------------- CONSTANTES ---------------------- #
CELL_SIZE   = 20              # Tamaño de cada celda en píxeles
GRID_WIDTH  = 30              # Número de celdas en horizontal (30 * 20 = 600 píxeles)
GRID_HEIGHT = 30              # Número de celdas en vertical (30 * 20 = 600 píxeles)
WINDOW_WIDTH  = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS_INICIAL = 10              # Velocidad inicial (se incrementa con el nivel)

# Colores (RGB)
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
ORANGE  = (255, 165, 0)
PURPLE  = (128, 0, 128)
GREY    = (128, 128, 128)
CYAN    = (0, 255, 255)  # Para indicar que el escudo está activo

# ---------------------- CLASES ---------------------- #

class Snake:
    def __init__(self):
        # La serpiente inicia en el centro de la cuadrícula
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)  # Se mueve inicialmente hacia arriba
        self.grow_amount = 0     # Cantidad de segmentos a agregar (al comer alimento)
        self.color = GREEN
        self.shield_end_time = 0  # Tiempo hasta el cual el escudo estará activo

    def get_head(self):
        return self.body[0]

    def move(self):
        head_x, head_y = self.get_head()
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if self.grow_amount > 0:
            self.grow_amount -= 1
        else:
            self.body.pop()  # Elimina el último segmento si no se está creciendo

    def change_direction(self, new_direction):
        # Evita invertir la dirección (por ejemplo, de arriba a abajo)
        dx, dy = self.direction
        ndx, ndy = new_direction
        if (dx, dy) == (-ndx, -ndy):
            return
        self.direction = new_direction

    def grow(self, amount):
        self.grow_amount += amount

    def is_shield_active(self):
        return time.time() < self.shield_end_time

    def activate_shield(self, duration):
        self.shield_end_time = time.time() + duration

    def draw(self, surface):
        # Dibuja cada segmento de la serpiente
        for segment in self.body:
            x, y = segment
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)
        # Si el escudo está activo, se dibuja un borde en la cabeza
        if self.is_shield_active():
            head_x, head_y = self.get_head()
            rect = pygame.Rect(head_x * CELL_SIZE, head_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, CYAN, rect, 3)

class Food:
    def __init__(self, position, food_type):
        self.position = position
        self.type = food_type
        # Asigna color según el tipo de alimento
        if self.type == "normal":
            self.color = ORANGE
        elif self.type == "bonus":
            self.color = BLUE
        elif self.type == "poison":
            self.color = PURPLE
        elif self.type == "shield":
            self.color = YELLOW

    def draw(self, surface):
        x, y = self.position
        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(surface, self.color, center, radius)

# ---------------------- FUNCIONES AUXILIARES ---------------------- #

def generate_obstacles(num, snake, food):
    """
    Genera una lista de obstáculos (posiciones en la cuadrícula) evitando colisiones
    con la serpiente y el alimento actual.
    """
    obstacles = []
    while len(obstacles) < num:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos in snake.body or pos == food.position or pos in obstacles:
            continue
        obstacles.append(pos)
    return obstacles

def draw_obstacles(surface, obstacles):
    for pos in obstacles:
        x, y = pos
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, GREY, rect)

def spawn_food(snake, obstacles):
    """
    Genera un alimento en una posición aleatoria que no esté ocupada por la serpiente ni por obstáculos.
    Se asigna el tipo de alimento usando probabilidades ponderadas:
      - "normal": 70%
      - "bonus": 15%
      - "poison": 5%
      - "shield": 10%
    """
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos in snake.body or pos in obstacles:
            continue
        food_type = random.choices(
            ["normal", "bonus", "poison", "shield"],
            weights=[70, 15, 5, 10]
        )[0]
        return Food(pos, food_type)

def draw_text(surface, text, size, color, center):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, rect)

# ---------------------- FUNCIÓN PRINCIPAL ---------------------- #

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game Único")
    clock = pygame.time.Clock()

    # Estado inicial del juego
    snake = Snake()
    score = 0
    level = 1
    speed = FPS_INICIAL

    # Inicia con un alimento y sin obstáculos en el nivel 1
    food = spawn_food(snake, [])
    obstacles = []

    running = True
    game_over = False

    while running:
        if game_over:
            # Pantalla de Game Over
            screen.fill(BLACK)
            draw_text(screen, "GAME OVER", 50, RED, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            draw_text(screen, f"Puntuación: {score}", 40, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            draw_text(screen, "Presiona R para reiniciar o Q para salir", 30, WHITE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()  # Reinicia el juego
                        return
                    elif event.key == pygame.K_q:
                        running = False
                        break
            continue

        # Procesa eventos de entrada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        # Movimiento de la serpiente
        snake.move()
        head = snake.get_head()

        # Colisión con los bordes de la ventana
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            game_over = True
            continue

        # Colisión con obstáculos (si no tiene escudo activo)
        if not snake.is_shield_active() and head in obstacles:
            game_over = True
            continue

        # Colisión con su propio cuerpo (si no tiene escudo activo)
        if not snake.is_shield_active() and head in snake.body[1:]:
            game_over = True
            continue

        # Colisión con el alimento
        if head == food.position:
            if food.type == "normal":
                snake.grow(1)
                score += 10
            elif food.type == "bonus":
                snake.grow(2)
                score += 20
            elif food.type == "poison":
                # Si la serpiente es lo suficientemente larga se quitan 2 segmentos;
                # de lo contrario, se termina el juego.
                if len(snake.body) > 3:
                    for _ in range(2):
                        if len(snake.body) > 0:
                            snake.body.pop()
                    score = max(0, score - 15)
                else:
                    game_over = True
                    continue
            elif food.type == "shield":
                snake.activate_shield(10)  # Escudo activo por 10 segundos
                score += 5
            # Genera un nuevo alimento
            food = spawn_food(snake, obstacles)

        # Progresión de nivel: cada 100 puntos se incrementa el nivel
        nuevo_nivel = score // 100 + 1
        if nuevo_nivel != level:
            level = nuevo_nivel
            speed = FPS_INICIAL + level  # Incrementa la velocidad según el nivel
            # Genera obstáculos: cantidad = (nivel - 1) * 3
            obstacles = generate_obstacles((level - 1) * 3, snake, food)

        # Dibujo de la escena
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_obstacles(screen, obstacles)
        draw_text(screen, f"Score: {score}  Level: {level}", 30, WHITE, (WINDOW_WIDTH // 2, 20))
        pygame.display.flip()

        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
