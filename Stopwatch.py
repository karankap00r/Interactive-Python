# template for "Stopwatch: The Game"

import simplegui

# define global variables
interval = 100
tenth_second = 0
x = 0
y = 0
a = 0
b = 0
c = 0
d = 0
running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global a,b,c,d
    d = t % 10
    t = t // 10
    a = t // 60
    temp = t % 60
    c = temp % 10
    b = temp // 10
    return str(a) + ":" + str(b) + str(c) + "." + str(d)    


# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global running
    timer.start()
    running = True
    
def stop_timer():
    global running
    timer.stop()
    global x,y
    if running == True :
        y = y + 1
        if d == 0 :
            x = x + 1
    running = False
    
def reset_timer():
    global tenth_second,x,y,running,a,b,c,d
    timer.stop()
    tenth_second = 0
    x = 0
    y = 0
    a = 0
    b = 0
    c = 0
    d = 0
    running = False

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tenth_second
    tenth_second=tenth_second + 1
    
# define draw handler
def draw(canvas):
    global tenth_second,x,y
    formatted_time = format(tenth_second)
    canvas.draw_text(formatted_time,(50,110),36,'White')
    canvas.draw_text(str(x) + "/" + str(y),(150,30),36,'Green')
    
# create frame
frame = simplegui.create_frame("Stopwatch",200,200)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval,timer_handler)
frame.add_button("Start",start_timer,100)
frame.add_button("Stop",stop_timer,100)
frame.add_button("Reset",reset_timer,100)

# start frame
frame.start()

# Please remember to review the grading rubric
