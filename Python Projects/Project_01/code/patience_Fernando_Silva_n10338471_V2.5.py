
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N10338471
#    Student name: FERNANDO BARBOSA SILVA
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
# PATIENCE
#
# This assignment tests your skills at processing data stored in
# lists, creating reusable code and following instructions to display
# a complex visual image.  The incomplete Python program below is
# missing a crucial function, "deal_cards".  You are required to
# complete this function so that when the program is run it draws a
# game of Patience (also called Solitaire in the US), consisting of
# multiple stacks of cards in four suits.  See the instruction sheet
# accompanying this file for full details.
#
# Note that this assignment is in two parts, the second of which
# will be released only just before the final deadline.  This
# template file will be used for both parts and you will submit
# your final solution as a single Python 3 file, whether or not you
# complete both parts of the assignment.
#
#--------------------------------------------------------------------#  



#-----Preamble-------------------------------------------------------#
#
# This section imports necessary functions and defines constant
# values used for creating the drawing canvas.  You should not change
# any of the code in this section.
#

# Import the functions needed to complete this assignment.  You
# should not need to use any other modules for your solution.  In
# particular, your solution must NOT rely on any non-standard Python
# modules that need to be installed separately, because the markers
# will not have access to such modules.

from turtle import *
from math import *
from random import *

# Define constant values used in the main program that sets up
# the drawing canvas.  Do not change any of these values.

# Constants defining the size of the card table
table_width = 1100 # width of the card table in pixels
table_height = 800 # height (actually depth) of the card table in pixels
canvas_border = 30 # border between playing area and window's edge in pixels
half_width = table_width // 2 # maximum x coordinate on table in either direction
half_height = table_height // 2 # maximum y coordinate on table in either direction

# Work out how wide some text is (in pixels)
def calculate_text_width(string, text_font = None):
    penup()
    home()
    write(string, align = 'left', move = True, font = text_font)
    text_width = xcor()
    undo() # write
    undo() # goto
    undo() # penup
    return text_width

# Constants used for drawing the coordinate axes
axis_font = ('Consolas', 10, 'normal') # font for drawing the axes
font_height = 14 # interline separation for text
tic_sep = 50 # gradations for the x and y scales shown on the screen
tics_width = calculate_text_width("-mmm -", axis_font) # width of y axis labels

# Constants defining the stacks of cards
stack_base = half_height - 25 # starting y coordinate for the stacks
num_stacks = 6 # how many locations there are for the stacks
stack_width = table_width / (num_stacks + 1) # max width of stacks
stack_gap = (table_width - num_stacks * stack_width) // (num_stacks + 1) # inter-stack gap
max_cards = 10 # maximum number of cards per stack

# Define the starting locations of each stack
stack_locations = [["Stack " + str(loc + 1),
                    [int(-half_width + (loc + 1) * stack_gap + loc * stack_width + stack_width / 2),
                     stack_base]] 
                    for loc in range(num_stacks)]

# Same as Turtle's write command, but writes upside down
def write_upside_down(string, **named_params):
    named_params['angle'] = 180
    tk_canvas = getscreen().cv
    tk_canvas.create_text(xcor(), -ycor(), named_params, text = string)

#
#--------------------------------------------------------------------#



#-----Functions for Creating the Drawing Canvas----------------------#
#
# The functions in this section are called by the main program to
# create the drawing canvas for your image.  You should not change
# any of the code in this section.
#

