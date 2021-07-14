import pgzrun  # import game library!
import random  # import random library!

# screen size
WIDTH = 1000
HEIGHT = 600
SCOREBOX_HEIGHT = 50

# score variable
score = 0  # counter variable
SCORE_END = -20  # end the game when score <= -20
# SCORE_END = 500 # end the game when score >= 500

# speed variables
junk_speed = 5
sat_speed = 3
debris_speed = 5
laser_speed = -5  # negative because moving LEFT

# image variables
BACKGROUND_IMG = "space_game_background"  # change to your file name!
PLAYER_IMG = "player_ship"  # change to your file name!
JUNK_IMG = "space_junk"  # change to your file name!
SAT_IMG = "satellite_adv"  # change to your file name, "tesla_roadster"
DEBRIS_IMG = "tesla_roadster"
LASER_IMG = "laser_red"

# initialize sprites
player = Actor(PLAYER_IMG)  # Actor("file_name")
player.midright = (WIDTH-15, HEIGHT/2)  # rect_position = (x, y)

# initialize junks
junks = []  # start with an empty list
for i in range(5):  # creating 5 junk sprite
    junk = Actor(JUNK_IMG)
    x_pos = random.randint(-500, -50)
    y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
    junk.topleft = (x_pos, y_pos)
    junks.append(junk)  # add new sprite to junks list

# initialize satellite sprites
satellite = Actor(SAT_IMG)
x_sat = random.randint(-500, -50)  # negative to start off screen
y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
satellite.topright = (x_sat, y_sat)

# initialize debris sprite
debris = Actor(DEBRIS_IMG)
x_deb = random.randint(-500, -50)
y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
debris.topright = (x_deb, y_deb)

# initialize lasers
lasers = []  # start with empty list

# background music
sounds.spacelife.play(-1)

# MAIN GAME LOOP
def update():
    if score > SCORE_END:  # negative value -20
        updatePlayer()  # call Player function
        updateJunk()
        updateSatellite()
        updateDebris()
        updateLaser()
    if score <= SCORE_END:
        sounds.spacelife.stop()  # stop the music
    
def draw():
    screen.clear()  # clear screen
    screen.blit(BACKGROUND_IMG, (0,0))  # draw background image
    player.draw()  # draw player sprite
    for junk in junks:
        junk.draw()  # draw junk sprite
    satellite.draw()  # draw satellite sprite
    debris.draw()
    for laser in lasers:
        laser.draw()

    # add some text
    show_score = "Score: " + str(score)
    screen.draw.text(show_score, fontsize=35, topleft=(450,15), color="light green")

    # game over
    show_game_over = "GAME OVER"
    if score <= SCORE_END:
        screen.draw.text(show_game_over, fontsize=60, center=(WIDTH/2, HEIGHT/2), color="red", ocolor="white", owidth=0.5)

# Sprite Update Functions
def updatePlayer():
    # detect keyboard input
    if keyboard.UP == 1:
        player.y += (-5)   # moving UP is -y direction
    elif keyboard.DOWN == 1:
        player.y += 5      # moving DOWN is +y direction
    # add boundaries
    if player.top < SCOREBOX_HEIGHT:
        player.top = SCOREBOX_HEIGHT
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
        
    # fire lasers
    if keyboard.space == 1:
        laser = Actor(LASER_IMG)
        laser.midright = player.midleft  # (x, y)
        fireLasers(laser)  # firing laser

def updateJunk():
    global junk_speed, score
    for junk in junks:
        # make junk move left
        junk.x += junk_speed  # move 5 pixels every loop

        collision = player.colliderect(junk)  # sprite.collidrect(other_sprite)
    
        if junk.left > WIDTH or collision == 1:  # if junk goes off screen
            x_pos = random.randint(-500, -50) # starting junk off screen
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if collision == 1:
            print("collision")
            score += 1
            print(score)
            sounds.collect_pep.play()

def updateSatellite():
    global score
    satellite.x += sat_speed  # move 3 pixels every loop

    collision = player.colliderect(satellite)

    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint(-500, -50)  # negative to start off screen
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score += -10  # decreasing score if player collides with satellite
        sounds.explosion.play()  # play sound effect

def updateDebris():
    global score
    debris.x += debris_speed
    # debris.angle += -1  # optional

    collision = player.colliderect(debris)

    if debris.left > WIDTH or collision == 1:
        x_deb = random.randint(-500, -50)
        y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)
    if collision == 1:
        score += -10
        sounds.explosion.play()

def updateLaser():
    global score
    for laser in lasers: # for each sprite in our list
        laser.x += laser_speed 

        collision_sat = satellite.colliderect(laser)
        collision_deb = debris.colliderect(laser)

        if laser.right < 0 or collision_sat == 1 or collision_deb == 1:
            lasers.remove(laser)

        # reposition our sprites
        if collision_sat == 1:
            x_sat = random.randint(-500, -50)  # negative to start off screen
            y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += -5

        if collision_deb == 1:  # if shoot debris
            x_deb = random.randint(-500, -50)
            y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 10
            

# activating lasers (template code)____________________________________________________________________________________________
player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list
        
pgzrun.go()

