import pygame
import json
import sys 
import random as rnt

# Pygame initialization 
pygame.init()

# variable 
SW, SH = 660, 660
BLOCKSIZE = 30
BG_COLOR = "#202020"
SCORE_COLOR = "#f39c12"
GRID = "#404040"
SNAKE_HEAD, SNAKE_BODY = "#009432", "green"
FONT = pygame.font.Font("AEXKON_Bold.ttf", BLOCKSIZE)
top_score = 1
alive = True


# setup screen 
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake game by @sakibullah2006")
clock = pygame.time.Clock()

def drawScore():
    global top_score
    score = len(snake.body) - 1
    score_text = FONT.render(f"score: {score}", True, SCORE_COLOR)
    screen.blit(score_text, (SW/2, SH/30))
    tscore_text = FONT.render(f"Top Score: {top_score}", True, SCORE_COLOR)
    screen.blit(tscore_text, (SW/2, SH/30+30))


def trackScore():
    global top_score  # Use the global keyword to modify the module-level variable
    score = len(snake.body) - 1
    score_file_name = "score.json"
    try:
        with open(score_file_name, 'r') as file:
            data = json.load(file)
            tscore = int(data.get('top_score', 0))
            lscore = int(data.get('last_score', 0))
            if tscore > score:
                top_score = tscore
            else:
                top_score = score
                data['top_score'] = score
        # Open the file in write mode to update the JSON data
        with open(score_file_name, 'w') as file:
            json.dump(data, file)
    except FileNotFoundError:
        print("could not open json file")


def drawGrid():
    for x in range(0, SW, BLOCKSIZE):
        for y in range(0, SH, BLOCKSIZE):
            ract = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(screen, GRID, ract, 1)

drawGrid()

class Snake:
    def __init__(self):
        self.x = (int(rnt.randrange(0, SW) / BLOCKSIZE) * BLOCKSIZE) - BLOCKSIZE*2
        self.y = int(rnt.randrange(0, SW) / BLOCKSIZE) * BLOCKSIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)
        self.body = [pygame.Rect(self.x - BLOCKSIZE, self.y, BLOCKSIZE, BLOCKSIZE)]

    def update(self):
        global alive
        trackScore()
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                alive = False
        
        if alive == False:
            self.x = (int(rnt.randrange(0, SW) / BLOCKSIZE) * BLOCKSIZE) - BLOCKSIZE*2
            self.y = int(rnt.randrange(0, SW) / BLOCKSIZE) * BLOCKSIZE
            self.xdir = 1
            self.ydir = 0
            self.body = [pygame.Rect(self.x - BLOCKSIZE, self.y, BLOCKSIZE, BLOCKSIZE)]
            self.head = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)
            # self.alive = True
            apple = Apple() 

        # Wrap around the screen
        if self.head.x >= SW: 
            self.head.x = 0
        elif self.head.x < 0:
            self.head.x = SW - BLOCKSIZE
        if self.head.y >= SH:
            self.head.y = 0
        elif self.head.y < 0:
            self.head.y = SH - BLOCKSIZE  

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x , self.body[i+1].y
        self.head.x += self.xdir *  BLOCKSIZE  
        self.head.y += self.ydir *  BLOCKSIZE 
        self.body.remove(self.head)

class Apple:
    def __init__(self):
        self.x = int(rnt.randrange(0, SW) / BLOCKSIZE) * BLOCKSIZE
        self.y = int(rnt.randrange(0, SH) / BLOCKSIZE) * BLOCKSIZE
        self.apple = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)

    def update(self):
        pygame.draw.rect(screen, "red", self.apple)

def gameOver():
    global alive
    running = True
    while running:
        game_over_text = FONT.render("Game Over", True, SCORE_COLOR)
        screen.blit(game_over_text, (SW/2 - game_over_text.get_width()/2, SH/2 - game_over_text.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    alive = True
                    running = False

apple = Apple()
snake = Snake()
trackScore()

def mainGame():
    global alive, snake, apple
    snake = Snake()
    apple = Apple()
    # Game loop
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit Pygame
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    snake.xdir = 0
                    snake.ydir = 1
                elif event.key == pygame.K_UP:
                    snake.xdir = 0 
                    snake.ydir = -1
                elif event.key == pygame.K_LEFT:
                    snake.xdir = -1
                    snake.ydir = 0
                elif event.key == pygame.K_RIGHT:
                    snake.xdir = 1 
                    snake.ydir = 0

        screen.fill(BG_COLOR)
        drawGrid()
        drawScore()
        apple.update()
        snake.update()

        pygame.draw.rect(screen, SNAKE_HEAD, snake.head)
        for square in snake.body:
            pygame.draw.rect(screen, SNAKE_BODY, square)

        if apple.x == snake.head.x and apple.y == snake.head.y :
            snake.body.append(pygame.Rect(snake.head.x, snake.head.y, BLOCKSIZE, BLOCKSIZE))
            snake.head.x += snake.xdir * BLOCKSIZE 
            snake.head.y += snake.ydir * BLOCKSIZE 
            apple = Apple()
            drawScore()
        
        pygame.display.update()
        clock.tick(10)
    gameOver()

while True:
    mainGame()
