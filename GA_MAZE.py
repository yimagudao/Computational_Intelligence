# -*- coding: utf-8 -*-
"""
Created on Wed May 30 08:29:16 2018

@author: moulf
"""

import pandas as pd
import numpy as np
import math
import random

class GA():
    MAZE_ENTRANCE_POS = 1
    MAZE_EXIT_POS = 2
    MAZE_DIRECTION_CODE =  [ [ 0, 0 ], [ 0, 1 ], [ 1, 0 ], [ 1, 1 ]]
    MAZE_DIRECTION_CHANGE =  [ [ -1, 0 ], [ 1, 0 ], [ 0, -1 ], [ 0, 1] ]
    MAZE_DIRECTION_LABEL =  [ "上", "下", "左", "右" ]
    startPos = [0,0]
    endPos = [0,0]
    stepNum = 1000
    initSets = []
    def __init__(self, filePath,initSetsNum):
        self.filePath = filePath 
        self.initSetsNum = initSetsNum
        self.mazeData = np.array(pd.read_csv(filePath,encoding = 'utf-8', sep=',',header=None))
        self.findPos(self.mazeData)
        self.gen_population(initSetsNum)
    
    # 找出入口位置和出口位置
    def findPos(self,mazeData):
        for i in range(len(mazeData)):
            for j in range(len(mazeData)):
                if mazeData[i][j] == GA.MAZE_ENTRANCE_POS :
                    GA.startPos[0] = i
                    GA.startPos[1] = j
                if mazeData[i][j] == GA.MAZE_EXIT_POS :
                    GA.endPos[0] = i
                    GA.endPos[1] = j
        #走出迷宫最短步数
        GA.stepNum = abs(GA.startPos[0] - GA.endPos[0]) + abs(GA.startPos[1] - GA.endPos[1])
    
    #产生初始数据集
    def gen_population(self,initSetsNum):
        for i in range(initSetsNum):
            GA.initSets.append(self.produceInitSet())
        
    
    def produceInitSet(self):
        # 方向编码
        directionCode = 0
        codeNum = [0]*GA.stepNum*2
        for j in range(GA.stepNum):
           directionCode = random.randint(0,3)
           codeNum[2 * j] = GA.MAZE_DIRECTION_CODE[directionCode][0]
           codeNum[2 * j + 1] = GA.MAZE_DIRECTION_CODE[directionCode][1]
        return codeNum
    
    #二进制数组转化为数字
    def binaryArrayToNum(self,binaryArray):
        result = 0
        k = 0
        for i in range(len(binaryArray)-1,-1,-1):
            if binaryArray[i] == 1:
                result += math.pow(2,k)
            k += 1
        return result
    
    #判断当前编码能否走出迷宫
    def ifArriveEndPos(self, code):
        isArrived = False
        #终点坐标
        endX = 0
        endY = 0
        #行走方向
        direction = 0
        #临时坐标
        tempX = 0
        tempY = 0
        
        endX = GA.startPos[0]
        endY = GA.startPos[1]
        for i in range(GA.stepNum):
            direction =int( self.binaryArrayToNum([code[2*i],code[2*i+1]]))
            
            #根据运动方向，改变坐标
            tempX = endX + GA.MAZE_DIRECTION_CHANGE[direction][0]
            tempY = endY + GA.MAZE_DIRECTION_CHANGE[direction][1]
            
            #判断坐标是否越界
            if tempX >= 0 and tempX < len(self.mazeData) and tempY >= 0 and tempY < len(self.mazeData) :
                # 障碍
                if self.mazeData[tempX][tempY] != -1 :
                    endX = tempX
                    endY = tempY
        
        if endX == GA.endPos[0] and endY == GA.endPos[1] :
            isArrived = True
        
        return isArrived
    
    #计算适应度
    def calFiteness(self, code):
        fintness = 0
        #行走的终点坐标
        endX = 0
        endY = 0
        #行走方向
        direction = 0
        #临时坐标
        tempX = 0
        tempY = 0
        
        endX = GA.startPos[0]
        endY = GA.startPos[1]
        for i in range(GA.stepNum):
            direction = int(self.binaryArrayToNum([code[2*i],code[2*i+1]]))
            
            #根据运动方向，改变坐标
            tempX = endX + GA.MAZE_DIRECTION_CHANGE[direction][0]
            tempY = endY + GA.MAZE_DIRECTION_CHANGE[direction][1]
            
            #判断坐标是否越界
            if tempX >= 0 and tempX < len(self.mazeData) and tempY >= 0 and tempY < len(self.mazeData) :
                # 障碍
                if self.mazeData[tempX][tempY] != -1 :
                    endX = tempX
                    endY = tempY
        # 计算适应度
        fintness = 1.0/(abs(endX-GA.endPos[0])+abs(endY-GA.endPos[1])+1)
        return fintness
        
    
    # 遗传算法，选择操作 轮盘赌选择方法
    def selectOperate(self , initCodes):
        randomNum = 0
        sumFitness = 0
        resulCodes = []
        adaptiveValue = [0] * self.initSetsNum
        
        for i in range(self.initSetsNum) :
            adaptiveValue[i] = self.calFiteness(initCodes[i])
            sumFitness += adaptiveValue[i]
        for i in range(self.initSetsNum) :
            adaptiveValue[i] = adaptiveValue[i]/sumFitness
        for i in range(self.initSetsNum) :
            randomNum = random.randint(1,100)
            randomNum = randomNum / 100
            if randomNum == 1:
                randomNum = randomNum -0.01
            sumFitness = 0
            # 轮盘赌选确定区间
            for j in range(self.initSetsNum) :
                if randomNum >sumFitness and randomNum <= sumFitness + adaptiveValue[j] :
                    resulCodes.append(initCodes[j].copy())
                    break
                else :
                    sumFitness += adaptiveValue[j]
        return resulCodes
    
    # 遗传算法交叉
    def crossOperate(self,selectedCodes):
