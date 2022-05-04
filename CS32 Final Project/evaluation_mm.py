import chess
import numpy as np
from pyparsing import alphanums
chess.Board()


class Node():
    def __init__(self, parent, action, children, depth, minimaxbest, evaluation, isTerminal):
        self.parent = parent
        self.action = action
        self.children = children
        self.evaluation = evaluation
        self.depth = depth
        self.minimaxbest = minimaxbest
        self.isTerminal = isTerminal

def mm_max(object):
    best = np.NINF
    bestmove = ""
    for i in object.children:
        if i.evaluation >= best:
            best = i.evaluation
            bestmove = i
    return best, bestmove

def mm_min(object):

    best = np.Inf
    bestmove = ""
    for i in object.children:
        if i.evaluation <= best:
            best = i.evaluation
            bestmove = i
    return best, bestmove

class Evaluations():
    '''This class allows me to generate score evaluations based on static game positions. The score takes into account the number and types
    of pieces, the static, current position of the pices, and the pieces's mobility.'''

    def __init__(self):

        self.board = chess.Board()
        self.referencetable = np.array([
            ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8'],
            ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
            ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6'],
            ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
            ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
            ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
            ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
            ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']
        ])

        self.wpawnsqt = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0], 
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5], 
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

        self.wknighsqt = np.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0], 
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0], 
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]])

        self.wbishsqt = np.zeros((8,8))
        col1bish = [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        col2bish = [-1.0, 0.0, 0.0, 0.5, 0.0, 1.0, 0.5, -1.0]
        col3bish = [-1.0, 0.0, 0.5, 0.5, 1.0, 1.0, 0.0, -1.0]
        col4bish = [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0]
        objects = [col1bish, col2bish, col3bish, col4bish]
        for i in range(4):
            self.wbishsqt[:,i] = objects[i]
            self.wbishsqt[:,7-i]=objects[i]

        self.wrooksqt = np.zeros((8,8))
        self.wrooksqt[2:6, (0,7)] = -0.5
        self.wrooksqt[1, 1:6] = 1.0
        self.wrooksqt[1,(0,7)] = 0.5
        self.wrooksqt[7, (3,4)] = 0.5

        self.wqueensqt = np.array([
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0,-2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ])

        self.wkingsqt = np.zeros((8,8))
        col1king = [-3.0, -3.0, -3.0, -3.0, -2.0, -1.0, 2.0, 2.0]
        col2king = [-4.0, -4.0, -4.0, -4.0, -3.0, -2.0, 2.0, 3.0]
        col3king = [-4.0, -4.0, -4.0, -4.0, -3.0, -2.0, 0.0, 1.0]
        col4bking = [-5.0, -5.0, -5.0, -5.0, -4.0, -2.0, 0.0, -0.0]
        objects = [col1king, col2king, col3king, col4bking]

        for i in range(4):
                self.wkingsqt[:,i] = objects[i]
                self.wkingsqt[:,7-i]=objects[i]
        
        self.blkpawnsqt = np.zeros((8,8))
        self.blkknighsqt = np.zeros((8,8))
        self.blkbishsqt = np.zeros((8,8))
        self.blkrooksqt = np.zeros((8,8))
        self.blkqueensqt = np.zeros((8,8))
        self.blkkingsqt = np.zeros((8,8))

        for i in range(8):
            self.blkpawnsqt[i, :] = self.wpawnsqt[7-i, :]
            self.blkknighsqt[i, :] = self.wknighsqt[7-i, :]
            self.blkbishsqt[i, :] = self.wbishsqt[7-i, :]
            self.blkrooksqt[i, :] = self.wrooksqt[7-i, :]
            self.blkqueensqt[i, :] = self.wqueensqt[7-i, :]
            self.blkkingsqt[i, :] = self.wkingsqt[7-i, :]


        self.whitepieceinfo = {1: {"Points": 10, "SQT": self.wpawnsqt} , 
        2 : {"Points": 32, "SQT": self.wknighsqt},
        3: {"Points": 33, "SQT": self.wbishsqt},
        4: {"Points": 50, "SQT": self.wrooksqt},
        5: {"Points": 90, "SQT": self.wqueensqt},
        6: {"Points": 900, "SQT": self.wkingsqt}}

        self.blackpieceinfo =  {1: {"Points": 10, "SQT": self.blkpawnsqt} , 
        2 : {"Points": 32, "SQT": self.blkknighsqt},
        3: {"Points": 33, "SQT": self.blkbishsqt},
        4: {"Points": 50, "SQT": self.blkrooksqt},
        5: {"Points": 90, "SQT": self.blkqueensqt},
        6: {"Points": 900, "SQT": self.blkkingsqt}}    

        self.white_prevmob = []
        self.black_prevmob = [] 

        
    def game_eval(self):

        if self.board.is_checkmate() and chess.Outcome == 1:
            game_score = np.Inf
            return game_score

        elif self.board.is_checkmate() and chess.Outcome == 2:
            game_score = np.NINF
            return game_score
        
        elif self.board.is_stalemate():
            game_score = 0
            return game_score
        
        else:

            def white_eval(self):

                pieces_score = 0
                for i in range(1,7):
                    pieces = self.board.pieces(i, True)
                    n = self.whitepieceinfo[i]["Points"]
                    pieces_score_standin = len(pieces) * n
                    pieces_score += pieces_score_standin

                for j in range(64):
                    if self.board.color_at(j) is True:
                        piecetype = self.board.piece_type_at(j)
                        ucipos = chess.square_name(j).upper()
                        tuplepos = np.where(self.referencetable == ucipos)

                        m = self.whitepieceinfo[piecetype]["SQT"][tuplepos]
                        pieces_score += m[0]
                    else:
                        pass
                
                return pieces_score

            def black_eval(self):

                pieces_score = 0
                for i in range(1,7):
                    pieces = self.board.pieces(i, False)
                    n = self.blackpieceinfo[i]["Points"]
                    pieces_score_standin = len(pieces) * n
                    pieces_score += pieces_score_standin

                for j in range(64):
                    if self.board.color_at(j) is False:
                        piecetype = self.board.piece_type_at(j)
                        ucipos = chess.square_name(j).upper()
                        tuplepos = np.where(self.referencetable == ucipos)

                        m = self.blackpieceinfo[piecetype]["SQT"][tuplepos]
                        pieces_score += m[0]
                    else:
                        pass

                return pieces_score

            def white_mobility(self):

                if self.board.turn is True:
                    legalmoves = list(self.board.legal_moves) 
                    mobtuplist = [(self.board.piece_at
                                    (chess.parse_square
                                    (str(legalmoves[j]).split("'")[0][0:2])).piece_type, 
                                    (str(legalmoves[j]).split("'")[0][2:]).upper()) for j in range(len(legalmoves)) 
                                    if self.board.color_at(chess.parse_square(str(legalmoves[j]).split("'")[0][0:2])) is True]

                    pieces_score = 0
                    for i in range(len(mobtuplist)):
                        tuplepos = np.where(self.referencetable == mobtuplist[i][1])
                        m = self.whitepieceinfo[mobtuplist[i][0]]["SQT"][tuplepos]
                        pieces_score += m[0]

                elif len(self.board.move_stack) != 0 and self.board.turn is False:
                    v = self.board.pop()
                    v = str(v)
                    pieces_score = white_mobility(self)
                    self.board.push_uci(v)

                return pieces_score

            def black_mobility(self):
                if self.board.turn is False:
                    legalmoves = list(self.board.legal_moves) 
                    mobtuplist = [(self.board.piece_at
                                    (chess.parse_square
                                    (str(legalmoves[j]).split("'")[0][0:2])).piece_type, 
                                    (str(legalmoves[j]).split("'")[0][2:]).upper()) for j in range(len(legalmoves)) 
                                    if self.board.color_at(chess.parse_square(str(legalmoves[j]).split("'")[0][0:2])) is False]

                    pieces_score = 0

                    for i in range(len(mobtuplist)):
                        tuplepos = np.where(self.referencetable == mobtuplist[i][1])
                        m = self.blackpieceinfo[mobtuplist[i][0]]["SQT"][tuplepos]
                        pieces_score += m[0]
                
                elif self.board.turn is True and len(self.board.move_stack) == 1:
                    pieces_score = white_mobility(self)

                elif self.board.turn is True and len(self.board.move_stack) > 1:
                    v = self.board.pop()
                    v = str(v)
                    pieces_score = black_mobility(self)
                    self.board.push_uci(v)

                return pieces_score

            whscore = white_eval(self) + white_mobility(self)
            blkscore = black_eval(self) + black_mobility(self)
            game_score = whscore - blkscore

            return game_score

    def minimax(self, legmov, minidepth, parent_node):
        '''I use the idea of recursion for the minimax algorithm.'''

        if legmov == []:
            legalmoves = list(self.board.legal_moves)
            legmov = [str(move) for move in legalmoves]
            parent_node = Node(depth = 0, parent = None, action = None, children = [], minimaxbest = 0, evaluation = 0,
                                isTerminal= False)
        

        if (minidepth - 1) == 0:
            for i in legmov:
                self.board.push_uci(i)
                deep = parent_node.depth + 1
                evaluatn = self.game_eval()
                cur_node = Node(parent = parent_node, depth = deep, action = i, evaluation = evaluatn, children = [],
                                 minimaxbest = 0, isTerminal = True)
                parent_node.children.append(cur_node)
                self.board.pop()

        else:
            for i in range(len(legmov)):
                
                self.board.push_uci(legmov[i])
                nextmoves = [str(move) for move in list(self.board.legal_moves)]
                deep = parent_node.depth + 1
                cur_node = Node(parent = parent_node, action = legmov[i], depth = deep, children = [], minimaxbest = 0, 
                                evaluation = 0, isTerminal= False)
                parent_node.children.append(cur_node)

                self.minimax(minidepth = minidepth - 1, legmov = nextmoves, parent_node = cur_node)

                if cur_node.depth %2 == 0:
                    cur_node.evaluation, cur_node.minimaxbest = mm_max(cur_node)


                else:
                    cur_node.evaluation, cur_node.minimaxbest = mm_min(cur_node)

                self.board.pop()

        if parent_node.depth == 0:
            parent_node.evaluation, parent_node.minimaxbest = mm_max(parent_node)
            return parent_node


