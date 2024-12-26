### Testing
### By Nicholas Catani


import pytest
from chess_puzzle import *



def test_location2index1():
    assert location2index("e2") == (5, 2)
    assert location2index("a1") == (1, 1)
    assert location2index("h8") == (8, 8)
    assert location2index("d4") == (4, 4)
    assert location2index("z10") == (26, 10)



def test_index2location1():
    assert index2location(5, 2) == "e2"
    assert index2location(1, 1) == "a1"
    assert index2location(8, 8) == "h8"
    assert index2location(4, 4) == "d4"
    assert index2location(26, 10) == "z10"



##### Settings

wb1 = Bishop(2,5,True)
wb2 = Bishop(4,4,True)
wb3 = Bishop(3,1,True)
wb4 = Bishop(5,5,True)
wb5 = Bishop(4,1,True)

wk1 = King(3,5,True)
wk1a = King(2,5,True)


bb1 = Bishop(3,3,False)
bb2 = Bishop(5,3,False)
bb3 = Bishop(1,2,False)

bk1 = King(2,3,False)


B1 = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1])



###########################
##### Single scenario test
###########################

def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False

########################
##### Comprehensive test
########################

def test_is_piece_at():
    board = (5, [Bishop(2, 2, True), King(4, 4, False)])
    assert is_piece_at(2, 2, board) == True    ### Piece exists
    assert is_piece_at(4, 4, board) == True    ### Piece exists
    assert is_piece_at(1, 1, board) == False    ### No piece at this position
    assert is_piece_at(3, 3, board) == False    ### Empty square
    assert is_piece_at(5, 5, board) == False    ### Out of range



###########################
##### Single scenario test
###########################

def test_piece_at1():
    assert piece_at(3,3, B1) == bb1

########################
##### Comprehensive test
########################

def test_piece_at():
    board = (5, [Bishop(2, 2, True), King(4, 4, False)])
    assert isinstance(piece_at(2, 2, board), Bishop)
    assert isinstance(piece_at(4, 4, board), King)
    assert piece_at(2, 2, board).side == True
    assert piece_at(4, 4, board).side == False
    with pytest.raises(ValueError):
        piece_at(1, 1, board)    ### No piece at this position



###########################
##### Single scenario test
###########################

def test_can_reach1():
    assert wb2.can_reach(5,5, B1) == True

########################
##### Comprehensive test
########################

def test_bishop_can_reach():
    board = (5, [Bishop(2, 2, True)])
    bishop = board[1][0]
    assert bishop.can_reach(4, 4, board) == True    ### Diagonal move
    assert bishop.can_reach(1, 1, board) == True    ### Diagonal move
    assert bishop.can_reach(2, 3, board) == False   ### Non-diagonal move
    assert bishop.can_reach(6, 6, board) == False   ### Out of range
    assert bishop.can_reach(2, 2, board) == False   ### No move



###########################
##### Single scenario test
###########################

def test_can_move_to1():
    assert wb2.can_move_to(5,5, B1) == False

########################
##### Comprehensive test
########################

def test_bishop_can_move_to():
    board = (5, [Bishop(2, 2, True), King(4, 4, False), King(5, 5, True)])
    bishop = board[1][0]
    assert bishop.can_move_to(4, 4, board) == True      ### Capture enemy King
    assert bishop.can_move_to(1, 1, board) == False     ### Blocked or self-check
    assert bishop.can_move_to(3, 3, board) == False     ### Valid move
    assert bishop.can_move_to(2, 2, board) == False     ### No move
    assert bishop.can_move_to(6, 6, board) == False     ### Out of range



###########################
##### Single scenario test
###########################

def test_move_to1():
    wb2a = Bishop(3,3,True)
    Actual_B = wb2.move_to(3,3, B1)
    Expected_B = (5, [wb2a, wb1, wk1, bk1, bb2, wb3]) 

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_is_check1():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2, wb3])
    assert is_check(True, B2) == True

def test_is_checkmate1():
    B3 = (5, [wk1a, wb4, bk1, bb2, bb3, wb3, wb5])
    assert is_checkmate(False, B3) == True

def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found



########################
##### Comprehensive test
########################

def test_king_can_move_to():
    board = (5, [King(2, 2, True), Bishop(3, 3, False), King(5, 5, False)])
    king = board[1][0]
    assert king.can_move_to(3, 3, board) == True    ### Capture Bishop
    assert king.can_move_to(1, 1, board) == False   ### Out of range
    assert king.can_move_to(3, 2, board) == True    ### Valid move
    assert king.can_move_to(5, 5, board) == False   ### Out of range
    assert king.can_move_to(2, 2, board) == False   ### No move

def test_is_check():
    board = (5, [King(2, 2, True), Bishop(4, 4, False), King(5, 5, False)])
    assert is_check(True, board) == True    ### White King is in check
    assert is_check(False, board) == False      ### Black is not in check

def test_is_checkmate():
    board = (5, [King(2, 2, True), Bishop(4, 4, False), Bishop(3, 3, False), King(5, 5, False)])
    assert is_checkmate(True, board) == False    ### Checkmate conditions not fully met
    assert is_checkmate(False, board) == False      ### Black is not checkmated

def test_read_board():
    board = read_board("board_examp.txt")
    assert board[0] == 5    ### Board size
    assert len(board[1]) == 7   ### Pieces count matches file
    assert isinstance(board[1][0], Bishop)  ### First piece is a Bishop
    assert isinstance(board[1][1], King)    ### Second piece is a King
    assert isinstance(board[1][2], Bishop)    ### Third piece is a Bishop
    assert isinstance(board[1][3], Bishop)    ### Forth piece is a Bishop
    assert isinstance(board[1][4], King)    ### Fifth piece is a King
    assert isinstance(board[1][5], Bishop)    ### Sixth piece is a Bishop
    assert isinstance(board[1][6], Bishop)    ### Seventh piece is a Bishop

def test_conf2unicode():
    board = (5, [Bishop(2, 2, True), King(4, 4, False)])
    result = conf2unicode(board)
    assert "\u2657" in result   ### White Bishop Unicode
    assert "\u265A" in result   ### Black King Unicode



