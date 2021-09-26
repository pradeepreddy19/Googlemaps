#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

#the map is parsed in the main function below.  this is for running in interactive
def parse_board(filename):
    with open(filename, "r") as f:
        return np.array([line.split() for line in f.readlines()])


# return a list of possible successor states
# the parse_board function and successor function below use 5 X 5 arrays
# but the main function parser is a 1 X 25 array...
def successors(state):
    
    ## outputs a 24 X 5 X 5 numpy array containing all possible board configs from current config##
    
    #left moves
    L1 = np.vstack([np.roll(state[0], -1),state[1:]])
    L2 = np.vstack([state[0], np.roll(state[1],-1), state[2:]])
    L3 = np.vstack([state[:2], np.roll(state[2],-1), state[3:]])
    L4 = np.vstack([state[:3], np.roll(state[3],-1), state[4:]])
    L5 = np.vstack([state[:4], np.roll(state[4],-1)])

    #right moves
    R1 = np.vstack([np.roll(state[0],1),state[1:]])
    R2 = np.vstack([state[0], np.roll(state[1],1), state[2:]])
    R3 = np.vstack([state[:2], np.roll(state[2],1), state[3:]])
    R4 = np.vstack([state[:3], np.roll(state[3],1), state[4:]])
    R5 = np.vstack([state[:4], np.roll(state[4],1)])

    #down moves
    D1 = np.vstack([np.roll(state[:,0],1),state[:,1:].T]).T
    D2 = np.vstack([state[:,0].T, np.roll(state[:,1],1), state[:,2:].T]).T
    D3 = np.vstack([state[:,:2].T, np.roll(state[:,2],1), state[:,3:].T]).T
    D4 = np.vstack([state[:,:3].T, np.roll(state[:,3],1), state[:,4:].T]).T
    D5 = np.vstack([state[:,:4].T, np.roll(state[:,4],1), state[:,5:].T]).T

    #up moves
    U1 = np.vstack([np.roll(state[:,0],-1),state[:,1:].T]).T
    U2 = np.vstack([state[:,0].T, np.roll(state[:,1],-1), state[:,2:].T]).T
    U3 = np.vstack([state[:,:2].T, np.roll(state[:,2],-1), state[:,3:].T]).T
    U4 = np.vstack([state[:,:3].T, np.roll(state[:,3],-1), state[:,4:].T]).T
    U5 = np.vstack([state[:,:4].T, np.roll(state[:,4],-1), state[:,5:].T]).T
    
    #ring moves
    flat_board = np.reshape(state, (1,25))

    #outer moves
    oc_ind = np.array([5,0,1,2,3,10,6,7,8,4,15,11,12,13,9,20,16,17,18,14,21,22,23,24,19])
    Oc = np.reshape(flat_board[:,oc_ind],(5,5))

    occ_ind = np.array([1,2,3,4,9,0,6,7,8,14,5,11,12,13,19,10,16,17,18,24,15,20,21,22,23])
    Occ = np.reshape(flat_board[:,occ_ind],(5,5))


    #inner moves
    ic_ind = np.array([0,1,2,3,4,5,11,8,7,9,10,16,12,8,14,15,17,18,13,19,20,21,22,23,24])
    Ic = np.reshape(flat_board[:,ic_ind],(5,5))

    icc_ind = np.array([0,1,2,3,4,5,7,8,13,9,10,6,12,18,14,15,11,16,17,19,20,21,22,23,24])
    Icc = np.reshape(flat_board[:,icc_ind],(5,5))
    
    return np.array([L1,L2,L3,L4,L5,R1,R2,R3,R4,R5,U1,U2,U3,U4,U5,D1,D2,D3,D4,D5,Oc,Occ,Ic,Icc])



# check if we've reached the goal
def is_goal(state):
    goal_state = np.array([str(x) for x in range(1,26)]).reshape(5,5)

    return np.all(state==goal_state)



def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    return ["Oc","L2","Icc", "R4"]

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
