## MY FINAL GAME


from enum import Enum     #enumerations
import random
#from turtle import window_height            #generate random cells
import pygame as pg     #abbreviates
import pygame,time, sys
from pygame.locals import*
import time
import os
from pygame.sprite import Sprite, Group

from pygame import mixer


#Global Settings
pygame.init()
win_WIDTH = 500        # screen dimensions
win_HEIGHT = 500
maze_WIDTH = 10       #number of cells in maze
maze_HEIGHT = 10
cell_COUNT = maze_WIDTH * maze_HEIGHT      #calculated number of cells

show_FPS = False 
show_DRAW = False  # doesnt' Show the maze being created

#FPS = 20

BLOCK_SIZE = 8      #PIXEL size/ wall thickness
PATH_WIDTH = 3      #width of pathway in blocks

CELL_SIZE = BLOCK_SIZE * PATH_WIDTH + BLOCK_SIZE  # extra BLOCK_SIZE to include wall to east and south of cell
maze_WIDTH_PX = CELL_SIZE * maze_WIDTH + BLOCK_SIZE  # extra BLOCK_SIZE to include left edge wall
MAZE_HEIGHT_PX = CELL_SIZE * maze_HEIGHT + BLOCK_SIZE  # extra BLOCK_SIZE to include top edge wal

