## 连六棋的深度强化学习AI
### python 依赖
- numpy, pytorch0.4.0, PyQt5

### 使用方法
 - 实例 python ui.py -s 10 -r 6 -m 800 -i model/10_10_6_best_policy_3.model 是对战的命令,使用时可以修改选择的模型文件
 - 实例 python train.py -s 10 -r 6 -m 800 --graphics -n 2000 -i model/10_10_6_current_policy_.model 是模型的训练命令
 - 具体请运行 python human_play.py -h 或者 python train.py -h 寻找帮助

### 文件说明
- human_play.py 命令行界面中的人机对战实现
- ui.py 图形界面代码
- game.py 游戏和棋盘的实现
- mcts_pure.py 纯粹的蒙特卡洛搜索树
- mcts_pureZero.py 基于连六棋游戏风格的蒙特卡洛搜索树
- policy_value_net_pytorch.py 深度强化神经网络的实现
- train.py 神经网络训练
