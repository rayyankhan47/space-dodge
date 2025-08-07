import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Dodge")

BG = pygame.transform.scale(pygame.image.load("background-image.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("Arial", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "blue", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                        PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000 # time in milliseconds
    star_count = 0

    stars = []

    hit = False


    while run:
        star_count += clock.tick(60) # while loop will only run 60 times in one second
        elapsed_time = time.time() - start_time
        # generate all of our stars
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
        # check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        # player moving
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + player.width + PLAYER_VEL <= WIDTH:
            player.x += PLAYER_VEL
        # move all of the stars
        for star in stars[:]: # creating a copy, since if we loop through a list as we're mutating it, things can get weird
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player): # the first part of the and statement just makes it so that we don't have to check for collision if we're not even in the same y coordinates as the player.
                stars.remove(star)
                hit = True
                break
        # draw everything
        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()

