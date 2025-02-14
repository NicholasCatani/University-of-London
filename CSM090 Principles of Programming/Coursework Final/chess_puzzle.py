### Development
### By Nicholas Catani


def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    x = ord(loc[0].lower()) - ord("a") + 1
    y = int(loc[1:])
    return (x, y)



def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    column = chr(x + ord("a") - 1)
    row = str(y)
    return f"{column}{row}"



class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_

Board = tuple[int, list[Piece]]



def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
    return any(piece.pos_x == pos_X and piece.pos_y == pos_Y for piece in B[1])



def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece
    raise ValueError("No piece at given location.")



class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
        ### Check board boundaries
        if not (1 <= pos_X <= B[0] and 1 <= pos_Y <= B[0]):
            return False

        ### Same position: Cannot move
        if (self.pos_x, self.pos_y) == (pos_X, pos_Y):
            return False
        
        dx, dy = abs(self.pos_x - pos_X), abs(self.pos_y - pos_Y)
        if dx != dy:
            return False    ### Not a diagonal move

        ### Check for blocking pieces
        step_x = 1 if pos_X > self.pos_x else -1
        step_y = 1 if pos_Y > self.pos_y else -1
        x, y = self.pos_x + step_x, self.pos_y + step_y
        
        while (x, y) != (pos_X, pos_Y):
            if is_piece_at(x, y, B):
                return False    ### Path is blocked
            x += step_x
            y += step_y
        
        ### Move is valid if no blockers found
        return True    

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''
        
        ### Must be able to reach the destination
        if not self.can_reach(pos_X, pos_Y, B):
            return False
        
        ### Cannot capture a piece of the same side
        if is_piece_at(pos_X, pos_Y, B):
            piece = piece_at(pos_X, pos_Y, B)
            if piece.side == self.side:
                return False
        
        ### Simulate the move and check for self-check
        temp_board = self.move_to(pos_X, pos_Y, B)
        if is_check(self.side, temp_board):
            return False    ### The move would live the King in check
        
        return True

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        new_pieces = [piece for piece in B[1] if piece != self]
        if is_piece_at(pos_X, pos_Y, B):
            target_piece = piece_at(pos_X, pos_Y, B)
            new_pieces.remove(target_piece)
        new_pieces.append(Bishop(pos_X, pos_Y, self.side))
        return (B[0], new_pieces)



class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''
        dx, dy = abs(self.pos_x - pos_X), abs(self.pos_y - pos_Y)
        return dx <= 1 and dy <= 1

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        if not (1 <= pos_X <= B[0] and 1 <= pos_Y <= B[0]):  ### Ensure within board boundaries
            return False
        if (self.pos_x, self.pos_y) == (pos_X, pos_Y):  ### Cannot move to the same position
            return False
        
        dx, dy = abs(self.pos_x - pos_X), abs(self.pos_y - pos_Y)
        if max(dx, dy) > 1:
            return False
        
        if is_piece_at(pos_X, pos_Y, B):
            piece = piece_at(pos_X, pos_Y, B)
            if piece.side == self.side: ### Cannot capture same-side pieces
                return False
        
        temp_board = self.move_to(pos_X, pos_Y, B)
        if is_check(self.side, temp_board): ### Cannot leave the king in check
            return False
        
        return True

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        new_pieces = [piece for piece in B[1] if piece != self]
        if is_piece_at(pos_X, pos_Y, B):
            target_piece = piece_at(pos_X, pos_Y, B)
            new_pieces.remove(target_piece)
        new_pieces.append(King(pos_X, pos_Y, self.side))
        return (B[0], new_pieces)



def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    ### Add a King for both sides in the test board to avoid unnecessary exceptions.
    try:
        king = next(piece for piece in B[1] if isinstance(piece, King) and piece.side == side)
    except StopIteration:
        raise ValueError("No King found for the specific side.")
    
    for piece in B[1]:
        if piece.side != side and piece.can_reach(king.pos_x, king.pos_y, B):
            return True
    return False



