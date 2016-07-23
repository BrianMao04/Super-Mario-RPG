#########################################
# Programmer: Brian Mao
# Date: 16/06/2014  
# File Name: RPG_Main_Program_Final_Brian_Mao
# Description: This is the main program to the battle system of an RPG game. 
#########################################

import pygame
pygame.init()

from random import randint
from RPG_Classes import*

#-------------------------------
#Game Window Properties
#-------------------------------
HEIGHT = 600                                               #Height of the game window
WIDTH  = 800                                               #Width of the game window

game_window=pygame.display.set_mode((WIDTH,HEIGHT))        #Creates game window

#-------------------------------------
#Colours used throughout the game
#-------------------------------------
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN= (100,255,100)
YELLOW=(255,255,0)
GREY = (200,200,200)                 
PURPLE  = (150,5,255)                   
BLUE= (150,190,220)                 
RED=(255,0,0)

#-----------------
#Text Fonts
#-----------------
genericfont=pygame.font.Font('freesansbold.ttf', 100)
menufont=pygame.font.Font('freesansbold.ttf', 25)
enemyfont=pygame.font.Font('freesansbold.ttf', 20)
creditsfont1=pygame.font.Font('freesansbold.ttf', 30)
creditsfont2=pygame.font.Font('freesansbold.ttf', 60)


menuxvalue=255
menuyshiftvalue=15

textlevel1= 400
textlevel2=500

#Basic Functions---------------------------------

#Text Drawing Function
def text(text,cord,genericfont,clr=WHITE):     
    text=str(text)
    fontsurface= genericfont.render(text, False, clr)   #Render the text onto the new surface
    fontrect=fontsurface.get_rect()                     #Get boundaries of text surface
    fontrect.center=cord                                #Center of text surface becomes cord parameter
    game_window.blit(fontsurface,fontrect)              #Copy font surface into game window

def loadpicture(filepath, clr=WHITE):                   #Function that loads and scales pictures, as well as making them transparent
    picture = pygame.image.load(filepath)               #Load picture
    picture.set_colorkey(clr)                           #Makes picture transparent
    picture = picture.convert_alpha()                   #Convert image pixel format
    picture= pygame.transform.scale(picture,(70,90))
    return picture


#Enemy Functions+ Death checks----------------------------
def spread(enemies):                                   #Resets the Y values of the enemies when they are to be redrawn
    yincrement=25
    for enemy in enemies:
        enemy.Y=yincrement
        yincrement+=120
        
def randomlygenerateenemies(enemy):                    #Generates a set of 3 different types of enemies randomly depending on wave count
    global playbattletheme2                            #Also adds corresponding enemy to the propper list

    pyevents = pygame.event.get()
    keys = pygame.key.get_pressed()
    
    choices = earlywaveenemylist[:]
    choices2 = laterwaveenemylist[:]
    for i in range(3):
        if wavecount<=5: 
            result=random.choice(choices)
            addenemytolist(result)
            addenemypicturetolist(earlywaveenemypicturelist[earlywaveenemylist.index(result)])
            choices.remove(result)
            
        if wavecount>5 and wavecount<10:
            result=random.choice(choices2)
            addenemytolist(result)
            addenemypicturetolist(laterwaveenemypicturelist[laterwaveenemylist.index(result)])
            choices2.remove(result)

    if wavecount==10 and keys[pygame.K_ESCAPE]==False:  #Final battle appears on wave 10
        battletheme2.stop()
        finalbattletheme.play(-1)
        finalbattletheme.set_volume(0.1)

        for enemy in (alex, alan, lisa):
            addenemytolist(enemy)

        for enemypicture in (alexpicture1,alanpicture,lisapicture):
            addenemypicturetolist(enemypicture)
        
        game_window.blit(finalbosspromptpicture,(0,0))  #Display final boss prompt
        pygame.display.update()
        pygame.time.delay(3000)                         #Delay to percieve image
        
    if wavecount<=10:
        spread(enemies)
            
        for enemy in enemies:
            enemy.reset()
            
        makeenemybuttons(enemies)
    
def addenemytolist(enemy):
    enemies.append(enemy)
    
def addenemypicturetolist(picture):
    enemypictures.append(picture)

def makeenemybuttons(enemies):                         #Creates an Enemybutton object for every enemy in the list with incremented Y coordinates
    yincrement=50
    for i in range(len(enemies)):
        enemybuttons.append(Enemybutton("            ", (WIDTH/2+250-20), yincrement)) 
        yincrement+=120
        
def checkplayerdeath(mario):
    if mario.health<=0:                                #Makes the health equal to 0 instead of a negative value for nicer outputs
        mario.health=0  
        return True
    else:
        return False
        
def checkenemydeath(enemy):                            #Removes enemies from the list that have 0 health
    enemybuttons[:] = [enemybuttons[i] for i in range(len(enemybuttons)) if enemies[i].health > 0]
    enemypictures[:] = [enemypictures[i] for i in range(len(enemypictures)) if enemies[i].health > 0]
    enemies[:] = [enemy for enemy in enemies if enemy.health > 0]
    
def checkenemywaveend(enemy):
    if len(enemy)<=0:  
        return True
    else:
        return False
    
def wavetransition():
    global enemiesturn
    
    if len(enemies)<=0:                
        enemiesturn=False                               #Makes it so that the enemies don't already attack you when a new wave is generated
        game_window.fill(RED) 
        text("Next Wave",((WIDTH/2),300),genericfont)   #Alert player of another wave of enemies
        pygame.display.update()
        pygame.time.delay(1000)                         #Delay to percieve image

        randomlygenerateenemies(enemies)
        

    
#Redraw Game Screen Functions-------------------------------------------

