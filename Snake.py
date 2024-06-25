import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((153, 255, 51))

background_color = (153, 255, 51)
grass_color = (0, 153, 76)
font_color = (0, 0, 0)


# snake_head_surface = pygame.Surface((50, 50))
text_surface = pygame.font.Font(None, 50).render("Snake Game", True, (0, 0, 0))
apple_surface = pygame.image.load("assets/Graphics/apple.png")

pygame.display.set_caption("Snake Game")

block_size = 40

clock = pygame.time.Clock()

# Snake class
class Snake:
    def __init__(self):
        self.size = 40
        self.body = [(100, 100), (60, 100), (20, 100)]
        self.direction = pygame.K_RIGHT
        self.load_images()

    def load_images(self):
        self.head_surface = pygame.image.load("assets/Graphics/head_right.png")
        self.body_surface = pygame.image.load("assets/Graphics/body_horizontal.png")
        self.tail_surface = pygame.image.load("assets/Graphics/tail_left.png")

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == pygame.K_RIGHT:
            head_x += self.size
            self.head_surface = pygame.image.load("assets/Graphics/head_right.png")
            self.body_surface = pygame.image.load("assets/Graphics/body_horizontal.png")
            self.tail_surface = pygame.image.load("assets/Graphics/tail_left.png")
        elif self.direction == pygame.K_LEFT:
            head_x -= self.size
            self.head_surface = pygame.image.load("assets/Graphics/head_left.png")
            self.body_surface = pygame.image.load("assets/Graphics/body_horizontal.png")
            self.tail_surface = pygame.image.load("assets/Graphics/tail_right.png")
        elif self.direction == pygame.K_UP:
            head_y -= self.size
            self.head_surface = pygame.image.load("assets/Graphics/head_up.png")
            self.body_surface = pygame.image.load("assets/Graphics/body_vertical.png")
            self.tail_surface = pygame.image.load("assets/Graphics/tail_down.png")
        elif self.direction == pygame.K_DOWN:
            head_y += self.size
            self.head_surface = pygame.image.load("assets/Graphics/head_down.png")
            self.body_surface = pygame.image.load("assets/Graphics/body_vertical.png")
            self.tail_surface = pygame.image.load("assets/Graphics/tail_up.png")

        new_head = (head_x, head_y)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        tail_x, tail_y = self.body[-1]
        self.body.append((tail_x, tail_y))

    def change_direction(self, direction):
        if direction in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
            self.direction = direction

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:] or \
               head[0] < 50 or head[0] >= 700 or \
               head[1] < 50 or head[1] >= 500


# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, (700 - 40) // 40) * 50,
                         random.randint(0, (500 - 40) // 40) * 50)
    
    def respawn(self):
        self.position = (random.randint(0, (700 - 40) // 40) * 50,
                         random.randint(0, (500 - 40) // 40) * 50)

# Main game function
def main():
    snake = Snake()
    food = Food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)

        snake.move()
        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()

        if snake.check_collision():
            running = False

        screen.fill(background_color)
        pygame.draw.rect(screen, grass_color, pygame.Rect(50, 50, 700, 500))

        for segment in snake.body[1:-1]:
            screen.blit(snake.body_surface, segment)
        screen.blit(snake.head_surface, snake.body[0])
        screen.blit(snake.tail_surface, snake.body[-1])
        screen.blit(apple_surface, food.position)

        pygame.display.update()
        clock.tick(5)

if __name__ == "__main__":
    main()
