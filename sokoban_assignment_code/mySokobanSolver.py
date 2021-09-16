
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

def _move_in_2d_coordinate(loc, delta):

    return (loc[0] + delta[0], loc[1] + delta[1])

def _check_wall(index, walls):

    return _move_in_2d_coordinate(index, direction["Up"]) in walls \
        or _move_in_2d_coordinate(index, direction["Down"]) in walls \
        or _move_in_2d_coordinate(index, direction["Left"]) in walls \
        or _move_in_2d_coordinate(index, direction["Right"]) in walls 

def _return_surrounding_wall(index, walls):

    surrounding_walls = []

    for key in list(direction.keys()):
        surrounding_location = _move_in_2d_coordinate(index, direction.get(key))
        if surrounding_location in walls:
            surrounding_walls.append(surrounding_location)

    return surrounding_walls

def _check_corner(index, walls):
    """Check if a cell is a corner of the warehouse by examining if
    the Up, Down, Left and Right sides cell is a wall mark.
    For tuple (x,y), x -> column index, y -> row index

    Args:
        index (tuple): A tuple (x,y) for the index of a element in a 2d-array 

    Returns:
        Boolen: Corner -> True, not Corner -> False
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
                        if _check_corner(matrix_index, walls):
                            warehouse_2d[row_index][col_index] = mark["taboo"]

    def _rule_2():
        for row_index in range(warehouse.nrows):
            for col_index in range(warehouse.ncols):
                matrix_index = (col_index, row_index)
                square = warehouse_2d[row_index][col_index]

                if square == mark["taboo"] and _check_corner(matrix_index, walls):
                    rest_of_this_row = warehouse_2d[row_index][col_index+1:]
                    rest_of_this_col = [row[col_index] for row in warehouse_2d[row_index+1:]]

                    for idx, val in enumerate(rest_of_this_row):
                        if val == mark["wall"] or val in mark["three_targets"]:
                            break

                        if val == mark["taboo"] and _check_corner((col_index+idx+1, row_index), walls):
                            if all([_check_wall((loc, row_index), walls) for loc in range(col_index+1, col_index+idx+1)]):
                                for loc in range(col_index+1, col_index+idx+1):
                                    warehouse_2d[row_index][loc] = mark["taboo"]
                    
                    for idx, val in enumerate(rest_of_this_col):
                        if val == mark["wall"] or val in mark["three_targets"]:
                            break

                        if val == mark["taboo"] and _check_corner((col_index, row_index+idx+1), walls):
                            if all([_check_wall((col_index, loc), walls) for loc in range(row_index+1, row_index+idx+1)]):
                                for loc in range(row_index+1, row_index+idx+1):
                                    warehouse_2d[loc][col_index] = mark["taboo"]


    walls = warehouse.walls

    # convert the warehouse to a string
    warehouse_str = str(warehouse)  # call __str__ method in class Warehouse

    # replace the cell marks for box and player with whitespace,
    # only leave wall and target cell marks
    for cell in mark["removed"]:
        warehouse_str = warehouse_str.replace(cell, " ")
    
    # split the warehouse string by line breaks to a 2D matrix
    warehouse_2d = [list(line) for line in warehouse_str.splitlines()]

    _rule_1()
    _rule_2()

    # join the sokoban string list to a full string by line breaks
    warehouse_str = '\n'.join(["".join(row) for row in warehouse_2d])

    # Replace all three target marks with white space
    for cell in mark["three_targets"]:
        warehouse_str = warehouse_str.replace(cell, " ")

    return warehouse_str

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Bugs:
# 1. Not consider the weights is 0, such as warehouse_01
# 2. Not consider already finished box, such as warehouse_01
# 3. Running time too slow
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

        self.warehouse = warehouse
        self.initial = warehouse.worker, tuple(warehouse.boxes)
        # self.taboo = [sokoban.find_2D_iterator(taboo_cells(self.warehouse).splitlines(), mark["taboo"])]
        self.weights = warehouse.weights
        self.boxes = warehouse.boxes
        self.goal = warehouse.targets
        self.walls = warehouse.walls


    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
       
        worker_state = state[0]
        boxes_state = list(state[1])
        actions = []
        

        for key in direction.keys():
            next_worker_state = _move_in_2d_coordinate(worker_state, direction.get(key))
            
            if next_worker_state not in _return_surrounding_wall(worker_state, self.walls):

                if next_worker_state in boxes_state:
                    next_box_state = _move_in_2d_coordinate(next_worker_state, direction.get(key))
                    if next_box_state not in _return_surrounding_wall(worker_state, self.walls):
                        if next_box_state not in boxes_state :
                            actions.append(key)
                        else:
                            break                  
                else:
                    actions.append(key)
        return actions
    

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        worker_state = state[0]
        boxes_state = list(state[1])

        if action in direction.keys():
            next_worker_state =  _move_in_2d_coordinate(worker_state, direction.get(action))

            if next_worker_state == boxes_state or next_worker_state in boxes_state:
                next_box_state =  _move_in_2d_coordinate(next_worker_state, direction.get(action))

                box_index = boxes_state.index(next_worker_state)

                boxes_state[box_index] = next_box_state
            
            worker_state = next_worker_state

        return worker_state, tuple(boxes_state)




    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""

        boxes = state[1]
        for box in boxes:
            if box not in self.goal:
                return False
        return True

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.
        
        Overide the default method """
        if state1[1] != state2[1]:
            box_index = state1[1].index(state2[0])
            box_cost = self.weights[box_index]
            return c + box_cost + 1
           
        return c + 1  # Elementary cost is one

    def h(self, node):
        '''
        Used for the weighted solver
        Heurtistic - Uses Manhattan Distance
        To make the heuristic admissible it should be optimisitc. It should
        underestimate the cost from the current state to the goal state.
        Possible option: Use the sum of the manhattan distance of each box 
        to it's nearest target.
        returns a int value which is an estimate of the puzzles distance to
        the goal state.
        '''
        boxes = list(node.state[1])
        targets = self.goal
        weights = self.weights

        manhattan_distance = []
        for idx, box in enumerate(boxes):
            weight_list = []
            for target in targets:
                weight_list.append( (abs(box[0]-target[0]) + abs(box[1]-target[1])) * weights[idx] ) # need to change this
            manhattan_distance.append(weight_list)

        heuristic = 0
        for distance in manhattan_distance:
            heuristic += min(distance)
        
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

    for action in action_seq:
        current_location = warehouse.worker
        if action in list(direction.keys()):
            # location of worker after actions
            post_worker_col = current_location[0] + direction.get(action)[0]
            post_worker_row = current_location[1] + direction.get(action)[1]
        
            if (post_worker_col, post_worker_row) in warehouse.walls:
                return "Impossible"
                
            elif (post_worker_col, post_worker_row) in warehouse.boxes:
                # coords of box after actions
                post_box_col = post_worker_col + direction.get(action)[0] 
                post_box_row = post_worker_row + direction.get(action)[1]
                    
                # if moved box is wall/ another box it's a wrong sequence
                if (post_box_col, post_box_row) in warehouse.walls or (post_box_col,post_box_row) in warehouse.boxes:                    
                    return "Impossible"
                    
                else:
                    warehouse.boxes.remove(post_worker_col, post_worker_row)
                    warehouse.boxes.append(post_box_col, post_box_row)
                    warehouse.worker = (post_worker_col, post_worker_row)
                        
            else:
                warehouse.worker = (post_worker_col, post_worker_row)
    
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
    
    my_sokoban = SokobanPuzzle(warehouse)

    solution = search.astar_graph_search(my_sokoban)
    if solution is None:
        return'Impossible'
    else: 
        S = solution.solution()
        C = solution.path_cost
    return S, C



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