def redraw_game_window(surface, buttons, enemy):         #Main redraw function that makes most outputs
    text("Hero Health", (textlevel1,textlevel1), enemyfont,RED)
    text(str(mario.health) + " / "+ str(mario.maxhealth),(textlevel1,textlevel1+50),enemyfont)
    text("Magic Points", (textlevel1,textlevel2), enemyfont,PURPLE)
    text(magicpoints,(textlevel1,textlevel2+50),enemyfont)
    text("Wave # "+ str(wavecount),(textlevel1+300,textlevel1), enemyfont,YELLOW )
    
    for button in buttons:
        button.update(pyevents)                          #Update button state for hovering+clicking
        button.draw(surface)    

    for enemy in enemies:                                #Outputs numerical values of enemy healths
        text(enemy.health,(760,enemy.Y+30),enemyfont)

    pygame.display.update()

def redrawenemies(surface):                              #Outputs pictures of enemies to be redrawn   
    for i in range(len(enemypictures)):
        surface.blit(enemypictures[i], ((WIDTH/2+250),enemies[i].Y))
    
def redrawplayer(surface):                               #Outputs picture of Mario 
    surface.blit(mariopicture1, ((WIDTH/2-100),150))

def redrawhealthbars(enemies):                           #Outputs health bars next to enemies that empties as their health lowers
    yincrement=50
    healthbarlength=75
    for enemy in enemies:
        fillincrement=enemy.health/float(enemy.defaulthealth)  #Calculates the amount of the health bar to fill
        
        pygame.draw.rect(game_window,RED,((WIDTH/2+375),enemy.Y,10,healthbarlength),0 )  
        pygame.draw.rect(game_window,PURPLE,((WIDTH/2+375),enemy.Y,10,healthbarlength-(healthbarlength*fillincrement)),0 ) #Portion of the health bar that changes as the enemy's health lowers
        yincrement+=120

def generalscreenupdates():                             #Package of several different redraw commands
    redrawenemies(game_window)
    redrawplayer(game_window)
    redrawhealthbars(enemies)
    redraw_game_window(game_window,(attackbutton,spellbutton,itembutton, backbutton),enemies)
    
#Redraw Attack Animation Functions-------------------------------------------

def redrawmarioattack(game_window):
        pygame.draw.rect(game_window,BLUE,((WIDTH/2-100),150,100,100),0 )   #Draw over the location of the mario picture with a blue rectangle to clear the last image
        game_window.blit(mariopicture2,((WIDTH/2-100),150)) 
        pygame.draw.rect(game_window, BLUE, (745, 25,  27, 400),0)          #Draw over the location of enemy health values with a blue rectangle to clear previous ouputted values

        for i in range(len(enemies)):
            if enemies[i].health<0:                                        #Used to avoid printing a negative enemy health value
                enemies[i].health=0
                
        for enemy in enemies:                                              #Output enemy health values after attack damage calculation
            text(enemy.health,(760,enemy.Y+30),enemyfont)
            
        redrawhealthbars(enemies) 
        redraw_game_window(game_window,(attackbutton,spellbutton, itembutton), enemies) 

        pygame.time.delay(500)                                              #Delay for visual impact

def resetYbullets(Y):                                                       #Resets Y values of bullets
    bullet.Y = Y
    if bullet.Y==25:
        bullet.speedy=5                                                     #Bullets Y speed changes at a different rate to animate a diagonal bullet
        
    elif bullet.Y==145:
        bullet.speedy=0.5
        
    elif bullet.Y==265:
        bullet.speedy=-3.5

def resetXbullets():                                                        #Resets X values of bullets
    bullet.X= (WIDTH/2+250)
        
def drawingbullet(game_window):
    for i in range(len(enemies)):                                           #Draws a bullet coming from each enemy still present on screen
        resetYbullets(enemies[i].Y)   
        resetXbullets()
    
        while bullet.X >=(WIDTH/2-50):                                      #Continues drawing bullet it until it'ds location is the same as the Mario picture
            bullet.update()                                                 #Creates all propper outputs 
            game_window.fill(BLUE)
            bullet.draw(game_window)
            redrawenemies(game_window)
            redrawplayer(game_window)
            redrawhealthbars(enemies)
            redraw_game_window(game_window,(attackbutton,spellbutton, itembutton), enemies)
            pygame.time.delay(20)   
        
        enemies[i].attack(mario)                                            #Lowers Mario health after the anikation is complete
        
        if mario.health<=0:                                                 #Makes the health equal to 0 instead of a negative value for nicer outputs
            mario.health=0
            break  
        
def redrawenemyattack(game_window):                                         #Function that controls animation during enemy attacks
    drawingbullet(game_window)
    pygame.draw.rect(game_window, BLUE, (300,420,300,60),0)                 #Draws a blue box over the player's health value to clear the last output
    redraw_game_window(game_window,(attackbutton,spellbutton, itembutton), enemies) 
    pygame.time.delay(50)
    

def redrawattackwindow(game_window, buttons, enemy):                        #Outputs after player clicks the attack button
    text("Hero Health", (textlevel1,textlevel1), enemyfont,RED)
    text(str(mario.health) + " / "+ str(mario.maxhealth),(textlevel1,textlevel1+50),enemyfont)
    text("Magic Points", (textlevel1,textlevel2), enemyfont,PURPLE)
    text(magicpoints,(textlevel1,textlevel2+50),enemyfont)
    text("Wave # "+ str(wavecount),(textlevel1+300,textlevel1), enemyfont,YELLOW )
    
    redrawhealthbars(enemies)                                                #Updates the health bars after damage calculation

    for enemy in enemies:
        text(enemy.health,(760,enemy.Y+30),enemyfont)
        redrawenemies(game_window)
        redrawplayer(game_window)
        redrawenemies(game_window)

        for button in buttons:                                                #Update and draws enemy buttons
            button.update(pyevents)                                           #Update button state for hovering+clicking
            attackbutton.hovering=True                                        #Keeps the attack button highlighted for visual impact
            button.draw(game_window)

        for enemy in enemybuttons:                                            #Updates and draws enemy pictures
            enemy.update(pyevents)
            enemy.draw(game_window)

        pygame.display.update()

#Redraw Menus--------------------------------------------------------------

