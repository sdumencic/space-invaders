import pygame
import random
import math

#inicijalizacija pygamea
pygame.init()

#inicijalizacija screena
screen = pygame.display.set_mode((600, 400))

#background
background = pygame.image.load('background.png')

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space invaders.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')
playerX = 270
playerY = 300
playerX_change = 0

#enemy
# enemyImg = pygame.image.load('enemy.png')
# enemyX = random.randint(0, 500)
# enemyY = random.randint(20, 200)
# enemyX_change = 1
# enemyY_change = 20

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 500))
    enemyY.append(random.randint(20, 200))
    enemyX_change.append(1)
    enemyY_change.append(20)

#shoot
shootImg = pygame.image.load('210108 space invaders shoot1.png')
shootX = 270
shootY = 300
shootX_change = 0
shootY_change = 1.5
shoot_state = False

#score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show(x, y):
    showScore = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(showScore, (x, y))

def game_over():
    showGame = font.render("Game over", True, (255, 255, 255))
    screen.blit(showGame, (200, 200))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def spawn():
    enemyX = random.randint(0, 500)
    enemyY = random.randint(20, 200)

def shoot(x, y):
    global shoot_state
    shoot_state = True
    screen.blit(shootImg, (x+32, y+10))

def isCollision(enemyX, enemyY, shootX, shootY):
    distance = math.sqrt(math.pow(enemyX - shootX, 2) + math.pow(enemyY - shootY, 2))
    if distance < 50:
        return True
    else:
        return False

running = True

while running:
    screen.fill((0, 85, 124))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if shoot_state == False:
                    shootX = playerX
                    shoot(playerX, shootY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 536: # granica - sirina slike
        playerX = 536

    # enemy
    for i in range(num_enemies):
        if enemyY[i] > 200:
            for j in range(num_enemies):
                enemyY[i] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 536:  # granica - sirina slike
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], shootX, shootY)
        if collision:
            shootY = 300
            shoot_state = False
            score += 1
            enemyX[i] = random.randint(0, 500)
            enemyY[i] = random.randint(20, 200)

        enemy(enemyX[i], enemyY[i], i)

    #shoot
    if shootY <= 0:
        shootY = 300
        shoot_state = False

    if shoot_state:
        shoot(shootX, shootY)
        shootY -= shootY_change

    player(playerX, playerY)
    show(textX, textY)
    pygame.display.update()
