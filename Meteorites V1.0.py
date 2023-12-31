#meterorites
#start date : 10/11/2020
#end date : 31/12/2023 project complete




# ------------------------------------------------------------- SETUP ----------------------------------------------------------------- #




# Setup - IMPORTING pygame Modules
import pygame, sys
import time
import random
from pygame.locals import *

# Setup - Setting global variables
screen_height = 500
screen_width = 500
GREEN = [0,255,0]
RED = [255,0,0]
PURPLE = [255,0,255]
BROWN = [204,102,0]

# Setup - Arrays used to store multiple objects
Meteorites = []
lasers = []

# Stores spawn locations for meteors
Spawn_Locations = [[100,0],[250,0],[400,0]]

# Stores Meteorite types
Meteor_types = [[20,5],[39,2]]

# Setup - used functions
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)




# ------------------------------------------------------ CLASSES FOR GAME_RUN ---------------------------------------------------------- #




# Creating player class which stores characteristics of the players ship
class Player():

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.destroyed = False
        self.speed = 10

    #method that when call draws the player
    def draw(self):
        pygame.draw.polygon(screen, PURPLE, ((self.x, self.y+self.height),(self.x +self.width, self.y+self.height),(self.x + (0.5 * self.width), self.y)))

    #Returns player X pos
    def get_x(self):
        return self.x

    #Returns player Y pos
    def get_y(self):
        return self.y

    #Returns player Width
    def get_width(self):
        return self.width

    #Returns player Height
    def get_height(self):
        return self.height

    #update is run rpeatedly so repeating methods and checks are run in here
    def update(self):
        key = pygame.key.get_pressed()

        #code checks if movement keys are pressed and alters charectors position acoringly
        if key[pygame.K_LEFT] and self.x > 0:
            self.x = self.x - self.speed
        if key[pygame.K_RIGHT] and ((self.x + self.width) < screen_width):
            self.x = self.x + self.speed
        if key[pygame.K_UP] and self.y > 0:
            self.y= self.y - self.speed
        if key[pygame.K_DOWN] and ((self.y + self.width) < screen_width):
            self.y = self.y + self.speed

#Meteor class stores all info on the meteorites
class Meteorite():

    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.destroyed = False
        self.speed = speed

    #method that when call draws the meteor
    def draw(self):
        if not self.destroyed:
            pygame.draw.circle(screen, BROWN, (self.x,self.y), self.radius)

    #returns X Pos
    def get_x(self):
        return self.x

    #returns Y pos
    def get_y(self):
        return self.y

    #returns radius of that meteor
    def get_radius(self):
        return self.radius

    #returns destroyed
    def get_destroyed(self):
        return self.destroyed

    #changes destroyed
    def set_destroyed(self, status):
        self.destroyed = status

    #tells the program to deduc a life once at the bottom
    def lives(self):
        #check if at the bottom and not destroyed
        if self.y == 500 and self.destroyed == False:

            #updates/removes a life from the players stats
            global player_stats
            player_stats.update_lives(1)

            #sets the meteor to destroyed
            self.set_destroyed(True)

    #update is run rpeatedly so repeating methods are run in here
    def update(self):
        self.move()
        self.lives()

    #moves the meteoor downwards
    def move(self):
        self.y = self.y + self.speed

#Laser class which is used to shoot the meteors
class Laser():

    #laser constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 5
        self.speed = 5

    #method that when call draws the laser
    def draw(self):

        #draws the laser
        pygame.draw.line(screen, GREEN, (self.x, self.y), (self.x, self.y + self.height))

    #Gets y position
    def get_y(self):
        return self.y


    #update is run rpeatedly so repeating methods are run in here
    def update(self,):

        #runs movement function
        self.move()

        #Runs collision check function
        self.collide()

    #Moves the laser upwards
    def move(self):
        self.y = self.y - self.speed

#checks is a meteor has collided with a laser
    def collide(self):
        #loops through all the meteorites
        for Meteorite in Meteorites:
            #checks if any collide with a laser and arent already hit
            if self.x <= Meteorite.get_x() + Meteorite.get_radius() and \
                self.x >= Meteorite.get_x() - Meteorite.get_radius() and \
                self.y + self.height >= Meteorite.get_y() - Meteorite.get_radius() and \
                self.y  <= Meteorite.get_y() + Meteorite.get_radius() and Meteorite.get_destroyed() == False:

                    #sets it to destroyed
                    Meteorite.set_destroyed(True)

                    #updates/increases the players score
                    global player_stats
                    player_stats.update_score(20)

