
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


# auxiliary function definitions

def _move_in_2d_coordinate(loc, delta):
    """
    A internal function for calculating the final location in the 2D coordinate space
    after a moving transformation.

    Args:
        loc (tuple): The original location (x,y) in the 2D coordinate
        delta (tuple): The moving transformation (deltaX, deltaY).

    Returns:
        tuple: The final location (x + deltaX, y + deltaY) in the 2D coordinate 
    """

    return (loc[0] + delta[0], loc[1] + delta[1])

def _check_wall(index, walls):
    """
    A internal function for checking if a cell having wall marks in the 
    Up, Down, Left, Right of itself.

    Args:
        index (tuple): The current location (x,y) of the cell.
        walls (list): A sequence of all wall marks location (x,y)

    Returns:
        Boolean: Return True if the cell has wall marks in thier surrounding
    """
    return _move_in_2d_coordinate(index, direction["Up"]) in walls \
        or _move_in_2d_coordinate(index, direction["Down"]) in walls \
        or _move_in_2d_coordinate(index, direction["Left"]) in walls \
        or _move_in_2d_coordinate(index, direction["Right"]) in walls 

def _check_corner(index, walls):
    """
    Check if a cell is a corner of the warehouse by examining if
    the Up, Down, Left and Right sides cell is a wall mark.
    For tuple (x,y), x -> column index, y -> row index

    Args:
        index (tuple): A tuple (x,y) for the index of a element in a 2d-array 

    Returns:
        Boolean: Return True if the cell is a corner
    """

    # Check if up and left cells are wall marks
    if _move_in_2d_coordinate(index, direction["Up"]) in walls \
        and _move_in_2d_coordinate(index, direction["Left"]) in walls:
        return True

    # Check if up and right cells are wall marks
    if _move_in_2d_coordinate(index, direction["Up"]) in walls \
        and _move_in_2d_coordinate(index, direction["Right"]) in walls:
        return True
    
    # Check if down and left cells are wall marks
    if _move_in_2d_coordinate(index, direction["Down"]) in walls \
        and _move_in_2d_coordinate(index, direction["Left"]) in walls:
        return True

    # Check if down and right cells are wall marks
    if _move_in_2d_coordinate(index, direction["Down"]) in walls \
        and _move_in_2d_coordinate(index, direction["Right"]) in walls:
        return True
    
    # otherwise, return it is not a corner
    return False

