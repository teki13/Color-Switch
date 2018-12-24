#Mariam AlHarmoodi mah816
#Teona Ristova ti1328
#The purpose of this game is to tap a ball so it can move upward (initially it would be of a particular colour) through
#obstacles of different colours (these obstacles will be circles whose center is empty but borders are of different colours).
#The speed of the ball will be constant with each key press.
#If the user stops pressing a key, the ball will fall down with gravity.
#The ball can only go through colours that are the same of its own.
#Throughout the game, the ball’s colour will change when the ball passes through a power-up (it would be bound to).
#If it collides with a different color, the game will end.
#The display method draws the circle twice (for graphic reasons)
#The outer collide method takes two arguments, the ball object and a boolen (this is to determine if the collision has occured with the
#color wheel or the arcs.




import pygame
import time
from math import radians 
import random
import sys
import pygame.sprite as sprite

#The following class is the Circle Class where the arcs and color wheel will be used.
#The class has several attributes that will be used throught the methods. The attributes include the start and end degrees of the 4 arcs,
#the drawing of the arc using the rect method (because with this we can move the arcs down the screen),
#a list containing the speeds.
#The move method adds a particular degree amount to the start and end of each arc, moving them accordingly. If the degree of an arc goes
#beyond 360, it is reset to 0 again (this is to facilitate the collision detection).

#The Ball class is what creates the ball, and displays it, and moves it in a way that mimics gravity. The way this is done is by
#checking to see if they keypress is up or down. If they key isn't pressed anymore, the ball's position is decreased continuosly
#by a factor 0.9

class Circle:
    scroll_down = False

    def __init__(self,surface,center,radius, thickness):
     
        self.velocity = 0
        self.radius = radius
        self.in_side = False

        self.rect = pygame.Rect(center[0]-radius,center[1]-radius,radius*2,radius*2)
        self.rect1 = pygame.Rect(center[0]-radius,center[1]-radius + 1,radius*2,radius*2)
        self.y = center[1]-radius
        self.startRad1 = radians(0)
        self.endDeg1 = radians(90)
        self.startRad2 = radians(90)
        self.endDeg2 = radians(180)
        self.startRad3 = radians(180)
        self.endDeg3 = radians(270)
        self.startRad4 = radians(270)
        self.endDeg4 = radians(360)
        self.thickness = thickness
        self.page_down = 20
        self.list_StartRad = [self.startRad1, self.startRad2, self.startRad3, self.startRad4]
        self.list_EndRad = [self.endDeg1, self.endDeg2, self.endDeg3, self.endDeg4]
        self.speed = [7.5,4.5,5,5.5,6,6.5,7]
        self.x = random.randint(0,6)
        
    def move(self):
        if Circle.scroll_down:
            self.rect.move_ip(0, 4)
            self.rect1.move_ip(0,4)
            self.page_down -= 4
        else:
            self.page_down = 30

        for i in range(len(self.list_StartRad)):
            self.list_StartRad[i] = self.list_StartRad[i] + radians(self.speed[self.x])
        for i in range(len(self.list_StartRad)):
            self.list_EndRad[i] = self.list_EndRad[i] + radians(self.speed[self.x])
            if self.list_StartRad[i] >= radians(360):
                self.list_StartRad[i] -= radians(360)
                self.list_EndRad[i] -= radians(360)
            
    def display(self, surface):
        #pygame.draw.circle(surface, colors[0], (int(self.rect[0]),int(self.rect[1])), 10, 5)
        for i in range(len(self.list_StartRad)):
            pygame.draw.arc(surface,colors[i],self.rect,self.list_StartRad[i],self.list_EndRad[i],self.thickness)
            pygame.draw.arc(surface,colors[i],self.rect1,self.list_StartRad[i],self.list_EndRad[i],self.thickness)

    def collide(self, radius1, radius2, y1, y2):
        total= radius1 + radius2
        current = y1 - y2
        if abs(current) < total:
            return True

    def outercollide(self, b, tiny_ball = False ):

        if tiny_ball:
            if self.rect.collidepoint(width/2, b.y):
                return 3
            else:
                return 2
            
        ret = -1
        if self.rect.collidepoint(width/2, b.y) :
            if self.in_side == False:
                ret = 1
                for i in range(len(self.list_StartRad)):
                    if self.list_StartRad[i] <  radians(270) and  self.list_EndRad[i] >  radians(270) and b.color == colors[i]:
                        #print("case 1")
                        ret = 2
                        break
            self.in_side = True
        else:
            if self.in_side == True:
                ret = 1
                self.in_side = False
                if b.velocity < 0:
                    for i in range(len(self.list_StartRad)):
                        if self.list_StartRad[i] <  radians(90) and  self.list_EndRad[i] >  radians(90) and b.color ==colors[i]:
                            #print("case 2")                        
                            ret = 3
                            break
                else:
                   for i in range(len(self.list_StartRad)):
                        if self.list_StartRad[i] <  radians(270) and  self.list_EndRad[i] >  radians(270) and b.color ==colors[i]:
                            #print("case 2")
                            ret = 2
        return ret

        
