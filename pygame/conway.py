"""
Youngmin Park yop6@pitt.edu

TODO: add buttons for initial conditions

Conway's game of life
http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

"""
import time 
import pygame
import copy
import numpy as np
 
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)
YELLOW   = (   255, 255, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]


width=10;height=10;margin=1
grids = 60

rightspace = 100
winw = (width+margin)*grids + rightspace
winh = (height+margin)*grids
size = (winw,winh)
screen = pygame.display.set_mode(size)

#def square(screen,x,y,width,height):


pygame.display.set_caption("Conway")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

grid = [ [0 for j in range(grids)] for i in range(grids)]
gridtemp = [ [0 for j in range(grids)] for i in range(grids)]

def survive(lives):
    """
    return True if there are a sufficient number of neighbors
    return False otherwise
    """
    if lives < 2:
        #print '^will die','lives',lives
        return 0
    elif lives == 2 or lives == 3:
        #print '^will cont','lives',lives
        return 1
    elif lives > 3:
        #print '^will die','lives',lives
        return 0

"""
glider init
"""

grid[2][2] = 1
grid[3][3] = 1
grid[3][4] = 1
grid[4][2] = 1
grid[4][3] = 1

"""
other init
"""
"""
for j in range(grids):
    grid[30][j]=1
    grid[50][j]=1
"""

rowm = -100;colm = -100
color = WHITE
prevgrid = [ [0 for j in range(grids)] for i in range(grids)]
prev2grid = [ [0 for j in range(grids)] for i in range(grids)]
prev3grid = [ [0 for j in range(grids)] for i in range(grids)]


# start/pause/stop button params
startx=winw-rightspace+margin;starty=margin # coord
startw=rightspace-2*margin;starth=50 # size
pausex=winw-rightspace+margin;pausey=2*margin+starth
pausew=rightspace-2*margin;pauseh=50
stopx=winw-rightspace+margin;stopy=3*margin+pauseh+starth
stopw=rightspace-2*margin;stoph=50

start=False
pause=True
stop=False

# intro textinstructions
introx=winw/10;introy=winh/4
intromargin=35

# --- user instructions
print "click and drag to add initial conditions"
print "press the green button to start"
print "press the yellow button to pause"
#print "press the red button to kill everything"


# FONTS
font = pygame.font.Font(None,30)

no_click = True # for use in flagging all events before click
# or after stop button press


