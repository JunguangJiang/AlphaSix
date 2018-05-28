# AlphaZero-Six
## 连六棋的深度强化学习AI
### 相对于AlphaZero-Gomoku(说明文档见下方）的改变
### 在写实验报告时可以参考的一些东西
- 文档还需要补充程序模块划分和功能说明、实验结果及分析、图形界面展示、参考文献，可以直接在latex中修改或者以word的形式发给我。
- 已有的实验结果在result文件夹中，其数值含义参见https://zhuanlan.zhihu.com/p/32089487
- 上述实验结果的绘制结果已放在Latex文件夹中
- 如何衡量机器的训练结果？一个是可以让ai和纯蒙特卡洛搜索树的ai对战，或者和alpha-beta剪枝的ai对战，测试比赛结果。另外一个可以是和人对战，记录棋局中的视频、截图，分析ai在训练后学会了什么下法。分析训练结果的优点和不足。对神经网络的选择、棋局表示的选择等提出建议。
- 上述内容只是建议。

### 使用方法
 - 实例 python human_play.py -s 10 -r 6 -m 800 -i model/10_10_6_best_policy_3.model 是对战的命令,使用时可以修改选择的模型文件
 - 实例 python train.py -s 10 -r 6 -m 800 --graphics -n 2000 -i model/10_10_6_current_policy_.model 是模型的训练命令
 - 具体请运行 python human_play.py -h 或者 python train.py -h 寻找帮助

#### 已经完成的部分
1. 提供了完善的命令行参数，方便神经网络训练时的调参
2. 游戏规则的改变：原先的五子棋（不论禁手不禁手都存在黑方必胜的问题），改成连六棋后，大大增加了公平性。
3. 改变原来的蒙特卡洛搜索树，使之适应每隔两个棋子改变一次玩家的游戏结构
4. 改变神经网络的状态输入
    - state依然由4个width x height的矩阵表示
    - 第一个矩阵表示所有我方的棋子
    - 第二个矩阵表示所有对方的棋子
    - 第三个矩阵表示对方在上一回合下的所有棋子
    - 第四个矩阵表示我方在该回合已经下的棋子
    - 由于改变了游戏规则，具体是谁先手已经不再重要，因此原先表示先后手的矩阵被移除
5. 实现了训练时模型的定期保存和重新训练时的载入
1. 动态绘制训练过程的损失和熵，具体见文件夹info中的数据，绘制效果可以参考https://zhuanlan.zhihu.com/p/32089487 中的结果图。这个任务非常简单，但是后面调参的时候会用到，DDL：5.4

#### 尚未完成的部分

2. 增加图形界面，要求如下
    - 在命令行中运行python human_play_window.py打开图形界面程序。上述命令提供和human_play.py相同的命令参数，具体参照human_play.py文件（这个文件请仔细阅读）DDL：12周周日晚
    - 一开始需要有一个开始按钮(可以放在菜单栏中），点击开始按钮后， 弹出一个对话框，让人类玩家选择谁先下棋。DDL：12周周日晚
    - 游戏的主界面背景为空白（不要加载任何图片！！！），由上述命令参数确定需要绘制的棋盘大小。DDL：12周周日晚
    - 在棋盘上接受用户的鼠标点击，得到下棋的位置 DDL：13周周日晚
    - 实现思路可以参照human_play.py以及Qt的信号与槽机制。
    
3. 15 x 15 下连六棋（感觉这个已经比较耗时间了，如果训练比较快，可以考虑增大模型）的模型训练，使用GPU训练模型（主要是之后要去实验室跑代码，需要理解目前我提供的命令行参数的意义）。
4. 游戏规则的完善：增加时间限制（这个任务可选，如果没有时间，可以放弃）

#### 文件说明
- human_play.py 命令行界面中的人机对战实现，实现图形界面必看！！！
- human_play_window.ui / human_play_window.py 图形界面代码
- game.py 游戏和棋盘的实现
- mcts_pure.py 纯粹的蒙特卡洛搜索树
- mcts_pureZero.py 基于连六棋游戏风格的蒙特卡洛搜索树
- policy_value_net_pytorch.py 深度强化神经网络的实现
- train.py 神经网络训练

## AlphaZero-Gomoku
This is an implementation of the AlphaZero algorithm for playing the simple board game Gomoku (also called Gobang or Five in a Row) from pure self-play training. The game Gomoku is much simpler than Go or chess, so that we can focus on the training scheme of AlphaZero and obtain a pretty good AI model on a single PC in a few hours. 

References:  
1. AlphaZero: Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm
2. AlphaGo Zero: Mastering the game of Go without human knowledge

### Update 2018.2.24: supports training with TensorFlow!
### Update 2018.1.17: supports training with PyTorch!

### Example Games Between Trained Models
- Each move with 400 MCTS playouts:  
![playout400](https://raw.githubusercontent.com/junxiaosong/AlphaZero_Gomoku/master/playout400.gif)

### Requirements
To play with the trained AI models, only need:
- Python >= 2.7
- Numpy >= 1.11

To train the AI model from scratch, further need, either:
- Theano >= 0.7 and Lasagne >= 0.1      
or
- PyTorch >= 0.2.0    
or
- TensorFlow

**PS**: if your Theano's version > 0.7, please follow this [issue](https://github.com/aigamedev/scikit-neuralnetwork/issues/235) to install Lasagne,  
otherwise, force pip to downgrade Theano to 0.7 ``pip install --upgrade theano==0.7.0``

If you would like to train the model using other DL frameworks, you only need to rewrite policy_value_net.py.

### Getting Started
To play with provided models, run the following script from the directory:  
```
python human_play.py  
```
You may modify human_play.py to try different provided models or the pure MCTS.

To train the AI model from scratch, with Theano and Lasagne, directly run:   
```
python train.py
```
With PyTorch or TensorFlow, first modify the file [train.py](https://github.com/junxiaosong/AlphaZero_Gomoku/blob/master/train.py), i.e., comment the line
```
from policy_value_net import PolicyValueNet  # Theano and Lasagne
```
and uncomment the line 
```
# from policy_value_net_pytorch import PolicyValueNet  # Pytorch
or
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
```
and then execute: ``python train.py``  (To use GPU in PyTorch, set ``use_gpu=True``)

The models (best_policy.model and current_policy.model) will be saved every a few updates (default 50).  

**Note:** the 4 provided models were trained using Theano/Lasagne, to use them with PyTorch, please refer to [issue 5](https://github.com/junxiaosong/AlphaZero_Gomoku/issues/5).

**Tips for training:**
1. It is good to start with a 6 * 6 board and 4 in a row. For this case, we may obtain a reasonably good model within 500~1000 self-play games in about 2 hours.
2. For the case of 8 * 8 board and 5 in a row, it may need 2000~3000 self-play games to get a good model, and it may take about 2 days on a single PC.

### Further reading
My article describing some details about the implementation in Chinese: [https://zhuanlan.zhihu.com/p/32089487](https://zhuanlan.zhihu.com/p/32089487) 