def redrawitemmenu(game_window, buttons):                                     #Outputs the item selection menu
    pygame.draw.rect(game_window,GREEN,(10,30,260,275),0 )                    #Item menu background

    for button in buttons:                                                    #Draws and updates item buttons
        button.update(pyevents)
        button.draw (game_window)  

    pygame.draw.rect(game_window,RED,(245,40,20,25),0 ) 
    text("#" , (menuxvalue,55), menufont,BLACK) 
    
    text(numberofpotions, (menuxvalue,70+menuyshiftvalue), menufont,GREY)     #Output number of remaining items
    text(numberofsuperpotions , (menuxvalue,150+menuyshiftvalue), menufont,GREY)
    text(numberofbombs, (menuxvalue,230+menuyshiftvalue), menufont,GREY)

    pygame.display.update()

def redrawspellmenu(game_window, buttons):                                   #Outputs the spell selection menu   
    pygame.draw.rect(game_window,YELLOW,(10,30,260,275),0 )                  #Spell menu background

    for button in buttons:                                                   #Draws and updates spell buttons
        button.update(pyevents)
        button.draw (game_window)  

    pygame.draw.rect(game_window,RED,(230,35,38,35),0 )                      #Background for "MP" text output
    text("MP" , (250,55), menufont,GREY)
    
    text(fireball.cost, (menuxvalue,70+menuyshiftvalue), menufont,GREY)      #Output the magic point costs for each spell
    text(lightning.cost , (menuxvalue,150+menuyshiftvalue), menufont,GREY)
    text(iceball.cost, (menuxvalue,230+menuyshiftvalue), menufont,GREY)
    
#Spells + Items + Running Mode Function-----------------------------------------------------

def redrawitemusage(game_window):                                            #Ouputs execution of an item
    pygame.draw.rect(game_window, BLUE, (745, 25,  27, 400),0)               #Draw over the location of enemy healths with a blue rectangle to clear ouputted values
    for i in range(len(enemies)):
        if enemies[i].health<0:                                              #Used to avoid printing a negative enemy health value
            enemies[i].health=0
            
    redrawhealthbars(enemies)         
    pygame.draw.rect(game_window, BLUE, (300,420,200,100),0)                 #Draw over the location of Mario's health value with a blue rectangle to clear the last value
    redraw_game_window(game_window,(attackbutton,spellbutton, itembutton), enemies)
    pygame.display.update()
            
    pygame.draw.rect(game_window,BLUE,((WIDTH/2-100),150,100,100),0 )        #Draw over the location of the mario picture with a blue rectangle to clear the last image
    game_window.blit(mariopicture3,((WIDTH/2-100),150))
    pygame.display.update()
    pygame.time.delay(1000)

def redrawspellusage(game_window, spell):                                    #Ouputs execution of a spell
    
    for i in range(len(enemies)):
        if enemies[i].health<0:                                              #Used to avoid printing a negative enemy health value
            enemies[i].health=0
            
    redrawhealthbars(enemies)    
    pygame.draw.rect(game_window, BLUE, (300,530,200,100),0)                 #Draw over the location of he magic points with a blue rectangle to clear the last value

    redraw_game_window(game_window,(attackbutton,spellbutton, itembutton), enemies)
    pygame.display.update()
            
    pygame.draw.rect(game_window,BLUE,((WIDTH/2-100),150,100,100),0 )        #Draw over the location of the mario picture with a blue rectangle to clear the last image
    game_window.blit(mariopicture4,((WIDTH/2-100),150))
    pygame.display.update()

    pygame.draw.rect(game_window,BLUE,((WIDTH/2+100),150,100,100),0 )        #Draw over the location of the spell picture with a blue rectangle to clear the last image
    game_window.blit(spell,((WIDTH/2+100),150))                              #Output spell picture
    redrawenemies(game_window)
    pygame.display.update()
    
    pygame.time.delay(1000)                                                  #Delay for visual impact

def executespell(game_window, spelltype, spelltypepicture, enemybuttons):    #Calculates enemy health values after spell is used
    global choosingspell, magicpoints, inPlay, spelltargetselectionmode, playersturn, enemiesturn
    
    while choosingspell==True:
        pyevents = pygame.event.get()
        keys = pygame.key.get_pressed()                                       # Act upon key events
        
        backbutton.update(pyevents)                                           #Updates and draws the back button
        backbutton.draw(game_window)
        
        if keys[pygame.K_ESCAPE]:                                             #Closes the game if ESC key is pressed               
                choosingspell=False
                spelltargetselectionmode=False  
                inPlay = False
                playersturn = True
                enemiesturn = False
                
        if backbutton.pressed==True:                                           #Exits the while loop if back button is pressed
            choosingspell=False
            spelltargetselectionmode=False
            playersturn = True
            enemiesturn = False

        for enemy in enemybuttons:                                            #Updates and draws enemy buttons
            enemy.update(pyevents)
            enemy.draw(game_window)
            
        for i in range(len(enemybuttons)):
            if enemybuttons[i].pressed:                                       #Enemies share same index as enemybuttons
                spelltype.use(enemies[i], spelltype.damagevalue)  

                game_window.fill(BLUE)                                        #Clears the screen before ouputting the spell execution
                redrawspellusage(game_window, spelltypepicture)
                game_window.fill(BLUE)
                                     
                magicpoints-=spelltype.cost                                   #Subtracts spell cost from magic points value
                choosingspell=False                                           #Exits the while loop in this function

        pygame.display.update()


