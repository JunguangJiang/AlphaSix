# -*- coding: utf-8 -*-
"""
Created on Sun May 13 11:40:52 2018

@author: chenyushao
"""

# Bacis constants or definitions
# Type of chess, which equivalent to the value of grid of chessboard

EMPTY = 0
BLACK = 1
WHITE = 2

"""
Actually personally I prefer setting black and white as accordingly 1 and -1,
to indicate their antagonistic relation.
But, considering the fact that we have already applied WHITE = 2 in our 
preliminary work, I believe it will be more proper to follow it.
Later I may implement the opposition between the two sides of players in my 
personal work~
"""

class ChessBoard(object):
    