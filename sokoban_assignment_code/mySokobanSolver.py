
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (10599070, 'Zhipeng', 'He') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#  Global variables

#  Cell mark definitions
mark = {
    "space": " ",
    "wall": "#",
    "box": "$",
    "target": ".",
    "worker": "@",
    "worker_target": "!",
    "box_target": "*",
    "taboo": "X",
    "removed": ['$', '@'], 
    "three_targets": ['.', '*', '!']
    }

#  Direction definitions - Up and Down is reversed from Cartesian coordinate
direction = {
    "Up": (0,-1), 
    "Down": (0,1), 
    "Left": (-1,0), 
    "Right": (1,0)
    }

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''

    def _check_corner(walls, index):
        """Check if a cell is a corner of the warehouse by examining if
        the Up, Down, Left and Right sides cell is a wall mark.
        For tuple (x,y), x -> column index, y -> row index

        Args:
            walls (list): A list of tuple (x,y) for all wall cells
            index (tuple): A tuple (x,y) for the index of a element in a 2d-array 

        Returns:
            Boolen: Corner -> True, not Corner -> False
        """

        # Check if up and left cells are wall marks
        if (index[0] + direction["Up"][0], index[1] + direction["Up"][1]) in walls \
            and (index[0] + direction["Left"][0], index[1] + direction["Left"][1]) in walls:
            return True

        # Check if up and right cells are wall marks
        if (index[0] + direction["Up"][0], index[1] + direction["Up"][1]) in walls \
            and (index[0] + direction["Right"][0], index[1] + direction["Right"][1]) in walls:
            return True
        
        # Check if down and left cells are wall marks
        if (index[0] + direction["Down"][0], index[1] + direction["Down"][1]) in walls \
            and (index[0] + direction["Left"][0], index[1] + direction["Left"][1]) in walls:
            return True

        # Check if down and right cells are wall marks
        if (index[0] + direction["Down"][0], index[1] + direction["Down"][1]) in walls \
            and (index[0] + direction["Right"][0], index[1] + direction["Right"][1]) in walls:
            return True
        
        # otherwise, return it is not a corner
        return False

    def _rule_1():

        rule_1_taboo = []

        for row_index in range(warehouse.nrows):
            out_wall = True
            for col_index in range(warehouse.ncols):
                matrix_index = (col_index, row_index)
                square = warehouse_2d[row_index][col_index]

                if out_wall and square == mark["wall"]:
                    out_wall = False
                
                elif not out_wall:
                    if all([cell == mark["space"] for cell in warehouse_2d[row_index][col_index:]]):
                        break

                    if square == mark["space"]:
                        if _check_corner(walls, matrix_index):
                            warehouse_2d[row_index][col_index] = mark["taboo"]
                            rule_1_taboo.append(matrix_index)
        return rule_1_taboo

    def _rule_2(rule_1_taboo):
        for row_index in range(warehouse.nrows):
            out_wall = True
            for col_index in range(warehouse.ncols):
                matrix_index = (col_index, row_index)
                square = warehouse_2d[row_index][col_index]
        

    walls = warehouse.walls

    # convert the warehouse to a string
    warehouse_str = str(warehouse)  # call __str__ method in class Warehouse

    # replace the cell marks for box and player with whitespace,
    # only leave wall and target cell marks
    for cell in mark["removed"]:
        warehouse_str = warehouse_str.replace(cell, " ")
    
    # split the warehouse string by line breaks to a 2D matrix
    warehouse_2d = [list(line) for line in warehouse_str.splitlines()]

    rule_1_taboo_index = _rule_1()
    _rule_2(rule_1_taboo_index)

    # join the sokoban string list to a full string by line breaks
    warehouse_str = '\n'.join(["".join(row) for row in warehouse_2d])

    # Replace all three target marks with white space
    for cell in mark["three_targets"]:
        warehouse_str = warehouse_str.replace(cell, " ")

    return warehouse_str

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
        raise NotImplementedError

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

