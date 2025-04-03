import pygame
import math
import random
import time
import numpy as np

colour=(0,0,0)
background=(255,255,255)

#Define the class 'turtle' to work for pygame
class turtle:
    pen=1
    #1:down, 0:up
    pos=(200,200)
    angle=0
    color=(0,0,0)
    size=1
    
    

    #Rotation to the left (to specific angle)
    def lt(self, a):
        self.angle=self.angle-a
    
    #Rotation to the right (to specific angle)
    def rt(self, a):
        self.angle=self.angle+a
        
    #Movement of the drawing turtle by 1 unit, uses trigonometry to determine the new coordinates of movement based on the angle.
    def fd(self, l):
        newpos=(round(self.pos[0]+l*100*math.cos(math.radians(self.angle))), round(self.pos[1]+l*100*math.sin(math.radians(self.angle))))
        pygame.draw.line(screen, self.color, (self.pos[0]/100, self.pos[1]/100),  (newpos[0]/100, newpos[1]/100), self.size)
        self.pos=newpos
    
    #Sets the position of the turtle
    def goto(self, p):
        self.pos = (p[0]*100, p[1]*100)

    #Retrieves and stores the position
    def getpos(self):
        return((self.pos[0]/100, self.pos[1]/100)) 

    #Sets angle (to specific fractal)
    def setangle(self, a):
        self.angle=a

 #Iteration: number of times to apply the transformation, axiom: starting pattern, rules: rules of transformation of axiom dependant on the amount of iterations. 
    #Goes in cycles: replace starting axiom according to the rules, store and update to the new string so the next transformation starts from the next string of axiom.
def create_l_system(iters, axiom, rules):
    start_string = axiom
    if iters == 0:
        return axiom
    end_string = ""
    for _ in range(iters):
        #Python magic for transformations
        end_string = "".join(rules[i] if i in rules else i for i in start_string)
        start_string = end_string
    #print(end_string)
    return end_string


#Makes transformation matrix: rotate: rotation angle, scale: scalling factor, shift: change of directino in terms if x and y. 
def trans(rotate, scale, shift):
   r=np.array([[math.cos(math.radians(rotate)),  math.sin(math.radians(rotate)), 0],
                   [-math.sin(math.radians(rotate)), math.cos(math.radians(rotate)), 0],
                   [0,0,1]]
                   )
   s=np.array([[scale, 0, 0],
              [0, scale, 0],
              [0, 0, 1],
              ])
   sh=np.array([[0,0,shift[0]],
                [0,0, shift[1]],
                [0,0,0]
               ])
   return np.dot(r,s)+sh


#Similar to trans but scale can differ on x and y
def transX(rotate, scale, shift):
   r=np.array([[math.cos(math.radians(rotate)), math.sin(math.radians(rotate)), 0],
                   [-math.sin(math.radians(rotate)), math.cos(math.radians(rotate)), 0],
                   [0,0,1]]
                   )
   s=np.array([[scale[0], 0, 0],
              [0, scale[1], 0],
              [0, 0, 1],
              ])
   sh=np.array([[0,0,shift[0]],
                [0,0, shift[1]],
                [0,0,0]
               ])
   return np.dot(r,s)+sh


#Vector 'vector' is drawn form point 'center', size scalled to 'L'.
def dt(vector,center,L):
   pygame.draw.line(screen, colour, (vector[0]*L+center[0],-vector[1]*L+center[1]), (vector[0]*L+center[0],-vector[1]*L+center[1]), 1)