def runningmode():                                                            #Mode in-between battle waves where Mario needs to run to the end of the screen
    global marioPic, marioPicNum, marioX, lastkey, inPlay, ESCbuttonpressed
    
    marioX=0                                                                  #Resets Mario X value with each call of the function
    
    while True:
        game_window.fill(WHITE)                                               #Clears screen
        game_window.blit(marioPic[marioPicNum-1], (marioX,HEIGHT-75))         #Output the propper Mario image picture
        events=pygame.event.get()
        keys=pygame.key.get_pressed()
        mariowidth=marioPic[1].get_width()                                    #Gets the width of a standard Mario picture 
        pygame.draw.rect(game_window,BLACK,(doorXvalue,(HEIGHT-75), doorwidth, 75)) #Draws the door at the end of the screen

        pygame.draw.rect(game_window, GREY, (0,(HEIGHT-10),WIDTH, 10))        #Draws the ground
        pygame.draw.rect(game_window, RED, (0,0,WIDTH, HEIGHT-100))           #Draws the red background
        
        xincrement=50
        barwidth=15
        
        for i in range (15):
            pygame.draw.rect(game_window, YELLOW, (xincrement,0,barwidth, HEIGHT-100) )       #Draws the yellow stripes in the background
            xincrement+=100

        game_window.blit(torchpicture,(WIDTH/2-300,HEIGHT/2))
        game_window.blit(windowpicture,(WIDTH/2-65,HEIGHT/2-130))
        game_window.blit(torchpicture,(WIDTH/2+300,HEIGHT/2))

        
        if keys[pygame.K_ESCAPE]:                                             #Closes the game if ESC key is pressed
            inPlay=False
            ESCbuttonpressed=True
            break

        if keys[pygame.K_LEFT]==True and marioX-mariowidth+20>=0:             #Move Mario as long as he is still within bounds 
            marioPicNum=nextLeftPic[marioPicNum]                              #Output the next Mario picture in the list
            marioX=marioX-marioXspeed                                         #Moves Mario to the left
            lastkey="left"

        elif keys[pygame.K_RIGHT]==True and marioX+mariowidth+20<=WIDTH:      #Move Mario as long as he has not yet entered the "door" 
            marioPicNum=nextRightPic[marioPicNum]                             #Output the next Mario picture in the list
            marioX=marioX+marioXspeed                                         #Moves Mario to the right
            lastkey="right"

        else:
            if lastkey=="left":                                               #Output the propper Mario image if the last key pressed is the left arrow
                marioPicNum=1                                                 #Used to avoid outputting pictures in mid-run while Mario stationary 
            elif lastkey=="right":                                            #Output the propper Mario image if the last key pressed is the right arrow
                marioPicNum=5                                                 #Used to avoid outputting pictures in mid-run while Mario stationary 

        if marioX>=doorXvalue:                                                #Exits running mode if Mario has entered the "door"
            pygame.time.delay(1500)                                           #Delay for visual impact
            break
                
        pygame.time.delay(70)                                                 #Adjusts the speed for smooth animation rate  
        pygame.display.update()

        
#Various Screen Updates--------------------------------------------------------------------

def titlescreen():                                                            #Outputs the titlescreen, which is the firts output when game is run
    global inPlay, skipintro
    
    while inPlay:
        game_window.blit(titlescreenpicture,(0,0))                            #Output image to take up the entire screen
        pyevents=pygame.event.get()
        keys=pygame.key.get_pressed()
        
        startbutton.update(pyevents)                                           #Update start button state for hovering+clicking
        startbutton.draw(game_window)                                          #Draws the start button

        quickstartbutton.update(pyevents)                                      #Update start button state for hovering+clicking
        quickstartbutton.draw(game_window)                                     #Draws the quick start button

        if startbutton.pressed==True:                                          #Exit the while loop after player clicks the button
            break
        
        elif keys [pygame.K_SPACE]:                                            #Proceed onto the game after the space bar is pressed
            break

        elif quickstartbutton.pressed==True:                                  #Exit the while loop and flip boolean flag to skip straight to gameplay
            skipintro=True
            break


        if keys[pygame.K_ESCAPE]:                                             #Exit the game if the ESC key is pressed
            inPlay = False
            skipintro=True
            break
            
        pygame.display.update()
        pygame.time.delay(1)
    
def intro():
    if skipintro==False:                                                      #Execute commands as long as player did not select quick start at the title screen
        
        pyevents=pygame.event.get()
        keys=pygame.key.get_pressed()
            
        if keys[pygame.K_ESCAPE]:                                             #Exit the game if the ESC key is pressed
            inPlay=False

        for pic in intropictures:                                             #Output each image used in the intro, and delay inbetween each output
            game_window.blit(pic, (0, 0))
            pygame.display.update()
            pygame.time.delay(4000)
        
def gameoverscreen():                                                            #Outputs the game over screen
    game_window.fill(BLUE)
    game_window.blit(gameoverpicture,(0,0))
    pygame.display.update()

def endingcutscene():                                                            #Outputs cutscene displayed after completing the game
    alexheight=500
    yincrement=0
    
    while yincrement<=alexheight-60:                                             #Output Mario image going down the screen until he "hits" Alex
        pygame.event.get()
        game_window.fill(BLACK)
        game_window.blit(mariopicture3,((WIDTH/2),yincrement))
        game_window.blit(alexpicture1, ((WIDTH/2),alexheight))
        yincrement+=10                                                           #Increments Mario Y value 
        pygame.time.delay(25)                                                    #Delay for smooth animation
        pygame.display.update()

    while yincrement>=-100:                                                      #Output Mario image going back up and off the screen 
        pygame.event.get()
        game_window.fill(BLACK)
        game_window.blit(mariopicture4, ((WIDTH/2),yincrement))
        game_window.blit(alexpicture2, ((WIDTH/2),alexheight))
        yincrement-=10                                                           #Increments Mario Y value
        pygame.time.delay(25)                                                    #Delay for smooth animation
        pygame.display.update()

    game_window.blit(endingpicture, (0,0))                                       #Ouput the winning screen
    pygame.display.update()
    pygame.time.delay(4000)
    
