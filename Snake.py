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
        self.was_direction = pygame.K_RIGHT
        self.load_images()

    def load_images(self):
        self.head_surfaces = {
            pygame.K_RIGHT: pygame.image.load("assets/Graphics/head_right.png"),
            pygame.K_LEFT: pygame.image.load("assets/Graphics/head_left.png"),
            pygame.K_UP: pygame.image.load("assets/Graphics/head_up.png"),
            pygame.K_DOWN: pygame.image.load("assets/Graphics/head_down.png")
        }
        self.body_surfaces = {
            "horizontal": pygame.image.load("assets/Graphics/body_horizontal.png"),
            "vertical": pygame.image.load("assets/Graphics/body_vertical.png"),
            "bottomleft": pygame.image.load("assets/Graphics/body_bottomleft.png"),
            "bottomright": pygame.image.load("assets/Graphics/body_bottomright.png"),
            "topleft": pygame.image.load("assets/Graphics/body_topleft.png"),
            "topright": pygame.image.load("assets/Graphics/body_topright.png")
        }
        self.tail_surfaces = {
            pygame.K_RIGHT: pygame.image.load("assets/Graphics/tail_left.png"),
            pygame.K_LEFT: pygame.image.load("assets/Graphics/tail_right.png"),
            pygame.K_UP: pygame.image.load("assets/Graphics/tail_down.png"),
            pygame.K_DOWN: pygame.image.load("assets/Graphics/tail_up.png")
        }
        self.head_surface = self.head_surfaces[self.direction]

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == pygame.K_RIGHT:
            head_x += self.size
        elif self.direction == pygame.K_LEFT:
            head_x -= self.size
        elif self.direction == pygame.K_UP:
            head_y -= self.size
        elif self.direction == pygame.K_DOWN:
            head_y += self.size

        new_head = (head_x, head_y)
        self.body = [new_head] + self.body[:-1]

        self.head_surface = self.head_surfaces[self.direction]
        self.tail_surface = self.tail_surfaces[self.direction]

    def grow(self):
        tail_x, tail_y = self.body[-1]
        self.body.append((tail_x, tail_y))

    def change_direction(self, direction):
        if direction in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
            self.was_direction = self.direction
            self.direction = direction

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:] or \
               head[0] < 40 or head[0] >= 680 or \
               head[1] < 40 or head[1] >= 480

    def get_body_surface(self, index):
        if index == 0:
            return self.head_surface
        elif index == len(self.body) - 1:
            return self.tail_surface
        else:
            previous_segment = self.body[index + 1]
            current_segment = self.body[index]
            next_segment = self.body[index - 1]

            if previous_segment[0] == next_segment[0]:
                return self.body_surfaces["vertical"]
            elif previous_segment[1] == next_segment[1]:
                return self.body_surfaces["horizontal"]
            else:
                if (previous_segment[0] < current_segment[0] and next_segment[1] < current_segment[1]) or \
                   (next_segment[0] < current_segment[0] and previous_segment[1] < current_segment[1]):
                    return self.body_surfaces["topleft"]
                elif (previous_segment[0] > current_segment[0] and next_segment[1] < current_segment[1]) or \
                     (next_segment[0] > current_segment[0] and previous_segment[1] < current_segment[1]):
                    return self.body_surfaces["topright"]
                elif (previous_segment[0] < current_segment[0] and next_segment[1] > current_segment[1]) or \
                     (next_segment[0] < current_segment[0] and previous_segment[1] > current_segment[1]):
                    return self.body_surfaces["bottomleft"]
                elif (previous_segment[0] > current_segment[0] and next_segment[1] > current_segment[1]) or \
                     (next_segment[0] > current_segment[0] and previous_segment[1] > current_segment[1]):
                    return self.body_surfaces["bottomright"]
                else:
                    return self.body_surfaces["horizontal"]

    def get_tail_surface(self):
        if len(self.body) < 2:
            return self.tail_surfaces[self.direction]

        tail_segment = self.body[-1]
        previous_segment = self.body[-2]

        if previous_segment[0] == tail_segment[0] and previous_segment[1] < tail_segment[1]:
            return self.tail_surfaces[pygame.K_UP]
        elif previous_segment[0] == tail_segment[0] and previous_segment[1] > tail_segment[1]:
            return self.tail_surfaces[pygame.K_DOWN]
        elif previous_segment[1] == tail_segment[1] and previous_segment[0] < tail_segment[0]:
            return self.tail_surfaces[pygame.K_LEFT]
        elif previous_segment[1] == tail_segment[1] and previous_segment[0] > tail_segment[0]:
            return self.tail_surfaces[pygame.K_RIGHT]
        else:
            return self.tail_surfaces[self.direction]

# Food class
class Food:
    def __init__(self):
        self.respawn()
    
    def respawn(self):
        self.position = (random.randint(1, (680 // 40) - 2) * 40 + 60,
                         random.randint(1, (480 // 40) - 2) * 40 + 60)

class Text:
    def __init__(self):
        self.text = "Score : 0"
        self.size = 50
        self.color = (144, 178, 106)
        self.font = pygame.font.Font('assets/Font/Pixeltype.ttf', self.size)
        self.surface = self.font.render(self.text, True, self.color)

    def update(self, score):
        self.text = "Score : {}".format(score)
        self.surface = self.font.render(self.text, True, self.color)

# Main game function
def main():
    snake = Snake()
    food = Food()
    text = Text()

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
            text.update(len(snake.body) - 3)

        if snake.check_collision():
            running = False

        screen.fill(background_color)
        pygame.draw.rect(screen, grass_color, pygame.Rect(60, 60, 680, 480))

        for index, segment in enumerate(snake.body):
            if index == len(snake.body) - 1:
                surface = snake.get_tail_surface()
            else:
                surface = snake.get_body_surface(index)
            screen.blit(surface, segment)

        screen.blit(apple_surface, food.position)
        screen.blit(text.surface, (330, 30))

        pygame.display.update()
        clock.tick(6)

if __name__ == "__main__":
    main()
