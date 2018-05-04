# -*- coding: utf-8 -*-
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
    """
    xmax = 0
    y1max = 0
    y2max = 0
    """
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
#        xmax = xtemp
        
        # test output
        """
        outFile.write(str(xtemp))
        outFile.write(' ')
        outFile.write(str(y1temp))
        outFile.write(' ')
        outFile.write(str(y2temp))
        outFile.write('\n')
        """
#        print(x[len(x) - 1], y1[len(y1) - 1], y2[len(y2) - 1])
    """
    y1num = [float(y1[i]) for i in range(len(y1))]
    y1max = max(y1num)
    y1maxIndex = argmax(y1num)
    y2num = [float(y2[i]) for i in range(len(y2))]
    y2max = max(y2num)
    y2maxIndex = argmax(y2num)
    """
    """
    print(y1max)
    print(y2max)
    """
    inFile.close()
    outFile.close()
    return (x, y1, y2)

def plotData(x, y, s = 'Loss'):
    
    plt.figure(figsize=(20,5))
    plt.title("Conclusion")
    plt.xlabel("Times of Self-Plays")
    plt.ylabel("Value of Loss and Entropy")
#    plt.xticks(np.linspace(0,xmax,10),(x))
    xrange = range(len(x))
#    yrange = np.linspace(0,max(y1max, y2max),10)
#    plt.yticks(yrange)
    plt.plot(xrange, y, '-', label = s)
    plt.grid(True)
    plt.legend()
    
    global order
    order += 1
    savename = time.strftime("%Y%m%d%H%M%S", time.localtime())
    plt.savefig(s + savename + str(order) + '.png')
    
    plt.show()
    
    
    return []

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('txt_plot.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    global order
    order = 0
    if inputfile is not '':
        (x, y1, y2) = loadData(inputfile)
        plotData(x, y1, 'Loss')
        plotData(x, y2, 'Entropy')
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
    