def _manhattan_distance(loc1, loc2):
    """Calculate the manhattan distance between two points loc1 and loc2.
    M=|q1−p1|+|q2−p2|

    Args: 
        loc1 (tuple): the position (p1,p2)
        loc1 (tuple): the position (q1,q2)

    Returns:
        int: the value of the manhattan distance 
    """

    return (abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1]))


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

    def _rule_1():
        """
        An inner function for determining the taboo cells by Rule 1: if a cell 
        is a corner and not a target, then it is a taboo cell.

        This fuction should be implemented before _rule_2().

        No parameters and returns are needed.
        """
        # loop all the rows in a 2d matrix
        for row_index in range(warehouse.nrows):
            # assume the beginning of each row is outside of the wall
            # out of game area
            # set the in/out flag as out 
            out_wall = True
            # loop all the columns in a 2d matrix
            for col_index in range(warehouse.ncols):

                # the index and marks of current cell in 2d matrix
                matrix_index = (col_index, row_index)
                square = warehouse_2d[row_index][col_index]
                
                # when current cell is the first wall mark in this row,
                # set the in/out flag as in 
                if out_wall and square == mark["wall"]:
                    out_wall = False
                
                # only process when inside the game area
                elif not out_wall:
                    # the rest of cells will be all the white spaces, if leaving the game area
                    # when leaving the game area, stop processing current row
                    if all([cell == mark["space"] for cell in warehouse_2d[row_index][col_index:]]):
                        break
                    
                    # during the game area, if the current cell is white space,
                    # and it is a corner, then mark it as taboo cell
                    if square == mark["space"] and _check_corner(matrix_index, walls):
                            warehouse_2d[row_index][col_index] = mark["taboo"]

    def _rule_2():
        """
        An inner function for determining the taboo cells by Rule 2: all the cells 
        between two corners along a wall are taboo if none of these cells is a target.

        Based on the previous rule 1 taboo cells in _rule_1(), implement this function.

        No parameters and returns are needed.
        """
        # loop all the rows in a 2d matrix
        for row_index in range(warehouse.nrows):

            # Since all rule 1 taboo cells have been found, 
            # no needs for check in/out of the game space
            
            # loop all the columns in a 2d matrix
            for col_index in range(warehouse.ncols):

                # the index and marks of current cell in 2d matrix
                matrix_index = (col_index, row_index)
                square = warehouse_2d[row_index][col_index]

                # if the current cell is rule 1 taboo cell
                if square == mark["taboo"] and _check_corner(matrix_index, walls):

                    # get all cells in the rest of current row and column
                    rest_of_this_row = warehouse_2d[row_index][col_index+1:]
                    rest_of_this_col = [row[col_index] for row in warehouse_2d[row_index+1:]]

                    # loop the rest of the row cells
                    for idx, val in enumerate(rest_of_this_row):
                        # if there is a target on this row, rule 2 is not applied
                        if val == mark["wall"] or val in mark["three_targets"]:
                            break
                        
                        # if it is a taboo, then check they all following a wall
                        # if so, all cells between two taboo cells should be taboo cells
                        if val == mark["taboo"] and _check_corner((col_index+idx+1, row_index), walls):
                            if all([_check_wall((loc, row_index), walls) for loc in range(col_index+1, col_index+idx+1)]):
                                for loc in range(col_index+1, col_index+idx+1):
                                    warehouse_2d[row_index][loc] = mark["taboo"]
                    
                    # loop the rest of the cells in column
                    for idx, val in enumerate(rest_of_this_col):
                        # if there is a target on this column, rule 2 is not applied
                        if val == mark["wall"] or val in mark["three_targets"]:
                            break
                        # if it is a taboo, then check they all following a wall
                        # if so, all cells between two taboo cells should be taboo cells
                        if val == mark["taboo"] and _check_corner((col_index, row_index+idx+1), walls):
                            if all([_check_wall((col_index, loc), walls) for loc in range(row_index+1, row_index+idx+1)]):
                                for loc in range(row_index+1, row_index+idx+1):
                                    warehouse_2d[loc][col_index] = mark["taboo"]

    # get the location sequence of all wall cells
    walls = warehouse.walls

    # convert the warehouse to a string
    warehouse_str = str(warehouse)  # call __str__ method in class Warehouse

    # replace the cell marks for box and player with whitespace,
    # only leave wall and target cell marks
    for cell in mark["removed"]:
        warehouse_str = warehouse_str.replace(cell, " ")
    
    # split the warehouse string by line breaks to a 2D matrix
    warehouse_2d = [list(line) for line in warehouse_str.splitlines()]

    # apply rule 1 and rule 2
    _rule_1()
    _rule_2()

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
    
    def __init__(self, warehouse):
        """
        Initialise essential variables for class
        """

        self.warehouse = warehouse
        # the initial state is combined with the worker state and all boxes state
        self.initial = warehouse.worker, tuple(warehouse.boxes)
        self.taboo = [sokoban.find_2D_iterator(taboo_cells(self.warehouse).splitlines(), mark["taboo"])]
        self.weights = warehouse.weights
        self.boxes = warehouse.boxes
        self.cache = {}
        self.goal = warehouse.targets
        self.walls = warehouse.walls

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
       
        # make a copy of the state of worker and boxes
        worker_state = state[0]
        boxes_state = list(state[1])
        # empty list of actions
        actions = []
        
        # loop four directions - Up, Down, Left, Right
        for key in direction.keys():
            # next potential state of worker
            next_worker_state = _move_in_2d_coordinate(worker_state, direction.get(key))

            # next potential state of worker should not be walls
            if next_worker_state in self.walls:
                continue
            # if worker push a box
            if next_worker_state in boxes_state:
                # next potential state of pushed box
                next_box_state = _move_in_2d_coordinate(next_worker_state, direction.get(key))
                # next potential state of pushed box should not be wall and taboo cells
                if next_box_state not in self.walls and \
                    next_box_state not in self.taboo and \
                    next_box_state not in boxes_state:
                    # if next potential state of pushed box is not a box, add this action to sequence
                    # if next_box_state not in boxes_state:
                        actions.append(key)
                                
            else: # not push box and add this action to sequence
                actions.append(key)

        return actions
    

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        # make a copy of the state of worker and boxes
        worker_state = state[0]
        boxes_state = list(state[1])

        # assume and calculate the next worker state
        next_worker_state =  _move_in_2d_coordinate(worker_state, direction.get(action))

        # check if the next worker state has a box on it
        if next_worker_state in boxes_state:
            # if so, calculate the new box state 
            next_box_state =  _move_in_2d_coordinate(next_worker_state, direction.get(action))
            # push this box to new state and update 
            box_index = boxes_state.index(next_worker_state)
            boxes_state[box_index] = next_box_state

        # return the result state combined by work state and box state
        return next_worker_state, tuple(boxes_state)

    def goal_test(self, state):
        """
        Return True if the state is a goal. 

        Overide the default method
        If all the boxes is in the target, return True
        """
        return set(self.goal) == set(state[1])


    def path_cost(self, c, state1, action, state2):
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. 
        
        Overide the default method 
        state1[1] and state2[1] both mean the boxes state
        If box is pushed, return the cost of pushing the weighted box and walking.
        If box is not pushed, return the cost of walking only.
        """

        if state1[1] != state2[1]: # box is pushed
            box_index = state1[1].index(state2[0])
            box_cost = self.weights[box_index]
            return c + box_cost + 1
        else: # box is pushed
            return c + 1

        

    def h(self, n):
        '''
        The value of the heurtistic by Taxicab Geometry (Manhattan Distance).
        
        The sum of the manhattan distance of 
            - each box to it's nearest target
            - worker to each box.
        '''
        worker = n.state[0]
        boxes = list(n.state[1])
        targets = self.goal
        weights = self.weights
        heuristic = 0


        # Simple Lower Bound algorithm
        for idx, box in enumerate(boxes):
            min_distance = float('inf')
            worker_distance = _manhattan_distance(box,worker)
            for target in targets:
                distance = _manhattan_distance(box,target) * (weights[idx] + 1)
                if min_distance > distance:
                    min_distance = distance
            heuristic += worker_distance
            heuristic += min_distance

        return heuristic


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
    # loop each action in sequence
    for action in action_seq:
        # make a copy of worker location
        current_location = warehouse.worker

        if action in list(direction.keys()):
            # location of worker after actions
            next_worker_location =_move_in_2d_coordinate(current_location, direction.get(action))

            # is wall, not valid
            if next_worker_location in warehouse.walls:
                return "Impossible"
                
            elif next_worker_location in warehouse.boxes:
                # coords of box after actions
                next_box_location =_move_in_2d_coordinate(next_worker_location, direction.get(action))

                # is wall or another box, not valid
                if next_box_location in warehouse.walls or next_box_location in warehouse.boxes:                    
                    return "Impossible"
                    
                else:
                    box_index = warehouse.boxes.index(next_worker_location)
                    warehouse.boxes[box_index] = next_box_location
                        
            else:
                warehouse.worker = next_worker_location
    
    return warehouse.__str__()


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
    # new class of SokobanPuzzle 
    my_sokoban = SokobanPuzzle(warehouse)

    # Apply astar_graph_search() to find solution
    solution = search.astar_graph_search(my_sokoban)

    if solution is None:
        return 'Impossible', None
    else:
        # get one possible action sequence from class Node.solution()
        S = solution.solution()
        # get the total cost
        C = solution.path_cost

    return S, C


#---------------------------------------------------------
#           TEST ONLY
#           These codes are
#           for test only
#---------------------------------------------------------

import os
import time
from multiprocessing import Process
import csv

# ONLY FOR TEST
def createFolder(directory):
    """
    Create a directory if don't exist
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: creating directory ' + directory)

