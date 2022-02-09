from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import random

'''
Above: Libraries for projects
    Tkinter: Visual window API, allows for buttons, labels, & more
    Image: Image handler, allows for images to be brought into the Tkinter window efficiently
    Random: Common Python library, allows for random values such as random enemy movement and image selection
Below: Constants/Creation of Tkinter window
'''

window = Tk()
window.geometry("1280x720")
max_width = 1280
max_height = 720
game_background = "#42f58d"
enemy_dictionary = {}
enemy_count = 0


# Starting window/main menu for entire game, runs some more constants within the window software
# to prevent repeating values from previous runs of the game within the same software run
def run_window():
    global enemy_dictionary
    enemy_dictionary = {}
    global enemy_count
    enemy_count = 0
    # Destroys widgets
    for widget in window.winfo_children():
        widget.destroy()
    # Creates title, starting button, game info button,
    title = Label(text="Mr. Clean's Washing Challenge!", font=tkFont.Font(family="Comic Sans MS", size=35),
                  bg=game_background)
    title.pack(padx=10)
    start = Button(text="Start!", width=30, height=3, font=50, command=run_game)
    start.pack(pady=140)
    game_info = Button(text="Game Info", width=25, command=run_game_info)
    game_info.pack()
    credits = Label(text="Made By: Sebastian Candelaria, 2021", font=5, width=50, height=3, bg=game_background)
    credits.pack(pady=50)
    # Changes background and loops all objects into a window
    window.configure(bg=game_background)
    window.mainloop()


# Game Info menu, holds controls/gameplay rundown, can have difficulty options & more in the future
def run_game_info():
    for widget in window.winfo_children():
        widget.destroy()
    # Creates title, main menu return button, and other texts
    title = Label(text="Game Info", font=tkFont.Font(family="Comic Sans MS", size=35),
                  bg=game_background)
    title.pack(padx=10)
    start_return = Button(text="Return to Start", command=run_window)
    start_return.pack(pady=30)
    controls_title = Label(text="Controls", font=tkFont.Font(family="Times New Roman", size=25), bg=game_background)
    controls_title.pack(pady=20)
    controls = Label(text="Move up: Up Arrow\nMove down: Down Arrow\nMove right: Right Arrow\nMove left: Left Arrow",
                     bg=game_background, font=10)
    controls.pack(pady=20)
    gameplay_title = Label(text="Gameplay", font=tkFont.Font(family="Times New Roman", size=25), bg=game_background)
    gameplay_title.pack(pady=20)
    gameplay = Label(text="""Your goal is to defeat all germs on the screen.
    To defeat them you must move onto the spaces they occupy on the screen.
    However, the germs will fight back! If they step on a space you are on, the game will be over.
    Note: More than one enemy at a time can occupy a space and an enemy can stand still next to the border.""",
                     bg=game_background, font=10)
    # Pady & padx puts padding or space between widgets
    gameplay.pack(pady=20)


# Global variables in run_game function
img_width = 100
img_height = 100
player_x = 640 - img_width / 2
player_y = 310 - img_height / 2
player = None
player_info = None
enemy_total = 3
enemy_amount = enemy_total


