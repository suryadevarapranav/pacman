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

# turns allowed for a player at any position: Right, Left, Up, Down.
turns_allowed = [False, False, False, False]

direction_command = 0

# player speed
player_speed = 2

# load player_images
player_images=[]
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45))) # load the player images and scale them.

# load the ghost images
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))


# player start position
player_x = 450
player_y = 663
# initializing the player direction and the start image to 0
direction = 0


# initializing starting positions and directions for the ghosts
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2

counter = 0

# initialize the score to '0'
score = 0

# power-up is false at the start.
powerup = False
power_counter = 0
# ghosts are all active at the start of the game.
eaten_ghost = [False, False, False, False]

# list of the ghost targets
"""
    if alive then its the player position
    else if dead then the door to be revived
    else if powerup phase then away from the player position.
"""

# ghost dead or not.
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False

# ghost in the box or not.
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False

# initialize the ghost speed
ghost_speed = 2

# used at the start of the game
startup_counter = 0
moving = False # don't allow the movement for the startup_counter time.

# initialize the lives for the player for every game
lives = 3




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


def check_position(centerx, centery):
    # possible turns at any point.
    # directions RIGHT, LEFT, UP, DOWN
    turns = [False, False, False, False]

    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15 # fudge factor, since the player himself isn't a 45X45 square.

    # check collisions based on center x and center y of player +/- fudge number.

    """check if it's possible to go back in the direction you came from."""
    if centerx // 30 < 29: # once we're in spot 0 or spot 29, we're going either through the wall or going backwards.
        if direction == 0: # right
            # can turn if the tile is 0, 1, 2
            if level[centery // num1][(centerx - num3) // num2] < 3: # row we're in based on y and column based on the x.
                turns[1] = True
        if direction == 1: #
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][(centerx) // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][(centerx) // num2] < 3:
                turns[2] = True

        # can only turn if we're at the mid-point.
        # fudge just to make the collisions look realistic.
        """
        check if we're able to turn up or down based on active direction, 
        we want to check if we can turn left or right at exact height so centery stays the sam,
        and check by a full square.
        """
        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18: # 12 to 18 is mid-point of the tile, each tile is 30 wide.
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18: # 12 to 18 is mid-point of the tile, each tile is 30 height.
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True

        """
        check if we're able to turn right or left based on active direction, 
        we want to check if we can turn up or down at exact width so centerx stays the same,
        and check by a full square.
        """
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True

    return turns


# moving the player, we can move in the direction we're moving as long as there isn't a collision. :)
def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed

    return play_x, play_y


# check to see if colliding with pieces.
def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870: # limits because these are the real positions, else off the screen.
        if level[center_y // num1][center_x // num2] == 1: # dot.
            level[center_y // num1][center_x // num2] = 0 # dot was eaten
            scor += 10
        if level[center_y // num1][center_x // num2] == 2: # power-up
            level[center_y // num1][center_x // num2] = 0 # power-up was eaten
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts


# display the player score, at any point in the game.
def display_score():
    score_text = font.render(f'Score: {score}', True, 'white') # True is anit=alias, smooths out the edges.
    screen.blit(score_text, (10, 920)) # put the score on the screen.

def powerup_indicator():
    if powerup:
        pygame.draw.circle(screen, 'purple', (140, 930), 15)

# display the lives remaining
def lives_indicator():
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))


# place all the misc stuff
def draw_misc():
    display_score() # display the current score
    powerup_indicator() # show an indicator that power-up is active
    lives_indicator() # remaining lives in the game

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

    if powerup and power_counter < 600: # power up lasts for 10 seconds.
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]

    # give a 3 sec time to look at the game before it starts
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True


    screen.fill('black')  # Fill the entire background with the color black.

    draw_board(level)  # draw the pac-man level board.
    draw_player() # player in the house!!!
    draw_misc() # display all the misc stuff

    # pass in the center position of the player,
    center_x = player_x + 23
    center_y = player_y + 24
    # pygame.draw.circle(screen, 'red', (center_x, center_y), 2) # mark the center of the player pos.

    turns_allowed = check_position(center_x, center_y) # check for player pos and see if he's colliding based on that whether an action is possible.

    # allow the player to move only if the moving is True
    if moving:
        player_x, player_y = move_player(player_x, player_y)

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    # Condition to exit the infinite while loop.
    for event in pygame.event.get():  # Built-in event handling the pygame module has.
        if event.type == pygame.QUIT:  # pygme.QUIT is the Cross button to close the window.
            run = False

        # get a joystick feel, don't change the direction right away, whatever key we hold down last should be in control.
        # direction_command will be conditional and won't be as instant in changing the direction.
        if event.type == pygame.KEYDOWN: # key press event.
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            elif event.key == pygame.K_LEFT:
                direction_command = 1
            elif event.key == pygame.K_UP:
                direction_command = 2
            elif event.key == pygame.K_DOWN:
                direction_command = 3

        if event.type == pygame.KEYUP: # key release event
            if event.key == pygame.K_RIGHT and direction_command == 0:  # and the last direction command was for that key.
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i


    # player moves across the screen
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()



pygame.quit()

## FIXME's:

"""
1. Turning direction at any time and getting stuck - Fix: Turn only when the direction is a possibility.
2. Game is being quit when going to the extremes. 

----- Fixed by indenting code in the check_positions function.
"""