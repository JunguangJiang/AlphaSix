# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
"""
Created on Thu May  3 21:01:13 2018

@author: chenyushao
"""

import sys, getopt
import matplotlib.pyplot as plt
import numpy as np
import time

def argmax(mylist):
    return mylist.index(max(mylist))
def argmin(mylist):
    return mylist.index(max(mylist))

def loadData(fileName):
    """
    global xmax
    global y1max
    global y2max
    global y1maxIndex
    global y2maxIndex
    """
    inFile = open(fileName, 'r')    #read-only way
    
    outFile = open("testOutFile", 'w')
    
    times = []
    loss = []
    entropy = []
    # references for easier and more explicit usage of variables
    x = times
    y1 = loss
    y2 = entropy

    count = 0
    for line in inFile:
        if line is '\n':
            continue
        
        count += 1
        trainingSet = line.split(',')
        if count == 1:
            continue
        xtemp = int(trainingSet[0])
        x.append(xtemp)
        y1temp = float(trainingSet[1])
        y1.append(y1temp)
        y2temp = float(trainingSet[2])
        y2.append(y2temp)
    inFile.close()
    outFile.close()
    return (x, y1, y2)

def plotData(x, y, s = 'Loss'):
    
    plt.figure(figsize=(20,5))
    # plt.title("Conclusion")
    plt.xlabel("训练局数")
    plt.ylabel(s)
    xrange = range(len(x))
    plt.plot(x, y, '-')
    plt.grid(True)
    plt.legend()
    
    plt.savefig(s+".pdf")
    
    plt.show()


def main(argv):
    inputfile = "info/10_10_6_loss_.txt"
    (x, y1, y2) = loadData(inputfile)
    plotData(x, y1, 'Loss')
    plotData(x, y2, 'Entropy')
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
    