# -------- Main Program Loop -----------
while not done:
    event_catch = False # use to catch a single frame event
    # --- Main event loop
    

    for event in pygame.event.get(): # User did something
        
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            no_click = False
            player_position = pygame.mouse.get_pos()
            x = player_position[0]
            y = player_position[1]
            if (x > startx and x < startx + startw) and (y > starty and y < starty+starth):
                start = True
                pause = False
                stop = False
                print 'start'
            if (x > pausex and x < pausex + pausew) and (y > pausey and y < pausey+pauseh):
                start = False
                pause = True
                stop = False
                print 'pause'

            if (x > stopx and x < stopx + stopw) and (y > stopy and y < stopy+stoph):
                event_catch = True
                start = False
                pause = False
                stop = True
                no_click = True
                print 'stop'

            #print start,pause,stop

        # user initial conditions click and drag
        if pygame.mouse.get_pressed()[0]:
            #elif event.type == pygame.MOUSEBUTTONDOWN:

            player_position = pygame.mouse.get_pos()
            x = player_position[0]
            y = player_position[1]
            #click_sound.play()
            counterx=0;countery=0
            if x < winw-rightspace:
                while x >= margin:
                    x -= (width+margin)
                    counterx += 1
                while y >= 1.:
                    y -= (width+margin)
                    countery += 1
                rowm=counterx;colm=countery
                grid[rowm-1][colm-1] = 1

    if start:
        #print "Click: (",x,",",y,")" 
        #print "startx",startx,"starty",starty
        #print "startx+startw",startx+startw,"starty+starth",starty+starth
        #print "Row:",rowm,"Column:",colm
        
        #print y > starty and y < starty+starth
        
        prev3grid = copy.deepcopy(prev2grid)
        prev2grid = copy.deepcopy(prevgrid)
        prevgrid = copy.deepcopy(grid)
        # interior update
        for i in range(grids):
            for j in range(grids):
                if i != 0 and j != 0 and i < grids-1 and j < grids-1:
                    top = grid[i-1][j]
                    bot = grid[i+1][j]
                    rht = grid[i][j+1]
                    lft = grid[i][j-1]
                    topr = grid[i-1][j+1]
                    topl = grid[i-1][j-1]
                    botr = grid[i+1][j+1]
                    botl = grid[i+1][j-1]
                    
                    lives = sum([top,bot,rht,lft,
                                 topr,topl,botr,botl])
                    
                    if grid[i][j] == 1:
                        gridtemp[i][j] = survive(lives)
                    else:
                        if lives == 3:
                            #print i,j, 'will be nonzero','lives',lives
                            gridtemp[i][j] = 1
        # top? update
        j = 0
        for i in range(grids):
            if i != 0 and j == 0 and i < grids-1:
                top = grid[i-1][j]
                #left = grid[i][j-1]
                bot = grid[i+1][j]
                rht = grid[i][j+1]
                topr = grid[i-1][j+1]
                botr = grid[i+1][j+1]
                lives = sum([top,bot,rht,
                             topr,botr])
                if grid[i][j] == 1:
                    gridtemp[i][j] = survive(lives)
                else:
                    if lives == 3:
                        #print i,j, 'will be nonzero','lives',lives
                        gridtemp[i][j] = 1
        # bot? update
        j = grids-1
        for i in range(grids):
            if i != 0 and i < grids-1:
                top = grid[i-1][j]
                bot = grid[i+1][j]
                lft = grid[i][j-1]
                topl = grid[i-1][j-1]
                botl = grid[i+1][j-1]            
                lives = sum([top,bot,lft,
                             topl,botl])
                if grid[i][j] == 1:
                    gridtemp[i][j] = survive(lives)
                else:
                    if lives == 3:
                        #print i,j, 'will be nonzero','lives',lives
                        gridtemp[i][j] = 1

        # left? update
        i = 0
        for j in range(grids):
            if j != 0 and j < grids-1:
                bot = grid[i+1][j]
                rht = grid[i][j+1]
                lft = grid[i][j-1]
                botr = grid[i+1][j+1]
                botl = grid[i+1][j-1]            
                lives = sum([bot,rht,lft,
                             botr,botl])
                if grid[i][j] == 1:
                    gridtemp[i][j] = survive(lives)
                else:
                    if lives == 3:
                        #print i,j, 'will be nonzero','lives',lives
                        gridtemp[i][j] = 1

        # right? update
        i = grids-1
        for j in range(grids):
            if j != 0 and j < grids-1:
                top = grid[i-1][j]
                rht = grid[i][j+1]
                lft = grid[i][j-1]
                topr = grid[i-1][j+1]
                topl = grid[i-1][j-1]
                
                lives = sum([top,rht,lft,
                             topr,topl])
                if grid[i][j] == 1:
                    gridtemp[i][j] = survive(lives)
                else:
                    if lives == 3:
                        #print i,j, 'will be nonzero','lives',lives
                        gridtemp[i][j] = 1
        #print "total animals:",np.sum(grid)
        grid = copy.deepcopy(gridtemp)
        gridtemp = [ [0 for j in range(grids)] for i in range(grids)]
        
        #print 
        #print grid
        
        # --- Drawing code should go here
            
    if stop and event_catch:
        grid = [ [0 for j in range(grids)] for i in range(grids)]
        prevgrid = [ [0 for j in range(grids)] for i in range(grids)]
        prev2grid = [ [0 for j in range(grids)] for i in range(grids)]
        prev3grid = [ [0 for j in range(grids)] for i in range(grids)]

        # see if no_click for intro text
    #    screen.fill(BLACK)
        
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    

    # draw start/pause/stop buttons (green/yellow/red)
    pygame.draw.rect(screen, GREEN, [startx,starty,startw,starth])
    pygame.draw.rect(screen, YELLOW, [pausex,pausey,pausew,pauseh])
    pygame.draw.rect(screen, RED, [stopx,stopy,stopw,stoph])

    # set up text on buttons
    font = pygame.font.Font(None,30)
    b_start_txt = font.render('Start',True,BLACK,GREEN)
    b_pause_txt = font.render('Pause',True,BLACK,YELLOW)
    b_stop_txt = font.render('Stop',True,BLACK,RED)
    screen.blit(b_start_txt,(startx,starty))
    screen.blit(b_pause_txt,(pausex,pausey))
    screen.blit(b_stop_txt,(stopx,stopy))
    
    #pygame.draw.rect(screen, RED, [stopx,stopy,stopw,stoph])

    

    # draw border

    for row in range(grids):
        for column in range(grids):
            color = BLACK
            if grid[row][column] == 1:
                color = WHITE
            elif prevgrid[row][column] == 1:
                color = RED#(200,200,200)#GREEN #
            elif prev2grid[row][column] == 1:
                color = GREEN #(100,100,100) #BLUE
            elif prev3grid[row][column] == 1:
                color = BLUE
            pygame.draw.rect(screen, color, [row*(width+margin)+margin,
                                             column*(width+margin)+margin,width,height]) 
    #for row in range(grids):
    #    for column in range(grids):
    #        #color = WHITE
    #        if prevgrid[row][column] == 1:
    #            color = (100,100,100)
    #        pygame.draw.rect(screen, color, [row*(width+margin)+margin,
    #                                         column*(width+margin)+margin,width,height]) 


    # display instructions before mouse click
    if no_click:
        intro_txt1 = font.render('1. Click and drag to set initial conditions',True,WHITE,BLACK)
        intro_txt2 = font.render('2. Then click the green start button',True,WHITE,BLACK)
        screen.blit(intro_txt1,(introx,introy))
        screen.blit(intro_txt2,(introx,introy+intromargin))



    # --- Limit to 60 frames per second
    
    clock.tick(60)

    #print grid
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    #time.sleep(3) 


 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