#used to store all information on the players performance
class Player_stats():

    def __init__(self, name):

        #stores the players name score and current lives
        self.name = name
        self.score = 0
        self.lives = 10

    #updates/adds to the score when a player hits a meteorite
    def update_score(self, num):
        self.score = self.score + num

    #updates/decreases a players lives when a meteor reaches the bottom
    def update_lives(self, num):
        self.lives = self.lives - num

    #returns the current score
    def get_score(self):
        return self.score
    #adds the time bonus to the users score
    def add_bonus(self,bonus):
        self.score = self.score + (int(bonus) * 20)

#used to store the leaderboard data
class Leaderboard_Pos():

    # stores record data
    def __init__(self, name, score):
        self.name = name
        self.score = score
        

#----------------------------------------------  FUNCTIONS   ----------------------------------------------------#



#Draw function is used to run the draw() method on multiple objects in the program when the Game is running
def draw():
    screen.fill((0,0,0))

    #draws text at the top
    draw_text('SCORE: ' + str(player_stats.score), font, RED, screen, 100, 20)
    draw_text('LIVES: ' + str(player_stats.lives), font, RED, screen, 300, 20)

    #draws player
    player1.draw()

    #loops through lasers array and draws all laser objects
    for laser in lasers:
        laser.draw()

    #loops through lasers array and draws all laser objects
    for Meteorite in Meteorites:
        Meteorite.draw()

    pygame.display.flip()


#update function is used to run the update() method on multiple objects in the program when the Game is running
def update():
    #updates the players character
    player1.update()

    #loops through lasers array and updates all laser objects
    for laser in lasers:
        laser.update()
        if laser.get_y() < 0:
            del laser

    #loops through meteorites array and updates all meteorite objects
    for Meteorite in Meteorites:
        Meteorite.update()
        if Meteorite.get_destroyed() == True:
            del Meteorite

# Draw text function is used to draw text across program without repeating code
def draw_text(text, font, color, surface, x, y):
    font = pygame.font.SysFont("Arial", 15)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# ------------------------------------------------- MAIN CLASSES FOR GAME SCREENS ---------------------------------------------------------- #


# The Main menu allows users to access the game and help menu
def main_menu():
    while True:

        #Draws Text
        screen.fill((0,0,0))
        draw_text('METEORITES', font, (GREEN), screen, 220, 20)
        draw_text('START', font, (GREEN), screen, 250, 100)
        draw_text('HELP', font, (GREEN), screen, 250, 200)
        draw_text('START', font, (GREEN), screen, 50, 120)
        draw_text('HELP', font, (GREEN), screen, 50, 220)

        #Defines Buttons 1&2
        button_1 = pygame.Rect(125, 100, 250, 50)
        button_2 = pygame.Rect(125, 200, 250, 50)

        #gets current positions of the mouse pointer
        mx, my = pygame.mouse.get_pos()

        #if button 1 is clicked the game code is run
        if button_1.collidepoint((mx, my)):
            if click:
                game_run()

        #if button 2 is clicked the Help page code is run
        if button_2.collidepoint((mx, my)):
            if click:
                help_page()

        #draws the 2 buttons
        pygame.draw.rect(screen, (PURPLE), button_1)
        pygame.draw.rect(screen, (PURPLE), button_2)

        click = False


        for event in pygame.event.get():
         
            #Closes window if cross is pressed
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #Closes window if ESSC is pressed
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            #checks if mouse is clicked
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


#help page displays the controls and the objective of the game for new players
def help_page():
    running = True
    while running:
        screen.fill((0,0,0))

        #Displays All help text
        draw_text('HELP PAGE', font, RED, screen, 220, 20)
        draw_text('Controls', font, GREEN, screen, 231, 80)
        draw_text('Use arrow keys to control the ship the shooting is done automatically', font, GREEN, screen, 30, 100)
        draw_text('Objective', font, GREEN, screen, 225, 160)
        draw_text('The objective of the game is to prevent any meteors from getting past you', font, GREEN, screen, 20, 180)
        draw_text('GOOD LUCK PILOT', font, GREEN, screen, 195, 200)
        draw_text('PRESS ESC TO CLOSE HELP', font, (GREEN), screen, 150, 450)


        for event in pygame.event.get():
            #Closes window if cross is pressed
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #Exits help menu to main menu
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)


