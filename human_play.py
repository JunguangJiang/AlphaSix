# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
@modifier: Junguang Jiang
"""

from __future__ import print_function
from game import Board, Game
from mcts_alphaZero import MCTSPlayer
from policy_value_net_pytorch import PolicyValueNet  # Pytorch


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run(n_in_row, width, height,
        model_file, ai_first,
        n_playout, use_gpu):
    try:
        board = Board(width=width, height=height, n_in_row=n_in_row)
        game = Game(board)

        # ############### human VS AI ###################
        best_policy = PolicyValueNet(width, height, model_file=model_file, use_gpu=use_gpu)
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=n_playout)
        human = Human()

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=ai_first, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')

def usage():
    print("-s 设置棋盘大小，默认为6")
    print("-r 设置是几子棋，默认为4")
    print("-m 设置每步棋执行MCTS模拟的次数，默认为400")
    print("-i ai使用哪个文件中的模型，默认为model/6_6_4_best_policy.model")
    print("--use_gpu 使用GPU进行运算")
    print("--human_first 让人类先下")


if __name__ == '__main__':
    import sys, getopt

    height = 6
    width = 6
    n_in_row = 4
    use_gpu = False
    n_playout = 400
    model_file = "model/6_6_4_best_policy.model"
    ai_first=True

    opts, args = getopt.getopt(sys.argv[1:], "hs:r:m:i:", ["use_gpu", "graphics", "human_first"])
    for op, value in opts:
        if op == "-h":
            usage()
            sys.exit()
        elif op == "-s":
            height = width = int(value)
        elif op == "-r":
            n_in_row = int(value)
        elif op == "--use_gpu":
            use_gpu = True
        elif op == "-m":
            n_playout = int(value)
        elif op == "-i":
            model_file = value
        elif op == "--human_first":
            ai_first=False
    run(height=height, width=width, n_in_row=n_in_row, use_gpu=use_gpu, n_playout=n_playout,
        model_file=model_file, ai_first=ai_first)
