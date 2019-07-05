"""minesweeper_updated.py
A minesweeper game
Author: Daniel Harris
Created: 13.07.18
"""
import random
from tkinter import *

window = Tk()
BUTTON_SIZE = 16
BUTTON_HALFSIZE = BUTTON_SIZE // 2

PHOTO_DICT = {
"NONE": PhotoImage(file="images\\none.gif"),
"MINE": PhotoImage(file="images\\mine.gif"),
"FLAG": PhotoImage(file="images\\flag.gif"),
"FLAG_WRONG": PhotoImage(file="images\\flag_wrong.gif"),
"CLICKED": PhotoImage(file="images\\clicked.gif"),
"1": PhotoImage(file="images\\1.gif"),
"2": PhotoImage(file="images\\2.gif"),
"3": PhotoImage(file="images\\3.gif"),
"4": PhotoImage(file="images\\4.gif"),
"5": PhotoImage(file="images\\5.gif"),
"6": PhotoImage(file="images\\6.gif"),
"7": PhotoImage(file="images\\7.gif"),
"8": PhotoImage(file="images\\8.gif")
}

PHOTO_DICT_COPY = {
"NONE": PhotoImage(file="images\\none.gif"),
"MINE": PhotoImage(file="images\\mine.gif"),
"FLAG": PhotoImage(file="images\\flag.gif"),
"FLAG_WRONG": PhotoImage(file="images\\flag_wrong.gif"),
"CLICKED": PhotoImage(file="images\\clicked.gif"),
"1": PhotoImage(file="images\\1.gif"),
"2": PhotoImage(file="images\\2.gif"),
"3": PhotoImage(file="images\\3.gif"),
"4": PhotoImage(file="images\\4.gif"),
"5": PhotoImage(file="images\\5.gif"),
"6": PhotoImage(file="images\\6.gif"),
"7": PhotoImage(file="images\\7.gif"),
"8": PhotoImage(file="images\\8.gif")
}    

STATES = ["empty", "mine"]

def get_int(name):
    """Returns an integer inputted by the user"""
    integer = ""
    while integer == "":
        try:
            integer = int(input("Please input the " + name + ": "))
        except TypeError:
            print("Please input a valid integer")
    return integer


