# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import math
import random
import simplegui

num_range=100
chances_left=7
secret_number=0
# assigned some default value to secret_number that may be modified later

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number,chances_left,num_range
    secret_number = random.randrange(0,num_range)
    chances_left = int(math.ceil(math.log(num_range+1,2)))
    
    #print without any argument prints blank line
    
    print
    print 'New game.Range is from 0 to ' + str(num_range)
    print 'Number of guesses left is ' + str(chances_left)


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range,chances_left
    num_range=100
    chances_left=7
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range,chances_left
    num_range=1000
    chances_left=10
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global chances_left
        
    num_guess=int(guess)
    print
    print 'Guess was ' + guess
    
    chances_left = chances_left - 1
    
    if chances_left == 0 :
        if num_guess !=secret_number:
            print 'Sorry,The guesses are over. '
            print 'The secret number was ' + str(secret_number)
            new_game()
        else:
            print 'Correct'
            new_game()
    else:
        if num_guess > secret_number :
            print 'Lower'
            print 'Number of remaining guesses is ' + str(chances_left)
        elif num_guess < secret_number :
            print 'Higher'
            print 'Number of remaining guesses is ' + str(chances_left)
        else:
            print 'Correct'
            new_game()
    
# create frame
frame = simplegui.create_frame('Guess the number',200,200)

# register event handlers for control elements and start frame

input_guess=frame.add_input('Enter a guess',input_guess,200)
button_range_100=frame.add_button('Range: 0-100',range100,200)
button_range_1000=frame.add_button('Range: 0-1000',range1000,200)
frame.start()

# call new_game 
new_game()