#        randomNum = 0
#        crossPoint = 0
        resultCodes = []
        randomCodeSeqs = []
        while len(selectedCodes) > 0 :
            randomNum = random.randint(0,len(selectedCodes)-1)
            randomCodeSeqs.append(selectedCodes[randomNum])
            del selectedCodes[randomNum]
        
        array1 = []
        array2 = []
        for i in range(len(randomCodeSeqs)) :
            if i % 2 ==1 :
                array1 = randomCodeSeqs[i-1]
                array2 = randomCodeSeqs[i]
                crossPoint = random.randint(0,2*GA.stepNum)
                # 交叉点后双亲编码位置互换
                for j in range(2*GA.stepNum) :
                    if j >= crossPoint :
                        array1[j] ,array2[j] = array2[j],array1[j]
                resultCodes.append(array1)
                resultCodes.append(array2)
        return resultCodes
    
    #遗传算法变异
    def mutationOpetate(self,crossCodes):
#        mutationPoint = 0;
        resultCodes = []
        for array in crossCodes:
            mutationPoint = random.randint(0,2*GA.stepNum-1)
            array[mutationPoint] =(0 if array[mutationPoint] == 1 else 1)
            resultCodes.append(array)
        return resultCodes

    #执行遗传算法走出迷宫
    def evolve(self):
        loopCount = 0;
        canExit = False;
        resultCode = []
#        initCodes = []
#        selectedCodes = []
#        crossedCodes = []
#        mutationCodes = []
        initCodes = GA.initSets
        while(True):
            for array in initCodes :
                if self.ifArriveEndPos(array):
                    resultCode = array
                    canExit = True
                    break
            if canExit :
                break
            selectedCodes = self.selectOperate(initCodes)
            crossedCodes = self.crossOperate(selectedCodes)
            mutationCodes = self.mutationOpetate(crossedCodes)
            initCodes = mutationCodes
            
            loopCount += 1
            if loopCount >= 100 :
                break;
            
        print('一共进行了%d 次进化'%loopCount)
        #print(resultCode)
        self.printFindedRoute(resultCode)
    
    #输出路径
    def printFindedRoute(self ,code):
        if code == None :
            print('在有限的进化内，没找到最优路径')
            return
        #行走方向
        direction = 0
        #临时坐标
        tempX = GA.startPos[0]
        tempY = GA.startPos[1]
        print('起点（%d,%d）,终点（%d,%d）'%(GA.startPos[0],GA.startPos[1],GA.endPos[0],GA.endPos[1]))
        print('路径编码为：')
        for x in code:
            print(x,end='')
        print()
        for i in range(GA.stepNum):
            direction = int(self.binaryArrayToNum([code[2*i],code[2*i+1]]))
            
            #根据运动方向，改变坐标
            tempX += GA.MAZE_DIRECTION_CHANGE[direction][0]
            tempY += GA.MAZE_DIRECTION_CHANGE[direction][1]
            
            print('第%d步，编码为%d%d,向%s移动，移动后到达(%d,%d)'%(i,code[2*i],code[2*i+1],GA.MAZE_DIRECTION_LABEL[direction],tempX,tempY))
      

if __name__ == '__main__':
    filePath = 'mapData.txt'
    initSetsNum = 10
    ga = GA(filePath,initSetsNum)
    data = ga.mazeData
    ga.evolve()