#Class L-system fractal. Noise: randomness of the movement to make a fractal look more natural, stack: used to save and restore the position and angle of the turtle, commands: rules for the fractal.
class lfractal:
    axiom=""
    rules=""
    center=(600,400)
    iterations=1
    distance=10
    noise=0
    t=turtle()
    angle=0
    stack=[]
    speed=1
    ccmd=0
    commands=""

    
    #Run a single command
    def draw_cmd(self, cmd):
        k=(1+self.noise*random.gauss(0, 1))
        if cmd == '+':
            self.t.rt(self.angle)
            #turn right
        elif cmd == '-':
            self.t.lt(self.angle)
            #Turn left
        elif cmd == '(':
            self.stack.append((self.t.getpos(), self.t.angle))
            #Save position to stack
        elif cmd == 'S':
            self.t.size=self.t.size+1
            #Increase width
        elif cmd == 's':
            self.t.size=self.t.size-1
            #Descrease width
        elif cmd == 'f':
            self.t.fd(self.distance*k/2)
            #Move half a step forward (with Noise)

        #Restore position from stack
        elif cmd == ')':
            p = self.stack.pop()
            self.t.goto(p[0])
            self.t.angle = p[1]
            
        #Move forward (with noise)
        elif cmd in 'FXYZK': 
            self.t.fd(self.distance*k)

    
    def draw(self):
        commands=create_l_system(self.iterations, self.axiom, self.rules)
        screen.fill(background)
        self.t.setangle(0)
        self.t.goto(self.center)
        s=1
        for cmd in commands:
            self.draw_cmd(cmd)
            if s >= self.speed:
                pygame.display.update()
                s=1
            else:
                s=s+1
                
    def init(self):
        self.commands=create_l_system(self.iterations, self.axiom, self.rules)
        screen.fill(background)
        self.t.setangle(0)
        self.t.goto(self.center)
        self.ccmd=0
        if self.speed==0:
            self.speed=10

    #Draw next 'self.speed' segment of the fractal (extremely fast), then update screen (slower).
    def drawdot(self):
        for _ in range(self.speed):
            if self.ccmd<len(self.commands):
                self.draw_cmd(self.commands[self.ccmd])
                self.ccmd=self.ccmd+1
            else:
                pygame.display.update()
                time.sleep(2)
                return(0)

        pygame.display.update()
        return(1)

#Define class IFS.
class IFSfractal:
    center=(600,400)
    speed=1
    #Limit of dots drawn
    limit=400000
    #List of transformations
    m=[]
    #Length / size
    L=700
    #Current iteration
    K=0
    #Current dot postion
    v=np.array([0, 0, 1])
    def __init__(self):
       self.m=list([]) 
    
    def init (self):
        screen.fill(background)
        self.K=0
        self.v=np.array([0, 0, 1])
        if self.speed==0:
            self.speed=10
            
    #Draw next 'self.speed' dots of the fractal (extremely fast), then update screen (slower).    
    def drawdot(self):
        for _ in range(self.speed):
            P = random.randint(0, 100)
            #Get the next random transformation
            ind=P%len(self.m)
            #Get the next 'dot' coordinates
            self.v = np.dot(self.m[ind], self.v)
            #Draw next dot
            dt(self.v, self.center,self.L)
            self.K=self.K+1
        pygame.display.update()
        #Stop when reaches limit
        if self.K>self.limit:
            time.sleep(2)
            return(0)
        else:
            return(1)
        
    def draw (self):
        screen.fill(background)
        K=0
        v=np.array([0, 0, 1])
        s=0
        
        while K<self.limit:
           P = random.randint(0, 100)
           ind=P%len(self.m)
           v = np.dot(self.m[ind], v)
           dt(v, self.center,self.L)
           K=K+1
           
           if s > self.speed:
              pygame.display.update()
              s=0
           else:
              s=s+1
        pygame.display.update()
        
#Create classes for all fractals
koh=lfractal()
koh.axiom="-F++F++F"
koh.rules={"F":"F-F++F-F"}
koh.center=(350,550)
koh.iterations=4
koh.distance=5
koh.noise=0
koh.angle=60
koh.speed=1

xmas=lfractal()
xmas.axiom="--F++F++F++F"
xmas.rules={"F":"ff---ff++F++F++ff---ff"}
xmas.center=(500,475)
xmas.iterations=7
xmas.distance=9
xmas.noise=0
xmas.angle=45
xmas.speed=2

dragon=IFSfractal()
dragon.L=500
dragon.center=(800,500)
dragon.speed=50
dragon.m.append(trans(45, math.sin(math.radians(45)), (0, 0)))
dragon.m.append(trans(135, math.sin(math.radians(45)), (-1, 0)))

tree=IFSfractal()
tree.center=(600,700)
tree.speed=25
tree.limit=320000
tree.m.append(transX(0, (1/100, 1/2), ( 0, 0)))
for i in range (3):
    tree.m.append(transX(25, (1/2, 3/5), ( 0, 2/5)))
tree.m.append(transX(45, (1/4, 1/2), ( 0, 1/6)))
for i in range (3):
    tree.m.append(transX(-35, (1/2, 3/5), ( 0, 2/5)))
tree.m.append(transX(-55, (1/4, 1/2), ( 0, 1/5)))

triasierpinski=IFSfractal()
triasierpinski.center=(600,375)
triasierpinski.speed=25
triasierpinski.limit=160000
triasierpinski.m.append(trans(0, 1/2, (0, 1/4)))
triasierpinski.m.append(trans(0, 1/2, (1/4, -1/4)))
triasierpinski.m.append(trans(0, 1/2, (-1/4, -1/4)))

