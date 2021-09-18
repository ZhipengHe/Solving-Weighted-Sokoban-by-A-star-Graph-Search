
'''

Quick "sanity check" script to test your submission 'mySokobanSolver.py'

This is not an exhaustive test program. It is only intended to catch major
blunders!

You should design your own test cases and write your own test functions.

Although a different script (with different inputs) will be used for 
marking your code, make sure that your code runs without errors with this script.


'''


from sokoban import Warehouse


try:
    from fredSokobanSolver import taboo_cells, solve_weighted_sokoban, check_elem_action_seq
    print("Using Fred's solver")
except ModuleNotFoundError:
    from mySokobanSolver import taboo_cells, solve_weighted_sokoban, check_elem_action_seq
    print("Using submitted solver")

    
def test_taboo_cells(filename, expected_answer):
    wh = Warehouse()
    wh.load_warehouse(filename)
    # expected_answer = '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  '
    answer = taboo_cells(wh)
    fcn = test_taboo_cells    
    print('<<  Testing {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        
def test_check_elem_action_seq():
    wh = Warehouse()
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

import time

def test_solve_weighted_sokoban(filename, expected_answer, expected_cost):
    wh = Warehouse()    
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


        
    

if __name__ == "__main__":
    pass    
#    print(my_team())  # should print your team

    test_taboo_cells("./warehouses/warehouse_01.txt", '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  ') 
    # test_taboo_cells("./warehouses/warehouse_5n.txt", '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  ') 
    test_taboo_cells("./warehouses/warehouse_25.txt", " ####  \n #XX###\n #   X#\n##   X#\n#X   X#\n#XXX###\n#####  ") 
    test_taboo_cells("./warehouses/warehouse_81.txt", " #####\n #XXX#\n #  X#\n##  X#\n#X  ##\n#X  ##\n##  X#\n #XXX#\n #####") 
    test_check_elem_action_seq()

    # print("Testing 01")
    # test_solve_weighted_sokoban("./warehouses/warehouse_01.txt",[], 0)

    # print("Testing 07")
    # test_solve_weighted_sokoban("./warehouses/warehouse_07.txt",
    # ['Up', 'Up', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Down', 'Right', 'Up', 'Down', 'Right', 'Down', 'Down', 'Left', 'Up','Down', 'Left', 'Left', 'Up', 'Left', 'Up', 'Up', 'Right'],
    # 26)

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

    # print("Testing 147")
    # test_solve_weighted_sokoban("./warehouses/warehouse_147.txt",
    # ['Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Right', 'Down', 'Down', 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Left', 'Down', 'Left', 'Up', 'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Down', 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Up', 'Right', 'Up', 'Left', 'Left', 'Left', 'Down', 'Left', 'Up', 'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Down', 'Right', 'Right', 'Up', 'Left', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Down', 'Left', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left', 'Left', 'Up', 'Left', 'Left'],
    # 521)



