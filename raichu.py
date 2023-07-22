#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
# from _typeshed import Self
import sys
import time
import heapq
from copy import deepcopy

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


class Board_helper():
    # give all right positions until obstacle
    pokemons = {
        'w': 'wW@',
        'b': 'bB$'
    }
    can_jump = {
        'w': 'b',
        'W': 'Bb',
        '@': '$Bb',
        'b': 'w',
        'B': 'Ww',
        '$': '@Ww',
    }
    cant_jump = {
        'w': '$B',
        'W': '$',
        '@': '',
        'b': '@W',
        'B': '@',
        '$': '',
    }

    def __init__(self, N, player, board_matrix):
        
        self.no_rows = N
        self.no_cols = N
        self.player = player
        self.board_matrix = board_matrix
        
        pass

    def get_down_positions(self, row, col, pokemon, current_board, length):
        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color
        # print(pokemon_color)
        move_newboard = []
        for i in range(row+1, self.no_rows):
            # print(i)
            r, c = i, col
            # print(r,self.no_rows-1)
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break
            elif((current_board[r][c] in self.can_jump[pokemon]) and (r < (self.no_rows-1)) and length):
                # print(r,self.no_rows-1)
                if(current_board[r+1][c] == '.'):
                    # row_cols.append((r+1, c))
                    succ_row, succ_col = r+1, c
                    succ_board = deepcopy(current_board)
                    # print(self.no_rows,succ_row, succ_col, pokemon)
                    # print(succ_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                #can be reused from above
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                # print(self.no_rows,succ_row,succ_col,pokemon)
                # print(succ_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((succ_row, succ_col), succ_board))
                length -= 1

        return move_newboard

    def get_up_positions(self, row, col, pokemon, current_board, length):
        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color
        move_newboard = []
        for i in range(row-1, -1, -1):
            r, c = i, col
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break

            elif(current_board[r][c] in self.can_jump[pokemon]) and (r > 0) and length:
                # print(r,c)
                if(current_board[r-1][c] == '.'):
                    succ_row, succ_col = r-1, c
                    succ_board = deepcopy(current_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    # print('hi',succ_row,pokemon_color)
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((succ_row, succ_col), succ_board))
                length -= 1
        return move_newboard

    def get_right_positions(self, row, col, pokemon, current_board, length):
        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color
        row_cols = []
        move_newboard = []
        for i in range(col+1, self.no_cols):
            r, c = row, i
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break

            elif(current_board[r][c] in self.can_jump[pokemon]) and (c < self.no_cols-1) and (length):
                if(current_board[r][c+1] == '.'):
                    succ_row, succ_col = r, c+1
                    succ_board = deepcopy(current_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((succ_row, succ_col), succ_board))
                length -= 1
        return move_newboard

    def get_left_positions(self, row, col, pokemon, current_board, length):

        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color
        move_newboard = []
        for i in range(col-1, -1, -1):
            r, c = row, i
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break
            elif(current_board[r][c] in self.can_jump[pokemon]) and (c > 0) and (length):
                if(current_board[r][c-1] == '.'):
                    succ_row, succ_col = r, c-1
                    succ_board = deepcopy(current_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((succ_row, succ_col), succ_board))
                length -= 1
        return move_newboard

    def get_right_up_positions(self, row, col, pokemon, current_board, length):
        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color
        move_newboard = []
        r = row-1
        c = col+1
        while(r < self.no_rows and c < self.no_cols and c != -1 and r != -1):
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break

            elif(current_board[r][c] in self.can_jump[pokemon]) and r > 0 and c < self.no_cols-1 and length:
                if(current_board[r-1][c+1] == '.'):
                    succ_row, succ_col = r-1, c+1
                    succ_board = deepcopy(current_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((r, c), succ_board))
                length -= 1
            r -= 1
            c += 1
        return move_newboard

    def get_right_down_positions(self, row, col, pokemon, current_board, length):
        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color
        move_newboard = []
        r = row+1
        c = col+1
        while(r < self.no_rows and c < self.no_cols and c != -1 and r != -1):
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break

            elif(current_board[r][c] in self.can_jump[pokemon] and length and r < self.no_rows-1 and c < self.no_cols-1):
                if(current_board[r+1][c+1] == '.'):
                    succ_row, succ_col = r+1, c+1
                    succ_board = deepcopy(current_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((r, c), succ_board))
                length -= 1
            r += 1
            c += 1
        return move_newboard

    def get_left_up_positions(self, row, col, pokemon, current_board, length):
        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color

        move_newboard = []
        r = row-1
        c = col-1
        while(r < self.no_rows and c < self.no_cols and c != -1 and r != -1):
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break
            # elif(current_board[r][c] != '.'):
            #     if(current_board[r][c] not in self.can_jump[pokemon]):
            #         break
            elif(current_board[r][c] in self.can_jump[pokemon] and c > 0 and r > 0 and length):
                if(current_board[r-1][c-1] == '.'):
                    succ_row, succ_col = r-1, c-1
                    succ_board = deepcopy(current_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((r, c), succ_board))
                length -= 1
            r -= 1
            c -= 1
        return move_newboard

    def get_left_down_positions(self, row, col, pokemon, current_board, length):
        for color, pokes in self.pokemons.items():
            if(pokemon in pokes):
                pokemon_color = color

        move_newboard = []
        r = row+1
        c = col-1
        while(r < self.no_rows and c < self.no_cols and c != -1 and r != -1):
            if(current_board[r][c] in self.pokemons[pokemon_color] or current_board[r][c] in self.cant_jump[pokemon]):
                break
            elif(current_board[r][c] in self.can_jump[pokemon] and r < self.no_rows-1 and c > 0 and length):
                if(current_board[r+1][c-1] == '.'):
                    succ_row, succ_col = r+1, c-1
                    succ_board = deepcopy(current_board)
                    succ_board[succ_row][succ_col] = pokemon
                    succ_board[r][c] = '.'
                    succ_board[row][col] = '.'
                    if(succ_row == 0 and pokemon_color == 'b'):
                        succ_board[succ_row][succ_col] = '$'
                    if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                        succ_board[succ_row][succ_col] = '@'
                    move_newboard.append(((succ_row, succ_col), succ_board))
                    length -= 1
                    break
                else:
                    break
            elif(length and current_board[r][c] == '.'):
                succ_row, succ_col = r, c
                succ_board = deepcopy(current_board)
                succ_board[succ_row][succ_col] = pokemon
                succ_board[row][col] = '.'
                if(succ_row == 0 and pokemon_color == 'b'):
                    succ_board[succ_row][succ_col] = '$'
                if(succ_row == self.no_rows-1 and pokemon_color == 'w'):
                    succ_board[succ_row][succ_col] = '@'
                move_newboard.append(((r, c), succ_board))
                length -= 1
            r += 1
            c -= 1
        return move_newboard

    def get_successors(self, player, board_matrix):
        if(player == 'b'):
            succs = []
            N = len(board_matrix)
            bm = deepcopy(board_matrix)
            for i in range(N):
                for j in range(N):
                    # print(i,j)
                    piece = bm[i][j]
                    if(piece == '.'):
                        continue
                    elif(piece == 'b'):
                        # for s in self.get_right_up_positions(row=i, col=j, pokemon=piece, current_board=bm, length=2):
                        #     succs.append(s)
                        # for s in self.get_left_up_positions(row=i, col=j, pokemon=piece, current_board=bm, length=2):
                        #     succs.append(s)
                        succs += self.get_right_up_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=1)
                        succs += self.get_left_up_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=1)
                        # succs.extend(self.get_right_up_positions(
                        #     row=i, col=j, pokemon=piece, current_board=bm, length=1))
                        # succs.extend(self.get_left_up_positions(
                        #     row=i, col=j, pokemon=piece, current_board=bm, length=1))
                    elif(piece == 'B'):

                        succs += self.get_right_positions(row=i, col=j,
                                                          pokemon=piece, current_board=bm, length=2)
                        succs += self.get_up_positions(row=i, col=j,
                                                       pokemon=piece, current_board=bm, length=2)
                        succs += self.get_left_positions(row=i, col=j,
                                                         pokemon=piece, current_board=bm, length=2)

                    elif(piece == '$'):
                        succs += self.get_right_positions(row=i, col=j,
                                                          pokemon=piece, current_board=bm, length=N)
                        succs += self.get_right_up_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)
                        succs += self.get_up_positions(row=i, col=j,
                                                       pokemon=piece, current_board=bm, length=N)
                        succs += self.get_left_up_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)
                        succs += self.get_left_positions(row=i, col=j,
                                                         pokemon=piece, current_board=bm, length=N)
                        succs += self.get_left_down_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)
                        succs += self.get_down_positions(row=i, col=j,
                                                         pokemon=piece, current_board=bm, length=N)
                        succs += self.get_right_down_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)
                    pass
        else:
            succs = []
            N = len(board_matrix)
            bm = deepcopy(board_matrix)
            for i in range(N):
                for j in range(N):
                    piece = bm[i][j]
                    if(piece == '.'):
                        continue
                    elif(piece == 'w'):

                        succs += self.get_right_down_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=1)
                        succs += self.get_left_down_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=1)
                        # succs.append(
                        #     self.get_right_down_positions(row=i, col=j, pokemon=piece, current_board=bm, length=1))
                        # succs.append(
                        #     self.get_left_down_positions(
                        #         row=i, col=j, pokemon=piece, current_board=bm, length=1)
                        # )
                    elif(piece == 'W'):
                        # print(i, j, piece, bm)
                        # print()
                        succs += self.get_right_positions(row=i, col=j,
                                                          pokemon=piece, current_board=bm, length=2)
                        succs += self.get_left_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=2)

                        succs += (
                            self.get_down_positions(
                                row=i, col=j, pokemon=piece, current_board=bm, length=2)
                        )
                    elif(piece == '@'):
                        succs += self.get_right_positions(row=i, col=j,
                                                          pokemon=piece, current_board=bm, length=N)
                        succs += self.get_right_up_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)
                        succs += self.get_up_positions(row=i, col=j,
                                                       pokemon=piece, current_board=bm, length=N)
                        succs += self.get_left_up_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)
                        succs += self.get_left_positions(row=i, col=j,
                                                         pokemon=piece, current_board=bm, length=N)
                        succs += self.get_left_down_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)
                        succs += self.get_down_positions(row=i, col=j,
                                                         pokemon=piece, current_board=bm, length=N)
                        succs += self.get_right_down_positions(
                            row=i, col=j, pokemon=piece, current_board=bm, length=N)

                    pass
        return succs