#Game run is used to display the actual game
#It brings together all the classes and runs them in 1 place
def game_run():

    #strts the start timer
    start_time = time.time()

    #sets time inbetween laser and meteor spawns
    seconds_laser = 0.25
    seconds_meteor = 0.6

    #begins loop
    playing = True
    while playing:


        for event in pygame.event.get():
            #Closes window if cross is pressed
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()

        #Exits Game to main menu
        if key[pygame.K_ESCAPE]:
            playing = False

        #starts the current timer
        current_time = time.time()

        #defines elapsed time since game_run() was called
        elapsed_time = current_time - start_time

        #determines if enought time has passed and spawns a laser
        if elapsed_time > (seconds_laser):
            lasers.append(Laser(player1.get_x() + (player1.get_width()/2),player1.get_y()))
            seconds_laser = seconds_laser + 0.25

        #determines if enought time has passed and spawns a meteor
        if elapsed_time > seconds_meteor:
            Spawn_Generator = random.randint(0,2)
            Type_Generator = random.randint(0,1)
            Meteorites.append(Meteorite(Spawn_Locations[Spawn_Generator][0],Spawn_Locations[Spawn_Generator][1], Meteor_types[Type_Generator][0], Meteor_types[Type_Generator][1]))
            seconds_meteor = seconds_meteor + 0.6

        #once player lives is over breaks loop and calls Game_over()
        #also adds the players time survived bonus to the players score
        if player_stats.lives == 0:
            playing = False
            player_stats.add_bonus(elapsed_time)
            game_over()

        print(Meteorites)
        
        #These are used to run the game
        update()
        draw()
        clock.tick(60)

#Game over displays after all lives are lost
#it displays your points and the leaderboard
def game_over():

    #Creates an array to store records
    Leaderboard = []

    #links to file
    file = open("Leaderboard.txt", "r")

    #loops througheach line being read in
    for line in file:

        #splits lines up
        line = line.strip()
        #splits data by the "," 
        line = line.split(",")
        
        #creates records to store data and appends them to the array
        record = Leaderboard_Pos(line[0],line[1])
        Leaderboard.append(record)

    #closes file when do done
    file.close()

    #Insertion sort
    #stores vallue being sorted
    value = 0

    #used to store the sorting progress
    index = 0

    #loops through the Array
    for i in range(len(Leaderboard)-1):
        #sets value = to current pos
        value = Leaderboard[i]
        #sets index to ccurrent pos
        index = i
        #loopsthrough array to find the correct posfor current score
        while index > 0 and value.score > Leaderboard[index-1].score:
            #moves all values up 1 till correct pos is found
            Leaderboard[index] = Leaderboard[index-1]
            index=index-1
        #the value is set to its correct position
        Leaderboard[index] = value

    #Writes the leaderboard to the file
    file = open("Leaderboard.txt", "w")

    #loops through array of records
    for i in range(len(Leaderboard)):
        #Writes the data back in a readable format
        file.write(Leaderboard[i].name + "," + str(Leaderboard[i].score) + "\n")

    #closes file when done
    file.close()

    running = True
    #starts loop
    while running:
        #Closes window if cross is pressed
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #Closes window if ESC is pressed
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #displays text
        screen.fill((0,0,0))
        draw_text('GAME OVER', font, RED, screen, 225, 20)
        draw_text('Press ESC to close game', font, (GREEN), screen, 175, 450)

        #displays players score
        draw_text('Your total score was: ' + str(player_stats.score), font, GREEN, screen, 190, 50)

        #displays leaderboard
        draw_text('LEADER BOARD', font, GREEN, screen, 205, 100)

       #loops 5 times and draws the data on the screen as text
        for i in range(5):
            #draws name
            draw_text(str(Leaderboard[i].name), font, GREEN, screen, 200, 150 + (i*20))
            #draws score
            draw_text(str(Leaderboard[i].score), font, GREEN, screen, 270, 150 + (i*20))

        pygame.display.update()
        clock.tick(60)



# -------------------------------------------------------- MAIN ---------------------------------------------------- #



#instanciates player
player1 = Player(screen_width/2, screen_height-20, 20, 20)

#instanciates Player_stats to store thier data
player_stats = Player_stats(input("Enter Player name: "))

#runs mennu which links to all other pages
main_menu()