def displaycredits():                                                           #Credits display sequence
    yincrement=HEIGHT
    seperation=50

    while yincrement>=0-(21*seperation):                                         #Continue scrolling until the last piece of text is at the top of the screen
        game_window.fill(BLUE)
        text("Credits", ((WIDTH/2),yincrement), genericfont,YELLOW)
        
        text("Programmed by: Brian Mao", ((WIDTH/2),yincrement+(2*seperation)), creditsfont1,RED)
        
        text("Music", ((WIDTH/2),yincrement+(4*seperation)), creditsfont1,RED)
        text("Intro: Final Fantasy 6 Dark World", ((WIDTH/2),yincrement+(5*seperation)), enemyfont,BLACK)
        text("Battle Theme 1: Rayman Legends Main Theme", ((WIDTH/2),yincrement+(6*seperation)), enemyfont,BLACK)
        text("Battle Theme 2: Super Smash Bros. Brawl Final Destination", ((WIDTH/2),yincrement+(7*seperation)), enemyfont,BLACK)
        text("Ending Theme: Paper mario The Thousand Year Door The Crystal Stars", ((WIDTH/2),yincrement+(8*seperation)), enemyfont,BLACK)
        text("Game Over Theme: The Legend of Zelda Game over", ((WIDTH/2),yincrement+(9*seperation)), enemyfont,BLACK)
             
        text("Art From:", ((WIDTH/2),yincrement+(11*seperation)), creditsfont1,RED)
        text("Hyper Turret Defense", ((WIDTH/2),yincrement+(12*seperation)), enemyfont,BLACK)
        text("Exit Dash", ((WIDTH/2),yincrement+(13*seperation)), enemyfont,BLACK)
        text("Skeleton Rush", ((WIDTH/2),yincrement+(14*seperation)), enemyfont,BLACK)
        text("Mario's Raining Coin Collector", ((WIDTH/2),yincrement+(15*seperation)), enemyfont,BLACK)
             
        text("Special Thanks To: Kenneth Sinder, Sam Raisbeck, Trey Robinson, Mr. Grigorov", ((WIDTH/2),yincrement+(17*seperation)), enemyfont,PURPLE)

        text("Thanks for Playing!", ((WIDTH/2),yincrement+(20*seperation)), creditsfont2,WHITE)

        yincrement-=10                                                          #Increment the Y values of the text to scroll up the screen
        pygame.time.delay(50)                                                   #Delay for visual impact
        pygame.display.update()
        
def displaylevelup():                                                           #Output stat values that change after a level up
        game_window.fill(GREEN)
        text("LEVEL UP!",((WIDTH/2),100),genericfont)
        text("Attack rose to " +str(mario.atkpower),((WIDTH/2),200),menufont, BLACK)
        text("Defense increased to "+ str(mario.defense),((WIDTH/2),300),menufont, BLACK)
        text("Max health goes up to "+ str(mario.maxhealth) ,((WIDTH/2),400),menufont, BLACK)
        text("You magic points increased to "+ str(magicpoints) ,((WIDTH/2),500),menufont, BLACK)
        pygame.display.update()
        pygame.time.delay(3000)                                                 #Delay for visual impact


def levelup():                                                                  #Adjust stat values of the player depending on the wavecount
    global magicpoints
    skiplevelup=False
    
    if wavecount<10:                                                            #Checks if the it is before the final battle     
        
        if (wavecount)==10:                                                     #Final level up before final battle
            mario.atkpower+=10   
            mario.defense+=10  
            mario.health+=200
            mario.maxhealth+=100
            magicpoints+=50
            
        elif (wavecount)==6:                                                    #Extra stat increases than usual half way through the game
            mario.atkpower+=10    
            mario.defense+=10  
            mario.health+=200
            mario.maxhealth+=100
            magicpoints+=50
            
        elif (wavecount) % 2 == 0:                                             #Increase stats going into every even wave number
            mario.atkpower+=10   
            mario.defense+=5  
            mario.health+=50
            mario.maxhealth+=100
            magicpoints+=10
            
        else:
            skiplevelup=True   
            
        if skiplevelup==False:                                                 #Alert the player of their new stat values as long as they increased 
            displaylevelup()
    

#----------------------Main Program-------------------------------------------

#Character creations                    
mario=Hero(500,25,0,500,"mario.bmp")   

snake=Enemy(5,20,20, "snake.png")  
tank=Enemy(30,20,20,"tank.png")
goomba=Enemy(15,20,20,"goomba.bmp")
tankyellow=Enemy(20,20,20,"tankyellow.png")
tankblue=Enemy(25,20,20,"tankblue.png")

glueturret=StrongEnemy(40,20,20,"glueTurret.png")
tankred=StrongEnemy(45,20,20,"tankred.png")
eightshot=StrongEnemy(50,20,20,"eightShotTurret.png")
fireturret=StrongEnemy(55,20,20,"fireTurret.png")
tower=StrongEnemy(60,20,20,"tower.png")


alex=StrongEnemy(99,50,20, "alexfront.png")
alan=StrongEnemy(80,50,20, "alanfront.png")
lisa=StrongEnemy(80,50,20, "lisafront.png")

############################################

#Loading Up and Converting Pictures
mariopicture1=loadpicture(mario.filepath)
mariopicture2=loadpicture("mariothrow.bmp")
mariopicture3=loadpicture("marioduck.bmp")
mariopicture4=loadpicture("mariojumpattack.bmp")

snakepicture=loadpicture(snake.filepath)
tankpicture=loadpicture(tank.filepath)
goombapicture=loadpicture(goomba.filepath)
tankyellowpicture=loadpicture(tankyellow.filepath)
tankbluepicture=loadpicture(tankblue.filepath)
tankredpicture=loadpicture(tankred.filepath)
eightshotpicture=loadpicture(eightshot.filepath)
fireturretpicture=loadpicture(fireturret.filepath)
towerpicture=loadpicture(tower.filepath)
glueturretpicture=loadpicture(glueturret.filepath)

alexpicture1=loadpicture(alex.filepath)  
alexpicture2=loadpicture("alexhurt.png")
alanpicture=loadpicture(alan.filepath)
lisapicture=loadpicture(lisa.filepath)

fireballpicture=loadpicture("fireball.bmp")
iceballpicture=loadpicture("iceball.bmp", BLACK)
lightningpicture=loadpicture("lightning.bmp", BLACK)

torchpicture=loadpicture("torchlit.png")
windowpicture=loadpicture("window.png")
windowpicture= pygame.transform.scale(windowpicture,(210,230))

titlescreenpicture=pygame.image.load("MarioTitleScreen.png")
titlescreenpicture= pygame.transform.scale(titlescreenpicture,(WIDTH,HEIGHT))

