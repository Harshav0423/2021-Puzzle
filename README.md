# This is EAI Assignment @ IUB MSCS
# Part 1: Raichu
Raichu is a turn-taking game of 2 players. Minimax algorithm is applied with Alpha beta pruning. 
###### Mathematical abstraction:
The board is represented as a string with '.' for empty spaces and a fixed letter for each piece (ex: b for black picchu)
**Set of states:**
All the positions of pieces on the board.
**Successor function:
**
Given a player, white or black, All possible moves of black piece according to the rules given are successors.
**Goal State:**
Jump over all opponents pieces and kill them. No other color pieces present on board. 

**Implementation:**
It is not possible to go until terminal states in min max tree within 10seconds timelimit. So, We are doing iterative deepening minimax search. So, Within 10min, Program runs for depth of 1 and yields result, next runs for depth 2 and so on until timelimit is hit. 

**Evaluation function:**
Assigned weight of 1 to picchu as picchu can move in length of 1. 
Assigned weight of 2 to Pikachu as Pikachu can move 2 length moves.
Assigned weight of N to Raichu can move in any direction and max length of N. 

**Additional heuristic or thoughts**
Thought of adding weight to move towards end of board but after testing with other players decided to remove it. Moving towards end makes a piece raichu and that is favourable. But In trying to become raichu, It is not killing other pieces.
shuffle. the successors inorder to add randomness and thought that would make alpha beta pruning better, pruning more nodes. But, We did not see much improvement in pruning. We have changed our successors to return foreward moving successors as left nodes of minimax. Intution was that foreward moves are better hence that would lead to better pruning.It worked. 
