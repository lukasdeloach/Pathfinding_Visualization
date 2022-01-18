import pygame
import Colors
from queue import PriorityQueue

"""
    This program runs the Visualization of the A* Pathfinding Algorithm
    
    Inspiration: Clément Mihailescu
    Code Help: TechWithTim Youtube
    
"""

WINDOW_WIDTH = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("Visualized A* Pathfinding Algorithm")

"""
    Class Node:
    This holds the information for the actual white square or node seen on the screen.
"""


class Node:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.width = width
        self.total_rows = total_rows
        self.nearest = []
        self.x = row * width
        self.y = column * width
        self.node_color = Colors.Color.WHITE.value

    # Returns the row, column position of the node
    def get_position(self):
        return self.row, self.column

    # Checks to see if the node is available
    def available(self):
        return self.node_color == Colors.Color.GREEN.value

    # Makes the Node available by changing its color to green
    def make_available(self):
        self.node_color = Colors.Color.GREEN.value

    # Basically a method that sets the node color back to white or open to barriers, nodes, or checks
    def make_open(self):
        self.node_color = Colors.Color.WHITE.value

    # Returns the boolean value on if the node is Black
    def unavailable(self):
        return self.node_color == Colors.Color.BLACK.value

    # Makes the node unavailable to be checked again by giving it the value red
    def make_unavailable(self):
        self.node_color = Colors.Color.RED.value

    # Checks to see if the node is a barrier
    def barrier(self):
        return self.node_color == Colors.Color.BLACK.value

    # Makes the node a barrier
    def make_barrier(self):
        self.node_color = Colors.Color.BLACK.value

    # Returns the boolean value if the node is the color magenta
    def start(self):
        return self.node_color == Colors.Color.MAGENTA.value

    # Makes the node Color magenta
    def make_start(self):
        self.node_color = Colors.Color.MAGENTA.value

    # Checks to see if the node is the end color
    def end(self):
        return self.node_color == Colors.Color.ORANGE.value

    # Sets the node color to the end value, orange
    def make_end(self):
        self.node_color = Colors.Color.ORANGE.value

    # The shortest path outlined in blue
    def make_path(self):
        self.node_color = Colors.Color.BLUE.value

    # Resets a node to white color
    def reset(self):
        self.node_color = Colors.Color.WHITE.value

    # Draws a rectangular node of the node_color and the size
    def draw_node(self, window):
        pygame.draw.rect(window, self.node_color, (self.x, self.y, self.width, self.width))

    # Creates an empty list to hold nearest nodes and adds them if they are not unavailable
    def new_nearest(self, grid):
        self.nearest = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].unavailable():  # Checks next row
            self.nearest.append((grid[self.row + 1][self.column]))

        if self.row > 0 and not grid[self.row - 1][self.column].unavailable():  # Checks previous row
            self.nearest.append((grid[self.row - 1][self.column]))

        if self.column < self.total_rows - 1 and not grid[self.row][
            self.column + 1].unavailable():  # Checks next column
            self.nearest.append((grid[self.row][self.column + 1]))

        if self.column > 0 and not grid[self.row][self.column - 1].unavailable():  # Checks previous column
            self.nearest.append((grid[self.row][self.column - 1]))


""""
The A* algorithm uses a calculation called the heuristic to determine the shortest path between to nodes
Returns the absolutue value of the x points + the y points
@:param node_one
@:param node_two
"""


def heuristic(node_one, node_two):
    x1, y1 = node_one
    x2, y2 = node_two
    return abs(x2 - x1) + abs(y2 - y1)


"""
Creates a new grid and holds the grid logic. 
@:param rows
@:param width
"""


def new_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):  # Iterates through all of the rows
        grid.append([])  # Appends the given row with an empty list that will hold the node value
        for j in range(rows):  # Iterates through all of the rows again in order to append the node
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


"""
Draws the grey grid lines first horizontally than vertically
@:param window
@:param rows
@:param width
"""


