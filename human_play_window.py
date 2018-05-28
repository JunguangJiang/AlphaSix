# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
@modifier: Junguang Jiang
@modifier2: Yushao Chen
@UI materials: https://blog.csdn.net/windowsyun/article/details/78877939
"""
from __future__ import print_function
from game import *
from mcts_alphaZero import MCTSPlayer
from policy_value_net_pytorch import PolicyValueNet  # Pytorch
import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

"""
Functions to implement
1. Beginning button and the selection of the first-move player

2. Drawing the chessboard:
    2.1 set the size of chessboard
    2.2 set the grid of chessboard
    2.3 set the effective area for every site in the grid

3. Implementing the interaction between human players and chessboard
"""

# Global variables
ai_first = 0
# Below are mainly the parametres for our board picture rather 
# rather than the logic board
WIDTH = 540
HEIGHT = 540
MARGIN = 22
SIZE = 15
GRID = (WIDTH - 2 * MARGIN) / (SIZE - 1)
PIECE = 34
EMPTY = 0
BLACK = 1
WHITE = 2    
# test variables
width = 8
height = 8
n_in_row = 5
model_file = 'model/8_8_5_best_policy_.model'
use_gpu = False# I don't know why but I just cannot use cuda in my computer = =
n_playout = 800


class cycleGroup(tuple):
    def __init__(self, parent):
        self.elements = parent
        self.order = len(parent)
        self.point = 0
    def pointTurnRight(self):
        self.point = (self.point + 1) % self.order
    def pointTurnLeft(self):
        self.point = (self.point + self.order - 1) % self.order
    def element(self):
        return self.elements[self.point]


class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()
  
# test PyQt5 codes
class HumanWindow(QWidget):
    # def
    mysignal = pyqtSignal(str)
    placeChess = pyqtSignal(int, int)
    def __init__(self):
        super(HumanWindow, self).__init__()
        self.mysignal.connect(self.UIinput)
        self.placeChess.connect(self.draw)
        # set the QWidget name
        #self.setWindowTitle("Five in A Row")
        # set the position with the first 2 numbers, and the size with the last 2 numbers
        #self.setGeometry(300, 300, 250, 150)
#        best_policy = PolicyValueNet(8, 8, "model/6_6_4_best_policy.model", use_gpu=1) # 加载最佳策略网络
#        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=n_playout) # 生成一个AI玩家
        self.isFirstMove = True
        
        best_policy = PolicyValueNet(width, height, model_file=model_file, use_gpu=use_gpu) # 加载最佳策略网络
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=n_playout) # 生成一个AI玩家
        self.AIPlayer = mcts_player
        self.ai_down = True
        
        #set 2 kinds of chesses#
        self.black = QPixmap('black.png')
        self.white = QPixmap('white.png')
        #set order cycle#
        cycle = (self.black, self.black, self.white, self.white)
        self.chesses = cycleGroup(cycle)
        #set colors of players
        self.colorToPlayer = {self.black:'AI', self.white:'HM'}

        
        self.board = Board()
        self.board.width = 8
        self.board.height = 8
        self.initUI()
        pass
    
##########Reserverd Place for the Consistence##########
    def set_player_ind(self, p):
        """设置人类玩家的编号，黑：1，白：2"""
        self.player = p
    def get_action(self, board):
        """根据棋盘返回动作"""
        self.nowStep = '0'
        try:
            while(self.nowStep == '0'):
                self.get_action(board)
            location = self.nowStep
            print("nowStep = ", self.nowStep)
            self.nowStep = '0'
            if isinstance(location, str):  # 如果location确实是字符串
                location = [int(n, 10) for n in location.split(",")] # 将location转换为对应的坐标点
            move = board.location_to_move(location) # 坐标点转换为一个一维的值move,介于[0,width*height)
        except Exception as e: #异常情况下
            move = -1
        if move == -1 or move not in board.availables: # 如果move值不合法
            print("invalid move")
            move = self.get_action(board) # 重新等待输入
        return move

    def __str__(self):
        return "Human {}".format(self.player)
 ######################################################   
    
    def UIinput(self, strInput):
        print("\n\rUIinput result:",strInput)
        return strInput
    
    def initUI(self):
        self.buttonStart()
        #testImage = ChessBoardPic()

    def buttonStart(self):
        self.button = QPushButton("开始", self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.setGeometry(100, 100, 60, 35)
        self.button.clicked.connect(self.askForFirst)  
        
    def askForFirst(self):
        message = QMessageBox()
        reply = message.question(self, '询问', '是否AI先手？', QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            ai_first = 1
            self.chesses.point = 1
            self.my_turn = False
            self.board.init_board(1)
        else:
            ai_first = 0
            self.chesses.point = 3
            self.my_turn = True
            self.board.init_board(0)
        print('ai_first = ', ai_first)
        # message.buttonClicked.connect(self.showBoard) # unknow invalidity
        self.button.close()
#        self.hide()
        self.showBoard()
        
    def showBoard(self):
        print("showBoard begins")
        
                
        palette1 = QPalette()  # 设置棋盘背景
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('chessboard.jpg')))
        self.setPalette(palette1)
#         self.setStyleSheet("board-image:url(img/chessboard.jpg)")  # 不知道这为什么不行
        self.setCursor(Qt.PointingHandCursor)  # 鼠标变成手指形状
        #self.sound_piece = QSound("sound/luozi.wav")  # 加载落子音效
        #self.sound_win = QSound("sound/win.wav")  # 加载胜利音效
        #self.sound_defeated = QSound("sound/defeated.wav")  # 加载失败音效

        self.resize(WIDTH, HEIGHT)  # 固定大小 540*540
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))
        print("hhh")
        self.setWindowTitle("GoBang")  # 窗口名称
        self.setWindowIcon(QIcon('black.png'))  # 窗口图标
        self.piece_now = BLACK  # 黑棋先行
        self.step = 0  # 步数
        self.x, self.y = 1000, 1000

        self.mouse_point = LaBel(self)  # 将鼠标图片改为棋子
        self.mouse_point.setScaledContents(True)
        self.mouse_point.setPixmap(self.black)  #加载黑棋
        self.mouse_point.setGeometry(270, 270, PIECE, PIECE)
        
        
        self.pieces = [LaBel(self) for i in range(SIZE * SIZE)]  # 新建棋子标签，准备在棋盘上绘制棋子
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  #图片大小根据标签大小可变
        print("hhh")
        
        self.mouse_point.raise_()  # 鼠标始终在最上层
        self.ai_down = True  # AI已下棋，主要是为了加锁，当值是False的时候说明AI正在思考，这时候玩家鼠标点击失效，要忽略掉 mousePressEvent

        self.setMouseTracking(True)
        if self.colorToPlayer[self.chesses.element()] == 'AI':
            self.turnToAiPlayer()
############Redefine the mouse event functions########    
        # By redefining mouseMoveEvent() we aim to set the mouse effect#
    def mouseMoveEvent(self, e): 
        # self.lb1.setText(str(e.x()) + ' ' + str(e.y()))
        self.mouse_point.move(e.x() - 16, e.y() - 16)
    """Here is our main body of codes for playing chess"""    
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.ai_down:
            x, y = e.x(), e.y()
            i, j = self.coordinate_transform_pixel2map(x, y)
            if self.isLegalCoordinates(i, j):
                self.applyCoordinates(i, j)
                if self.colorToPlayer[self.chesses.element()] == 'AI':
                    self.turnToAiPlayer()
            else:
                print("Move not legal")
        elif e.button() is not Qt.LeftButton:
            print("Left Button Please :-) ")
        else:
            print("Wait for AI move please :-> ")
#        if e.button() == Qt.LeftButton and self.ai_down == True:
#            x, y = e.x(), e.y()  # 鼠标坐标
#            self.i, self.j = self.coordinate_transform_pixel2map(x, y)  # 对应棋盘坐标
#            self.nowStep = (str(self.i)+','+str(self.j))
#            print("nowStep: ", self.nowStep)
#            self.mysignal.emit(self.nowStep)
#            self.draw(self.i, self.j)
######################################################   
    
    def isLegalCoordinates(self, i, j):
        location = [i, j]
        move = self.board.location_to_move(location)
        if move in self.board.availables:
            return True
        return False
    
    def applyCoordinates(self, i, j):
        move = self.board.location_to_move([i, j])
        self.board.do_move(move)
        self.draw(i, j)
        print("\nhuman move ends~")
        location = self.board.move_to_location(move)
        print("with location ", location)
        self.endTest()
        if self.colorToPlayer[self.chesses.element()] == 'AI':
            self.turnToAiPlayer()
    
    def turnToAiPlayer(self):
        move = self.AIPlayer.get_action(self.board)
        self.board.do_move(move)
        location = self.board.move_to_location(move)
        self.draw(location[0], location[1])
        print("\nAI move ends~")
        location = self.board.move_to_location(move)
        print("with location ", location)
        self.endTest()
        
    def endTest(self):
        end, winner = self.board.game_end()
        if end:
            QMessageBox.information(self,
                                    "游戏结束！",
                                    "胜利者为"+str(winner))

##############button for exiting######################   
    def button0Exit(self):
        button0 = QPushButton('关闭', self)
        button0.resize(button0.sizeHint())
        button0.move(30, 30)
        QToolTip.setFont(QFont('SansSerif', 30))
        button0.setToolTip('点击退出程序')
        button0.clicked.connect(self.button0Quit)    
    def button0Quit(self):
        sys.exit(0)
    # end of design of exiting button
###################################################### 
    """Place chesses in the chessboard"""
    def draw(self, i, j):
        x, y = self.coordinate_transform_map2pixel(i, j)
        self.pieces[self.step].setPixmap(self.chesses.element())
        self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)
        self.step+=1
        self.chesses.pointTurnRight()

        
    ################Cordinates Transformation################
    # self-defined functions offering transformation between 
    # pixel cordinates and 
    # relative grid cordinates
    
    def coordinate_transform_map2pixel(self, i, j):
        # 从 chessMap 里的逻辑坐标到 UI 上的绘制坐标的转换
        return MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int(round((y - MARGIN) / GRID)), int(round((x - MARGIN) / GRID))
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= 15 or j < 0 or j >= 15:
            return None, None
        else:
            return i, j
    #########################################################        

if __name__ == '__main__':
    from PyQt5 import QtWidgets
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance() 
    main = HumanWindow()
    main.show()
    sys.exit(app.exec_())

"""

if __name__ == '__main__':
    import sys, getopt

    height = 6
    width = 6
    n_in_row = 4
    use_gpu = False
    n_playout = 400
    model_file = "model/5_5_4_best_policy.model"
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
"""