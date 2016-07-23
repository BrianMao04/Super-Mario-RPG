#########################################
# Programmer: Brian Mao
# Date: 16/06/2014  
# File Name: RPG_Classes
# Description: These are the classes for the battle system of an RPG game. 
#########################################
import pygame, random, os

#----------------------------------------------------------
class Character(object):
    """General class for all characters in the game"""
    def __init__(self, health, atkpower,defense):
        self.health=health
        self.atkpower=atkpower
        self.defense=defense
        
    def attack():
        pass


class Hero(Character):
    """Class for the player's character"""
    def __init__(self,health, atkpower, defense, maxhealth, filepath=None):
        Character.__init__(self,health, atkpower, defense)
        self.maxhealth=maxhealth
        self.filepath=filepath
        
    
    def attack(self, other):                                    #Attack damage calculation for player's attack
        if other.defense<self.atkpower:
            other.health=other.health-self.atkpower+other.defense
            
        if other.defense>=self.atkpower:                        #Don't change any health values if the player's attack
            pass                                                #is weaker than the enemy's defense
            

class Enemy(Character):
    """Class for basic enemies"""
    def __init__(self,health, atkpower, defense, filepath=None):
        Character.__init__(self,health, atkpower, defense)
        self.Y=0                                                #Default Y value used for drawing enemies
        self.filepath=filepath
        self.defaulthealth=health
        
    def reset(self):                                            #Gives enemies their default amount of health back
        self.health=self.defaulthealth
    
    def attack(self, other):
        weakattack=10 
        semiweakattack=15
        mediumattack=20

        listofattacks=[weakattack, semiweakattack, mediumattack]
        chosenattack=listofattacks[random.randint(0,2)]         #Enemy randomly chooses their type of attack each turn
        
        if other.defense<chosenattack:                          #Attack damage calculation for enemy's attack
            other.health=other.health-chosenattack+other.defense
            
        elif other.defense>=self.atkpower:                      #Don't change any health values if the enemy's attack
            pass                                                #is weaker than the player's defense
        
        
class StrongEnemy(Enemy):
    """Class for more powerful enemies appearing during later parts of the game"""
    def attack(self, other):   
        mediumattack=40
        semistrongattack=60
        strongattack=70
        listofattacks=[mediumattack, semistrongattack, strongattack]
        
        chosenattack=listofattacks[random.randint(0,2)]          #Enemy randomly chooses their type of attack each turn

        if other.defense<chosenattack:                           #Attack damage calculation for enemy's attack
            other.health=other.health-chosenattack+other.defense
            
        elif other.defense>=self.atkpower:                       #Don't change any health values if the enemy's attack 
            pass                                                 #is weaker than the player's defense

#------------------------------------------------------
class Button(object):
    """ Pygame-based button """
    def __init__(self, text, x, y, w=100, h=40, hovercolour=(200,100,0), defcolour=(0,0,0)):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.hovercolour = hovercolour                           #Colour of the button if mouse hovers over it
        self.defcolour = defcolour                               #Default colour of the button when mouse is not hovering over it
        self.pressed = False                              
        self.hovering = False                                    #Mouse location
        self.font = pygame.font.Font('freesansbold.ttf', 32)     # Font object
        self.font_surf = None
        self.font_rect = None               
        self.setuptext()                                         #Function Call

    def setuptext(self):                                         #Sets up font surface
        self.font_surf=self.font.render(self.text, True, self.hovercolour)
        self.font_rect=self.font_surf.get_rect()
        self.font_rect.centerx=(self.rect.left + self.rect.right) / 2
        self.font_rect.centery=(self.rect.top + self.rect.bottom) / 2

    def update(self, events):                                    #Gather mouse position
        mousex=pygame.mouse.get_pos()[0]
        mousey=pygame.mouse.get_pos()[1]
        left=self.rect.left
        right=self.rect.right
        top=self.rect.bottom
        bottom=self.rect.top
        self.pressed = False                                     #Check if a button is clicked upon
        
        if mousex>=left and mousex<=right and mousey>=bottom and mousey<=top:  #Check if the cursor location is over a button location
            self.hovering=True
        else:
            self.hovering=False
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.hovering==True:
                self.pressed = True                              #Button is pressed if cursor is over a button and the mouse is clicked

    def draw(self, surface):                                     # Draw a button as a rectangle with text inside
        if self.hovering==True:
            pygame.draw.rect(surface, self.hovercolour, self.font_rect.inflate(10, 10), 4)
            self.font_surf = self.font.render(self.text, True, self.hovercolour) #Colour output if mouse is hovering over the button
        else:
            pygame.draw.rect(surface, self.defcolour, self.font_rect.inflate(10, 10), 6)
            self.font_surf = self.font.render(self.text, True, self.defcolour)  #Colour output if mouse is not hovering over the button
            
        surface.blit(self.font_surf, self.font_rect)             #Copy onto game window



