
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
mark_space = ' '

mark_box = '$'
mark_player = '@'

mark_target = '.'
mark_target_box = '*'
mark_target_player = '!'

mark_wall = '#'
mark_taboo = 'X'

#  Direction definitions
tuple_up = (0,1)
tuple_down = (0,-1)
tuple_left = (-1,0)
tuple_right = (1,0)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
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

    def _corner_checker(warehouse_list, x, y, rule_2=False):

        wall_x_axis = 0
        wall_y_axis = 0
        # check for walls above and below
        for (m, n) in [tuple_up, tuple_down]:
            if warehouse_list[y + n][x + m] == mark_wall:
                wall_y_axis += 1
        # check for walls left and right
        for (m, n) in [tuple_left, tuple_right]:
            if warehouse_list[y + n][x + m] == mark_wall:
                wall_x_axis += 1

        if rule_2: 
            return wall_x_axis or wall_y_axis
        else:
            return wall_x_axis and wall_y_axis

    
    # wall_x_axis and wall_y_axis
    
    def _taboo_rule_1(warehouse_list):

        # loop axis-y, by row
        for y in range(len(warehouse_list)): 
            # assuming the first square of each row is out of the wall
            outwall = 1 
            # loop axis-x, by column
            for x in range(len(warehouse_list[y])): 
                # keep looking the first wall mark in the row
                if outwall and warehouse_list[y][x] == mark_wall:
                    outwall = 0     # set the outwall to 0 when find wall mark
                elif not outwall: 
                    # check if all the cells to the right of current cell are empty
                    # means we are now outside the warehouse
                    if all([mark == mark_space for mark in warehouse_list[y][x:]]):
                        break
                    if warehouse_list[y][x]  == mark_space and _corner_checker(warehouse_list, x, y): 
                        # if this cell is corner
                        warehouse_list[y][x]  = mark_taboo
        return warehouse_list

    def _taboo_rule_2(warehouse_list):

        for y in range(len(warehouse_list)):
            for x in range(len(warehouse_list[y])):
                if warehouse_list[y][x] == mark_taboo and _corner_checker(warehouse_list, x, y):
                    row = warehouse_list[y][x + 1:]
                    col = [row[x] for row in warehouse_list[y + 1:][:]]
                    # fill in taboo_cells in row to the right of corner taboo cell
                    for x2 in range(len(row)):
                        if row[x2] in [mark_target, mark_target_box, mark_target_player, mark_wall]:
                            break
                        if row[x2] == mark_taboo and _corner_checker(warehouse_list, x2 + x + 1, y):
                            if all([_corner_checker(warehouse_list, x3, y, rule_2=True)
                                    for x3 in range(x + 1, x2 + x + 1)]):
                                for x4 in range(x + 1, x2 + x + 1):
                                    warehouse_list[y][x4] = 'X'
                    # fill in taboo_cells in column moving down from corner taboo
                    # cell
                    for y2 in range(len(col)):
                        if col[y2] in [mark_target, mark_target_box, mark_target_player, mark_wall]:
                            break
                        if col[y2] == mark_taboo and _corner_checker(warehouse_list, x, y2 + y + 1):
                            if all([_corner_checker(warehouse_list, x, y3, rule_2=True)
                                    for y3 in range(y + 1, y2 + y + 1)]):
                                for y4 in range(y + 1, y2 + y + 1):
                                    warehouse_list[y4][x] = 'X'

        return warehouse_list

    # convert the warehouse to a string
    warehouse_string = str(warehouse)  # call __str__ method in class Warehouse

    # replace the cell marks for box and player with free space,
    # only leave wall and target cell marks
    for mark in [mark_box, mark_player]:
        warehouse_string = warehouse_string.replace(mark, mark_space)
    
    # split the warehouse string by line breaks to a list
    warehouse_list = [list(line) for line in warehouse_string.split('\n')]

    warehouse_list = _taboo_rule_1(warehouse_list)
    warehouse_list = _taboo_rule_2(warehouse_list)

    warehouse_string = '\n'.join([''.join(line) for line in warehouse_list])


    for mark in [mark_target, mark_target_player, mark_target_box]:
        warehouse_string = warehouse_string.replace(mark, mark_space)

    return warehouse_string

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
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
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

