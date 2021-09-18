
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Automatic 
#   Testing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
import time
from multiprocessing import Process
from mySokobanSolver import *

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: creating directory ' + directory)

def warehouse_solution(warehouse_problem):
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


if __name__ == "__main__":
    createFolder('./Warehouse_solutions')

    directory = os.path.join(os.getcwd(),"warehouses")

    counts = 1

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print("Start test case {} of 108".format(counts))
            p = Process(target=warehouse_solution, args=(os.path.join(directory, filename),))
            p.start()

            # Wait for 60 seconds or until process finishes
            p.join(60)

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