gameoverpicture=pygame.image.load("mariogameover.bmp")
gameoverpicture= pygame.transform.scale(gameoverpicture,(WIDTH,HEIGHT))


intropictures = []
for i in range(6):
    intropictures.append(pygame.image.load('intro' + str(i) + '.png'))
    intropictures[-1] = pygame.transform.scale(intropictures[-1], (WIDTH, HEIGHT))

finalbosspromptpicture=pygame.image.load("finalbossapproaching.png")
finalbosspromptpicture= pygame.transform.scale(finalbosspromptpicture,(WIDTH,HEIGHT))

endingpicture=pygame.image.load("ending.png")

########################################

#Various enemy lists
enemies=[]
enemybuttons=[]
enemypictures=[]

earlywaveenemylist=[snake,tank,goomba,tankyellow,tankblue]
earlywaveenemypicturelist=[snakepicture,tankpicture,goombapicture,tankyellowpicture,tankbluepicture]

laterwaveenemylist=[glueturret,tankred,eightshot,fireturret,tower]
laterwaveenemypicturelist=[glueturretpicture,tankredpicture,eightshotpicture,fireturretpicture,towerpicture]

#Bullet Creation
bullet = Bullet(WIDTH/2+250, -999, -10,0,"bullet.png")
bullet_index = 0

#Button creations
attackbutton=Button("Attack", 50,350)
spellbutton=Button("Spells", 50,425)
itembutton=Button("Items", 50,500)

backbutton=Button("Back", (WIDTH/2-125), 40)
startbutton=Button("Start", (WIDTH-150),400)
quickstartbutton=Button("Quick Start", (WIDTH-150),500)
retrybutton=Button("Retry", (WIDTH-150),50)

fireballbutton=Itembutton("Fire",80,70)
lightningbutton=Itembutton("Lightning", 80, 150)
iceballbutton=Itembutton("Ice",80,230)

potionbutton=Itembutton("Potion",80,70)
superpotionbutton=Itembutton("Super Potion", 80,150)
bombbutton=Itembutton("Bomb", 80, 230)

#Spell Creations
fireball=Spell(50,20)
iceball=Spell(20,10)
lightning=Spell(35,15)


#Item Creations
potion=Healingitem(200)
superpotion=Healingitem(300)
bomb=Damageitem(50)


#Soundtrack Creations
introtheme=Sound("finalfantasy6.mp3")
introtheme.set_volume(0.5)

battletheme1=Sound("raymanmain.mp3")
battletheme2=Sound("supersmashbros.mp3")
finalbattletheme=Sound("soniccolors.mp3")
gameovertheme=Sound("zelda.mp3")
endingtheme=Sound("papermario.mp3")


#Boolean Flags
inPlay=True
skipintro=False
outputgeneraldisplays=True

playersturn=True
enemiesturn=False

attackselectionmode=False
itemselectionmode=False
spellselectionmode=False
spelltargetselectionmode=False

fireballpath=False
iceballpath=False
lightningpath=False

choosingspell=False

battletheme1playing=False
battletheme2playing=False
battlethemehaschanged=False

ESCbuttonpressed=False

playerlost=False


#Game Values
numberofpotions=5
numberofsuperpotions=2
numberofbombs=2
magicpoints=25
wavecount=1


#Mario Animation Picture Variables 
marioPic=[0]*12

for i in range(12):
    marioPic[i]=pygame.image.load("pic" + str(i+1) + ".bmp")

nextLeftPic=[2, 3, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2]
nextRightPic=[5, 5, 5, 5, 6, 7, 8, 6, 5, 5, 5, 5]

marioDir="left"
marioPicNum=1

lastkey="left"

marioX=(WIDTH/2)
marioXspeed=20

doorXvalue=WIDTH-100
doorwidth=50

########################################################

#-------------------Main Program---------------------------------
pyevents=pygame.event.get()

introtheme.play(-1)                                                             #Intro music begins as soon as the program as run
titlescreen()

intro()                                                                         #Intro plays after titlescreen is exited
introtheme.stop()                                                               #Intro music stops after intro is over

battletheme1.play(-1)                                                           #The first battle theme plays after the intro music stops
battletheme1.set_volume(0.9)
battletheme1playing=True

game_window.fill(WHITE)                                                         #Clear the screen
runningmode()                                                                   #Mode that player enters before each battle


randomlygenerateenemies(enemies)                                                #Start the game with a set of enemies generated

#-----------------------Main Game Loop--------------------------
while inPlay==True:
    game_window.fill(BLUE)                                                      #Clear the Screen
    pyevents=pygame.event.get()                                                 #Check for events
    keys = pygame.key.get_pressed()                                             # Act upon key events
    
    if keys[pygame.K_ESCAPE]:                                                   #Closes the game          
        inPlay = False                        

    if attackbutton.pressed==True:                                              #Game mode will differ depending on the button player clicks
        attackselectionmode=True

    if itembutton.pressed==True:
        itemselectionmode=True

    if spellbutton.pressed==True:
        spellselectionmode=True
        
        
#Attack Target Selection Mode----------------------------
    while attackselectionmode==True:
        pyevents = pygame.event.get()
        keys = pygame.key.get_pressed()
        redrawattackwindow(game_window,(attackbutton,spellbutton,itembutton, backbutton),enemies) #General outputs during this mode
        
        if keys[pygame.K_ESCAPE]:                                               #Closes the game
            attackselectionmode=False
            inPlay = False
            
        if backbutton.pressed==True:                                            #Exits the mode if a player clicks this button, and reverts back to the main game loop
            attackselectionmode=False

        pygame.display.update()
            
        for i in range(len(enemybuttons)):                                      #Checks if an enemy button is clicked
            if enemybuttons[i].pressed:  
                mario.attack(enemies[i])                                        #Lowers enemy health values accordingly
                redrawmarioattack(game_window)                                  #Output attack animation
                
                playersturn = False                                             #Player's turn ends after an attack
                enemiesturn = True                                              #Enemies' turn begins after an attack
                attackselectionmode=False                                       #Exits this mode
                
        checkenemydeath(enemies)                                                #Removes any enemies with no health remaining from the battle
        redrawenemies(game_window)                                              #Draw enemies remaining
                
        if checkenemywaveend(enemies)==True:                                    #Procedure if no enemies are left with any health in the wave
            wavecount+=1
            levelup()
            runningmode()                                                       #Enter running mode after each wave
            
            if wavecount<=10 and ESCbuttonpressed==False:                       #Perform a regular wave transition as long as player has not yet beaten the final battle
                wavetransition()
           
            