carpsierpinski=IFSfractal()
carpsierpinski.center=(250,725)
carpsierpinski.speed=100
carpsierpinski.m.append(trans(0, 1/3, ( 0, 0)))
carpsierpinski.m.append(trans(0, 1/3, ( 0, 1/3)))
carpsierpinski.m.append(trans(0, 1/3, ( 0, 2/3)))
carpsierpinski.m.append(trans(0, 1/3, ( 1/3, 2/3)))
carpsierpinski.m.append(trans(0, 1/3, ( 2/3, 2/3)))
carpsierpinski.m.append(trans(0, 1/3, ( 2/3, 1/3)))
carpsierpinski.m.append(trans(0, 1/3, ( 2/3, 0)))
carpsierpinski.m.append(trans(0, 1/3, ( 1/3, 0)))

anneslace=IFSfractal()
anneslace.center=(600,400)
anneslace.speed=200
anneslace.m.append(trans(0, 1/4, ( 3/8, 0)))
anneslace.m.append(trans(90, 1, ( 0, 0)))
for i in range (16):
   anneslace.m.append(trans(0, -1, ( 0, 0)))
for i in range (16):
  anneslace.m.append(trans(45, 1, ( 0, 0)))
anneslace.m.append(trans(22.5, 1/2, ( 0, 0)))

spiral=IFSfractal()
spiral.center=(400,500)
spiral.speed=50
spiral.L=1000
spiral.m.append(trans(0, 1/3, ( 2/5, 0)))
for i in range(8):
   spiral.m.append(trans(-25, 0.9, ( 0, 0)))

spiral2=IFSfractal()
spiral2.center=(400,450)
spiral2.speed=75
spiral2.L=400
spiral2.m.append(trans(-135, 1/3, ( 1, 0)))
for i in range (8):
   spiral2.m.append(trans(-40, 0.9, ( 0, 0)))

snowflake=IFSfractal()
snowflake.center=(600,400)
snowflake.speed=75
snowflake.m.append(transX(0, (1/2, 1/4), ( 1/4, 0)))
snowflake.m.append(transX(0, (1/2, 1/4), ( -1/4, 0)))
for i in range(8):
    snowflake.m.append(transX(60, (1, 1), ( 0, 0)))
    snowflake.m.append(transX(-60, (1, 1), ( 0, 0)))

tree2=IFSfractal()
tree2.center=(600,700)
tree2.speed=50
tree2.limit=240000
tree2.L=600
T=2/3*1.05
tree2.m.append(transX(0, (0, 1/3), ( 0, 0)))
for i in range(3):
    tree2.m.append(transX(30, (T, T), ( 0, 1/3)))
    tree2.m.append(transX(-30, (T, T), ( 0, 1/3)))

bush=IFSfractal()
bush.center=(600,700)
bush.speed=50
bush.limit=240000
bush.m.append(transX(0, (0, 2/5), ( 0, 0)))
bush.m.append(transX(15, (3/5, 3/5), ( 0, 0)))
bush.m.append(transX(-15, (3/5, 3/5), ( 0, 0)))
for i in range (3):
   bush.m.append(transX(0, (3/5, 3/5), ( 0, 2/5)))

fern=IFSfractal()
fern.center=(600,700)
fern.speed=25
fern.limit=280000
fern.m.append(transX(0, (0, 1/7), ( 0, 0)))
fern.m.append(transX(50, (-1/5, 2/5), ( 0, 1/12)))
fern.m.append(transX(-45, (1/5, 2/5), ( 0, 1/15)))
for i in range (10):
   fern.m.append(transX(2, (6/7, 6/7), ( 0, 1/7)))

maple=IFSfractal()
maple.center=(600,700)
maple.speed=150
maple.m.append(transX(0, (0, 1/2), ( 0, 0)))
maple.m.append(transX(0, (1/2, 3/5), ( 0, 2/5)))
maple.m.append(transX(45, (1/2, 1/2), ( 1/5, 1/5)))
maple.m.append(transX(-45, (1/2, 1/2), ( -1/5, 1/5)))
maple.m.append(trans(0, 3/4, ( 0, 0)))

snowflake2=lfractal()
snowflake2.center=(550,400)
snowflake2.speed=2
snowflake2.axiom="-LLB+LLB+LLB+LLB+LLB+LLB"
snowflake2.rules={"L": "FL", "A":"--L+LL+L+L+LL+L---", "B":"--L+LLA+LB+LA+LL+L---"}
snowflake2.iterations=7
snowflake2.angle=60
snowflake2.distance=5

