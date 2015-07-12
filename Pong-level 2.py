# PONG-LEVEL 2
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 1000
HEIGHT = 425       
BALL_RADIUS = 6  
PAD_WIDTH = 8
PAD_HEIGHT = 80

ball_pos = [WIDTH/2, HEIGHT/2]
prev_ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0] 
score1 = 0
score2 = 0
BallPlay = True
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
goal_delay = 350
goal_color1 = "Yellow"
goal_color2 = "Yellow"
ball_acceleration = 1.02 ## initial puck acceleration when puck hits paddle
randampl = 40 ## causes small random variation in puck angle

# define event handlers
#############################  NEW  GAME  ###############################
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel                 
    global score1, score2, goal_color1, goal_color2                                                      # these are ints
  
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    goal_color1 = "Yellow"
    goal_color2 = "Yellow"
    if int(random.randrange(0,100)) < 50:
        spawn_ball("LEFT")
    else: 
        spawn_ball("RIGHT")  
#############################  SPAWN PUCK  ##############################
def spawn_ball(direction):
    global ball_pos, ball_vel, goal_color1, goal_color2
    global prev_ball_pos, ball_acceleration
    goal_color1 = "Yellow"
    goal_color2 = "Yellow"
    ball_acceleration = 1.02
    if direction == "LEFT": 
        dir = -1
        ball_pos[0] = 2 * WIDTH/3
    else: 
        dir = 1
        ball_pos[0] = WIDTH/3
    ball_pos[1] = HEIGHT/2
    ball_vel = [dir * int(random.randrange(360, 480)/float(60)),\
                random.randrange(-1,2,2)*(random.randrange(120,275)\
                /float(60))]
    prev_ball_pos[0] = ball_pos[0] - ball_vel[0]
    prev_ball_pos[1] = ball_pos[1] - ball_vel[1]

