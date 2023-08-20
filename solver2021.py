#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Harsha Valiveti hvalivet
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import heapq

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]
# successor generation from a board
def move1(state,ip):
    b=[[0]*5 for _ in range(5)]
    k=0
    for i in range(5):
        for j in range(5):
            b[i][j]=state[k]
            k+=1
    if 'O' in ip or 'I' in ip:
        
        # Outer Initialization
        if 'O' in ip:
            top =0 #rows starting to end
            bottom =len(b)-1
            
            left=0 # columns starting to end
            right=len(b[0])-1
        
        # Inner initialization
        if 'I' in ip:
            top =1 #rows starting to end
            bottom =3
            
            left=1 # columns starting to end
            right=3
        # https://www.geeksforgeeks.org/rotate-matrix-elements/ 
        # i have implemented the code for outer ring rotation only and the rest is my own
        # clock-wise rotation
        if ip.count('c') == 1:
            
            prev=b[top+1][left]
            
            for i in range(left,right+1):
                curr,b[top][i] = b[top][i],prev
                prev=curr
            top+=1
            
            for i in range(top,bottom+1):
                curr,b[i][right]=b[i][right],prev
                prev=curr
            right-=1
            
            for i in range(right,left-1,-1):
                curr,b[bottom][i]=b[bottom][i],prev
                prev=curr
                
            bottom-=1
            
            for i in range(bottom,top-1,-1):
                curr,b[i][left]=b[i][left],prev
                prev=curr
            
            left+=1
            return b
        # counter clock-wise   
        if ip.count('c') == 2:
            
            prev=b[top][left]
            #moving left col a step
            for i in range(top+1,bottom+1):
                curr,b[i][left]=b[i][left],prev
                prev=curr
            
            left+=1
            #moving bottom row a step
            for i in range(left,right+1):
                curr,b[bottom][i]=b[bottom][i],prev
                prev=curr
            
            bottom-=1
            #moving right col a step
            for i in range(bottom,top-1,-1):
                curr,b[i][right]=b[i][right],prev
                prev=curr
            right-=1
            #moving top row a step backwards
            for i in range(right,left-2,-1):
                curr,b[top][i]=b[top][i],prev
                prev=curr
            top+=1
            return b
    #move right or left when given row number
    if 'R' in ip:
        r=int(ip[1])-1
        ls=b[r][-1:]
        rst=b[r][:-1]
        b[r]=ls+rst
        return b
    if 'L' in ip:
        r=int(ip[1])-1
        ls=b[r][1:]
        rst=b[r][:1]
        b[r]=ls+rst
        
        return b
    if 'U' in ip:
        col=int(ip[1])-1
        prev=b[0][col]
        for i in range(len(b)-1,-1,-1):
            curr=b[i][col]
            b[i][col]=prev
            prev=curr
        return b
    if 'D' in ip:
        col=int(ip[1])-1
        prev=b[0][col]
        for i in range(0,len(b)):
            curr=b[i][col]
            b[i][col]=prev
            prev=curr
        b[0][col]=prev
        return b

# return a list of possible successor states
def successors(state):
    move = ['L1','L2','L3','L4','L5','R1','R2','R3','R4','R5','U1','U2','U3','U4','U5','D1','D2','D3','D4','D5','Oc','Occ','Ic','Icc']
    
    nstates=[] # list to store the rotation
    
    for m in move:
        a=move1(state,m)
        b=tuple(a[i][j] for i in range(5) for j in range(5))
        nstates.append(b)
    return nstates        

#checking misplaced tiles
def check_tiles(initial_board):
    k=1
    count=0
    for i in range(25):
        if initial_board[i] != k:
                count+=1
        k+=1
    return count # returns number of misplaced tiles
def manhattan(state_tuple):
    m_dist = 0
    #Assigns each tile a (row,col) coordiate from (0,0) to (4,4) 
    #and compares actual location to needed location
    for i in range(len(state_tuple)):
        actual = [(i)//5,(i)%5]
        needed = [(state_tuple[i]-1)//5,(state_tuple[i]-1)%5]
        row_diff = abs(actual[0] - needed[0])
        col_diff = abs(actual[1] - needed[1])
    #Adjusts for the fact that tiles can teleport from edge to other edge
        if row_diff > 2:
            row_diff = 5 - row_diff
        if col_diff > 2:
            col_diff = 5 - col_diff
        m_dist += row_diff + col_diff
    return m_dist
#min_xyz
def min_xyz(manh):
    sums = []
    while len(sums)==0:
        x,y,z = [],[],[]
        for i in range(0,manh+1,16):
            x.append(i//16)
        for j in range(0,manh+1,8):
            y.append(j//8)
        for k in range(0,manh+1,5):
            z.append(k//5)
        for xi in x:
            for yi in y:
                for zi in z:
                    if xi*16+yi*8+zi*5==manh:
                        print(xi,yi,zi)
                        sums.append(xi+yi+zi)
        manh = manh-1
    return min(sums)
# check if we've reached the goal
def is_goal(state):
    if manhattan(state) == 0:
        return True
    return False

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
    
    fringe=[]
    #using Heapqueue to sort the fringe
    heapq.heappush(fringe,(manhattan(initial_board),initial_board,[]))
    heapq.heapify(fringe)
    #list of successors that can be formed using rotations
    move = ['L1','L2','L3','L4','L5','R1','R2','R3','R4','R5','U1','U2','U3','U4','U5','D1','D2','D3','D4','D5','Oc','Occ','Ic','Icc']
    f={} # dictionary to search states in fringe
    closed =[] # to store visiting states    
    
    
    while len(fringe) > 0:
        cost,curr_state,path = heapq.heappop(fringe)
        f[curr_state]=(cost,path)
        
        closed.append(curr_state)
        
        # checking goal state
        if is_goal(curr_state):
                return path
        
        
        for state,m in zip(successors(curr_state),move):
            c = manhattan(state)
            
            if m in ['Oc','Occ']:
                c = manhattan(state)/16
            elif m in ['Ic','Icc']:
                c = manhattan(state)/8
            else:
                c= manhattan(state)/5
            #checking the goal state and returns the path
            if is_goal(curr_state):
                path.append(m)
                return path
            # if the state present in closed list, skip
            if state in closed:
                continue
            #checks if a state present in fringe, has less cost than present in fringe, update them
            if state in f.keys():
                
                if c < f[state][0]:
                    if (f[state][0],state,f[state][1]) in fringe:
                        fringe.remove((f[state][0],state,f[state][1]))
                    o=f[state][1]
                    del f[state]
                    f[state]=(c,o)
            #appending into the fringe
            if state not in f.keys():
                f[state]=(c+1,path+[m])
                heapq.heappush(fringe,(c+1,state,path+[m]))
        
    return []

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