#Item Selection Mode------------------------------------------
    while itemselectionmode==True:
        pyevents = pygame.event.get()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:                                                #Closes the game
            itemselectionmode=False 
            inPlay = False

        if potionbutton.pressed==True and numberofpotions>0:                     #Checks if potions are used
            potion.use(mario, potion.healvalue)  
            
            if mario.health>mario.maxhealth:                                     #Limits the player's health to their maximum health value
                mario.health=mario.maxhealth

            redrawitemusage(game_window)                                         #Updates the screen
            
            numberofpotions-=1                                                   #Adjusts value
            itemselectionmode=False                                              #Exits the mode
            playersturn = False                                                  #End player's turn after using an item
            enemiesturn = True                                                   #Enemies' turn begins afterwards

        if superpotionbutton.pressed==True and numberofsuperpotions>0:           #Checks if super potions are used
            superpotion.use(mario, superpotion.healvalue)
            if mario.health>mario.maxhealth:
                mario.health=mario.maxhealth
                     
            redrawitemusage(game_window)                                         #Updates the screen
            
            numberofsuperpotions-=1                                              #Adjusts value
            itemselectionmode=False                                              #Exits the mode
            playersturn = False                                                  #End player's turn after using an item
            enemiesturn = True                                                   #Enemies' turn begins afterwards

        if bombbutton.pressed==True and numberofbombs>0:                         #Checks if bombs are used
            bomb.use(enemies, bomb.damage) 
            
            redrawitemusage(game_window)                                        #Updates the screen

            numberofbombs-=1                                                    #Adjusts value
            itemselectionmode=False                                             #Exits the mode
            playersturn = False                                                 #End player's turn after using an item
            enemiesturn = True                                                  #Enemies' turn begins afterwards
            
            checkenemydeath(enemies)                                            #Removes any enemies with no health remaining from the battle
            
            generalscreenupdates()                                              #Updates the screen
            
            
            for enemy in enemybuttons:
                enemy.update(pyevents)
                enemy.draw(game_window)

            if checkenemywaveend(enemies)==True:                                #Procedure if no enemies are left with any health in the wave
                wavecount+=1
                levelup()                                                       #Level up if wavecount is a multiple of 3
                
                runningmode()                                                   #Enter running mode after each wave

                if wavecount<=10 and ESCbuttonpressed==False:                   #Perform a regular wave transition as long as player has not yet beaten the final battle
                    wavetransition()
        
        if backbutton.pressed==True:                                            #Exits the mode if back button is pressed and returns to the main game loop
            itemselectionmode=False
            
        if ESCbuttonpressed==False and wavecount<=10:
            generalscreenupdates()                                                  #Updates the screen
            redrawitemmenu(game_window, (potionbutton, superpotionbutton, bombbutton) )  #Outputs the item menu

#Spell Selection Mode-------------------------------------------------------
    while spellselectionmode==True:     
        pyevents = pygame.event.get()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:                                               #Closes the game
            spellselectionmode=False  
            inPlay = False

        if fireballbutton.pressed==True and magicpoints>=fireball.cost:         #Checks if fire spell is selected
            spellselectionmode=False                                            #Exits the mode
            spelltargetselectionmode=True                                       #Enter spell target selection mode
            fireballpath=True                                                   #Indicates the path taking into spell target selection mode

        if iceballbutton.pressed==True and magicpoints >=iceball.cost:          #Checks if ice spell is selected
            spellselectionmode=False                                            #Exits the mode
            spelltargetselectionmode=True                                       #Enter spell target selection mode
            iceballpath=True                                                    #Indicates the path taking into spell target selection mode

        if lightningbutton.pressed==True and magicpoints>=lightning.cost:       #Checks if lightning spell is selected
            spellselectionmode=False                                            #Exits the mode
            spelltargetselectionmode=True                                       #Enter spell target selection mode
            lightningpath=True                                                  #Indicates the path taking into spell target selection mode

        if backbutton.pressed==True:                                            #Exits the mode if the back button is pressed and returns to the main loop
            spellselectionmode=False
            
        generalscreenupdates()                                                  #Updates the screen
        
        redrawspellmenu(game_window, (fireballbutton, iceballbutton, lightningbutton) ) #Outputs the spell manu