#########################  START DRAW HANDLER ###########################
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global BALL_RADIUS, HEIGHT, WIDTH, PAD_WIDTH, leftteamforward
    global paddle1_vel, paddle2_vel, score1, score2, rightteamforward 
    global BallPlay, leftgoalie, rightgoalie, collide_list
    global leftgoalsideup,leftgoalsidedown,leftgoalback, goal_delay
    global prev_ball_pos, goal_color1, goal_color2, ball_acceleration
    global randampl
    
    ## EACH OBJECT PUCK MIGHT COLLIDE WITH IS DESCRIBED IN AN 8 ELEMENT LIST: 
    ## object = [x-dim center, y-dim center, x-width, y-height, left-surface, 
    ## right-surface, top-surface, bottom-surface]. S
    ## Surface code:
    ## 0 = reflective, 1 = transmissive, 2 = goal, 3 = invidible.  
    roof = [WIDTH/2, -20, WIDTH + 20, 40, 0,0,0,0]
    floor =  [WIDTH/2, HEIGHT + 20, WIDTH + 40, 40, 0,0,0,0]
    leftwall = [-20, HEIGHT/2, 40, HEIGHT + 40, 0,0,0,0]
    rightwall = [WIDTH + 20, HEIGHT/2, 40, HEIGHT + 40, 0,0,0,0]
    leftgoalie = [3*WIDTH/40 + 0.5*PAD_WIDTH, paddle1_pos,\
                  PAD_WIDTH, PAD_HEIGHT,0,0,0,0]
    rightgoalie = [37*WIDTH/40 - 0.5*PAD_WIDTH, paddle2_pos,\
                   PAD_WIDTH, PAD_HEIGHT,0,0,0,0]
    leftteamforward = [WIDTH - 6 * WIDTH/20, paddle1_pos,\
                       PAD_WIDTH, PAD_HEIGHT,1,0,0,0]
    rightteamforward = [6 * WIDTH/20, paddle2_pos,\
                        PAD_WIDTH, PAD_HEIGHT,0,1,0,0]
    leftgoaldetect = [WIDTH/20 + 10, HEIGHT/2, 1, HEIGHT/3 - 22, 0,2,0,0]
    rightgoaldetect = [19 * WIDTH/20 - 10, HEIGHT/2, 1, HEIGHT/3 - 22, 2,0,0,0]
    rightgoaltotal = [75*WIDTH/80, HEIGHT/2, WIDTH/40, HEIGHT/3, 3,0,0,0]
    leftgoaltotal = [5*WIDTH/80, HEIGHT/2, WIDTH/40, HEIGHT/3, 0,3,0,0]
        
    # CenterLine
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 4, "Red")    
    # left crease line
    canvas.draw_line([3 * WIDTH/40, 0],[3 * WIDTH/40, HEIGHT], 1, "Red") 
    # right crease line
    canvas.draw_line([37 * WIDTH/40, 0],[37 * WIDTH/40, HEIGHT], 1, "Red")      
    # Left Blue Line
    canvas.draw_line([WIDTH / 3, 0],[WIDTH / 3, HEIGHT], 10, "Blue")    
    # Right Blue Line
    canvas.draw_line([2 * WIDTH / 3, 0],[2 * WIDTH / 3, HEIGHT],10, "Blue")    
    # center circle
    canvas.draw_circle((WIDTH/2,HEIGHT/2),WIDTH/12,1,"Blue")
    # center circle dot
    canvas.draw_circle((WIDTH/2,HEIGHT/2),WIDTH/100,1,"Red", "Red")             
    # upper left circle
    canvas.draw_circle((WIDTH/5,HEIGHT/4),WIDTH/12,1,"Red")   
    # upper left dot
    canvas.draw_circle((WIDTH/5,HEIGHT/4),WIDTH/100,1,"Red", "Red")              
    # upper right circle
    canvas.draw_circle((4 * WIDTH/5,HEIGHT/4),WIDTH/12,1,"Red")
    # upper right dot
    canvas.draw_circle((4 * WIDTH/5,HEIGHT/4),WIDTH/100,1,"Red", "Red")         
    # lower left circle
    canvas.draw_circle((WIDTH/5,3 * HEIGHT/4),WIDTH/12,1,"Red")      
    # lower left dot  
    canvas.draw_circle((WIDTH/5,3 * HEIGHT/4),WIDTH/100,1,"Red", "Red")         
    # lower right circle
    canvas.draw_circle((4 * WIDTH/5,3 * HEIGHT/4),WIDTH/12,1,"Red")   
    # lower right dot 
    canvas.draw_circle((4 * WIDTH/5,3 * HEIGHT/4),WIDTH/100,1,"Red", "Red")     
    # DRAW LEFT GOAL  
    canvas.draw_polygon([(3*WIDTH/40,HEIGHT/3),(3*WIDTH/40,2*HEIGHT/3), \
        (WIDTH/20,2*HEIGHT/3),(2*WIDTH/40,HEIGHT/3)],2,"Red", goal_color1)          
    # DRAW RIGHT GOAL 
    canvas.draw_polygon([(37*WIDTH/40,HEIGHT/3),(37*WIDTH/40,2*HEIGHT/3), \
        (38*WIDTH/40,2*HEIGHT/3),(38*WIDTH/40,HEIGHT/3)],2,"Red", goal_color2)     
    # DRAW LEFT GOAL PIPES
    canvas.draw_line([3*WIDTH/40,HEIGHT/3],[2*WIDTH/40-2,HEIGHT/3],3,"Black")   
    canvas.draw_line([3*WIDTH/40,2*HEIGHT/3],[2*WIDTH/40-2,2*HEIGHT/3],3,"Black")    
    canvas.draw_line([2*WIDTH/40,HEIGHT/3],[2*WIDTH/40,2*HEIGHT/3],3,"Black")      
    # DRAW RIGHT GOAL PIPES
    canvas.draw_line([37*WIDTH/40,HEIGHT/3],[38*WIDTH/40+2,HEIGHT/3],3,"Black") 
    canvas.draw_line([37*WIDTH/40,2*HEIGHT/3],[38*WIDTH/40+2,2*HEIGHT/3],3,"Black")    
    canvas.draw_line([38*WIDTH/40,HEIGHT/3],[38*WIDTH/40,2*HEIGHT/3],3,"Black")  
    
    ##########################     DRAW  BALL    #################################   
    canvas.draw_circle((ball_pos[0],ball_pos[1]),BALL_RADIUS,2, "Black","Black")
    
    ##########################     MOVE  BALL    #################################     
    prev_ball_pos[0] = ball_pos[0]
    prev_ball_pos[1] = ball_pos[1]
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]    
    
    speed = (ball_vel[0]**2 + ball_vel[1]**2)**0.5
    
    if speed > 11: 
        ball_acceleration = 1.00
    elif speed > 0 and speed < 7: 
        ball_acceleration = 1.04
    else: 
        ball_acceleration = 1.015
    
    #####################     CHECK FOR COLLISONS    #############################
    ## List of items that need to be checked to see if a collision with the puck 
    ## has occurred. Each item itself is  an 8 element list: 
    collide_list = [roof, floor, leftwall, rightwall, leftgoalie, rightgoalie,\
        leftteamforward, rightteamforward, \
        leftgoaltotal, leftgoaldetect, rightgoaltotal, rightgoaldetect]
    
    
    ###############################################################################
    ###############################################################################
    ## TO CHECK FOR COLLISIONS, DIVIDE DRAW HANDLER TIMEFRAME INTO SMALLER TIME 
    ## STEPS SINCE PUCK MOVES SO QUICKLY IT CAN JUMP THROUGH NET IN A SINGLE TIME 
    ## HANDLER INTERVAL. DEFAULT IS timesplits = 4. CALCULATE SUB-INTERVAL PUCK
    ## MOVEMENTS USING sub-prefix. FOR timesplits = 4, BALL POSITION WILL BE CALCUATED
    ## 4 TIMES FOR EACH DRAW HANDLER STEP. 
    
    sub_prev_ball_pos = [0,0]
    sub_ball_pos = [0,0]
    sub_ball_vel = [0,0]
    
    
    sub_prev_ball_pos[0] = prev_ball_pos[0]
    sub_prev_ball_pos[1] = prev_ball_pos[1]
    
    sub_ball_pos[0] = prev_ball_pos[0]
    sub_ball_pos[1] = prev_ball_pos[1]
    
    timesplits = 4
    for subtime in range(1,timesplits + 1): 
        
        sub_ball_vel[0] = ball_vel[0]/timesplits
        sub_ball_vel[1] = ball_vel[1]/timesplits
        
        sub_ball_pos[0] = sub_ball_pos[0] + sub_ball_vel[0]
        sub_ball_pos[1] = sub_ball_pos[1] + sub_ball_vel[1]
        
        for structure in collide_list: 
            xcenter = structure[0]
            ycenter = structure[1]
            xlength = structure[2]
            ylength = structure[3]
            xleftsurface = structure[4]
            xrightsurface = structure[5]
            ytopsurface = structure[6]
            ybotsurface = structure[7]

            ### check for positive x-direction collisions (right moving puck): 
            if  (sub_ball_pos[0] + BALL_RADIUS) >= (xcenter - xlength/2) and \
                (sub_prev_ball_pos[0] + BALL_RADIUS) < (xcenter - xlength/2) and \
                (sub_ball_pos[1] + BALL_RADIUS > ycenter - ylength/2) and \
                (sub_ball_pos[1] - BALL_RADIUS < ycenter + ylength/2):

                if xleftsurface == 0:
                    sub_ball_vel[0] = -sub_ball_vel[0] * ball_acceleration
                    sub_ball_vel[1] = sub_ball_vel[1] + \
                    (random.randrange(-randampl,randampl)/float(60))/timesplits
                    
                    ball_vel[0] = -ball_vel[0] * ball_acceleration
                    ball_vel[1] = ball_vel[1] + \
                    (random.randrange(-randampl,randampl)/float(60))

                elif xleftsurface == 1: 
                    sub_ball_vel[0] = sub_ball_vel[0] \
                    +(random.randrange(-randampl,randampl)/float(60))/timesplits
                    sub_ball_vel[1] = -sub_ball_vel[1] * ball_acceleration
                    
                    ball_vel[0] = ball_vel[0] +\
                    (random.randrange(-randampl,randampl)/float(60))
                    ball_vel[1] = -ball_vel[1] * ball_acceleration

                elif xleftsurface == 2: 
                    ball_vel[0] = 0
                    ball_vel[1] = 0 
                    sub_ball_vel[0] = 0
                    sub_ball_vel[1] = 0 
                    goal_delay = 350
                    score1 = score1 + 1
                    goal_color2 = "Red"  

            ### check for negative x-direction collisions (left moving puck): 
            if  (sub_ball_pos[0] - BALL_RADIUS) <= (xcenter + xlength/2) and \
                (sub_prev_ball_pos[0] - BALL_RADIUS) > (xcenter + xlength/2) and \
                (sub_ball_pos[1] + BALL_RADIUS > ycenter - ylength/2) and \
                (sub_ball_pos[1] - BALL_RADIUS < ycenter + ylength/2): 

                if xrightsurface == 0: 
                    sub_ball_vel[0] = -sub_ball_vel[0] * ball_acceleration
                    sub_ball_vel[1] = sub_ball_vel[1] + \
                    (random.randrange(-randampl,randampl)/float(60))/timesplits
                    
                    ball_vel[0] = -ball_vel[0] * ball_acceleration
                    ball_vel[1] = ball_vel[1] + \
                    (random.randrange(-randampl,randampl)/float(60))

                elif xrightsurface ==1: 
                    sub_ball_vel[0] = sub_ball_vel[0] + \
                    (random.randrange(-randampl,randampl)/float(60))/timesplits
                    sub_ball_vel[1] = -sub_ball_vel[1] * ball_acceleration
                    
                    ball_vel[0] = ball_vel[0] + \
                    (random.randrange(-randampl,randampl)/float(60))
                    ball_vel[1] = -ball_vel[1] * ball_acceleration

                elif xrightsurface == 2: 
                    sub_ball_vel[0] = 0
                    sub_ball_vel[1] = 0  
                    ball_vel[0] = 0
                    ball_vel[1] = 0
                    goal_delay = 350
                    score2 = score2 + 1
                    goal_color1 = "Red"

                elif xrightsurface == 3: 
                    pass
                
            ### check for positive y-direction collisions (downward moving puck): 
            if  (sub_ball_pos[1] + BALL_RADIUS) >= (ycenter - ylength/2) and \
                (sub_prev_ball_pos[1] + BALL_RADIUS) < (ycenter - ylength/2) and \
                (sub_ball_pos[0] + BALL_RADIUS > xcenter - xlength/2) and \
                (sub_ball_pos[0] + BALL_RADIUS < xcenter + xlength/2):

                sub_ball_vel[0] = sub_ball_vel[0] +\
                (random.randrange(-randampl,randampl)/float(60))/timesplits
                sub_ball_vel[1] = -sub_ball_vel[1] * ball_acceleration 
                
                ball_vel[0] = ball_vel[0] +\
                (random.randrange(-randampl,randampl)/float(60))
                ball_vel[1] = -ball_vel[1] * ball_acceleration 

            ### check for negative y-direction collisions (upward moving puck): 
            if  (sub_ball_pos[1] - BALL_RADIUS) <= (ycenter + ylength/2) and \
                (sub_prev_ball_pos[1] - BALL_RADIUS) > (ycenter + ylength/2) and \
                (sub_ball_pos[0] + BALL_RADIUS > xcenter - xlength/2) and \
                (sub_ball_pos[0] + BALL_RADIUS < xcenter + xlength/2): 

                sub_ball_vel[0] = sub_ball_vel[0] +\
                (random.randrange(-randampl,randampl)/float(60))/timesplits
                sub_ball_vel[1] = -sub_ball_vel[1] * ball_acceleration 
                
                ball_vel[0] = ball_vel[0] + \
                (random.randrange(-randampl,randampl)/float(60))
                ball_vel[1] = -ball_vel[1] * ball_acceleration  
           
        sub_prev_ball_pos[0] = sub_ball_pos[0]
        sub_prev_ball_pos[1] = sub_ball_pos[1]

         
    ################ IF GOAL SCORED (PUCK IN BACK OF NET    #######################     
        if ball_vel[0] ==0 and ball_vel[1] == 0:
            goal_delay = goal_delay -1 
            if goal_delay == 0: 
                
                if ball_pos[0] < WIDTH/2:
                    spawn_ball("RIGHT")
                else: 
                    spawn_ball("LEFT")
               
    ###############################################################################   
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos <= PAD_HEIGHT/2 + 4 and  paddle1_vel < 0): 
        paddle1_pos = paddle1_pos
    elif (paddle1_pos >= HEIGHT - 6 - PAD_HEIGHT/2 and  paddle1_vel > 0):
        paddle1_pos = paddle1_pos
    else:
        paddle1_pos = paddle1_pos + paddle1_vel
               
    if (paddle2_pos <= PAD_HEIGHT/2 + 4 and  paddle2_vel < 0): 
        paddle2_pos = paddle2_pos
    elif (paddle2_pos >= HEIGHT - 6 - PAD_HEIGHT/2 and  paddle2_vel > 0):
        paddle2_pos = paddle2_pos
    else:
        paddle2_pos = paddle2_pos + paddle2_vel

    #########################   DRAW  GOALIE PADDLES     ##########################
    canvas.draw_line((3*WIDTH/40 + 0.5*PAD_WIDTH,paddle1_pos + PAD_HEIGHT/2), \
        (3*WIDTH/40 + 0.5*PAD_WIDTH,paddle1_pos - PAD_HEIGHT/2),PAD_WIDTH,"Gray")
    
    canvas.draw_line((37*WIDTH/40 - 0.5*PAD_WIDTH,paddle2_pos + PAD_HEIGHT/2),\
        (37 * WIDTH/40-0.5*PAD_WIDTH,paddle2_pos - PAD_HEIGHT/2),PAD_WIDTH,"Orange")
    
    ########################   DRAW  FORWARD PADDLES     ###########################
    canvas.draw_line((WIDTH - 6 * WIDTH/20,paddle1_pos + PAD_HEIGHT/2), \
        (WIDTH - 6 * WIDTH/20,paddle1_pos - PAD_HEIGHT/2),PAD_WIDTH,"Gray")
    
    canvas.draw_line((6 * WIDTH/20,paddle2_pos + PAD_HEIGHT/2),\
        (6 * WIDTH/20,paddle2_pos - PAD_HEIGHT/2),PAD_WIDTH,"Orange")
    
    ############################### DRAW SCORES ######################################
    canvas.draw_text(str(score1),(WIDTH/2  - 60, 40), 48,"Gray", "sans-serif")
    canvas.draw_text(str(score2),(WIDTH/2  + 40, 40), 48,"Orange", "sans-serif")   
    
    #canvas.draw_text(str(speed),(WIDTH/2  + 200, 25), 18,"Black", "sans-serif")   
    #canvas.draw_text(str(ball_acceleration),(WIDTH/2+ 200,50),18,"Black") 

##############################   END DRAW HANDLER      ###############################
######################################################################################  

####################   KEYDOWN FUNCTION (move paddles)      ##########################
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos, HALF_PAD_HEIGHT, HEIGHT
    
    acc = 10
    if key==simplegui.KEY_MAP["down"]:
        #print paddle2_pos, paddle2_vel
        paddle2_vel = paddle2_vel + acc
            
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = paddle2_vel - acc
                   
    if key==simplegui.KEY_MAP["s"]:
        #print paddle1_pos, paddle1_vel
        paddle1_vel = paddle1_vel + acc
            
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel = paddle1_vel - acc
        
####################    KEYUP FUNCTION (move paddles)      ###########################
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    acc = 0
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
        
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
        
################    CRATE FRAME / INITIALIZE HANDLERS      ###########################

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("White")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
new_game_button = frame.add_button("New Game",new_game,120)

new_game()
frame.start()