class Board:
    """The Board class"""
    
    def __init__(self, window):
        """The board initializer"""
        window.title("Minesweeper")
        self.window = window
        self.frame = Frame(window, highlightthickness=2, relief="groove")
        self.frame.grid(row=0, column=0)
        self.block_dict = {}
        self.height = get_int("height of the board")
        self.width = get_int("width of the board")
        window.minsize(self.width * BUTTON_SIZE + 4, self.height * BUTTON_SIZE + 4)
        self.mine_count = get_int("number of mines")
        while not (0 < self.mine_count < self.height * self.width - 9):
            print("Please make sure the number of mines is less than", 
                  self.height * self.width - 9, "and more than 0")
            self.mine_count = get_int("number of mines")
        self.game_over = False
        self.old_wheight = 0
        self.old_wwidth = 0
        self.generate_board()
    
    def generate_board(self):
        """Generates a board full of blocks"""
        for x_pos in range(0, self.width):
            for y_pos in range(0, self.height):
                x_coord = "0" * (len(str(self.width)) - len(str(x_pos))) + str(x_pos)
                y_coord = "0" * (len(str(self.height)) - len(str(y_pos))) + str(y_pos)
                dict_position = x_coord + "," + y_coord                
                self.block_dict[dict_position] = Block(x_pos, y_pos, self)
    
    def start_game(self, x_start, y_start):
        """Prepares the game after the first block is clicked"""
        starting_blocks = self.find_adjacent_blocks(x_start, y_start)
        first_block = self.get_block(x_start, y_start)
        starting_blocks.append(first_block)
        
        non_mines = list(set(self.block_dict.values()) - set(starting_blocks))
        for mine_num in range(0, self.mine_count):
            non_mines.pop(random.randint(0, len(non_mines) - 1)).create_mine()
        
        for block in self.block_dict.values():
            block.prep()
        first_block.reveal()
        self.ready = True
    
    def find_adjacent_blocks(self, x_pos, y_pos):
        """Returns a list containing all blocks adjacent to the one specified"""
        block_list = []
        if x_pos > 0 and y_pos > 0:
            block_list.append(self.get_block(x_pos - 1, y_pos - 1))
            
        if x_pos > 0:
            block_list.append(self.get_block(x_pos - 1, y_pos))
        
        if x_pos > 0 and y_pos < self.height - 1:
            block_list.append(self.get_block(x_pos - 1, y_pos + 1))
        
        if y_pos < self.height - 1:
            block_list.append(self.get_block(x_pos, y_pos + 1))
        
        if x_pos < self.width - 1 and y_pos < self.height - 1:
            block_list.append(self.get_block(x_pos + 1, y_pos + 1))
        
        if x_pos < self.width - 1:
            block_list.append(self.get_block(x_pos + 1, y_pos))
        
        if x_pos < self.width - 1 and y_pos > 0:
            block_list.append(self.get_block(x_pos + 1, y_pos - 1))
        
        if y_pos > 0:
            block_list.append(self.get_block(x_pos, y_pos - 1))
        return block_list
    
    def end_game(self):
        """Ends the game"""
        self.game_over = True
        for block in self.block_dict.values():
            block.button["command"] = lambda: print("")
            block.button.unbind("<Button-3>")
            if block.state == STATES[1] and not block.flagged:
                block.button.grid_forget()
                block.label.grid(row=block.y_pos, column=block.x_pos)                
            elif block.state == STATES[0] and block.flagged:
                block.button["image"] = PHOTO_DICT["FLAG_WRONG"]
    
    def get_block(self, x_pos, y_pos):
        """Returns the Block at the specified coordinate"""
        x_coord = "0" * (len(str(self.width)) - len(str(x_pos))) + str(x_pos)
        y_coord = "0" * (len(str(self.height)) - len(str(y_pos))) + str(y_pos)
        dict_position = x_coord + "," + y_coord
        return self.block_dict[dict_position]
    
    def resize_elements(self, event=None):
        """Resizes all the elements of the window"""
        global PHOTO_DICT
        wwidth, wheight = self.window.geometry().split("+")[0].split("x")
        wheight, wwidth = int(wheight), int(wwidth)
        if wheight >= self.height * BUTTON_SIZE and wwidth >= self.width * BUTTON_SIZE and\
           (wheight // (self.height * 2) != self.old_wheight // (self.height * 2) or\
           wwidth // (self.width * 2) != self.old_wwidth // (self.width * 2)):
            scale_from_one = min(wheight // (self.height * 2), 
                                 wwidth // (self.width * 2))
            scale = scale_from_one / BUTTON_SIZE
            
            PHOTO_DICT["NONE"] = PHOTO_DICT_COPY["NONE"].zoom(x=scale_from_one)
            PHOTO_DICT["MINE"] = PHOTO_DICT_COPY["MINE"].zoom(x=scale_from_one)
            PHOTO_DICT["FLAG"] = PHOTO_DICT_COPY["FLAG"].zoom(x=scale_from_one)
            PHOTO_DICT["FLAG_WRONG"] = PHOTO_DICT_COPY["FLAG_WRONG"].zoom(x=scale_from_one)
            PHOTO_DICT["CLICKED"] = PHOTO_DICT_COPY["CLICKED"].zoom(x=scale_from_one)
            PHOTO_DICT["1"] = PHOTO_DICT_COPY["1"].zoom(x=scale_from_one)
            PHOTO_DICT["2"] = PHOTO_DICT_COPY["2"].zoom(x=scale_from_one)
            PHOTO_DICT["3"] = PHOTO_DICT_COPY["3"].zoom(x=scale_from_one)
            PHOTO_DICT["4"] = PHOTO_DICT_COPY["4"].zoom(x=scale_from_one)
            PHOTO_DICT["5"] = PHOTO_DICT_COPY["5"].zoom(x=scale_from_one)
            PHOTO_DICT["6"] = PHOTO_DICT_COPY["6"].zoom(x=scale_from_one)
            PHOTO_DICT["7"] = PHOTO_DICT_COPY["7"].zoom(x=scale_from_one)
            PHOTO_DICT["8"] = PHOTO_DICT_COPY["8"].zoom(x=scale_from_one)
            PHOTO_DICT["NONE"] = PHOTO_DICT["NONE"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["MINE"] = PHOTO_DICT["MINE"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["FLAG"] = PHOTO_DICT["FLAG"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["FLAG_WRONG"] = PHOTO_DICT["FLAG_WRONG"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["CLICKED"] = PHOTO_DICT["CLICKED"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["1"] = PHOTO_DICT["1"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["2"] = PHOTO_DICT["2"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["3"] = PHOTO_DICT["3"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["4"] = PHOTO_DICT["4"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["5"] = PHOTO_DICT["5"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["6"] = PHOTO_DICT["6"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["7"] = PHOTO_DICT["7"].subsample(x=BUTTON_HALFSIZE)
            PHOTO_DICT["8"] = PHOTO_DICT["8"].subsample(x=BUTTON_HALFSIZE)
            for block in self.block_dict.values():
                if block.flagged:
                    if self.game_over and block.state != STATES[1]:
                        block.button["image"] = PHOTO_DICT["FLAG_WRONG"]
                    else:
                        block.button["image"] = PHOTO_DICT["FLAG"]
                else:
                    block.button["image"] = PHOTO_DICT["NONE"]
                block.update_image()
            self.old_wheight = wheight
            self.old_wwidth = wwidth
        
class Block:
    """The Block class
    Represents a block on the board"""
    def __init__(self, x_pos, y_pos, master):
        """The Block initializer"""
        self.state = STATES[0]
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.board = master
        self.button = Button(master.frame, image=PHOTO_DICT["NONE"], 
                             relief="flat", highlightthickness=0, 
                             command=self.start, borderwidth=0)
        self.button.grid(row=y_pos, column=x_pos)
        self.label = Label(master.frame, highlightthickness=0, 
                           image=PHOTO_DICT["NONE"], borderwidth=0)
        self.adjacent_mine_num = 0
        self.pressed = False
        self.flagged = False
    
    def create_mine(self):
        """Turns this block into a mine"""
        self.state = STATES[1]
        for block in self.board.find_adjacent_blocks(self.x_pos, self.y_pos):
            block.adjacent_mine_num += 1
    
    def prep(self):
        """Prepares this non-mine block for the game once mines are placed"""
        self.button["command"] = self.reveal
        self.button.bind("<Button-3>", self.flag)
        if self.state == STATES[1]:
            self.label["image"] = PHOTO_DICT["MINE"]
        elif self.adjacent_mine_num == 0:
            self.label["image"] = PHOTO_DICT["CLICKED"]
        elif self.adjacent_mine_num == 1:
            self.label = Button(self.board.frame, image=PHOTO_DICT["1"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
        elif self.adjacent_mine_num == 2:
            self.label = Button(self.board.frame, image=PHOTO_DICT["2"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
        elif self.adjacent_mine_num == 3:
            self.label = Button(self.board.frame, image=PHOTO_DICT["3"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
        elif self.adjacent_mine_num == 4:
            self.label = Button(self.board.frame, image=PHOTO_DICT["4"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
        elif self.adjacent_mine_num == 5:
            self.label = Button(self.board.frame, image=PHOTO_DICT["5"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
        elif self.adjacent_mine_num == 6:
            self.label = Button(self.board.frame, image=PHOTO_DICT["6"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
        elif self.adjacent_mine_num == 7:
            self.label = Button(self.board.frame, image=PHOTO_DICT["7"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
        else:
            self.label = Button(self.board.frame, image=PHOTO_DICT["8"], 
                                relief="flat", highlightthickness=0, 
                                command=self.reveal_around_label, borderwidth=0)
    
    def update_image(self):
        """Updates the image for this block's label"""
        if self.state == STATES[1]:
            self.label["image"] = PHOTO_DICT["MINE"]
        elif self.adjacent_mine_num == 0:
            self.label["image"] = PHOTO_DICT["CLICKED"]
        elif self.adjacent_mine_num == 1:
            self.label["image"] = PHOTO_DICT["1"]
        elif self.adjacent_mine_num == 2:
            self.label["image"] = PHOTO_DICT["2"]  
        elif self.adjacent_mine_num == 3:
            self.label["image"] = PHOTO_DICT["3"]  
        elif self.adjacent_mine_num == 4:
            self.label["image"] = PHOTO_DICT["4"]  
        elif self.adjacent_mine_num == 5:
            self.label["image"] = PHOTO_DICT["5"]  
        elif self.adjacent_mine_num == 6:
            self.label["image"] = PHOTO_DICT["6"]  
        elif self.adjacent_mine_num == 7:
            self.label["image"] = PHOTO_DICT["7"]  
        elif self.adjacent_mine_num == 8:
            self.label["image"] = PHOTO_DICT["8"]          
        
    
    def start(self):
        """Calls the start_game() function of the board with this blocks
        coordinates"""
        self.board.start_game(self.x_pos, self.y_pos)
    
    def reveal_around_label(self):
        """Reveals the blocks around a label"""
        for block in self.board.find_adjacent_blocks(self.x_pos, self.y_pos):
            if (not block.pressed) and (not block.flagged):
                block.reveal()        
    
    def reveal(self):
        """Reveals this block"""
        if (not self.pressed) and (not self.flagged):
            if self.state == STATES[1]:
                self.board.end_game()
                self.button.grid_forget()
                self.label.grid(row=self.y_pos, column=self.x_pos)
                self.pressed = True                
            else:
                self.button.grid_forget()
                self.label.grid(row=self.y_pos, column=self.x_pos)
                self.pressed = True
                if self.adjacent_mine_num == 0:
                    for block in self.board.find_adjacent_blocks(self.x_pos, 
                                                                 self.y_pos):
                        if (not block.pressed) and (not block.flagged):
                            block.reveal()

    def flag(self, event):
        """Flags this block"""
        self.flagged = not self.flagged
        if self.flagged:
            self.button["image"] = PHOTO_DICT["FLAG"]
            self.button.image = PHOTO_DICT["FLAG"]
        else:
            self.button["image"] = PHOTO_DICT["NONE"]
            self.button.image = PHOTO_DICT["NONE"]

board = Board(window)
window.bind("<Configure>", board.resize_elements)
window.mainloop()