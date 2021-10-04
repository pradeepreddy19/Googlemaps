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

def parse_board(board):
    return np.array(start_state).reshape(5,5)

# return a list of possible successor states
def successors(state):
    
    ## outputs a 24 X 5 X 5 numpy array containing all possible board configs from current config##
    
    #left moves
    L1 = np.vstack([np.roll(state[0], -1),state[1:]])
    L2 = np.vstack([state[:1], np.roll(state[1],-1), state[2:]])
    L3 = np.vstack([state[:2], np.roll(state[2],-1), state[3:]])
    L4 = np.vstack([state[:3], np.roll(state[3],-1), state[4:]])
    L5 = np.vstack([state[:4], np.roll(state[4],-1)])

    #right moves
    R1 = np.vstack([np.roll(state[0],1),state[1:]])
    R2 = np.vstack([state[:1], np.roll(state[1],1), state[2:]])
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
    ic_ind = np.array([0,1,2,3,4,5,11,6,7,9,10,16,12,8,14,15,17,18,13,19,20,21,22,23,24])
    Ic = np.reshape(flat_board[:,ic_ind],(5,5))

    icc_ind = np.array([0,1,2,3,4,5,7,8,13,9,10,6,12,18,14,15,11,16,17,19,20,21,22,23,24])
    Icc = np.reshape(flat_board[:,icc_ind],(5,5))
    
    return np.array([(L1,'L1'),(L2,'L2'),(L3,'L3'),(L4,'L4'),(L5,'L5'),
                     (R1,'R1'),(R2,'R2'),(R3,'R3'),(R4,'R4'),(R5,'R5'),
                     (U1,'U1'),(U2, 'U2'),(U3,'U3'),(U4,'U4'),(U5,'U5'),
                     (D1,'D1'),(D2,'D2'),(D3,'D3'),(D4,'D4'),(D5,'D5'),
                     (Oc,'Oc'),(Occ,'Occ'),(Ic,'Ic'),(Icc,'Icc')], dtype = object)

# check if we've reached the goal
def is_goal(state):
    goal_state = np.array([x for x in range(1,26)]).reshape(5,5)

    return np.all(state==goal_state)

def path_trace_back(goal, visited):

    path =[]
    path.append(goal[2])
    step = goal

    # sequence of moves generated by successor function
    moves_list = [x for x in successors(goal[0])[:,1]]

    # index to find inverse move given a certain move, e.g., L1 --> R1
    inverse_moves_idx = [5,6,7,8,9,0,1,2,3,4,15,16,17,18,19,10,11,12,13,14,21,20,23,22]

    while step[1]>0:
        # find current move in the moves list generated from successor function
        inverse_move = moves_list.index(step[2])


        # find index of inverse of current move
        succ_idx = inverse_moves_idx[inverse_move]

        # use successor fucntion to find previous state
        prev_state = successors(step[0])[succ_idx][0]

        # find possible previous steps from visited list
        prev_idx = np.where(visited[:,1] == step[1]-1)

        #index of previous state from possibles
        possible_prev = visited[prev_idx]
        # find match for board in visited list
        step_back_idx = [np.all(possible_prev[n][0] == prev_state) for n in range(len(possible_prev))].index(1)
        step_back = possible_prev[step_back_idx]

        path.append(step_back[2])

        step = step_back
    path.pop()
    path.reverse()

    return path

def n_out_of_row(board):

    correct_in_row = []
    correct_in_row.append([x in board[0,:] for x in [1,2,3,4,5]])
    correct_in_row.append([x in board[1,:] for x in [6,7,8,9,10]])
    correct_in_row.append([x in board[2,:] for x in [11,12,13,14,15]])
    correct_in_row.append([x in board[3,:] for x in [16,17,18,19,20]])
    correct_in_row.append([x in board[4,:] for x in [21,22,23,24,25]])

    return 25-np.count_nonzero(np.array(correct_in_row).reshape(1,25))


def n_out_of_col(board):
    correct_in_column =[]
    correct_in_column.append([x in board[:,0] for x in [1,6,11,16,21]])
    correct_in_column.append([x in board[:,1] for x in [2,7,12,17,22]])
    correct_in_column.append([x in board[:,2] for x in [3,8,13,18,23]])
    correct_in_column.append([x in board[:,3] for x in [4,9,14,19,24]])
    correct_in_column.append([x in board[:,4] for x in [5,10,15,20,25]])
    
    return 25 - np.count_nonzero(np.array(correct_in_column).reshape(1,25))

def out_over_moves(board):
    return (n_out_of_row(board)/5)+(n_out_of_col(board)/5)

def solve(start_state):
    #initialize fringe
    initial_board = parse_board(start_state)
    fringe = (initial_board,0,'staring point', 0)# (board, g, move, f)
    fringe = np.array(fringe, dtype = object).reshape(1,4)

    #create list to keep track of items from fringe that are checked
    visited = np.zeros(4).reshape(1,4)

    while len(fringe)>0:
        pop_idx = np.argmin(fringe[:,3])
        pop_state = fringe[np.argmin(fringe[:,3])].reshape(1,4)

        visited = np.append(visited, pop_state).reshape(-1,4)
        fringe = np.delete(fringe, pop_idx, axis =0)

        state = pop_state[0][0]
        g = pop_state[0][1]
        move = pop_state[0][2]
        f = pop_state[0][3]

        if is_goal(state):
            goal = visited[-1]
            route = path_trace_back(goal, visited)
            print('goal found')
            break


        else:
            for board, move in successors(state):   
                h = out_over_moves(board)
                f= g+1+h
                fringe = np.append(fringe, (board, g+1, move, f)).reshape(-1,4)
    return route


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
