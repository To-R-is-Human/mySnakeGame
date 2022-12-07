import os.path, random, pygame as pg
from sys import exit


pg.init()
pg.mixer.init()


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
gameWindow = pg.display.set_mode((600, 500))
img = pg.image.load('snake.svg')
pg.display.set_icon(img)
bg_img = [pg.image.load('snakebg.jpg'), pg.image.load('snake_pass.jpg')]
bg_img = [pg.transform.scale(img, (600, 500)).convert_alpha() for img in bg_img]
pg.display.set_caption("Snake Game")
font = pg.font.SysFont('Calibre', 25)
watch = pg.time.Clock()


def screen_score(text, color, x, y):
    score_update = font.render(text, True, color)
    gameWindow.blit(score_update, [x, y])


def plot_snake(canvas, color, snk_list, snake_size):
    for x, y in snk_list:
        pg.draw.rect(canvas, color, [x, y, snake_size, snake_size])


def welcome():
    pg.mixer.music.load('game_start.mp3')
    pg.mixer.music.play()
    gameWindow.blit(bg_img[0], (0, 0))
    screen_score("Welcome to Snakes", black, 220, 220)
    screen_score("Press Enter to start game", black, 200, 240)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    pg.mixer.music.load('bg.mp3')
                    pg.mixer.music.play()
                    game_loop()
        pg.display.update()
        watch.tick(60)


# Game Loop
def game_loop():
    game_over = False
    snake_x, snake_y = 50, 50
    velocity_x, velocity_y = 0, 0
    snake_size = 10
    food_x = random.randint(2, 50) * 10
    food_y = random.randint(2, 40) * 10
    fps = 30
    score = 0
    snk_list = []
    snk_length = 1
    if not (os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()
    while True:
        if game_over:
            pg.mixer.music.load('gameover.mp3')
            pg.mixer.music.play()
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.blit(bg_img[1], (0, 0))
            screen_score(f"Game Over, Your score: {str(score)}", white, 200, 240)
            screen_score(f"Press Enter to continue", white, 210, 260)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        welcome()
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        velocity_x, velocity_y = 5, 0
                    elif event.key == pg.K_LEFT:
                        velocity_x, velocity_y = -5, 0
                    elif event.key == pg.K_UP:
                        velocity_x, velocity_y = 0, -5
                    elif event.key == pg.K_DOWN:
                        velocity_x, velocity_y = 0, 5
                    elif event.key == pg.K_SPACE:
                        score += 2
                    elif event.key == pg.K_w:
                        score += int(hiscore)
            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x) <= 5 and abs(snake_y-food_y) <= 5:
                score += 1
                food_x = random.randint(2, 50) * 10
                food_y = random.randint(2, 45) * 10
                snk_length += 2
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            screen_score(f"Score: {str(score)} Hiscore: {str(hiscore)}", red, 5, 5)
            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
            if snake_x < 0 or snake_x > 600 or snake_y < 0 or snake_y > 500:
                game_over = True
            plot_snake(gameWindow, blue, snk_list, snake_size)
            pg.draw.rect(gameWindow, green, [food_x, food_y, snake_size, snake_size])
        pg.display.update()
        watch.tick(fps)


welcome()