top_left_corner = (win_WIDTH // 2 - maze_WIDTH_PX // 2, win_HEIGHT // 2 - MAZE_HEIGHT_PX // 2)


#defining colours
bg_colour = (255, 255, 255)
wall_colour = (33, 33, 222)
maze_colour = (0, 0, 0)
unvisted_colour = (100, 100, 100)
fonts = (255, 255, 255)

PLAYER1_COLOUR = (34 , 139,34)
PLAYER2_COLOUR = (208, 62, 25)

message_COLOUR = (0, 255, 0)
screen = pg.display.set_mode((win_WIDTH, win_HEIGHT))


#background sound
mixer.music.load("pygameBackground.mp3")
mixer.music.play(-1)


class CellProp(Enum):
    Path_N = 1           #bitwise flags defined to mark the directions of the players movement
    Path_E = 2          
    Path_S = 4
    Path_W = 8
    Visited = 16

class Direction(Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)


class Player(pg.sprite.Sprite):
    def __init__(self, colour, x, y, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Save the start position
        self.start_x = x
        self.start_y = y

        # Create the rectangular image, fill and set background to transparent
        self.image = pg.Surface([radius * 2, radius * 2])
        self.image.fill(maze_colour)
        self.image.set_colorkey(maze_colour)

        # Draw our player onto the transparent rectangle
        pg.draw.circle(self.image, colour, (radius, radius), radius)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



    def reset(self):      #puts player back into starting position
        self.rect.x = self.start_x
        self.rect.y = self.start_y

class Text(Sprite):
    def __init__(self, text, font, color, position, anchor="topleft"):
        Sprite.__init__(self)
        self._text = text
        self._font = font
        self._color = color
        self._anchor = anchor
        self._position = position
        self.render()
 
    def render(self):
        self.image = self._font.render(self._text, 1, self._color)
        self.rect = self.image.get_rect(**{self._anchor: self._position})
 
    def set_text(self, text):
        self._text = text
        self.render()
class Timer:
    def __init__(self, start, interval, callback):
        self.tick = start
        self.interval = interval
        self.callback = callback
 
    def update(self, ticks):
        while ticks > self.tick:
            self.tick += self.interval
            self.callback(self)
 
class CountDownTimer:
    def __init__(self, count, callback, interval=1000):
        self.count = count
        self.callback = callback
        self.timer = Timer(pygame.time.get_ticks(), interval, self.countdown)
 
    def countdown(self, timer):
        self.count -= 1
        self.callback(self)
 
    def update(self, ticks):
        if self.count >= 0:
            self.timer.update(ticks)
 
class DisplayCountDown:
    def __init__(self, count, font, color, position, anchor="topleft", interval=1000):
        self.countdown = CountDownTimer(count, self.update_text, interval)
        self.display = "{:02d}"
        self.text = Text(self.display.format(self.countdown.count), font, color, position, anchor)

        self.player1 = Player(PLAYER1_COLOUR, top_left_corner[0] + BLOCK_SIZE, top_left_corner[1] + BLOCK_SIZE, (BLOCK_SIZE * 3) // 2)

        #PLayer 2 in bottome right
        self.player2 = Player(PLAYER2_COLOUR, top_left_corner[0] + maze_WIDTH_PX - CELL_SIZE, top_left_corner[1] + MAZE_HEIGHT_PX - CELL_SIZE, (BLOCK_SIZE * 3) // 2)
        
 
    def update_text(self, countdown):               #if the timer runs our will print game over
        if countdown.count >= 00:
            self.text.set_text(self.display.format(countdown.count))
        elif countdown.count <=00:
            font = pg.font.SysFont('Arial', 30, True)
            msg = "GAME OVER, press r to restart "

            size = font.size(msg)
            s = font.render(msg, True, message_COLOUR, (0, 0, 0))
            
            x = win_WIDTH // 2 - size[0] // 2
            y = win_HEIGHT //2 - size[1] // 2
            w = s.get_rect().w 
            h = s.get_rect().h

            screen.blit(s, (x, y))
            pg.display.update([(x, y, w, h)])



            pygame.display.flip()

        else:
            self.text.kill()

 
    def update(self, ticks):
        self.countdown.update(ticks)

    def initialize(self):
    
        self.player1.reset()
        self.player2.reset()
 
 


class MazeGenerator:


    direction_to_flag = {
        Direction.North: CellProp.Path_N,
        Direction.East: CellProp.Path_E,
        Direction.South: CellProp.Path_S,
        Direction.West: CellProp.Path_W
    }

    opposite_direction = {
        Direction.North: Direction.South,
        Direction.East: Direction.West,
        Direction.South: Direction.North,
        Direction.West: Direction.East
    }

    def __init__(self):   #initializing pygame before using it
        pg.init()

        #creates display surface for the game to be made on
        self.screen = pg.display.set_mode((win_WIDTH, win_HEIGHT))
        pg.display.set_caption('MAZE RACE') #creates title on window

    

        self.maze = []    #single list to store 2D array
        
        #random number generator with current time
        random.seed()

        # Store maze as image after we create it so that we just have to redraw the image on update
        self.maze_image = None

        #Player 1 starts in the upper left corner
        self.player1 = Player(PLAYER1_COLOUR, top_left_corner[0] + BLOCK_SIZE, top_left_corner[1] + BLOCK_SIZE, (BLOCK_SIZE * 3) // 2)
        #self.player1_sprite = None

        #PLayer 2 in bottome right
        self.player2 = Player(PLAYER2_COLOUR, top_left_corner[0] + maze_WIDTH_PX - CELL_SIZE, top_left_corner[1] + MAZE_HEIGHT_PX - CELL_SIZE, (BLOCK_SIZE * 3) // 2)
        #self.player2_sprite = None

        self.all_sprites = pg.sprite.RenderUpdates()
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        self.player1_score = 0     #players score
        self.player2_score = 0

        self.round = 1

        self.win1_flag = False
        self.win2_flag = False


    @staticmethod
    def get_cell_index(position):
        x, y = position
        return y * maze_WIDTH + x

    
    


    def generate_maze(self):
        #initializes the maze wit zero values
        self.maze = [0] * cell_COUNT
        visited_count = 0

        # start at alternating corners
        #the first cell (0,0) is added onto stack and visited count increased
        process_stack = [(0,0)]       #bottom of stack
        if self.round % 2 == 0:
            process_stack = [(maze_WIDTH - 1, maze_HEIGHT - 1)]
            self.maze[cell_COUNT - 1] |= CellProp.Visited.value
        else:
            process_stack = [(0, 0)]
            self.maze[0] |= CellProp.Visited.value


        visited_count += 1
        while visited_count < cell_COUNT:    #loops until visted count reaches the number of cells in maze
            #step 1: create list of the unvisited neighbours
            x, y = process_stack[-1]   #get position to top item on stack
            current_cell_index = self.get_cell_index((x,y))    # get the cell's index

            #find all unvisited neighbours
            neighbours = []
            #check each direction
            for direction in Direction:
                dir = direction.value
                #creates new x and new y values by adding corresponding values in the dir tuple
                new_X, new_Y = (x + dir[0], y + dir[1])             
                if 0 <= new_X < maze_WIDTH and 0 <= new_Y < maze_HEIGHT:
                    index = self.get_cell_index((new_X, new_Y))
                    if not self.maze[index] & CellProp.Visited.value:
                        #cell was not already visited so add to neighbours list with the direction
                        neighbours.append((new_X, new_Y, direction))

            if len(neighbours) > 0:    #to get length or number os items in the neighbours list
                #choose random neighbouring cell
                cell = neighbours[random.randrange(len(neighbours))]     #radrange returns a number from 0 to the bumebr passed in
                cell_x, cell_y, cell_direction = cell     #unpacks 3 values stored
                cell_position = (cell_x, cell_y)             #creates packed tuple containind x an y values
                cell_index = self.get_cell_index(cell_position)       #gets index into our maze lsit of cell

                #set a direction property flag to create a path between neighbour and current cell
                flag_to = MazeGenerator.direction_to_flag[cell_direction]                  #stores Cellprop value of the pathh to and from cells
                flag_from = MazeGenerator.direction_to_flag[MazeGenerator.opposite_direction[cell_direction]]       #direction to flag and opposite direction are dictionaru lookups to map direction of cell property path

                self.maze[current_cell_index]  |= flag_to.value                    #set CellPop Values on the currect annd new cells using our bitwise logic
                self.maze[cell_index]  |= flag_from.value  | CellProp.Visited.value

                process_stack.append(cell_position)
                visited_count += 1                       #adds new cell onto stack and line 17 increments visited count

            else:
                #Backtrack since there was no unvisited neighours
                process_stack.pop()

            if show_DRAW:
                self.draw_maze()
                pg.display.update()
                #pg.time.wait(500)
                pg.event.pump()
            
        # save image of completed maze
        self.draw_maze()
        pg.display.update()
        self.maze_image = self.screen.copy()



    def draw_maze(self):
        self.screen.fill(bg_colour)
        pg.draw.rect(self.screen, wall_colour, (top_left_corner[0], top_left_corner[0], maze_WIDTH_PX, MAZE_HEIGHT_PX))
        
        for x in range(maze_WIDTH):
            for y in range(maze_HEIGHT):
                for py in range(PATH_WIDTH):
                    for px in range(PATH_WIDTH):
                        cell_index = self.get_cell_index((x,y))
                        if self.maze[cell_index] & CellProp.Visited.value:
                            self.draw(maze_colour, x * (PATH_WIDTH + 1) + px, y * (PATH_WIDTH + 1) + py)
                        else:
                            self.draw(unvisted_colour, x * (PATH_WIDTH + 1) + px, y * (PATH_WIDTH + 1) + py)
        
                for p in range (PATH_WIDTH):      # add a loop to check cell props for a pth to the eat of the south
                    if self.maze[y * maze_WIDTH + x] & CellProp.Path_S.value:
                        self.draw(maze_colour, x * (PATH_WIDTH + 1) + p, y * (PATH_WIDTH + 1) + PATH_WIDTH)
                    
                    if self.maze[y * maze_WIDTH + x] & CellProp.Path_E.value:
                        self.draw(maze_colour, x * (PATH_WIDTH + 1) + PATH_WIDTH, y * (PATH_WIDTH + 1) + p)


        # Color the player exits
        pg.draw.rect(self.screen, PLAYER2_COLOUR, (top_left_corner[0],
                     top_left_corner[1] + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE * 3))

        pg.draw.rect(self.screen, PLAYER1_COLOUR,
                     (top_left_corner[0] + maze_WIDTH_PX - BLOCK_SIZE,
                      top_left_corner[1] + MAZE_HEIGHT_PX - BLOCK_SIZE * 4,
                      BLOCK_SIZE, BLOCK_SIZE * 3))

    def draw(self, colour, x, y):
        x_offset = top_left_corner[0] + BLOCK_SIZE
        y_offset = top_left_corner[0] + BLOCK_SIZE
        #draws wall one block to the right and one block down as i added extra wall to maze width
        pg.draw.rect(self.screen, colour, (x * BLOCK_SIZE + x_offset, y * BLOCK_SIZE + y_offset, BLOCK_SIZE, BLOCK_SIZE))
        
    def draw_scores(self):

        font = pg.font.SysFont('Arial', 18, True)

        # Display Scores
        p1_msg = f"PLAYER 1: {self.player1_score}"
        p2_msg = f"PLAYER 2: {self.player2_score}"
        p1_size = font.size(p1_msg)
        p2_size = font.size(p2_msg)
        p1 = font.render(p1_msg, True, PLAYER1_COLOUR)
        p2 = font.render(p2_msg, True, PLAYER2_COLOUR)
        
        
        
        p1_x = top_left_corner[0]
        p1_y = top_left_corner[1] - p1_size[1]
        p1_w = p1.get_rect().w
        p1_h = p1.get_rect().h
        p2_x = top_left_corner[0] + maze_WIDTH_PX - p2_size[0]
        p2_y = top_left_corner[1] - p1_size[1]
        p2_w = p2.get_rect().w
        p2_h = p2.get_rect().h
        
        self.screen.blit(p1, (p1_x, p1_y))
        self.screen.blit(p2, (p2_x, p2_y))

    

        pg.display.update([(p1_x, p1_y, p1_w, p1_h), (p2_x, p2_y, p2_w, p2_h)])


    def draw_instructions(self):
        #Displays intructions
        font = pg.font.SysFont("Arial", 18, True)

        p1_msg = "a w s d to move"
        p2_msg = "← ↑ ↓ → to move"
        p2_size = font.size(p2_msg)
        p1 = font.render(p1_msg, True, PLAYER1_COLOUR)
        p2 = font.render(p2_msg, True, PLAYER2_COLOUR)

        p1_x = top_left_corner[0]
        p1_y = top_left_corner[1] + MAZE_HEIGHT_PX + 2
        p1_w = p1.get_rect().w
        p1_h = p1.get_rect().h
        p2_x = top_left_corner[0] + maze_WIDTH_PX - p2_size[0]
        p2_y = top_left_corner[1] + MAZE_HEIGHT_PX + 2
        p2_w = p2.get_rect().w
        p2_h = p2.get_rect().h

        self.screen.blit(p1, (p1_x, p1_y))
        self.screen.blit(p2, (p2_x, p2_y))

        pg.display.update([(p1_x, p1_y, p1_w, p1_h), (p2_x, p2_y, p2_w, p2_h)])

    def draw_players(self):
        self.all_sprites.clear(self.screen, self.maze_image)
        dirty_recs = self.all_sprites.draw(self.screen)
        pg.display.update(dirty_recs)


    def draw_win(self):                                         #prints if player 1 or 2 wins and adds a point
        font = pg.font.SysFont('Arial', 72, True)
        msg = "Player 1 Wins" if self.win1_flag else "Player 2 Wins"
        if self.win1_flag:
            self.player1_score += 1
        else:
            self.player2_score += 1

        self.draw_scores()

        size = font.size(msg)
        s = font.render(msg, True, message_COLOUR, (0, 0, 0))
        
        x = win_WIDTH // 2 - size[0] // 2
        y = win_HEIGHT //2 - size[1] // 2
        w = s.get_rect().w 
        h = s.get_rect().h


        self.screen.blit(s, (x, y))
        pg.display.update([(x, y, w, h)])

        pg.time.wait(3000)



        pygame.display.flip()           #restarts maze

    
    def time(self):                                           #defines countdown lemgth
        pygame.init()

        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 100)
        counter = 41
        text = font.render(str(counter), True, (0, 128, 0))
        self.screen.fill(bg_colour)

        timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(timer_event, 1000)

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == timer_event:
                    counter -= 1
                    text = font.render(str(counter), True, (0, 128, 0))
                    if counter == 0:
                        pygame.time.set_timer(timer_event, 0)                

        
            self.screen.fill((255, 255, 255))
            self.screen.blit(text, (20, 20))
            pygame.display.flip()
        
    def get_player_cell_indexes(self, player):
        # Top left corner of first cell
        corner_offset_x = top_left_corner[0] + BLOCK_SIZE
        corner_offset_y = top_left_corner[1] + BLOCK_SIZE

        # Calculate which cells the player occupies
        square = BLOCK_SIZE * 4
        p1 = (player.rect.x - corner_offset_x, player.rect.y - corner_offset_y)
        p2 = (p1[0] + square - 1, p1[1] + square - 1)
        player_pos1 = (p1[0] // square, p1[1] // square)
        player_pos2 = (p2[0] // square, p2[1] // square)
        cell_index1 = self.get_cell_index((player_pos1[0], player_pos1[1]))
        cell_index2 = self.get_cell_index((player_pos2[0], player_pos2[1]))


        return cell_index1, cell_index2
    
    def can_move(self, direction, player):     #verifies player can move in that direction

        cell_index1, cell_index2 = self.get_player_cell_indexes(player)

        functions = {
            Direction.North: self.can_move_up,          #create a dictionary to look up helper methods
            Direction.East: self.can_move_right,
            Direction.South: self.can_move_down,
            Direction.West: self.can_move_left
        }

        # Check for maze exit/win
        # Check if player is at opposing player's start x,y
        if self.player1.rect.x == self.player2.start_x and self.player1.rect.y == self.player2.start_y:
            self.win1_flag = True
        elif self.player2.rect.x == self.player1.start_x and self.player2.rect.y == self.player1.start_y:
            self.win2_flag = True

        return functions[direction](cell_index1, cell_index2)

    #if player is trying to move between 2 cells we can then verfiy it's moving in the same direction
    def can_move_up(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_N.value
        else:
            return index2 == index1 + maze_WIDTH

    def can_move_right(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_E.value
        else:
            return index2 == index1 + 1

    def can_move_down(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_S.value
        else:
            return index2 == index1 + maze_WIDTH

    def can_move_left(self, index1, index2):
        if index1 == index2:
            return self.maze[index1] & CellProp.Path_W.value
        else:
            return index2 == index1 + 1 

    def move(self, player, move):
        x, y = move
        player.rect.x += x
        player.rect.y += y
        self.draw_players()     
 

    def try_move(self, player, direction):
        if self.can_move(direction, player):
            self.move(player, direction.value)
        else:
            # Check if open corridor is nearby
            index1, index2 = self.get_player_cell_indexes(player)

            move1 = self.maze[index1] & self.direction_to_flag[direction].value
            move2 = self.maze[index2] & self.direction_to_flag[direction].value

            if move1 or move2:
                # Move assist - move player closer to closest pathway in direction player is trying to move
                # We know that index1 and index2 must be different cells
                # get direction of closest pathway
                # measure center of player to center of each cell
                player_center = player.rect.x + (player.rect.w // 2), player.rect.y + (player.rect.h // 2)

                corner_offset_x = top_left_corner[0] + BLOCK_SIZE
                corner_offset_y = top_left_corner[1] + BLOCK_SIZE
                cell1_x, cell1_y = index1 % maze_WIDTH, index1 // maze_WIDTH
                cell2_x, cell2_y = index2 % maze_WIDTH, index2 // maze_WIDTH

                square = BLOCK_SIZE * 4
                cell1_x_px = corner_offset_x + cell1_x * square
                cell1_y_px = corner_offset_y + cell1_y * square
                cell2_x_px = corner_offset_x + cell2_x * square
                cell2_y_px = corner_offset_y + cell2_y * square

                cell1_center = cell1_x_px + (BLOCK_SIZE * PATH_WIDTH) // 2, cell1_y_px + (BLOCK_SIZE * PATH_WIDTH) // 2
                cell2_center = cell2_x_px + (BLOCK_SIZE * PATH_WIDTH) // 2, cell2_y_px + (BLOCK_SIZE * PATH_WIDTH) // 2

                if cell1_center[0] == player_center[0]:
                    # player is N/S corridor
                    if move1 and move2:
                        l1, l2 = abs(player_center[1] - cell1_center[1]), abs(player_center[1] - cell2_center[1])
                        if l1 < l2:
                            # move up
                            self.move(player, Direction.North.value)
                        else:
                            # move down
                            self.move(player, Direction.South.value)
                    else:
                        if move1:
                            # move up
                            self.move(player, Direction.North.value)
                        else:
                            # move down
                            self.move(player, Direction.South.value)
                else:
                    # player is E/W corridor
                    if move1 and move2:
                        l1, l2 = abs(player_center[0] - cell1_center[0]), abs(player_center[0] - cell2_center[0])
                        if l1 < l2:
                            # move left
                            self.move(player, Direction.West.value)
                        else:
                            # move right
                            self.move(player, Direction.East.value)
                    else:
                        if move1:
                            # move left
                            self.move(player, Direction.West.value)
                        else:
                            # move right
                            self.move(player, Direction.East.value)

    def show_start_screen(self):        #prescreen before actual game starts
        self.screen.fill(0)
        font = pg.font.SysFont('Arial', 30, True)
        msg = "MAZE RACE  " + "press any key to start"

        size = font.size(msg)
        s = font.render(msg, True, message_COLOUR, (0, 0, 0))
        
        x = win_WIDTH // 2 - size[0] // 2
        y = win_HEIGHT //2 - size[1] // 2
        w = s.get_rect().w 
        h = s.get_rect().h

        screen.blit(s, (x, y))
        pg.display.update([(x, y, w, h)])
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            #self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    waiting = False

    def initialize(self):              #initialises restart
    
        self.player1.reset()
        self.player2.reset()
    
        self.generate_maze()
        self.draw_instructions()
        self.draw_scores()
        self.draw_players()
       
 

    def run_game(self):
        pygame.init()
        
        clock = pg.time.Clock()

        self.initialize()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        rect = self.screen.get_rect()
        delta = 0
        fps = 100
        
        timer_font = pygame.font.Font(None, 38)
        position = rect.centerx, 20

        # Game Variables
        timer = DisplayCountDown(41, timer_font, pygame.Color("white"), position, "midtop")
        timer_group = Group(timer.text)
 
      
        #main loop
 

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            ticks = pygame.time.get_ticks()
            timer.update(ticks)
            color = (0,0,0)

            pygame.draw.rect(self.screen, color, pygame.Rect(220, 10, 60, 50))
            timer_group.draw(self.screen)
            
            # Render to screen
            pygame.display.flip()
    
            # Sleep, Idle, and Delta
            delta = clock.tick(fps)

        
            
            if not self.win1_flag and not self.win2_flag:
                keys = pg.key.get_pressed()
                if keys[pg.K_LEFT]:
                    self.try_move(self.player2, Direction.West)
                if keys[pg.K_RIGHT]:
                    self.try_move(self.player2, Direction.East)
                if keys[pg.K_UP]:
                    self.try_move(self.player2, Direction.North)
                if keys[pg.K_DOWN]:
                    self.try_move(self.player2, Direction.South)
                if keys[pg.K_a]:
                    self.try_move(self.player1, Direction.West)
                if keys[pg.K_d]:
                    self.try_move(self.player1, Direction.East)
                if keys[pg.K_w]:
                    self.try_move(self.player1, Direction.North)
                if keys[pg.K_s]:
                    self.try_move(self.player1, Direction.South)    

                if keys[pg.K_r]:  # restart game (but don't exit)
                #running = False  # DON'T DO THIS
                    self.initialize()
                    timer = DisplayCountDown(41, timer_font, pygame.Color("white"), position, "midtop")
                    clock = pg.time.Clock()

                    os.environ['SDL_VIDEO_CENTERED'] = '1'
                    rect = self.screen.get_rect()
                    delta = 0
                    fps = 100
                    
                    timer_font = pygame.font.Font(None, 38)
                    position = rect.centerx, 20

            
                    timer_group = Group(timer.text)

                    

                if self.win1_flag or self.win2_flag:        #call method to display a win message
                    self.draw_win()
                    self.win1_flag = self.win2_flag = False
                    self.initialize()
                    clock = pg.time.Clock()

        
                    os.environ['SDL_VIDEO_CENTERED'] = '1'
                    rect = self.screen.get_rect()
                    delta = 0
                    fps =100
                    
                    timer_font = pygame.font.Font(None, 38)
                    position = rect.centerx, 20

                    # Game Variables
                    timer = DisplayCountDown(41, timer_font, pygame.Color("white"), position, "midtop")
                    timer_group = Group(timer.text)
                
                    
                if show_FPS:
                    pg.display.set_caption(f'PyMaze ({str(int(clock.get_fps()))} FPS)')
                    clock.tick()
                else:
                    clock.tick(1000)

                

      
        
        pg.quit()

MG = MazeGenerator()      #creates an instance of the classans start of loop
MG.show_start_screen()
MG.run_game()