class Enemybutton(Button):
    """Special type of Button that's drawn and updated differently"""
    def draw(self, surface):                                     # Draw a button as a rectangle with text inside
        if self.hovering==True:
            pygame.draw.rect(surface, self.hovercolour, self.font_rect.inflate(10, 65), 4)
            self.font_surf = self.font.render(self.text, True, self.hovercolour) #Colour output if mouse is hovering over the button
        else:
            pygame.draw.rect(surface, self.defcolour, self.font_rect.inflate(10, 65), 6)
            self.font_surf = self.font.render(self.text, True, self.defcolour) #Colour output if mouse is not hovering over the button
        surface.blit(self.font_surf, self.font_rect)              #Copy onto game window

    def update(self, events):                                     #Gather mouse position
        mousex=pygame.mouse.get_pos()[0]
        mousey=pygame.mouse.get_pos()[1]
        left=self.rect.left - 5
        right=self.rect.right + 5
        top=self.rect.bottom + (65/2)
        bottom=self.rect.top - (65/2)
        self.pressed = False                                      #Check if a button is clicked upon
        
        if mousex>=left and mousex<=right and mousey>=bottom and mousey<=top:  #Check if the cursor location is over a button location
            self.hovering=True
        else:
            self.hovering=False
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.hovering==True:
                self.pressed = True
                
class Itembutton(Button):
    """Special type of Button that's drawn and updated differently"""
    def draw(self, surface):                                       # Draw a button as a rectangle with text inside
        if self.hovering==True:  
            pygame.draw.rect(surface, self.hovercolour, self.font_rect.inflate(10, 10), 4)
            self.font_surf = self.font.render(self.text, True, self.hovercolour) #Colour output if mouse is hovering over the button
        else:
            pygame.draw.rect(surface, self.defcolour, self.font_rect.inflate(10, 10), 6)
            self.font_surf = self.font.render(self.text, True, self.defcolour) #Colour output if mouse is not hovering over the button
            
        surface.blit(self.font_surf, self.font_rect)                #Copy onto game window

#----------------------------------------------------------
class Bullet(object):
    """Bullet that enemies fire during their attack animation"""
    def __init__(self, x, y, speedx, speedy, image=None):
        self.X=x
        self.Y=y
        self.speedx=speedx
        self.speedy=speedy
        self.image=pygame.image.load(image)
        
    def update(self):                                                #Sets the speed at which its coordinates are incremented
        self.X+=self.speedx
        self.Y+=self.speedy
        
    def draw(self, surface):
        surface.blit(self.image, (self.X, self.Y))
        
#----------------------------------------------------------
class Item(object):
    """General class for items that can be used in the game"""
    def __init__(self):
        #self.used=False
        self.healvalue=None
        self.damage=None
        
    def use(self):
        pass
        

class Healingitem(Item):
    """Class for items that increase player health"""
    def __init__(self, healvalue):
        self.healvalue=healvalue
        
    def use(self, other, healvalue):
        other.health+=healvalue                                       #Health calculation during item's use
        self.used=True
        

class Damageitem(Item):
    """Class for items that decrease enemies' health"""
    def __init__(self, damage):
        self.damage=damage
        
    def use(self,other, damagevalue):
        for i in range(len(other)):                                    #Damages all enemies left in the wave
            other[i].health-=damagevalue                               #Damage calculation during item's use
        self.used=True

#----------------------------------------------------------
class Spell(object):  
    """Class for spells that can be used in the game"""
    def __init__(self, damagevalue, cost):
        self.damagevalue=damagevalue
        self.cost=cost

    def use(self,other, damagevalue):  
        other.health-=damagevalue                                      #Damage calculation during spell's execution

#----------------------------------------------------------
class Sound(object):
    """Class for music soundtracks"""
    def __init__(self, filepath):
        self.filepath=filepath

    def play(self,loop=0):    
        pygame.mixer.music.load(self.filepath)
        pygame.mixer.music.play(loop)
            
    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):                                       #Adjusts the volume between values of 0.0 to 1.0
        pygame.mixer.music.set_volume(volume)

    