# Set up the canvas and draw the background for the overall image.
# By default the coordinate axes displayed - call the function
# with False as the argument to prevent this.
def create_drawing_canvas(show_axes = True):

    # Set up the drawing canvas
    setup(table_width + tics_width + canvas_border * 2,
          table_height + font_height + canvas_border * 2)

    # Draw as fast as possible
    tracer(False)

    # Make the background felt green and the pen a lighter colour
    bgcolor('green')
    pencolor('light green')

    # Lift the pen while drawing the axes
    penup()

    # Optionally draw x coordinates along the bottom of the table
    if show_axes:
        for x_coord in range(-half_width + tic_sep, half_width, tic_sep):
            goto(x_coord, -half_height - font_height)
            write('| ' + str(x_coord), align = 'left', font = axis_font)

    # Optionally draw y coordinates to the left of the table
    if show_axes:
        max_tic = int(stack_base / tic_sep) * tic_sep
        for y_coord in range(-max_tic, max_tic + tic_sep, tic_sep):
            goto(-half_width, y_coord - font_height / 2)
            write(str(y_coord).rjust(4) + ' -', font = axis_font, align = 'right')

    # Optionally mark each of the starting points for the stacks
    if show_axes:
        for name, location in stack_locations:
            # Draw the central dot
            goto(location)
            color('light green')
            dot(7)
            # Draw the horizontal line
            pensize(2)
            goto(location[0] - (stack_width // 2), location[1])
            setheading(0)
            pendown()
            forward(stack_width)
            penup()
            goto(location[0] -  (stack_width // 2), location[1] + 4)
            # Write the coordinate
            write(name + ': ' + str(location), font = axis_font)

    #Draw a border around the entire table
    penup()
    pensize(3)
    goto(-half_width, half_height) # top left
    pendown()
    goto(half_width, half_height) # top
    goto(half_width, -half_height) # right
    goto(-half_width, -half_height) # bottom
    goto(-half_width, half_height) # left

    # Reset everything, ready for the student's solution
    pencolor('black')
    width(1)
    penup()
    home()
    tracer(True)


# End the program and release the drawing canvas.
# By default the cursor (turtle) is hidden when the program
# ends - call the function with False as the argument to
# prevent this.
def release_drawing_canvas(hide_cursor = True):
    tracer(True) # ensure any partial drawing in progress is displayed
    if hide_cursor:
        hideturtle()
    done()
    
#
#--------------------------------------------------------------------#



#-----Test Data for Use During Code Development----------------------#
#
# The "fixed" data sets in this section are provided to help you
# develop and test your code.  You can use them as the argument to
# the deal_cards function while perfecting your solution.  However,
# they will NOT be used to assess your program.  Your solution will
# be assessed using the random_game function appearing below.  Your
# program must work correctly for any data set that can be generated
# by the random_game function.
#

# Each of these fixed games draws just one card
fixed_game_0 = [['Stack 1', 'Suit A', 1, 0]]
fixed_game_1 = [['Stack 2', 'Suit B', 1, 0]]
fixed_game_2 = [['Stack 3', 'Suit C', 1, 0]]
fixed_game_3 = [['Stack 4', 'Suit D', 1, 0]]

# Each of these fixed games draws several copies of just one card
fixed_game_4 = [['Stack 2', 'Suit A', 4, 0]]
fixed_game_5 = [['Stack 3', 'Suit B', 3, 0]]
fixed_game_6 = [['Stack 4', 'Suit C', 2, 0]]
fixed_game_7 = [['Stack 5', 'Suit D', 5, 0]]

# This fixed game draws each of the four cards once
fixed_game_8 = [['Stack 1', 'Suit A', 1, 0],
                ['Stack 2', 'Suit B', 1, 0],
                ['Stack 3', 'Suit C', 1, 0],
                ['Stack 4', 'Suit D', 1, 0]]

# These fixed games each contain a non-zero "extra" value
fixed_game_9 = [['Stack 3', 'Suit D', 4, 4]]
fixed_game_10 = [['Stack 4', 'Suit C', 3, 2]]
fixed_game_11 = [['Stack 5', 'Suit B', 2, 1]]
fixed_game_12 = [['Stack 6', 'Suit A', 5, 5]]

# These fixed games describe some "typical" layouts with multiple
# cards and suits. You can create more such data sets yourself
# by calling function random_game in the shell window

fixed_game_13 = \
 [['Stack 6', 'Suit D', 9, 6],
  ['Stack 4', 'Suit B', 5, 0],
  ['Stack 5', 'Suit B', 1, 1],
  ['Stack 2', 'Suit C', 4, 0]]
 
fixed_game_14 = \
 [['Stack 1', 'Suit C', 1, 0],
  ['Stack 5', 'Suit D', 2, 1],
  ['Stack 3', 'Suit A', 2, 0],
  ['Stack 2', 'Suit A', 8, 5],
  ['Stack 6', 'Suit C', 10, 0]]

fixed_game_15 = \
 [['Stack 3', 'Suit D', 0, 0],
  ['Stack 6', 'Suit B', 2, 0],
  ['Stack 2', 'Suit D', 6, 0],
  ['Stack 1', 'Suit C', 1, 0],
  ['Stack 4', 'Suit B', 1, 1],
  ['Stack 5', 'Suit A', 3, 0]]

fixed_game_16 = \
 [['Stack 6', 'Suit C', 8, 0],
  ['Stack 2', 'Suit C', 4, 4],
  ['Stack 5', 'Suit A', 9, 3],
  ['Stack 4', 'Suit C', 0, 0],
  ['Stack 1', 'Suit A', 5, 0],
  ['Stack 3', 'Suit B', 5, 0]]

fixed_game_17 = \
 [['Stack 4', 'Suit A', 6, 0],
  ['Stack 6', 'Suit C', 1, 1],
  ['Stack 5', 'Suit C', 4, 0],
  ['Stack 1', 'Suit D', 10, 0],
  ['Stack 3', 'Suit B', 9, 0],
  ['Stack 2', 'Suit D', 2, 2]]
 
# The "full_game" dataset describes a random game
# containing the maximum number of cards
stacks = ['Stack ' + str(stack_num+1) for stack_num in range(num_stacks)]
shuffle(stacks)
suits = ['Suit ' + chr(ord('A')+suit_num) for suit_num in range(4)]
shuffle(suits)
full_game = [[stacks[stack], suits[stack % 4], max_cards, randint(0, max_cards)]
             for stack in range(num_stacks)]

#
#--------------------------------------------------------------------#



#-----Function for Assessing Your Solution---------------------------#
#
# The function in this section will be used to mark your solution.
# Do not change any of the code in this section.
#
# The following function creates a random data set specifying a game
# of Patience to be drawn.  Your program must work for any data set 
# returned by this function.  The results returned by calling this 
# function will be used as the argument to your deal_cards function 
# during marking. For convenience during code development and marking 
# this function also prints the game data to the shell window.
#
# Each of the data sets generated is a list specifying a set of
# card stacks to be drawn. Each specification consists of the
# following parts:
#
# a) Which stack is being described, from Stack 1 to num_stacks.
# b) The suit of cards in the stack, from 'A' to 'D'.
# c) The number of cards in the stack, from 0 to max_cards
# d) An "extra" value, from 0 to max_cards, whose purpose will be
#    revealed only in Part B of the assignment.  You should
#    ignore it while completing Part A.
#
# There will be up to num_stacks specifications, but sometimes fewer
# stacks will be described, so your code must work for any number
# of stack specifications.
#
def random_game(print_game = True):

    # Percent chance of the extra value being non-zero
    extra_probability = 20

    # Generate all the stack and suit names playable
    game_stacks = ['Stack ' + str(stack_num+1)
                   for stack_num in range(num_stacks)]
    game_suits = ['Suit ' + chr(ord('A')+suit_num)
                  for suit_num in range(4)]

    # Create a list of stack specifications
    game = []

    # Randomly order the stacks
    shuffle(game_stacks)

    # Create the individual stack specifications 
    for stack in game_stacks:
        # Choose the suit and number of cards
        suit = choice(game_suits)
        num_cards = randint(0, max_cards)
        # Choose the extra value
        if num_cards > 0 and randint(1, 100) <= extra_probability: 
            option = randint(1,num_cards)
        else:
            option = 0
        # Add the stack to the game, but if the number of cards
        # is zero we will usually choose to omit it entirely
        if num_cards != 0 or randint(1, 4) == 4:
            game.append([stack, suit, num_cards, option])
        
    # Optionally print the result to the shell window
    if print_game:
        print('\nCards to draw ' +
              '(stack, suit, no. cards, option):\n\n',
              str(game).replace('],', '],\n '))
    
    # Return the result to the student's deal_cards function
    return game

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
#  Complete the assignment by replacing the dummy function below with
#  your own "deal_cards" function.
#

########################################################################################################################## 
#                                                IMPORTANT VARIABLES                                                     #
########################################################################################################################## 

# Variables to position the cards in the correct stack posstion

yAxis = 375 - 5      # Stack corrdenates for Y axel (Same for all stacks)
xAxisStack1 = -449   # Stack 1 - X coordenates
xAxisStack2 = -270   # Stack 2 - X coordenates
xAxisStack3 = -91    # Stack 3 - X coordenates
xAxisStack4 = 88     # Stack 4 - X coordenates
xAxisStack5 = 267    # Stack 5 - X coordenates
xAxisStack6 = 446    # Stack 6 - X coordenates



# Variables used to define card's specificatons

card_pile_variation = 55     # Variable to controle the distace of each card in the pile (Y Axis)
card_color = 'khaki'         # Color of the cards
pen_color = 'white'          # Color of the card's boarder
pen_size = 4                 # Thickness of card's boarder 
card_height = 220            # Card height
card_width = 140             # Card width
CardID_color = "darkblue"    # Define color of the cardID (numbers used to identify each card)
card_curved_edge = -10       # Ajust the size of the round edges in the function card1()



# Variable used to define suit specifications

penSize_suit = 1             # Thickness of the suit drawings
y_PositioSuits = 10          # Ajust the height of the suit's draw in the card



# Variables used to define flag's specification

flag_size_small = 40         # Smal flag width size
flag_size_big = 120          # Big flag width size



########################################################################################################################## 
#                                                    CARD DRAW FUNCTION                                                  #
##########################################################################################################################

'''This function  uses the parameter given by the function deal_cards(gamelist) to; draw the cards
in the right positon, to define the number of the cards that will be drawn in each stack, and  define each suit
will be drawn in the stack.'''

def card1(x , y, suit, nrCards, joker):     # Card draw  "x = Stack coordenate in X axis"
                                            # "y = Stack coordinate in Y axis"
                                              
    count = 1                               # Counts the number of card to controle when place the joker
    
    for card in range(nrCards):             # nrCads in the number of card that must be drawn 

        # Important variables used to draw the cards
        pencolor(pen_color)       
        fillcolor(card_color)           
        pensize(pen_size)
        begin_fill()
        newCardCoordenate = y - card_pile_variation  # Ajust coordenade of each card in the stack
        y = newCardCoordenate                        # Cordenate of each new card in the pile

        # Statement to draw the card
        pendown()
        forward(card_width / 2)
        circle(card_curved_edge, 90)
        forward(card_height)
        circle(card_curved_edge, 90)
        forward(card_width)
        circle(card_curved_edge, 90)
        forward(card_height)
        circle(card_curved_edge, 90)
        forward(card_width)
        end_fill()
        
        if joker == count:              # Call the function "joker() when count is iqual to joker index in the list"
            joker_suit (x - flag_size_big/2 , y - flag_size_big/5, flag_size_big)
            joker_suit (x + flag_size_small/2, y + flag_size_small, flag_size_small )
                      
        else:
            
            if suit == 'Suit A':        # Call the function "suitA(x,y)"
                suitA (x - flag_size_big/2 , y - flag_size_big/5, flag_size_big)
                suitA (x + flag_size_small/2, y + flag_size_small, flag_size_small )

            if suit == 'Suit B':        # Call the function "suitB(x,y)"
                suitB (x - flag_size_big/2 , y - flag_size_big/5, flag_size_big)
                suitB (x + flag_size_small/2, y + flag_size_small, flag_size_small )

            if suit == 'Suit C':        # Call the function "suitC(x,y)"
                suitC (x - flag_size_big/2 , y - flag_size_big/5, flag_size_big)
                suitC (x + flag_size_small/2, y + flag_size_small, flag_size_small )

            if suit == 'Suit D':        # Call the function "suitD(x,y,flagSize)"
                suitD (x - flag_size_big/2 , y - flag_size_big/5, flag_size_big)
                suitD (x + flag_size_small/2, y + flag_size_small, flag_size_small )
                
        cardID(x,y,card)                # Call cardID Function to put number in the cards
        penup()  
        count = count + 1
        goto(x, y)


##########################################################################################################################
#                                                   CARDID FUNCTION                                                      #
##########################################################################################################################
        
'''Draw the id number in each card in the stack. The cardID function is called by the function card1(). '''

def cardID(x,y,card):
    cardID_Top_positio_X = 65                       # Used to position cardID in  the top of card
    cardID_Top_positio_Y = 30                       # Used to position cardID in  the top of card
    cardID_Bottom_positio_X = 50                    # Used to position cardID in the bottom of the card
    cardID_Bottom_positio_Y = card_height - 40      # Used to position cardID in the bottom of the card 
    
    ## Coordenates list to position the cardID in the top and bottom of the cards
    list_position = [[x - cardID_Top_positio_X, y + cardID_Top_positio_Y],\
                     [x + cardID_Bottom_positio_X, y - cardID_Bottom_positio_Y]]
   
    for index in list_position:  
        penup()
        goto(index[0], index[1])      # Position to write cardID in the card
        pendown()
        pencolor(CardID_color)             
        write(card + 1, False, 'left', font=('Arial', 14, 'bold')) # Statement and specifications
                                                                          # to write the card number ID

##########################################################################################################################
#                                              NATIONAL FLAG FUNCTIONS SUITS                                             #
##########################################################################################################################                                                                         
                                                                          
'''Code to draw the 5 different suits used by the program. The suitA(),
suitB(), suitC(), suitD() ,and joker() function are called by the function card1(). '''



#********************************************* SUIT A = NORWEGIAN FLAG **************************************************
'''Draw the Norwegian flag suit. Follow the Norwegian flag measurements guideline'''

def suitA(x, y, flagSize):       # "x = suit position in X axis"
                                 # "y = suit position in Y axis" inside the card

    # Importnt variables do draw the flag
    flagWidth = flagSize                
    flagHeight = flagWidth * 0.7272             # Flag height size in proportion of the flagWidth
    pen_size = 1
    pen_color = "black"  
    penup()
    square_red = flagWidth * 0.272727           # squares's proportion in relation of the flag size
    rectangle_red_width = flagWidth * 0.545454  # rectangle's width proportion in relation of the flag width
    rectangle_blue_height = flagHeight * 0.125  # rectangle's height proportion in relation of the flag height
    white_height = flagWidth * 0.04545          # height proportion of the white part in the flag
    

    ## Draw the red squares in the flag 
    def square():
        pendown()
        begin_fill()
        color('red')
        pensize (pen_size)
        for size in range (4):
            forward(square_red ) 
            left(-90)
        end_fill()
        penup()

    ## Draw the rectangles in the flag      
    def rectangle(width, height, color_rect): # Draw the rectangle Flag
        pendown()
        begin_fill()
        color(color_rect)
        pensize (pen_size)
        for size in range (2):
            forward(width)
            left(-90)
            forward (height)
            left(-90)
        end_fill()
        penup()


    ## Call the functions in order to build the flag       
    goto(x,y) 
    rectangle (flagWidth, flagHeight, "white")

    goto(x,y) 
    square()

    goto(x + (flagWidth - rectangle_red_width), y)
    pendown()
    rectangle (rectangle_red_width, square_red, "red" ) 

    goto (x, y - (flagHeight - square_red)) 
    square()

    goto (x + (flagWidth - rectangle_red_width), y - (flagHeight - square_red)) 
    rectangle (rectangle_red_width, square_red, "red" )

    goto (x, y - (square_red + white_height))
    rectangle (flagWidth, rectangle_blue_height, "blue" )

    goto(x +(square_red + white_height), y)
    rectangle (rectangle_blue_height, flagHeight , "blue")




#********************************************* SUIT B = CANADIAN FLAG **************************************************
'''Draw the Canadian flag suit. Follow the Canadian flag measurements guideline'''
                                 
def suitB(x, y , flagSize):      # "x = suit position in X axis"
                                 # "y = suit position in Y axis" inside the card
                                 
   ## Importnt variables do draw the flag                               
    flagWidth = flagSize               
    flagHeight = flagWidth * 0.6    # Flag height size in proportion of the fladWidth 
    pen_size = 1
    pen_color = "black"  
    penup()
    red_rectangle_width = flagSize / 4
    mapleLeaf_y_coordinate = flagHeight *0.9275 # Flag proportional position
    
    
    ## Draw the rectangles of the flag    
    def rectangle(width, height, colour_rec): 
        pendown()
        begin_fill()
        color(colour_rec)
        pensize (pen_size)
        for size in range (2):
            forward(width)
            left(-90)
            forward (height)
            left(-90)
        end_fill()
        penup()


    ## Draw the maple leaf in the flag
    '''Draw the maple leaf using coordinates and proportions in relation to the flagSize.
       Each coordinate and proportion (e.g. 0.007881) was calculated manually.'''
    
    def maple_leaf(): 
        pendown()
        begin_fill()
        color('red')
        forward(flagSize * 0.00781)
        left(90)  
        forward(flagSize * 0.09375)
        left(-95) 
        forward(flagSize * 0.10938)
        left(120)
        forward(flagSize * 0.03125)
        left(-70) 
        forward(flagSize * 0.09375)
        left(120) 
        forward(flagSize * 0.03125)
        left(-100)
        forward(flagSize * 0.06250)
        left(120) 
        forward(flagSize * 0.06250)
        left(-100) 
        forward(flagSize * 0.03125)
        left(140) 
        forward(flagSize * 0.06250)
        left(-140) 
        forward(flagSize * 0.09375)
        left(140) 
        forward(flagSize * 0.03125)
        left(-100) 
        forward(flagSize * 0.06250)
        left(110) 
        forward(flagSize * 0.06250)
        left(-100) 
        forward(flagSize * 0.03125)
        left(140) 
        forward(flagSize * 0.09375)
        left(-140) 
        forward(flagSize * 0.06250)
        left(140) 
        forward(flagSize * 0.03125)
        left(-100) 
        forward(flagSize * 0.06250)
        left(120) 
        forward(flagSize * 0.06250)
        left(-100) 
        forward(flagSize * 0.03125)
        left(120) 
        forward(flagSize * 0.09375)
        left(-70) 
        forward(flagSize * 0.03125)
        left(121)
        forward(flagSize * 0.09375)
        left(-97) 
        forward(flagSize * 0.09375)
        left(90)
        forward(flagSize * 0.00781)
        end_fill()
        left(1)

     
    ## Call the functions in order to build the flag        
    goto(x,y)
    rectangle(flagWidth,flagHeight, 'white')

    goto(x,y)
    rectangle(red_rectangle_width, flagHeight, 'red')

    goto(x + (3*red_rectangle_width),y)
    rectangle(red_rectangle_width, flagHeight, 'red')

    goto(x + flagSize / 2, y - mapleLeaf_y_coordinate)
    maple_leaf()
    



#********************************************* SUIT D = SOUTH AFRICA FLAG **************************************************    
'''Draw the South Africa flag suit. Follow the South Africa flag measurements guideline'''

def suitC(x, y , flagSize):      # "x = suit position in X axis"
                                 # "y = suit position in Y axis" inside the card
                                 
    ## Importnt variables do draw the flag 
    flagWidth = flagSize                 
    flagHeight = flagWidth * 0.6666      # Flag height size in proportion of the flagWidth
    pen_size = 1
    pen_color = "black"  
    penup()
    red_rectangle_height  = flagHeight / 3
    blue_rectangle_height = flagHeight / 3
    green_rectangle_height = flagHeight * 0.20

    
    
    ## Draw the white rectangle of the flag
    def rectangle(width, height, colour): # Draw the rectangles of the Flag
        pendown()
        begin_fill()
        color(colour)
        pensize (pen_size)
        for size in range (2):
            forward(width)
            left(-90)
            forward (height)
            left(-90)
        end_fill()
        penup()


    ## Draw triangle in proportion of the size of the flag  
    def triangle(flagWidth, height_pro, hypotenuse_pro,tri_colour): # heigh_pro and hypotenuse is a proportion of the flag
        pendown()
        begin_fill()
        color(tri_colour)
        left(-90)
        forward(flagWidth * height_pro)     # Height of the triangle * proportion of flagWidth
        left(123.69)                        
        forward(flagWidth * hypotenuse_pro) # Hypotenuse in proportion of flagWidth
        left(112.62)
        forward(flagWidth * hypotenuse_pro) # Hypotenuse in proportion of flagWidth
        end_fill()
    
        
    ## Call each function in order to draw the South Africa flag
    '''Draw the rectangles and triangles of the flag in the right position and size.
       Each coordinate and proportion (e.g. 0.6666 and 0.60093) was calculated manually
       occording with the flag proportion guideline.'''
    
    goto(x, y)
    rectangle(flagWidth, flagHeight, "white")

    goto(x, y)
    rectangle(flagWidth, red_rectangle_height, "red")

    goto(x, y - (blue_rectangle_height * 2))
    rectangle(flagWidth, blue_rectangle_height, "blue")

    goto(x + (flagWidth * 0.2) , y )                    
    triangle(flagWidth, 0.6666 , 0.60093,"white")       # 0.6666 and 0.60093 are proportions in relation to the flagWidth.
    left(213.69)

    goto(x, y - (flagHeight * 0.4))  
    rectangle(flagWidth, green_rectangle_height, "green")

    goto(x, y)
    rectangle(flagWidth * 0.20, flagHeight, "white")    # 0.2 is the rectangle proportion in relation to the
                                                            #flagWidth to draw the rectangle

    goto(x + (flagWidth * 0.12) , y )
    triangle(flagWidth, 0.6666 , 0.60093,"green")       # 0.6666 and 0.60093 are the triangle proportions in
                                                            #relation to the flagWidth.
    left(213.69)  

    goto(x, y)
    rectangle(flagWidth * 0.12, flagHeight, "green")    # 0.12 is the rectangle proportion in relation to the
                                                            #flagWidth to draw the rectangle
    
    goto(x, y -(flagHeight * 0.12) )
    triangle(flagWidth, 0.5066, 0.45741,"yellow")       # 0.5066 and 0.45741 are the triangle proportions in
                                                            #relation to the flagWidth to draw the triangle.
    left(213.69)   

    goto(x, y -(flagHeight * 0.2) )
    triangle(flagWidth, 0.40, 0.36056,"black")          # 0.4 and 0.36056 are the triangle proportions in
                                                            #relation to the flagWidth to draw the triangle.
    left(213.69)
    


#********************************************* SUIT D = BRAZILIAN FLAG **************************************************
'''Draw the Brazilian flag suit. Follow the Brazilian flag measurements guideline'''
    
def suitD(x,y,flagSize): # (position X, position Y, Flag widthSize)
    
    ## Important variables    
    flagWidth = flagSize                    
    flagHeight = flagWidth * .7             # Flag height size in proportion of the flagWidth
    distance = flagWidth * 0.085            # Distance from the rectangle to draw the yellow diamond
    hypotenuse = sqrt((flagWidth/2 - distance)**2 + (flagHeight/2 - distance)**2)  # Size of each side in the yellow diamond
    circleRadius = flagWidth * 0.175        # Size of the blue circle
    pen_size = 1
    pen_color = "black"  
    penup()
    
    ## Draw the green rectangle    
    def rectangle(x,y):
        goto(x,y)
        pendown()
        pensize(pen_size)
        pencolor(pen_color)
        fillcolor('green')
        begin_fill()
        for size in range (2):    
            forward(flagWidth)
            left(-90)
            forward(flagHeight)
            left(-90)
        end_fill()
        penup()

    ## Draw the yellow diamond       
    def diamend(x,y):
        goto(x + (flagWidth / 2), y - distance)
        pensize(pen_size)
        pencolor(pen_color)
        fillcolor('yellow')
        begin_fill()
        pendown()
        left(-32.56)
        forward(hypotenuse)
        left(-114.88)
        forward(hypotenuse)
        left(- 65.12)
        forward(hypotenuse)
        left(-114.88)
        forward(hypotenuse)
        end_fill()
        penup()

    ## Draw the blue circle        
    def circle_flag(x,y):
        goto((x + flagWidth/2), (y - flagHeight * 0.75))
        pensize(pen_size)
        pencolor(pen_color)
        fillcolor('blue')
        begin_fill()
        pendown()
        left(-31.56)
        circle(circleRadius)
        end_fill()
        penup()

    ## Draw the while line inside the circle      
    def line(x,y):
        pensize(flagWidth*0.02333)              # Difine the pen size to draw the white line inside the blue circle
        goto((x + flagWidth/2 - circleRadius), (y - flagHeight/2))
        left(-20)
        pendown()
        pencolor('white')
        left(30)
        for move in range(4):      
            forward(circleRadius/2)
            left(-10)
        penup()
        left(29)
        pensize(pen_size)

    ## Call each function in order to draw the Brazilian flag  
    rectangle(x,y)
    diamend(x,y)
    circle_flag(x,y)
    line(x,y)

    

#********************************************* SUIT JOKER = Black Cross Flag **************************************************

'''Draw the Black Cross Flag flag suit'''
    
def joker_suit(x,y,flagSize):                   # (position X, position Y, Flag widthSize)
    
    ## Importnt variables do draw the flag   
    flagWidth = flagSize                 
    flagHeight = flagWidth * 0.7272              # Flag height size in proportion of flagWidth
    pen_size = 1
    pen_color = "black"  
    penup()
    square = flagWidth * 0.272727                # Squares's proportion in relation of the flag size
    rectangle_width = flagWidth * 0.545454       # Rectangle's width proportion in relation of the flag width
    
    ## Draw the white black square in the flag
    def square_draw(): 
        pendown()
        begin_fill()
        color('black')
        pensize (pen_size)
        for size in range (4):
            forward(square ) 
            left(-90)
        end_fill()
        penup()


    ## Draw the rectangles in the flag   
    def rectangle(side1, side2, color_rec): 
        pendown()
        begin_fill()
        color(color_rec)
        pensize (pen_size)
        for size in range (2):
            forward(side1 ) 
            left(-90)
            forward (side2)
            left(-90)
        end_fill()
        penup()
    
        
    # Call each function in order to draw the Joker flag  
    goto (x,y)
    rectangle (flagWidth, flagHeight, 'white')
    
    goto (x,y)
    square_draw ()
    
    goto (x + (flagWidth - rectangle_width), y)
    pendown ()
    rectangle(rectangle_width, square, 'black')   

    goto (x, y - (flagHeight - square))
    square_draw()
    
    goto (x + (flagWidth - rectangle_width), y - (flagHeight - square))
    rectangle(rectangle_width, square, 'black')
    


##########################################################################################################################
#                                                   DEAL CARDS FUNCTION                                                  #
##########################################################################################################################
    
''' The deal_cards() function reads the list provided by the porogram and give a name for each index
in the list. This function call the function card1(x , y, suit, nrCards, joker) in the right position
of the stack '''


def deal_cards(gamelist):
    for stack, suit, nrCards, joker in gamelist:
        if stack == 'Stack 1':  # Lay the cards in the Stack 1 position
            penup()
            goto(xAxisStack1, yAxis)
            card1(xAxisStack1, yAxis, suit, nrCards, joker)

        if stack == 'Stack 2':  # Lay the cards in the Stack 2 position
            penup()
            goto(xAxisStack2, yAxis)
            card1(xAxisStack2, yAxis, suit, nrCards, joker)

        if stack == 'Stack 3':  # Lay the cards in the Stack 3 position
            penup()
            goto(xAxisStack3, yAxis)
            card1(xAxisStack3, yAxis, suit, nrCards, joker)

        if stack == 'Stack 4':  # Lay the cards in the Stack 4 position
            penup()
            goto(xAxisStack4, yAxis)
            card1(xAxisStack4, yAxis, suit, nrCards, joker )         

        if stack == 'Stack 5':   # Lay the cards in the Stack 5 position
            penup()
            goto(xAxisStack5, yAxis)
            card1(xAxisStack5, yAxis, suit, nrCards, joker)
            
        if stack == 'Stack 6':  # Lay the cards in the Stack 6 position
            penup()
            goto(xAxisStack6, yAxis)
            card1(xAxisStack6, yAxis, suit, nrCards, joker)



#
#--------------------------------------------------------------------#



#-----Main Program---------------------------------------------------#
#
# This main program sets up the background, ready for you to start
# drawing the card game.  Do not change any of this code except
# as indicated by the comments marked '*****'.
#

# Set up the drawing canvas
# ***** Change the default argument to False if you don't want to
# ***** display the coordinates and stack locations
create_drawing_canvas(False)

# Control the drawing speed
# ***** Modify the following argument if you want to adjust
# ***** the drawing speed
speed('fastest')

# Decide whether or not to show the drawing being done step-by-step
# ***** Set the following argument to False if you don't want to wait
# ***** while the cursor moves around the screen
tracer(False)

# Give the drawing canvas a title
# ***** Replace this title with a description of your cards' theme
title("NATIONAL FLAGS")

### Call the student's function to draw the game
### ***** While developing your program you can call the deal_cards
### ***** function with one of the "fixed" data sets, but your
### ***** final solution must work with "random_game()" as the
### ***** argument to the deal_cards function.  Your program must
### ***** work for any data set that can be returned by the
### ***** random_game function.
# deal_cards(fixed_game_0) # <-- used for code development only, not marking
# deal_cards(full_game) # <-- used for code development only, not marking
deal_cards(random_game()) # <-- used for assessment

# Exit gracefully
# ***** Change the default argument to False if you want the
# ***** cursor (turtle) to remain visible at the end of the
# ***** program as a debugging aid
release_drawing_canvas()

#
#--------------------------------------------------------------------#