class MMX:
    def __init__(self, max_depth, max_player,board_helper):
        self.max_depth = max_depth
        self.depth = 0
        self.max_player = max_player
        self.board_helper = board_helper

    def pretty_print(self, board_matrix):
        for i in board_matrix:
            print(i)

    # (w-b)+2*(W-B)+N*(@-$)

 # (w-b)+2*(W-B)+N*(@-$)
    def is_end(self, board_matrix):
        N = len(board_matrix)
        black_pokemons = 'bB$'
        while_pokemons = 'wW@'
        count_b = 0
        count_w = 0
        for i in range(N):
            for j in range(N):
                if(board_matrix[i][j] in black_pokemons):
                    count_b += 1
                elif(board_matrix[i][j] in while_pokemons):
                    count_w += 1
                pass
        if(count_w == 0):
            return True, 'b'
        elif(count_b == 0):
            return True, 'w'
        else:
            return False, '.'

    def eval_board(self, board_matrix):
        end, winner = self.is_end(board_matrix)
        if(end):
            if(winner == self.max_player):
                return +2222
            else:
                return -2222

        N = len(board_matrix)
        score = 0
        for i in board_matrix:
            for j in i:
                if(j == '.'):
                    continue
                elif(j == 'w'):
                    score += 1
                elif(j == 'W'):
                    score += 2
                elif(j == '@'):
                    score += N
                elif(j == 'b'):
                    score -= 1
                elif(j == 'B'):
                    score -= 2
                elif(j == '$'):
                    score -= N
        if(self.max_player == 'b'):
            return -1 * score
        else:
            return score

    #computes the minimum value among the successors of a given state
    def min_play(self, successor, alpha, beta, depth, player, depthlimit, N):
        depth += 1
        if depth == depthlimit or self.is_end(successor)[0]:
            return self.eval_board(successor)
        else:
            if (player == "w"):
                other_player = "b"
            else:
                other_player = "w"
            maxsuccessors = self.board_helper.get_successors(other_player, successor)
            for (r, c), maxsucc in maxsuccessors:
                beta = min(beta, self.max_play(maxsucc, alpha,
                                               beta, depth, player, depthlimit, N))
                if alpha >= beta:
                    return beta
            return beta

    #computes the maximum value among the successors of a given state
    def max_play(self, successor, alpha, beta, depth, player, depthlimit, N):
        depth += 1

        if depth >= depthlimit or self.is_end(successor)[0]:
            return self.eval_board(successor)
        else:
            minsuccessors = self.board_helper.get_successors(player, successor)
            for (r, c), minsucc in minsuccessors:
                alpha = max(alpha, self.min_play(minsucc, alpha,
                            beta, depth, player, depthlimit, N))
                if alpha >= beta:
                    return alpha
            return alpha

    def min_max(self, board, player, N, depth):
        succs = self.board_helper.get_successors(player, board)
        init_beta, init_alpha = float("inf"), float('-inf')
        max_heap = []
        for (r, c), minsucc in succs:
            heapq.heappush(max_heap, (self.min_play(
                minsucc, init_alpha, init_beta, 0, player, depth, N)*-1, minsucc))
        return heapq.heappop(max_heap)[1]


class Util():

    def row_encoding_to_matrix(self, row_encoding, N):
        board_matrix = []
        k = 0
        for i in range(N):
            row = []
            for j in range(N):
                row.append(row_encoding[k])
                k += 1
            board_matrix.append(row)

        return board_matrix

    def pretty_print_board_matrix(self, board_matrix):
        for i in board_matrix:
            print(' '.join(i))
    
    def matrix_to_row_encoding(self,board_matrix):
        out=''
        for i in board_matrix:
            for j in i:
                out+=j
        return out





def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    depth=0
    while True:
        if(time.time()>endtime):
            sys.exit(0)
        util = Util()
        board_matrix = util.row_encoding_to_matrix(board,N)
        board_helper=Board_helper(
            N=N,
            player=player,
            board_matrix=board_matrix
        )
        mmx=MMX(
            max_depth=depth,
            max_player=player,
            board_helper=board_helper
        )
        result = mmx.min_max(board_matrix, player, len(board_matrix), depth=depth)
        # print (result)
        depth+=1
        yield util.matrix_to_row_encoding(result)
        # yield board

import time
if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    global endtime
    endtime = time.time()+timelimit
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
