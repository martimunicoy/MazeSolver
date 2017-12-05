# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from copy import copy
import sys

map_matrix = np.matrix(((1,1,1,1,1),(1,0,0,0,1),(1,0,1,0,1),(1,0,1,0,1),(1,1,1,1,1)), dtype = bool)

sys.setrecursionlimit(100000)

class Map(object):
    
    def __init__(self, map_matrix, start=(1,1), end=None):
        self.map_matrix = map_matrix
        self.shape = map_matrix.shape
        self.start = start
        if end is None:
            self.end = tuple([i - 2 for i in self.shape])
        else:
            self.end = end
        
        self.cells = np.zeros(map_matrix.shape, dtype='object')
        for row in xrange(self.shape[0]):
            for col in xrange(self.shape[1]):
                end_cell = False
                if (row, col) == self.end:
                    end_cell = True
                self.cells[row, col] = Cell(map_matrix[row, col], row, col, end_cell)
        
    def cell(self, row, col):
        return self.cells[row, col]
    
    def draw(self):
        self.maze = plt.gca()
        
        # self.maze.patch.set_facecolor('black')
        self.maze.set_aspect('equal', 'box')
        self.maze.axis([0, self.shape[1], 0, self.shape[0]])
        self.maze.xaxis.set_major_locator(plt.NullLocator())
        self.maze.yaxis.set_major_locator(plt.NullLocator())
        
        grid = []
        for cell in np.nditer(self.cells, flags=['refs_ok']):
            if cell.item().wall:
                y, x = cell.item().ind
                grid.append(patches.Rectangle((x, y), 1, 1, facecolor='grey'))
            else:
                y, x = cell.item().ind
                grid.append(patches.Rectangle((x, y), 1, 1, facecolor='white'))
                
        
        for cell in grid:
            self.maze.add_patch(cell)
        
        y, x = self.start
        self.maze.add_patch(patches.Rectangle((x, y), 1, 1, facecolor='green'))
        
        y, x = self.end
        self.maze.add_patch(patches.Rectangle((x, y), 1, 1, facecolor='yellow'))
        
        # maze.autoscale_view()
        # maze.invert_yaxis()
        # plt.savefig('maze.png', dpi=300, bbox_inches='tight')
        
        #self.maze.show()
        
    
class Cell(object):
    
    def __init__(self, wall, row, col, end):
        self.wall = wall
        self.ind = (row, col)
        self.seen = False
        self.end = end


class PathSearcher(object):
    
    def __init__(self, maze_map, start_ind, end_ind):
        self.maze_map = Map(maze_map, start_ind, end_ind)
        self.starter_cell = self.maze_map.cell(*start_ind)
        self.ending_cell = self.maze_map.cell(*end_ind)
        self.list = []
        self.solutions = []
        
    def find(self):
        self.starter_cell.seen = True
        path = [self.starter_cell,]
        self.recursive(path)
        
    """def rand_recursive(self, path):
        ..."""
    
    def recursive(self, cells_list):
        current_cell = cells_list[-1]
        # print current_cell.ind
        
        # Check if we arrived to the ending cell
        if current_cell.end:
            # print 'End!'
            path = Path(cells_list)
            self.solutions.append(path)
            return
        
        # Explore the surroundings
        directions = ('right', 'left', 'top', 'bottom')
        free_cells = []
    
        for direction in directions:
            new_cell = self.swift_cell(current_cell, direction)
            if self.check_cell(new_cell):
                free_cells.append(new_cell)
        
        # In case we are in a cul-de-sac
        if len(free_cells) == 0:
            # print 'Culdesac'
            path = Path(cells_list)
            self.list.append(path)
            return
        
        # In case we have only one possible way
        elif len(free_cells) == 1:
            # print 'only one way'
            cells_list.append(free_cells.pop())
            self.recursive(cells_list)
        
        # In case we are in a crossing
        elif len(free_cells) > 1:
            # print 'crossing'
            for cell in free_cells:
                cells_list_copy = copy(cells_list)
                cells_list_copy.append(cell)
                self.recursive(cells_list_copy)

    
    def swift_cell(self, current_cell, direction):
        current_ind = current_cell.ind
        
        if direction == 'right':
            new_ind = (current_ind[0], current_ind[1] + 1)
            new_cell = self.maze_map.cell(*new_ind)
        
        elif direction == 'left':
            new_ind = (current_ind[0], current_ind[1] - 1)
            new_cell = self.maze_map.cell(*new_ind)
        
        elif direction == 'top':
            new_ind = (current_ind[0] + 1, current_ind[1])
            new_cell = self.maze_map.cell(*new_ind)
        
        elif direction == 'bottom':
            new_ind = (current_ind[0] - 1, current_ind[1])
            new_cell = self.maze_map.cell(*new_ind)
            
        return new_cell
    

    def check_cell(self, cell):     
        if not cell.wall and not cell.seen:
            """self.culdesac= False
            cell.seen = True
            path.trail.append(cell)
            self.recursive(path)"""
            cell.seen = True
            return True
        
        else:
            return False
        
        
    def draw_path(self, path):
        self.maze_map.draw()
        maze = self.maze_map.maze
        plot_path(maze, path.trail, color='blue')
        

class Path(object):
    
    def __init__(self, cells_list):
        self.trail = cells_list
    
    def get_indexes(self):
        return [i.ind for i in self.trail]
    

def plot_path(canvas, cell_list, color='black'):
    for cell in cell_list:
        y, x = cell.ind
        canvas.add_patch(patches.Rectangle((x, y), 1, 1, facecolor=color))

    #canvas.show()
    
        