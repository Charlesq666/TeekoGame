import random
from copy import deepcopy
from time import time
from random import choice

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.my_move = True if self.my_piece == self.pieces[0] else False
        self.l = 3
        # self.my_piece_pos = []
        # self.opp_piece_pos = []

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        myPieces = []
        oppPieces = []
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] == self.my_piece:
                    myPieces.append((r,c))
                elif state[r][c] == self.opp:
                    oppPieces.append((r,c))

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        start = time()
        if(len(myPieces) == 0):
            if(len(oppPieces) == 0 or oppPieces[0] != (2,2)):
                step = (2,2)
            else:
                step = (2,1)
        else:
            step = self.max_value(state, 3, True)[1]
        end = time()
        print(f"time {end - start}")
        move = []
        if(type(step[1]) == int):
            self.my_move = False
            move.insert(0, step)
            return move
        else:
            self.my_move = True
            move.append(step[1])
            move.append(step[0])
            return move

    def succ(self, state):
        occupied = []
        drop_phase = True
        succs = []
        for r in range(len(state)):
            for c in range(len(state[r])):
                if state[r][c] != ' ':
                    occupied.append((r,c));
                else:
                    succs.append((r,c))
        if len(occupied) >= 8: 
            drop_phase = False
        # print(f"length occupied is {len(occupied)}")
        # print(f"length succ is {len(succs)}")

        if drop_phase:
            # print(succs)
            return succs
        else:
            # print("not drop phase")
            succs = []
            for pos in occupied:
                r = pos[0]
                c = pos[1]
                for row in range(r-1,r+2):
                    for col in range(c-1, c+2):
                        if row in range(0,5) and col in range(0,5) and state[row][col] == ' ' and (row,col) not in succs:
                            succs.append((row,col))
            return succs

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.my_move = True
        self.place_piece(move, self.opp)
        # self.opp_piece_pos.append(move[0])

    def random_move(self, state):
        ch = choice(self.succ(state))
        print(ch)
        myPieces = []
        oppPieces = []
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] == self.my_piece:
                    myPieces.append((r,c))
                elif state[r][c] == self.opp:
                    oppPieces.append((r,c))
        if(len(myPieces) + len(oppPieces) < 8):
            return [ch]
        else:
            opptemp = choice(oppPieces)
            for suc in self.succ(state):               
                if(self.adjacent(suc, opptemp) and suc != opptemp):
                    return [suc, opptemp]
        return [opptemp, opptemp]

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for r in range(2):
            for c in range(2):
                if state[r][c] != ' ' and state[r][c] == state[r+1][c+1] == state[r+2][c+2] == state[r+3][c+3]:
                    return 1 if state[r][c] == self.my_piece else -1

        # check / diagonal wins
        for r in range(2):
            for c in range(2):
                if state[r][4-c] != ' ' and state[r][4-c] == state[r+1][4-c-1] == state[r+2][4-c-2] == state[r+3][4-c-3]:
                    return 1 if state[r][4-c] == self.my_piece else -1 

        # check 3x3 square corners wins
        for r in range(3):
            for c in range(3):
                if state[r][c] != ' ' and state[r][c] == state[r][c+2] == state[r+2][c] == state[r+2][c+2] and state[r+1][c+1] == ' ':
                    return 1 if state[r][c] == self.my_piece else -1

        return 0 # no winner yet

    # def heuristic_game_value(self, state):
        myPieceWeight = 0
        myPieces = []
        oppPieces = []
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] == self.my_piece:
                    myPieces.append((r,c))
                elif state[r][c] == self.opp:
                    oppPieces.append((r,c))

        if(self.game_value(state) == 1): 
            myPieceWeight = 1
        elif(len(myPieces)>0):
            obs = myPieces[0]
            dist = 0
            for piece in myPieces:
                r = piece[0]
                c = piece[1]
                dr = abs(obs[0] - r)
                dc = abs(obs[1] - c)
                dist += max(dr, dc)
            myPieceWeight = 1 if dist == 6 else abs(1/(6-dist))

        oppPieceWeight = 0
        if(self.game_value(state) == -1):
            oppPieceWeight = 1
        elif(len(oppPieces)>0):
            obs = oppPieces[0]
            dist = 0
            for piece in oppPieces:
                r = piece[0]
                c = piece[1]
                dr = abs(obs[0] - r)
                dc = abs(obs[1] - c)
                dist += max(dr,dc)
            oppPieceWeight = 1 if dist == 6 else abs(1/(6-dist))
        # print(f"my piece weight is {myPieceWeight}")
        # print(f"opp weight is {oppPieceWeight}")
        return myPieceWeight- oppPieceWeight

    def heuristic_game_value(self, state):
        myPieceWeight = 0
        myPieces = []
        oppPieces = []
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] == self.my_piece:
                    myPieces.append((r,c))
                elif state[r][c] == self.opp:
                    oppPieces.append((r,c))

        if(self.game_value(state) == 1): 
            return 1
        else:
            mostReach = 0
            initial = 0
            for piece in myPieces:
                r = piece[0]
                c = piece[1]
                l = 0
                if(r == 0 or r == 4):
                    initial -= 0.1
                    if(c == 0 or c == 4):
                        initial -= 0.1
                while(r < 5):                
                    if(state[r][c] == self.my_piece):
                        l += 1.5
                    else:
                        break
                    r += 1
                mostReach = max(mostReach, l)
                l = initial
                r = piece[0]
                c = piece[1]
                while(r < 5 and c < 5):
                    if(state[r][c] == self.my_piece):
                        l += 1.5
                    else:
                        break
                    r += 1
                    c += 1
                mostReach = max(mostReach, l)
                l = initial
                r = piece[0]
                c = piece[1]
                while(r < 5 and c >= 0):
                    if(state[r][c] == self.my_piece):
                        l += 1.5
                    else:
                        break
                    r += 1
                    c -= 1
                mostReach = max(mostReach, l)
                l = initial
                r = piece[0]
                c = piece[1]
                while(c < 5):
                    if(state[r][c] == self.my_piece):
                        l += 1.5
                    else:
                        break
                    c += 1

                
                mostReach = max(mostReach, 1)
                myPieceWeight = 1 - 1/(mostReach+1)

        oppPieceWeight = 0
        if(self.game_value(state) == -1):
            return -1
        else:
            mostReach = 0
            for piece in oppPieces:
                r = piece[0]
                c = piece[1]
                l = 0
                while(r < 5):                
                    if(state[r][c] == self.opp):
                        l += 1
                        if(l >= self.l and ((r < 4 and state[r+1][c] == self.my_piece) or 
                        (piece[0] > 0 and state[piece[0]-1][piece[1]] == self.my_piece))):
                            # print("blocked1")
                            myPieceWeight = 0.9
                        if(l >= self.l and ((r < 4 and state[r+1][c] == self.my_piece) and 
                        (piece[0] > 0 and state[piece[0]-1][piece[1]] == self.my_piece))):
                            myPieceWeight = 1
                    else:
                        break
                    r += 1
                mostReach = max(mostReach, l)
                l = 0
                r = piece[0]
                c = piece[1]
                while(r < 5 and c < 5):
                    if(state[r][c] == self.opp):
                        l += 1
                        if( l >= self.l and ((c <4 and r < 4 and state[r+1][c+1] == self.my_piece) or 
                        (piece[0]>0 and piece[1]>0 and state[piece[0]-1][piece[1]-1] == self.my_piece))):
                            # print("blocked2")
                            myPieceWeight = 0.9
                        if(l >= self.l and ((c <4 and r < 4 and state[r+1][c+1] == self.my_piece) and 
                        (piece[0]>0 and piece[1]>0 and state[piece[0]-1][piece[1]-1] == self.my_piece))):
                            myPieceWeight = 1
                    else:
                        break
                    r += 1
                    c += 1
                mostReach = max(mostReach, l)
                l = 0
                r = piece[0]
                c = piece[1]
                while(r < 5 and c >= 0):
                    if(state[r][c] == self.opp):
                        l += 1
                        if(l >= self.l and ((c > 0 and r < 4 and state[r+1][c-1] == self.my_piece) or 
                        (piece[0]>0 and piece[1]<4 and state[piece[0]-1][piece[1]+1] == self.my_piece))):
                            # print("blocked3")
                            myPieceWeight = 0.9
                        if(l >= self.l and ((c > 0 and r < 4 and state[r+1][c-1] == self.my_piece) and 
                        (piece[0]>0 and piece[1]<4 and state[piece[0]-1][piece[1]+1] == self.my_piece))):
                            # print("blocked3")
                            myPieceWeight = 1
                    else:
                        break
                    r += 1
                    c -= 1
                mostReach = max(mostReach, l)
                l = 0
                r = piece[0]
                c = piece[1]
                while(c < 5):
                    if(state[r][c] == self.opp):
                        l += 1
                        if(l >= self.l and ((c < 4 and state[r][c+1] == self.my_piece) or 
                        (piece[1] > 0 and state[r][piece[1]-1] == self.my_piece))):
                            # print("blocked4")
                            # print(f"r {r}, c{c}")
                            myPieceWeight = 0.9
                        if(l >= self.l and ((c < 4 and state[r][c+1] == self.my_piece) or 
                        (piece[1] > 0 and state[r][piece[1]-1] == self.my_piece))):
                            myPieceWeight = 1
                    else:
                        break
                    c += 1
                
                mostReach = max(mostReach, 1)
                oppPieceWeight = 1 - 1/(mostReach+1)

        return myPieceWeight- oppPieceWeight

    def printM(self, matrix):
        print()
        print("  0 1 2 3 4")
        index = 0
        for r in matrix:
            print(str(index)+ " " + " ".join(r))
            index += 1

    def max_value(self, state, depth, my_move, pre_action = ()):
        myPieces = []
        oppPieces = []
        step = ()
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] == self.my_piece:
                    myPieces.append((r,c))
                elif state[r][c] == self.opp:
                    oppPieces.append((r,c))
        
        value = self.game_value(state)
        if(value == -1 or value == 1):
            # self.printM(state) 
            # print(f"value is {value}")
            # print(f"termination value: {value}")
            # print("termination print")       
            return value, pre_action
        elif(depth == 0):
            value = self.heuristic_game_value(state)
            # self.printM(state) 
            # print(f"value is {value}")
            # print(f"heuritic {value}")
            # print("heu print")
            return value, pre_action
        elif(my_move):         
            maximum = -1000
            dropFace = False if len(myPieces) >= 4 else True
            for succ in self.succ(state):
                newstate = deepcopy(state)
                if(dropFace):
                    newstate[succ[0]][succ[1]] = self.my_piece
                    next = self.max_value(newstate,depth-1, not my_move, succ)
                    if(maximum < next[0]):
                        maximum = next[0]
                        step = succ 
                        # if(step == (1,3)):
                        #     self.printM(newstate) 
                        #     print(f"value is {value}")
                        #     print(f"maximum {maximum} {step} next {next}")
                        #     print("this is the best state (1,3)")
                        #     print(self.game_value(newstate))
                    if(maximum == 1 and depth > 0):
                        # self.printM(state) 
                        # print(f"value is {value}")
                        # print(f"maximum {maximum} {step} next {next}")
                        # print(f"end mpre print, depth {depth}")
                        return maximum, step
                else:
                    for piece in myPieces:
                        newstate2 = deepcopy(newstate)
                        if self.adjacent(piece, succ):
                            newstate2[succ[0]][succ[1]] = self.my_piece
                            newstate2[piece[0]][piece[1]] = ' '
                            next = self.max_value(newstate2,depth-1, not my_move, (piece,succ))
                            if(maximum < next[0]):
                                maximum = next[0]
                                step = (piece, succ) 
                            if(maximum == 1 and depth > 0):                               
                                # self.printM(state)
                                # print(f"value is {value}")
                                # print(f"maximum {maximum} {step} next {next}")
                                # print(f"end mp print #no drop face, depth {depth}")
                                return maximum, step
                            
            # self.printM(state) 
            # print(f"value is {value}")
            # print(f"maximum {maximum} {step} pre {pre_action}")
            # print(f"end m print, depth {depth}")
            return maximum, step
        else:
            minimum = 1000
            dropFace = False if len(oppPieces) >= 4 else True
            for succ in self.succ(state):
                newstate = deepcopy(state)
                if(dropFace):
                    newstate[succ[0]][succ[1]] = self.opp
                    next = self.max_value(newstate,depth-1, not my_move, succ)
                    if(minimum > next[0]):   
                        premin = minimum                    
                        minimum = next[0]
                        step = succ
                        # self.printM(newstate)
                        # print(f"min changed, premin {premin}, minimum {minimum}, step {step}")
                    if(minimum == -1):
                        # self.printM(state) 
                        # print(f"value is {value}")
                        # print(f"minimum {minimum} next {next}")
                        # print(f"end opre print, depth {depth}")
                        return minimum, step
                else:
                    for piece in oppPieces:
                        newstate2 = deepcopy(newstate)
                        # if(piece == (4,0) and succ == (3,1)):
                            # self.printM(newstate2)
                            # print(f"piece {piece}, succ {succ}") if self.adjacent(piece, succ) else 0
                            # print(f"next {self.max_value(newstate2,depth-1, not my_move, (piece,succ))}")
                        if self.adjacent(piece, succ):
                            newstate2[succ[0]][succ[1]] = self.opp
                            newstate2[piece[0]][piece[1]] = ' '
                            next = self.max_value(newstate2,depth-1, not my_move, (piece,succ))
                            if(minimum > next[0]):
                                premin = minimum
                                minimum = next[0]
                                step = (piece, succ) 
                                # self.printM(newstate2)
                                # print(f"min changed, premin {premin}, minimum {minimum}, step {step}")
                            if(minimum == -1):
                                # self.printM(state) 
                                # print(f"value is {value}")
                                # print(f"minimum {minimum} next {next}")
                                # print(f"end op print #no drop face, depth {depth}")
                                return minimum, step             
            
            # self.printM(state) 
            # print(f"value is {value}")
            # print(f"minimum {minimum} step {step}")
            # print(f"end o print, depth {depth}") 
            return minimum, step
    
    def adjacent(self, p1,p2):
        return True if abs(p1[0]-p2[0])<=1 and abs(p1[1]-p2[1])<=1 else False

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    ai.board = [[' ' for j in range(5)] for i in range(5)]
    ai.my_piece = 'b'
    ai.opp = 'r'
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            # move_made = False
            # ai.print_board()
            # print(ai.opp+"'s turn")
            # while not move_made:
            #     player_move = input("Move (e.g. B3): ")
            #     while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
            #         player_move = input("Move (e.g. B3): ")
            #     try:
            #         ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
            #         move_made = True
            #     except Exception as e:
            #         print(e)
            ai.print_board()
            move = ai.random_move(ai.board)
            ai.place_piece(move, ai.opp)
            print(ai.opp+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    count = 0
    while ai.game_value(ai.board) == 0:
        print(f"count {count}")
        if count > 20:
            return -1
        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            # move_made = False
            # ai.print_board()
            # print(ai.opp+"'s turn")
            # while not move_made:
            #     move_from = input("Move from (e.g. B3): ")
            #     while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
            #         move_from = input("Move from (e.g. B3): ")
            #     move_to = input("Move to (e.g. B3): ")
            #     while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
            #         move_to = input("Move to (e.g. B3): ")
            #     try:
            #         ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
            #                         (int(move_from[1]), ord(move_from[0])-ord("A"))])
            #         move_made = True
            #     except Exception as e:
            #         print(e)
            ai.print_board()
            move = ai.random_move(ai.board)
            ai.place_piece(move, ai.opp)
            print(ai.opp+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))

        # update the game variables
        turn += 1
        turn %= 2
        count += 1

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
        return 1
    else:
        print("You win! Game over.")
        return -1