def draw_grid_lines(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, Colors.Color.GREY.value, (0, i * gap), (width, i * gap), 5)
        for j in range(rows):
            pygame.draw.line(window, Colors.Color.GREY.value, (j * gap, 0), (j * gap, width), 5)


"""
Fills the window white the iterates through the row and adds then draws the node in the given row spot
@:param window
@:param grid
@:param rows
@:param width
"""


def draw(window, grid, rows, width):
    window.fill(Colors.Color.WHITE.value)

    for row in grid:
        for node in row:
            node.draw_node(window)

    draw_grid_lines(window, rows, width)
    pygame.display.update()


"""Returns the position of the mouse position by seeing what row and column it is"""


def get_mouse_position(position, rows, width):
    gap = width // rows
    y, x = position

    row = y // gap
    column = x // gap

    return row, column


"""main methood which runs the program"""


def main(window, width):
    ROWS = 50
    grid = new_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:  # while the program is running draws a grid
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():  # Checks to see user did not close the application
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Handles the left click of the mouse
                position = pygame.mouse.get_pos()
                row, column = get_mouse_position(position, ROWS, width)  # Sets the row and column to be the mouse pos
                node = grid[row][column]
                if not start and node != end:  # Checks to see that there is no Start node
                    start = node  # sets the start node to be the node
                    Node.make_start(start)  # Calls the function make_start which sets the node to the start color

                elif not end and node != start:  # Same process but for the end node
                    end = node
                    Node.make_end(end)

                elif node != start and node != end:  # Checks to see the node is not the start or end node
                    Node.make_barrier(node)  # Sets the node to be the barrier color which is black

            elif pygame.mouse.get_pressed()[2]:  # Enables the right click to operate as the node reset
                position = pygame.mouse.get_pos()
                row, column = get_mouse_position(position, ROWS, width)
                node = grid[row][column]
                Node.make_open(node)  # Sets the node to be white

                if node == start:  # Does some resets here
                    start = None

                elif node == end:
                    end = None
            # Holds the key info for running the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:  # If the space bar is pressed
                    for row in grid:
                        for node in row:
                            node.new_nearest(grid)  #  Calls the new_nearest function, checks the nearest node states

                    aStar(lambda: draw(window, grid, ROWS, width), grid, start, end)

            #When the c key is pressed clears the nodes and makes a new grid
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = new_grid(ROWS, width)
    pygame.quit()

""" Reconstructs the shortest path"""
def shortest_path(last_node, current, draw_new):
    while current in last_node:
        current = last_node[current]
        current.make_path()
        draw_new()

""" Implements the A* algorithm. The """
def aStar(draw, grid, start, end):
    count = 0
    last_node = {}  # Keeps track of previous node
    open_set = PriorityQueue()
    open_set.put((0, count, start))  #  Adds start node and f score which is 0
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0 # G score of start node

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())  #  Estiamte f score with heuristic

    open_set_hash = {start}  # Keeps track of items in priority queue

    while not open_set.empty():  # Algorithm runs until set is empty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # While loop exit
                pygame.quit()

        current = open_set.get()[2]  # Checks the count of open set
        open_set_hash.remove(current) # Removes the current node

        if current == end:  # If the current node just pulled out is the end node makes the shortest path
            shortest_path(last_node, current, draw)
            end.make_end()
            return True

        for neighbor in current.nearest:
            temp_g_score = g_score[current] + 1  # Temporary g score the next node is

            if temp_g_score < g_score[neighbor]:  # If the g score of the nxt node is less than the previous
                last_node[neighbor] = current
                g_score[neighbor] = temp_g_score  #
                #  F score takes the temporary g score + the heuristic
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())

                if neighbor not in open_set_hash:
                    count += 1  #  Adds 1 to the neighbor
                    open_set.put((f_score[neighbor], count, neighbor))  #  Puts in f score count and node
                    open_set_hash.add(neighbor)  # Puts in node
                    neighbor.make_available()  #  Makes the node green which is the available to check

        draw()  #  Calls lambda function in main

        if current != start:
            current.make_unavailable()

    return False


main(WINDOW, WINDOW_WIDTH)