tree3=lfractal()
tree3.center=(600,700)
tree3.speed=5
tree3.axiom="---A"
tree3.rules={"K":"KFF", "A":"K-(AF)+(AF)+(AF)"}
tree3.iterations=7
tree3.angle=30
tree3.distance=10
tree3.noise=0.4

cross=lfractal()
cross.center=(400,150)
cross.axiom="F+F+F+F"
cross.rules={"F":"F+F-F-FF+F+F-F"}
cross.iterations=3
cross.angle=90
cross.distance=7

auseklis=lfractal()
auseklis.center=(550,400)
auseklis.speed=15
auseklis.axiom="F+++F+++F+++F"
auseklis.rules={"F":"---F+++++ff----ff+++++F---"}
auseklis.iterations=9
auseklis.angle=30
auseklis.distance=50

sierarrow=lfractal()
sierarrow.center=(250,700)
sierarrow.speed=6
sierarrow.axiom="X"
sierarrow.rules={"X":"-Y+X+Y-", "Y":"+X-Y-X+"}
sierarrow.iterations=8
sierarrow.angle=60
sierarrow.distance=3

dragon2=lfractal()
dragon2.center=(200,300)
dragon2.speed=6
dragon2.axiom="X"
dragon2.rules={"X":"+Y--X+", "Y":"-Y++X-"}
dragon2.iterations=12
dragon2.angle=45
dragon2.distance=10

tree3=lfractal()
tree3.center=(600,700)
tree3.speed=6
tree3.axiom="---A"
tree3.rules={"K":"KFF", "A":"K-(AF)+(AF)+(AF)"}
tree3.iterations=7
tree3.angle=30
tree3.distance=12.5
tree3.noise=0.4

bush2=lfractal()
bush2.center=(600,700)
bush2.speed=6
bush2.axiom="------A"
bush2.rules={"K":"KF", "A":"-(A)++(A)-K(A)"}
bush2.iterations=8
bush2.angle=15
bush2.distance=20

peanogosper=lfractal()
peanogosper.center=(700,100)
peanogosper.speed=6
peanogosper.axiom="FA"
peanogosper.rules={"A":"A+BF++BF-FA--FAFA-BF+", "B":"-FA+BFBF++BF+FA--FA-B"}
peanogosper.iterations=4
peanogosper.angle=60
peanogosper.distance=12

hilbert=lfractal()
hilbert.center=(300,50)
hilbert.speed=6
hilbert.axiom="L"
hilbert.rules={"L":"+RF-LFL-FR+", "R":"-LF+RFR+FL-"}
hilbert.iterations=6
hilbert.angle=90
hilbert.distance=10


mainloop=[]
mainloop.append(koh)
mainloop.append(cross)
mainloop.append(xmas)
mainloop.append(hilbert)
mainloop.append(peanogosper)
mainloop.append(auseklis)
mainloop.append(dragon2)
mainloop.append(dragon)
mainloop.append(sierarrow)
mainloop.append(triasierpinski)
mainloop.append(carpsierpinski)
mainloop.append(anneslace)
mainloop.append(spiral)
mainloop.append(spiral2)
mainloop.append(snowflake2)
mainloop.append(snowflake)
mainloop.append(tree3)
mainloop.append(tree2)
mainloop.append(tree)
mainloop.append(bush2)
mainloop.append(bush)
mainloop.append(fern)
mainloop.append(maple)

pygame.init()
screen = pygame.display.set_mode((1200, 800))

pause=False
cFractal=0
mainloop[cFractal].init()

#Get previous / next fractal 
def getnext(c,dir):
    c=c+dir
    if c>len(mainloop)-1:
        c=0
    if c<0:
        c=len(mainloop)-1
    mainloop[c].init()
    return c

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: 
                pygame.quit()
            elif event.key == pygame.K_LEFT: 
                #Draw next fractal
                cFractal=getnext(cFractal,-1)
            elif event.key == pygame.K_RIGHT:
                #Draw previous fractal
                cFractal=getnext(cFractal,1) 
            elif event.key == pygame.K_SPACE: 
                pause=not pause
            elif event.key == pygame.K_UP: 
                #Increase speed
                mainloop[cFractal].speed=mainloop[cFractal].speed*2
            elif event.key == pygame.K_DOWN: 
                #Decrease speed
                mainloop[cFractal].speed=mainloop[cFractal].speed//2
                
    if not pause:
        if mainloop[cFractal].drawdot()==0:
            #print(next fractal)
            cFractal=getnext(cFractal,1)