# ONLY FOR TEST
def warehouse_solution(warehouse_problem):
    """
    Loop all warehouses in the test folder, and output the results to txt and csv file
    """
    head, problem_file = os.path.split(warehouse_problem)
    t0 = time.time()
    wh = sokoban.Warehouse()
    wh.load_warehouse(warehouse_problem)
    solution, cost = solve_weighted_sokoban(wh)
    t1 = time.time()

    with open("./Warehouse_solutions/"+problem_file, "w+") as file:
        file.write("The solution for warehouse "+problem_file+" is \n {}\nThe cost is {}\n".format(solution, cost))
        file.write('It took {:.6f} seconds'.format(t1-t0))
        file.close()

    with open("./Warehouse_solutions/overall.csv", "a+") as file:
        file.write(problem_file+", {}, {}\n".format(t1-t0, cost))
        file.close()

# ONLY FOR TEST
def test_taboo_cells(filename, expected_answer):
    """Test for taboo_cells()
    get from sanity_check.py
    """

    wh = sokoban.Warehouse()
    wh.load_warehouse(filename)
    answer = taboo_cells(wh)
    fcn = test_taboo_cells    
    print('<<  Testing {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)

# ONLY FOR TEST
def test_check_elem_action_seq():
    """
    Test for check_elem_action_seq()
    Testing for some case only
    get from sanity_check.py
    """
    wh = sokoban.Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    # first test
    answer = check_elem_action_seq(wh, ['Right', 'Right','Down'])
    expected_answer = '####  \n# .#  \n#  ###\n#*   #\n#  $@#\n#  ###\n####  '
    print('<<  check_elem_action_seq, test 1>>')
    if answer==expected_answer:
        print('Test 1 passed!  :-)\n')
    else:
        print('Test 1 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    answer = check_elem_action_seq(wh, ['Right', 'Right','Right'])
    expected_answer = 'Impossible'
    print('<<  check_elem_action_seq, test 2>>')
    if answer==expected_answer:
        print('Test 2 passed!  :-)\n')
    else:
        print('Test 2 failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)


# ONLY FOR TEST
def test_solve_weighted_sokoban(filename, expected_answer, expected_cost):
    """
    Test for solve_weighted_sokoban()
    only for some cases
    get from sanity_check.py
    """
    wh = sokoban.Warehouse()    
    wh.load_warehouse(filename)
    # first test
    t0 = time.time()
    try:
        answer, cost = solve_weighted_sokoban(wh)
    except ValueError:
        return print("Impossible")
    
    t1 = time.time()
    print('<<  test_solve_weighted_sokoban >>')
    if answer==expected_answer:
        print(' Answer as expected!  :-)\n')
    else:
        print('unexpected answer!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        print('Your answer is different but it might still be correct')
        print('Check that you pushed the right box onto the left target!')
    print(f'Your cost = {cost}, expected cost = {expected_cost}')
    print ('It took {:.6f} seconds'.format(t1-t0))
    print("")


# ONLY FOR TEST
def test_solve_weighted_sokoban_all():
    """
    Test for solve_weighted_sokoban()
    Testing for all warehouses by Automatic Timeout"""

    createFolder('./Warehouse_solutions')

    directory = os.path.join(os.getcwd(),"warehouses")

    counts = 1

    with open("./Warehouse_solutions/overall.csv", "a+") as file:
        file.write("case,time,cost\n")
        file.close()

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print("Start test case " + filename +  " in {} of 108".format(counts))
            p = Process(target=warehouse_solution, args=(os.path.join(directory, filename),))
            p.start()

            # Wait for 300 seconds or until process finishes
            p.join(300)

            if p.is_alive():
                with open("./Warehouse_solutions/outtime.txt", 'a+') as file:
                    file.write(filename+"\n")
                    file.close()
                print("Test case {} is timeout.".format(counts))
                # Terminate - may not work if process is stuck for good
                p.terminate()
                # OR Kill - will work for sure, no chance for process to finish nicely however
                # p.kill()
            
            counts += 1
            
        else:
            continue
    
    print("Finish All Tests")


if __name__ == "__main__":
    # ONLY FOR TEST

    test_taboo_cells("./warehouses/warehouse_01.txt", '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  ') 
    test_taboo_cells("./warehouses/warehouse_25.txt", " ####  \n #XX###\n #   X#\n##   X#\n#X   X#\n#XXX###\n#####  ") 
    test_taboo_cells("./warehouses/warehouse_81.txt", " #####\n #XXX#\n #  X#\n##  X#\n#X  ##\n#X  ##\n##  X#\n #XXX#\n #####") 

    test_check_elem_action_seq()

    print("Testing 8a")
    test_solve_weighted_sokoban("./warehouses/warehouse_8a.txt",
                                ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
                                'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 
                                'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 
                                'Right', 'Right', 'Right', 'Right', 'Right', 'Right'],
                                431
                                )
                                
    print("Testing 09")
    test_solve_weighted_sokoban("./warehouses/warehouse_09.txt",
    ['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 'Left', 'Down', 'Right', 'Down', 'Right', 'Left', 'Up', 'Up', 'Right', 'Down', 'Right', 'Down', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left'],
                                396 
                                )
    print("Testing 47")
    test_solve_weighted_sokoban("./warehouses/warehouse_47.txt",
    ['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Up', 'Up', 'Right', 'Right', 'Up', 'Right', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Down', 'Down', 'Up', 'Up', 'Left', 'Left', 'Down', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', 'Up', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Up', 'Right', 'Down', 'Down', 'Up', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Right', 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 'Right', 'Right'],
    179)

    print("Testing 81")
    test_solve_weighted_sokoban("./warehouses/warehouse_81.txt",
    ['Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Down', 'Left', 'Down', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Up', 'Right', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Down', 'Right', 'Down', 'Down', 'Left', 'Down', 'Down', 'Right', 'Up', 'Up', 'Up', 'Down', 'Left', 'Left', 'Up', 'Right'],
    376)

    # test all warehouses for solve_weighted_sokoban()
    test_solve_weighted_sokoban_all()