class Ball:
    def __init__(self, surface, color, center, radius, thickness):
        self.color = color
        #self.Rect = pygame.Rect(center[0] - radius, center[1] -radius ,radius, radius)
        self.x = center[0]
        self.y = center[1]
        self.center = center
        self.radius = radius
        self.thickness = thickness
        self.surface = surface
        self.velocity= 0
        self.gravity = 0.9
        self.direction = 1
        self.key_triggered_velocity = -10 #up direction
        
    def display(self):
        
        pygame.draw.circle(self.surface, self.color, (self.x,int(self.y)), self.radius, self.thickness)
        
    def move(self):

        self.y += self.velocity
        
        if self.direction == -1:

            self.velocity = self.key_triggered_velocity
        else:
            self.velocity += self.gravity

        if self.y > self.surface.get_height():
            self.y = self.surface.get_height()
            return
     

width = 640
height = 680
surface = pygame.display.set_mode((width,height))
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

#The list of colors

red = (255,0,0)
green = (0,255,0)
blue = (0,255,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,105,180)
purple = (153,50,204)
yellow =    (255,255,0)

colors = [purple, yellow, blue, pink]
x = random.randint(0,3)
b = Ball(surface, colors[x], (320, surface.get_height()), 10, 0)


#The following is a a block of code which creates the wheels and the circles before the game starts, seperating them by a constant distance.
c = []
w = []

y_pos = 3*height/4
y_pos_ball = y_pos - 165
for i in range(100):
    circ = Circle(surface, (width/2, int(y_pos)) , 100, 20)
    y_pos -= 365
    c.append(circ)
for i in range(50):
    circ = Circle(surface, (width/2, int(y_pos_ball)) , 10,10)
    y_pos_ball -= 365
    w.append(circ)
    
#Music file
file = 'music.wav'
bounce = 'bounce.wav'
over = 'over.wav'
pygame.mixer.init()
file = pygame.mixer.Sound(file)
bounce = pygame.mixer.Sound(bounce)
over = pygame.mixer.Sound(over)
file.play()

#Background Image
img1 = pygame.image.load('rainbow.png')
img2 = pygame.image.load('rainbow.png')
m = 0

font = pygame.font.SysFont("monospace", 50)
pygame.display.flip()
clock = pygame.time.Clock()   
score=0


#The while loop will first begin with a START page, which will have the word "START" that will change color once the mouse hovers over it.
#The game will begin when it is clicked.
#The background music will play.
#The game will start. The screen will shift down if the ball crosses half of the screen. This includes the backgrounds and the other arcs,
#and the color wheel. The color wheel will be removed from its list once the ball collides with it.
#Once the game is over, a GAMEOVER page will appear and the game will end with an option of replaying.
#A highscore will be displayed. The highscores will be read from a file. If the player gets a score higher than
#that in the file, only then will the file be rewritten.

done = False
play = True
start = False
same = False
mouse = (0,0)
while play:

#Checking for the Up keys, and the mouse position on the screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            file.stop()
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            bounce.play()
            b.direction = -1
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            b.direction = 1
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if width/3 <=pos[0] <= ((width/3)+150) and height/2<=pos[1] <= ((height/2)+ 50):
                start = True
            if done == True:
                if ((width/4)+ 40) <=mouse[0] <= ((width/4)+ 40+180) and (height/2) - 60 <=mouse[1] <= ((height/2) - 60)+ 50:
                    over.stop()
                    start = True

    msElapsed = clock.tick(100)
    

    clock.tick(60)
    #Shifting the screen and the components on the screen downwards
    if b.y < height/2 and b.velocity < 5:
        b.key_triggered_velocity = -5
        Circle.scroll_down = True
        m += 1
        if m == height:
            m = 0
        
    else:
        b.key_triggered_velocity = -8
        Circle.scroll_down = False
    
    surface.fill((0,0,0))

    pygame.draw.rect(surface, black, (width/3,height/2,150,50))
    text = font.render('START',True, (255, 255, 255))
    surface.blit(text, (width/3, height/2))
    mouse = pygame.mouse.get_pos()
    if width/3 <=mouse[0] <= ((width/3)+150) and height/2<=mouse[1] <= ((height/2)+ 50):
        text = font.render('START',True, yellow)
        surface.blit(text, (width/3, height/2))

        
    if start:
        surface.fill((0,0,0))
        surface.blit(img1, (0,m))
        surface.blit(img2,(0,m-height))

        b.move()
        b.display()
        #collision detection of the arcs
        for i in c:
            i.move()
            i.display(surface)
            ret = i.outercollide(b)
            if ret == 2 or ret ==3:
                score += 1
            if ret == 1:
               over.play()
               start = False
               done = True
               break
            #collision detection of the color wheel
        for i in w:
            i.move()
            i.display(surface)
            #tiny_ball = True
            ret = i.outercollide(b, tiny_ball = True)
            if ret == 3:
                colors = [purple, yellow, blue, pink]
                while True:
                    m = random.randint(0,3)
                    if colors[m] != b.color:
                        b.color = colors[m]
                        break

                w.remove(i)
                b.display()
#score display
        text = font.render('Score: ' + str(score), True, (255,255,255))
        surface.blit(text, (15,25))
        
    if done:
        c = []
        w = []
        file.stop()
        surface.fill((0,0,0))
        high_score = open('highscore.txt', 'r')
        for i in high_score:
            if int(i.strip()) < score:
                #high_score.close()
                highest = open('highscore.txt', 'w')
                best = str(score)
                highest.write(str(score))
                highest.close()
            else:
                best = i.strip()
                #high_score.close()
        text5 = font.render('HIGH SCORE:' + best, True, (255,255,255))
        surface.blit(text5, (width/4- 10,height/2 - 120))
        
        score = 0
        #surface.fill((0,0,0))
        text1 = font.render('GAME OVER' , True, (255,255,255))
        surface.blit(text1, (width/4,height/2))
        text2 = font.render("REPLAY", True, (255,255,255))
        surface.blit(text2, ((width/4)+ 40, (height/2) - 60))
        pygame.draw.rect(surface, black, (width/4+ 40,height/2 - 60,180,50))
        text2 = font.render("REPLAY", True, (255,255,255))
        surface.blit(text2, ((width/4)+ 40, (height/2) - 60))
        mouse = pygame.mouse.get_pos()
        if ((width/4)+ 40) <=mouse[0] <= ((width/4)+ 40+180) and (height/2) - 60 <=mouse[1] <= ((height/2) - 60)+ 50:
            text2 = font.render('REPLAY',True, yellow)
            surface.blit(text2, ((width/4)+ 40, (height/2) - 60))
        if start == True:
            b = Ball(surface, colors[x], (320, surface.get_height()), 10, 0)
            y_pos = 3*height/4
            y_pos_ball = y_pos - 165
            for i in range(100):
                circ = Circle(surface, (width/2, int(y_pos)) , 100, 20)
                y_pos -= 365
                c.append(circ)
            for i in range(50):
                circ = Circle(surface, (width/2, int(y_pos_ball)) , 10,10)
                y_pos_ball -= 365
                w.append(circ)
                                       
            file.play()
            done = False
                
 
    pygame.display.update()
                   

pygame.display.quit()       