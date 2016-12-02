import os
path=os.getcwd()

add_library('minim')#adding sounds, call library minim from processing,  but using java that is y 'this'
minim=Minim(this)

class Game:#generic class for the game,everything u put on game is part of game class
    def __init__(self,w,h):#w and h saved so that later u need the values to move
        self.w=w#the scree size
        self.h=h
        self.y=0
        self.x1=0
        self.x2=0
        self.g=620#ground
        self.platforms=[]#initialize platform list
        
    def loadImages(self):
        
        self.robber=Robber(100,620,35,102,145,4,'robber')#Object instantiation from juju class
    
        for i in range(3):
            self.platforms.append(Platform(100+i*200,450-i*100,200,52,451,3000,'step'))#so that it goes up 'y' decreases
            self.platforms[-1].loadImages()
       
        self.bg=loadImage(path+'/wall.png') 
        self.robber.loadImages()#the order matters a lot
    
    
        # self.music=minim.loadFile(path+'/Lost-Jungle.mp3')
        # self.music.loop() #background hence defined in the game class
        
    def display(self):#also display

        m=game.y
            
        image(self.bg,0,0,game.w,game.h-m%game.h,0,m%game.h,game.w,game.h)
        image(self.bg,0,game.h-m%game.h,game.w,m%game.h,0,0,game.w,m%game.h)

        for p in self.platforms:
            p.display()
        self.robber.display()
        
        
    # def menu(self):
    #     #fill(255,0,0)#THIS IS JUST TO UNDERSTAND BORDERS
    #     #rect(580,270,170,40)#trial and error
    #     text("Play Game",600,300)#increase font in setup
            
class Robber:#generic for all creatures
    def __init__(self,x,y,r,w,h,F,img):#x,y where u want to load the image,bt its center
        self.x=x
        self.y=y
        self.r=r#radius of the circle
        self.w=w#width and height of one frame
        self.h=h
        self.F=F
        self.f=0#instantaneous frame
        self.g=game.g
        self.vy=0#velocity in y direction,needed to create acceleration
        self.vx=0#every frame goes one to right
        self.dir=1#u create another attribute for knowing the direction
        self.img=img
        self.dead=False
        self.keyHandler={LEFT:False,RIGHT:False,UP:False}#create dictionaries,
        
    def loadImages(self):
        self.img=loadImage(path+'/robber.png')
        
        
    def gravity(self):
        
        if self.y+self.r<self.g:#bcs y increases downwards
           self.vy+=0.1
           self.y+=2
        else:
            self.vy=0
            self.y=self.g-self.r#so that it stops correct at ground, if on ground my y is going to be ground -radius
            
        if  not self.dead:        
            for p in game.platforms:
                if self.x+self.r>p.x and self.x-self.r<p.x+p.w and self.y+self.r <= p.y +5 :#giving a margin of error so even if u fall slightly blw the platform it detects it, bcs frames can shift#and <=p.y bcs y decreases going upwards# within boundaries of platform, that is right side slightly bigger than p and left smaller than p and
                    self.g=p.y
                    return#when u find urself on platform return, so exit the function at this line if it finds a platform so never goes
            self.g=game.g  # so reset ground if u dont find a platform    
                                
    def update(self):
        if self.vx!=0:#if moving forward
                self.f=(self.f+0.1)%self.F#to wrap around 8 frames, u load first 7 and for 8th u go back to 1st one,it goes 0,1,2,3...
        self.gravity()
        if not self.dead:#all basic stuff done
    
            if self.vx!=0:#if u have velocity update frame, otherwise u stopt the frame and it stands still
                self.f=(self.f+0.1)%self.F#to wrap around 8 frames, u load first 7 and for 8th u go back to 1st one,it goes 0,1,2,3...
            else:
                self.f=2#
            
            
            if self.keyHandler[LEFT]:#whenits true
                self.vx=-5
                self.dir=-1
            elif self.keyHandler[RIGHT]:
                self.vx=5
                self.dir=1
            else:
                self.vx=0#to stop oving when u r not pressing any key
            
            
            if self.keyHandler[UP] and self.vy==0:
                self.vy=-8
                
                    
            if self.y>game.h/2 and self.vy!=0:#when u reach half of screen AND VELOCITY IS NOT 0
                game.y+=self.vy#u r moving the background, so shift all the images by game.x
                
        self.x+=self.vx#3enabled inspite of the condition
        self.y+=self.vy  
    
    def display(self):#u need to wrap around the individual frame to create motion
        self.update()
        if self.dir==1:
            image(self.img,self.x-self.r-game.y,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,int(self.f)*self.w+self.w,self.h)#every image there for 1/6th of a second and then changes
        elif self.dir==-1:#u flip image
            image(self.img,self.x-self.r-game.y,self.y-self.r,self.w,self.h,int(self.f)*self.w+self.w,0,int(self.f)*self.w,self.h)        
        
class Platform:#gneric so tha tu can have different platform
    def __init__(self,x,y,w,h,x1,x2,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img=img
        self.x1=x1
        self.x2=x2
        
    def loadImages(self):
        self.img=loadImage(path+'/'+self.img+'.png')
        
    def display(self):
        image(self.img,self.x,self.y-game.y)#bcs otherwise it will shif twith u as that is how we coded it
        
        
    def update(self):
        
        if self.x>self.x2:
            self.dir=-1#need to change both direction and veocity, other wise moonwalk
            self.vx=-2
        elif self.x<self.x1:
            self.dir=1
            self.vx=2
        
        self.x+=self.vx
        self.y+=self.vy      

game=Game(1280,720)

def setup():
    size(game.w,game.h)
    background(0)
    fill(255)
    textSize(32)
    game.loadImages()#we need to load images in reverse order bcsso they dont overlap, and 1 has transparent place and .png reserves it
    
    
def draw():
    
    # if game.state=='menu':
    #     background(0)
    #     game.menu()
    # elif game.state=='play':
    fill(255)
    textSize(24)
    game.display()
    # if 600<=mouseX<=755 and 272<=mouseY<=307:
    #    fill(255,255,0)
    # else:
    #     fill(255)
            
def keyPressed():
    game.robber.keyHandler[keyCode]=True
    
def keyReleased():  
    game.robber.keyHandler[keyCode]=False  
        
# def mouseClicked():
#     if game.state=="menu":
#         if 600<=mouseX<=755 and 272<=mouseY<=307:
#             game.state='play' 
        
#     if game.juju.dead and game.juju.y>900:
#         game.__init__(1280,720)
#         game.loadImages()
            
    