#Spell Target Selection Mode--------------------------------------------------------
    while spelltargetselectionmode==True:
        pyevents = pygame.event.get()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:                                               #Closes the game
            spelltargetselectionmode=False  
            inPlay = False

        if fireballpath==True:
            choosingspell=True
            playersturn = False                                                 #End player's turn
            enemiesturn = True                                                  #Enemies turn begins after player chooses a target for their spell
            
            executespell(game_window,fireball,fireballpicture, enemybuttons)    #Deals damage to enemies and displays propper outputs
            
            fireballpath=False                                                  #Reset back to default value
            spelltargetselectionmode=False                                      #Exits mode

            checkenemydeath(enemies)                                            #Removes any enemies with no health remaining from the battle
            generalscreenupdates()                                              #Updates the game screen

            if checkenemywaveend(enemies)==True:                                #Procedure if no enemies are left with any health in the wave
                wavecount+=1
                levelup()                                                       #Level up if wavecount is a multiple of 3
                
                runningmode()
                if wavecount<=10 and ESCbuttonpressed==False:                   #Enter running mode after each wave
                    wavetransition()                                            #Perform a regular wave transition as long as player has not yet beaten the final battle
            
        if iceballpath==True:
            choosingspell=True
            playersturn = False                                                #End player's turn
            enemiesturn = True                                                 #Enemies turn begins after player chooses a target for their spell
            
            executespell(game_window,iceball,iceballpicture, enemybuttons)     #Deals damage to enemies and displays propper outputs
            
            iceballpath=False                                                  #Reset back to default value
            spelltargetselectionmode=False                                     #Exits mode


            checkenemydeath(enemies)                                           #Removes any enemies with no health remaining from the battle
            generalscreenupdates()                                             #Updates the screen
            
            if checkenemywaveend(enemies)==True:                               #Procedure if no enemies are left with any health in the wave
                wavecount+=1
                levelup()                                                      #Level up if wavecount is a multiple of 3
                runningmode()
                if wavecount<=10 and ESCbuttonpressed==False:                  #Enter running mode after each wave
                    wavetransition()                                           #Perform a regular wave transition as long as player has not yet beaten the final battle
 
                    
        if lightningpath==True:
            choosingspell=True
            playersturn = False                                                #End player's turn
            enemiesturn = True                                                 #Enemies turn begins after player chooses a target for their spell
            
            executespell(game_window,lightning,lightningpicture, enemybuttons) #Deals damage to enemies and displays propper outputs
            
            lightningpath=False                                                #Reset back to default value
            spelltargetselectionmode=False                                     #Exits mode


            checkenemydeath(enemies)                                            #Removes any enemies with no health remaining from the battle
            generalscreenupdates()                                              #Updates the screen

            if checkenemywaveend(enemies)==True:                                #Procedure if no enemies are left with any health in the wave
                wavecount+=1
                levelup()                                                       #Level up if wavecount is a multiple of 3
                runningmode()
                
                if wavecount<=10 and ESCbuttonpressed==False:                   #Enter running mode after each wave
                    wavetransition()                                            #Perform a regular wave transition as long as player has not yet beaten the final battle
                    
        checkenemydeath(enemies)                                                #Removes any enemies with no health remaining from the battle
        if ESCbuttonpressed==False:
            generalscreenupdates()                                              #Updates the screen
        
#Enemies' Turn---------------------------------------------
        
    if playersturn==False and enemiesturn==True and ESCbuttonpressed==False and wavecount<=10 : 
 
        redrawenemyattack(game_window)                                          #Allow enemies to attack
        enemiesturn=False                                                       #Enemies turn ends after thay all attack
        playersturn=True                                                        #Player's turn begins again after the enemies' turn ends
        
#Game Over Check------------------------------------------------
    if checkplayerdeath(mario)==True:                                           #Check if the player's health becomes 0
        playerlost=True
        if battletheme1playing==True:                                           #Stop the first battle theme if it is playing
            battletheme1.stop()
        elif battletheme2playing==True:                                         #Stop the second battle theme if it is playing
            battletheme2.stop()
        
        pygame.draw.rect(game_window, BLUE, (300,420,300,60),0)                 #Draws a blue box over player's health output to clear the last output
        pygame.display.update()
        
        text(str(mario.health) + " / "+ str(mario.maxhealth),(textlevel1,textlevel1+50),enemyfont) #Output the player's health
        pygame.display.update()
        pygame.time.delay(2000)                                                 #Delay for visual effect

        
        gameovertheme.play(-1)                                                  #Play the game over soundtrack
        gameovertheme.set_volume(0.5)
        gameoverscreen()                                                        #Output game over screen
        text("Hit ESC to Close the Game", (WIDTH/2,50), creditsfont1,WHITE)
        
        while playerlost==True:
            pyevents=pygame.event.get()
            keys = pygame.key.get_pressed()
            retrybutton.update(pyevents)
            retrybutton.draw(game_window)
                   
        
            if keys[pygame.K_ESCAPE]:                                           #Closes the game
                playerlost=False 
                inPlay = False
                ESCbuttonpressed=True
            
            if retrybutton.pressed==True:
                wavecount=1                                                     #Reset all values back to their
                mario.health=500                                                #default value at the beginning of the game
                mario.atkpower=25
                mario.defense=0
                mario.maxhealth=500
                magicpoints=25
                numberofpotions=5
                numberofsuperpotions=2
                numberofbombs=2
                
                gameovertheme.stop()   
                playerlost=False                                               #Exits the while loop after the retry button is pressed
            pygame.display.update()
            
        battletheme1.play(-1)                                                  #Restart the first battle theme plays after the intro music stops
        battletheme1.set_volume(0.9)
        battletheme1playing=True
        
        if ESCbuttonpressed==False:                                             #Only enter running mode again if the ESC key was not pressed 
            runningmode()
        
        enemies=[]                                                              #Clear previous wave of enemies
        enemypictures=[]
        enemybuttons=[]
        randomlygenerateenemies(enemies)                                        #Generate a new wave of enemies
            

#Back in Main Game Loop-------------------------------------------
    if wavecount>5 and wavecount<10 and battlethemehaschanged==False:           #Changes the battle theme playing if stronger enemies start to appear
        battletheme2.play(-1)
        battletheme2.set_volume(0.2)
        battletheme2playing=True
        battlethemehaschanged=True                                              #Flips boolean flag so that the if statement is not satisfied more than once
            
    if wavecount>10 and ESCbuttonpressed==False:                                #Checks if the player has overcome the final battle since it is loacted at wave 10 
        outputgeneraldisplays=False                                             #Stops outputting displays present during the rest of the game
        inPlay=False
        finalbattletheme.stop()
        endingtheme.play(-1)                                                    #Play ending theme, cutscene, and credits
        endingtheme.set_volume(0.2)
        endingcutscene()   
        displaycredits()
        endingtheme.stop()

    if outputgeneraldisplays==True and ESCbuttonpressed==False:                 #General outputs in the main loop for most of the game
        redrawenemies(game_window)    
        redrawplayer(game_window)
        redrawhealthbars(enemies)
        redraw_game_window(game_window,(attackbutton,spellbutton,itembutton),enemies)
    
    pygame.display.update()
    
pygame.quit()                                                                   #Exit pygame when done