# Where the entire game actually runs, including player and enemy objects, movement, and interaction logic
def run_game():
    # Creates constants and sets global variables to be used and manipulated everywhere in the program
    buttons = []
    enemy_count = 0
    global enemy_total
    global enemy_amount
    enemy_total = 3
    enemy_amount = enemy_total
    enemy_images = ['red_virus.png', 'yellow_virus.png', 'blue_virus.png']
    for widget in window.winfo_children():
        widget.destroy()

    # Creates enemies remaining display and orange game borders
    total = Label(text="Enemies: " + str(enemy_amount) + "/" + str(enemy_total), bg=game_background,
                  font=tkFont.Font(family="Times New Roman", size=20))
    total.place(x=780, y=600)
    left_border = Label(text='', bg='orange', width=26, height=38)
    # Place method puts widgets on pixel positions along their top-left corners
    left_border.place(x=0, y=0)
    right_border = Label(text='', bg='orange', width=26, height=38)
    right_border.place(x=1095, y=0)
    bottom_border = Label(text='', bg='orange', width=200, height=1)
    bottom_border.place(x=0, y=565)
    top_border = Label(text='', bg='orange', width=200, height=4)
    top_border.place(x=0, y=-8)

    # Creates player representation and places on the game board
    img = Image.open("Mr Clean.jpeg")
    img = img.resize((img_width, img_height))
    img = ImageTk.PhotoImage(img)
    player = Label(image=img)
    player.photo = img
    player.place(x=player_x, y=player_y)

    # When called, this function will create an enemy and place them on a position not occupied by the player or
    # another enemy
    def create_enemy():
        global enemy_count
        # Creates enemy object
        img = Image.open(random.choice(enemy_images))
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        enemy = Label(image=img)
        enemy.photo = img
        enemy_x, enemy_y = player_x, player_y
        # Picks a random coordinates for the enemy and randomizes again if the
        # coordinates are already occupied by an enemy or the player
        reset = True
        while enemy_x == player_x or enemy_y == player_y or reset:
            enemy_x = random.choice([190, 290, 390, 490, 590, 690, 790, 890, 990])
            enemy_y = random.choice([60, 160, 260, 360, 460])
            reset = False
            for i in range(len(enemy_dictionary)):
                if enemy_dictionary.get(i) is None:
                    break
                elif enemy_dictionary[i + 1].place_info()['x'] == enemy_x and \
                        enemy_dictionary[i + 1].place_info()['y'] == enemy_y:
                    reset = True
        # Places enemy and adds their info to a dictionary, keys being integers from 1 to 3
        enemy.place(x=enemy_x, y=enemy_y)
        enemy_dictionary[enemy_count + 1] = enemy
        enemy_count += 1

    # Creates an enemy three times
    for i in range(3):
        create_enemy()

    # If the player is on the same space as an enemy, the enemy widget is destroyed and erased from the dictionary,
    # the info in dictionary being replaced by other widgets to adjust to the dictionary size change
    def kill_enemy():
        global enemy_amount
        for i in range(len(enemy_dictionary) + 1):
            if enemy_dictionary.get(i) is None:
                continue
            elif enemy_dictionary.get(i).place_info()['x'] == player_info['x'] and \
                    enemy_dictionary.get(i).place_info()['y'] == player_info['y']:
                enemy_dictionary[i].destroy()
                del enemy_dictionary[i]
                for a in range(i, len(enemy_dictionary) + 1):
                    enemy_dictionary[i] = enemy_dictionary.get(a + 1)
                    del enemy_dictionary[a + 1]
                    i += 1
                # Decreases number of enemies displayed in the bottom next to the buttons
                enemy_amount -= 1
                total.config(text="Enemies: " + str(enemy_amount) + "/" + str(enemy_total))

    # Determines left movement in a grid pattern for both players and enemies, the actions occuring being based on
    # the variables inputted
    def move_left(event=None, x=False, y=False, enemy=False):
        global player_x
        global player_info
        global enemy_dictionary
        # Checks whether the widget being moved is an enemy or not
        if not enemy:
            # Checks if the player is already next to the border, if not the player is moved and info is updated
            if player_x > 230:
                player.place(x=player_x - 100, y=player_y)
                player_info = player.place_info()
                player_x = int(player_info['x'])
                # Checks if an enemy can be killed
                kill_enemy()
                # Moves enemies around after player has moved
                move_enemies()
        else:
            # Checks if enemy is next to the border, if not the enemy moves and the program checks if the enemy has
            # killed the player
            if x > 230:
                enemy_dictionary.get(enemy).place(x=x - 100, y=y)
                attempt_game_over(enemy)

    # Creates a left button that can be used by the player for movement
    left_button = Button(window, text='Move Left', command=move_left)
    left_button.place(x=280, y=600)
    # Binds the left arrow key to the left player movement
    window.bind('<Left>', move_left)
    # Adds button and binding to a list of buttons that will be used later
    buttons.append([left_button, '<Left>'])

    # Same as before except moving upwards instead
    def move_up(event=None, x=False, y=False, enemy=False):
        global player_y
        global player_info
        global enemy_dictionary
        if not enemy:
            if player_y > 60:
                player.place(x=player_x, y=player_y - 100)
                player_info = player.place_info()
                player_y = int(player_info['y'])
                kill_enemy()
                move_enemies()
        else:
            if y > 60:
                enemy_dictionary.get(enemy).place(x=x, y=y - 100)
                attempt_game_over(enemy)

    up_button = Button(window, text='Move Up', command=move_up)
    up_button.place(x=380, y=600)
    window.bind('<Up>', move_up)
    buttons.append([up_button, '<Up>'])

    # Again, same as before but for right button
    def move_right(event=None, x=False, y=False, enemy=False):
        global player_x
        global player_info
        global enemy_dictionary
        if not enemy:
            if player_x < 980:
                player.place(x=player_x + 100, y=player_y)
                player_info = player.place_info()
                player_x = int(player_info['x'])
                kill_enemy()
                move_enemies()
        else:
            if x < 980:
                enemy_dictionary.get(enemy).place(x=x + 100, y=y)
                attempt_game_over(enemy)

    right_button = Button(window, text='Move right', command=move_right)
    right_button.place(x=480, y=600)
    window.bind('<Right>', move_right)
    buttons.append([right_button, '<Right>'])

    # Once more, same as before but for moving downward
    def move_down(event=None, x=None, y=None, enemy=False):
        global player_y
        global player_info
        global enemy_dictionary
        if not enemy:
            if player_y < 450:
                player.place(x=player_x, y=player_y + 100)
                player_info = player.place_info()
                player_y = int(player_info['y'])
                kill_enemy()
                move_enemies()
        else:
            if y < 450:
                enemy_dictionary.get(enemy).place(x=x, y=y + 100)
                attempt_game_over(enemy)

    down_button = Button(window, text='Move down', command=move_down)
    down_button.place(x=580, y=600)
    window.bind('<Down>', move_down)
    buttons.append([down_button, '<Down>'])

    # Game Over screen, only kills player when enemy walks onto player space
    def attempt_game_over(a):
        global player_x
        global player_y
        # Checks if an enemy is on the same position as the player, if so displays "Game Over" text and a main menu
        # return button
        if enemy_dictionary.get(a).place_info()['x'] == player.place_info()['x'] and \
                enemy_dictionary.get(a).place_info()['y'] == player.place_info()['y']:
            # Resets player position to center for next game run
            player_x = 640 - img_width / 2
            player_y = 310 - img_height / 2
            game_over = Label(text="Game Over", fg="red", bg=game_background,
                              font=tkFont.Font(family="Times New Roman", size=35), justify=CENTER)
            game_over.place(x=640 - img_width, y=360 - img_height / 2)
            restart = Button(text="Back to Main Menu", command=run_window)
            restart.place(x=640 - img_width / 2, y=460 - img_height / 2)
            # Buttons are destroyed and keys are unbinded preventing player from moving
            for button in buttons:
                window.unbind(button[1])
                button[0].destroy()

    # When called, this function will move enemies onto unoccupied spots within the game grid
    def move_enemies():
        # Checks if there are no more enemies, if so the game begins the victory sequence
        if len(enemy_dictionary) == 0:
            run_victory()
        else:
            # For each enemy, a random movement is done and if the movement leads to a space occupied by an enemy the
            # enemy is reset to their original position and randomly selects a new movement
            for e in range(len(enemy_dictionary) + 1):
                if enemy_dictionary.get(e) is None:
                    continue
                enemy_x = int(enemy_dictionary.get(e).place_info()['x'])
                enemy_y = int(enemy_dictionary.get(e).place_info()['y'])
                reset = True
                while enemy_dictionary.get(e).place_info()['x'] == enemy_x or \
                        enemy_dictionary.get(e).place_info()['y'] == enemy_y or reset:
                    enemy_dictionary.get(e).place(x=enemy_x, y=enemy_y)
                    # Randomly selects a number that determines the movement done
                    movement = random.randint(0, 3)
                    if movement == 0:
                        move_down(x=enemy_x, y=enemy_y, enemy=e)
                    elif movement == 1:
                        move_left(x=enemy_x, y=enemy_y, enemy=e)
                    elif movement == 2:
                        move_right(x=enemy_x, y=enemy_y, enemy=e)
                    else:
                        move_up(x=enemy_x, y=enemy_y, enemy=e)
                    reset = False
                    for a in range(len(enemy_dictionary) + 1):
                        if enemy_dictionary.get(a) is None:
                            break
                        elif enemy_dictionary.get(a).place_info()['x'] == enemy_dictionary.get(e).place_info()['x'] or \
                                enemy_dictionary.get(a).place_info()['y'] == enemy_dictionary.get(e).place_info()['y']:
                            enemy_dictionary.get(e).place(x=enemy_x, y=enemy_y)
                            reset = True


# Victory Screen

def run_victory():
    global player_x
    global player_y
    for widget in window.winfo_children():
        widget.destroy()
    player_x = 640 - img_width / 2
    player_y = 310 - img_height / 2
    # Shows a victory message and a button that will return the player to the main menu
    message = Label(text="Congratulations! You defeated all of the germs! You are a true",
                    font=tkFont.Font(family="Comic Sans MS", size=20), bg=game_background)
    message.pack(padx=100)
    winner = Label(text="Cleaning Master", justify=CENTER, fg="#34a8eb",
                   font=tkFont.Font(family="Times New Roman", size=100), bg=game_background)
    winner.pack(pady=100)
    restart = Button(text="Back to Main Menu", command=run_window)
    restart.pack()


# Printing out exposition/introductory text
print("Hello fellow gamers, welcome to Mr. Clean's Washing Challenge!",
      "\nIn this game, you will command Mr. Clean on his mission to eliminate the pesky germs!",
      '\nKill enough germs with your detergent and soap in hand to complete the challenge, good luck!',
      '\n(Controls: Move up = Up Arrow, Move right = Right Arrow, Move down = Down Arrow, Move left = Left Arrow)')
# Running game on Tkinter window
run_window()