def main2():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:
        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")

def debug():
    t = Teeko2Player()
    board = [[' ' for j in range(5)] for i in range(5)]
    t.my_piece = 'b'
    t.opp = 'r'
    # board[0] = ['r', ' ', ' ', ' ', ' ']
    # board[1] = ['r', 'b', ' ', ' ', ' ']
    # board[2] = [' ', ' ', 'b', ' ', 'r']
    # board[3] = [' ', ' ', ' ', 'b', ' ']
    # board[4] = ['r', ' ', ' ', ' ', ' ']

    # board[0] = ['r', ' ', ' ', ' ', ' ']
    # board[1] = ['r', 'b', ' ', ' ', ' ']
    # board[2] = [' ', ' ', 'b', ' ', ' ']
    # board[3] = [' ', ' ', ' ', 'b', ' ']
    # board[4] = ['r', ' ', ' ', ' ', ' ']

    board[0] = [' ', ' ', ' ', ' ', ' ']
    board[1] = [' ', 'b', ' ', ' ', 'b']
    board[2] = [' ', ' ', 'r', 'r', 'r']
    board[3] = [' ', 'b', ' ', 'b', ' ']
    board[4] = [' ', ' ', ' ', ' ', 'r']
    
    # start = time()
    # print(t.max_value(board, 3, True))
    # end = time()
    # print(f"time {(end-start)}")
    print(t.random_move(board))

    # print(t.succ(board))
    # print(t.heuristic_game_value(board))
    # print(t.game_value(board))

if __name__ == "__main__":
    # debug()
    # value = 0
    # for i in range(100):      
    #     value += main()
    # print(f"value {value}")
    main2()