def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_move_to
    '''
    if not is_check(side, B):   ### Not in check
        return False
    
    for piece in B[1]:
        if piece.side == side:  ### Only consider pieces of the current side
            for x in range(1, B[0] + 1):
                for y in range(1, B[0] + 1):
                    if piece.can_move_to(x, y, B):  ### Check if any valid move exists
                        return False
    
    return True ### No valid moves; it is checkmate



def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''
    if is_check(side, B):
        return False

    for piece in B[1]:
        if piece.side == side:
            for x in range(1, B[0] + 1):
                for y in range(1, B[0] + 1):
                    if piece.can_move_to(x, y, B):
                        return False

    return True



def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    with open(filename, "r") as file:
        lines = file.readlines()
    
    size = int(lines[0].strip())
    pieces = []
    
    for i, line in enumerate(lines[1:]):
        if not line.strip():
            continue
        
        side = True if i == 0 else False    ### First piece line is white, second piece line is black

        for piece in line.strip().split(", "):
            piece_type, pos = piece[0], piece[1:]
            pos_x, pos_y = location2index(pos)
            
            ### Create the appropriate piece and append it to the list
            if piece_type == "K":
                pieces.append(King(pos_x, pos_y, side))
            elif piece_type == "B":
                pieces.append(Bishop(pos_x, pos_y, side))

    return (size, pieces)



def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    with open(filename, "w") as file:
        file.write(f"{B[0]}\n")
        white_pieces = [piece for piece in B[1] if piece.side]
        black_pieces = [piece for piece in B[1] if not piece.side]
        file.write(", ".join(f"{type(piece).__name__[0]}{index2location(piece.pos_x, piece.pos_y)}" for piece in white_pieces) + "\n")
        file.write(", ".join(f"{type(piece).__name__[0]}{index2location(piece.pos_x, piece.pos_y)}" for piece in black_pieces))


####### Library #####
import random     ###
#####################


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''
    black_pieces = [piece for piece in B[1] if not piece.side]
    random.shuffle(black_pieces)
    for piece in black_pieces:
        for x in range(1, B[0] + 1):
            for y in range(1, B[0] + 1):
                if piece.can_move_to(x, y, B):
                    return (piece, x, y)
    raise ValueError("No valid move found for Black.")



def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    board = [["\u2001" for _ in range(B[0])] for _ in range (B[0])]
    for piece in B[1]:
        symbol = ""
        if isinstance(piece, King):
            symbol = "\u2654" if piece.side else "\u265A"
        elif isinstance(piece, Bishop):
            symbol = "\u2657" if piece.side else "\u265D"
        board[piece.pos_y - 1][piece.pos_x - 1] = symbol
    return "\n".join("".join(row) for row in board)



def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''    
    
    filename = input("File name for initial configuration: ")
    while True:
        if filename.strip().upper() == "QUIT":
            print("Game terminated.")
            return
        try:
            board = read_board(filename)
            break
        except Exception as e:
            print("This is not a valid file. File name for initial configuration: ")
            filename = input()

    print(f"The initial configuration is:\n{conf2unicode(board)}")

    while True:
        print("Next move of White:")
        move = input().strip()
        if move.upper() == "QUIT":
            print("File name to store the configuration:")
            save_file = input().strip()
            save_board(save_file, board)
            print("The game configuration saved.")
            return
        try:
            start, end = location2index(move[:2]), location2index(move[2:])
            piece = piece_at(start[0], start[1], board)
            if piece.side:
                board = piece.move_to(end[0], end[1], board)
                print(f"The configuration after White's move is:\n{conf2unicode(board)}")
                if is_checkmate(False, board):
                    print("Game over. White wins.")
                    return
                if is_stalemate(False, board):
                    print("Game over. Stalemate.")
                    return
            else:
                raise ValueError("Invalid move for White.")
        except Exception as e:
            print("This is not a valid move. Next move of White:")
            continue

        black_piece, x, y = find_black_move(board)
        board = black_piece.move_to(x, y, board)
        print(f"Next move of Black is {index2location(black_piece.pos_x, black_piece.pos_y)}{index2location(x, y)}.")
        print(f"The configuration after Black's move is:\n{conf2unicode(board)}")
        if is_checkmate(True, board):
            print("Game over. Black wins.")
            return
        if is_stalemate(True, board):
            print("Game over. Stalemate.")
            return



if __name__ == '__main__': #keep this in
   main()
