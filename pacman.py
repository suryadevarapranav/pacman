# Pac-Man
from board import boards
import pygame
import math

#
pygame.init()

# import PI
PI = math.pi

# Game Window Size.
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])

timer = pygame.time.Clock()  # Speed at which the game is played.
fps = 60  # Max Speed at which the game could be played.
font = pygame.font.Font('freesansbold.ttf', 20)  # Font to display the text in.
level = boards
color = 'blue'

# flicker the powerup points.
flicker = False

# turns allowed for a player at any position
# R, L, U, D.
turns_allowed = [False, False, False, False]

player_images=[]
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45))) # load the player images and scale them.

# player start position
player_x = 450
player_y = 663

# initializing the player direction and the start image to 0
direction = 0
counter = 0


# parsing out the board.
def draw_board(lvl):
    # 32 rows and 30 columns, so dividing by those numbers to get the sizing of each tile.
    # Floor division because the draw command requires an integer.
    # Draw requires the center coordinate to be given as a parameter.

    num1 = ((HEIGHT - 50) // 32)  # 50 pixel padding at the bottom.
    num2 = (WIDTH // 30)

    for i in range(len(lvl)):  # Iterate through the rows
        for j in range(len(lvl[i])):  # Iterate through the columns
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4) # Small dot
            elif lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10) # Large dot
            
            # draw.line takes in the start and the finish coordinates.
            
            elif lvl[i][j] == 3:
                # Vertical line
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), 
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3) # x stays the same but y is entire block start and finish.
            elif lvl[i][j] == 4:
                # Horizontal line
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), 
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)  # y stays the same but x is entire block start and finish.
            elif lvl[i][j] == 9: # Ghost Door.
                # Horizontal line except that it's white, doesn't allow the player to move. logic difference only.
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), 
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

            # draw.arc rectangle the arc exists in, because 5, 6, 7, 8 are just flips of each other.
            # x start, y start and total width, total height.

            elif lvl[i][j] == 5:
                # pygame.draw.arc(screen, color, [(j * num2 - (0.5 * num2)), (i * num1 + (0.5 * num1)), num2, num1], 0, PI/2, 3) 
                # these titled a bit towards left so went with this implementation to make it better.

                pygame.draw.arc(screen, color, 
                                [(j * num2 - (0.4 * num2) - 2), 
                                 (i * num1 + (0.5 * num1)), 
                                 num2, num1], 0, PI/2, 3)
            
            elif lvl[i][j] == 6:
                pygame.draw.arc(screen, color, 
                                [(j * num2 + (0.5 * num2)), 
                                 (i * num1 + (0.5 * num1)), 
                                 num2, num1], PI/2, PI, 3)

            elif lvl[i][j] == 7:
                pygame.draw.arc(screen, color, 
                                [(j * num2 + (0.5 * num2)), 
                                 (i * num1 - (0.4 * num1)), 
                                 num2, num1], PI, 3*PI/2, 3)
            
            elif lvl[i][j] == 8:
                pygame.draw.arc(screen, color, 
                                [(j * num2 - (0.4 * num2) - 2), 
                                 (i * num1 - (0.4 * num1)), 
                                 num2, num1], 3*PI/2, 2*PI, 3)


# set the player moving animations
def draw_player():
    # directions RIGHT, LEFT, UP, DOWN
    # counter to track how fast pacman moves (cycling through images).
    # pygame.transform.flip takes in two arguments which are to flip in the x direction and the y direction.
    # pygame.transform.rotate takes in the angle to rotate.

    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], -90), (player_x, player_y))







# Game Loop
run = True
while run:
    # Everything we want to execute in every single iteration of the game.

    timer.tick(fps)  # Run the game at set fps.
    if counter < 19: # 5 pings per image, 5 frames per images, 60fps 1/12 of a sec, 3 times a min.
        counter += 1
        if counter > 5:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill('black')  # Fill the entire background with the color black.

    draw_board(level)  # draw the pac-man level board.
    draw_player() # player in the house!!!

    # pass in the cener position of the player,
    center_x = player_x + 23
    center_y = player_y + 24
    # pygame.draw.circle(screen, 'red', (center_x, center_y), 2) # mark the center of the player pos.

    turns_allowed = check_position(center_x, center_y) # check for player pos and see if he's colliding based on that whether an action is possible.

    # Condition to exit the infinite while loop.
    for event in pygame.event.get():  # Built-in event handling the pygame module has.
        if event.type == pygame.QUIT:  # pygme.QUIT is the Cross button to close the window.
            run = False

        if event.type == pygame.KEYDOWN: # key press event.
            if event.key == pygame.K_RIGHT:
                direction = 0
            elif event.key == pygame.K_LEFT:
                direction = 1
            elif event.key == pygame.K_UP:
                direction = 2
            elif event.key == pygame.K_DOWN:
                direction = 3

    pygame.display.flip()



pygame.quit()
