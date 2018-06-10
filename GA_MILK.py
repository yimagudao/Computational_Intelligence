# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 10:40:49 2018

@author: moulf
"""

import math
import random

class GA():
    def __init__(self, length, count,mutation_rate=0.5):
        # 染色体长度
        self.length = length
        # 种群中的染色体数量
        self.count = count
        #变异概率
        self.mutation_rate = mutation_rate
        # 随机生成初始种群
        self.population = self.gen_population(length, count)

    def evolve(self):
        """
        进化
        对当前一代种群依次进行选择、交叉并生成新一代种群，然后对新一代种群进行变异
        """
        parents = self.selection()
        self.crossover(parents)
        self.mutation()

    def gen_chromosome(self, length):
        """
        随机生成长度为length的染色体，每个基因的取值是0或1
        这里用一个字符表示一个基因
        """
        chromosome = ''
        for i in range(length):
            chromosome =chromosome + str(random.randint(0, 1))
        return chromosome

    def gen_population(self, length, count):
        """
        获取初始种群（一个含有count个长度为length的染色体的列表）
        """
        return [self.gen_chromosome(length) for i in range(count)]

        #二进制字符串转化为数字
    def binaryArrayToNum(self,binaryArray):
        """
        二进制字符串转化为数字
        """
        result = 0
        k = 0
        length = len(binaryArray)
        for i in range(length):
            if binaryArray[length-i-1] == '1':
                result += math.pow(2,k)
            k += 1
        return result
    
    def fitness(self, chromosome):
        """
        计算适应度，将染色体解码为0~9之间数字，代入函数计算
        因为是求最大值，所以数值越大，适应度越高
        """
        result = 0
        mid  = int(self.length/2)
        str1 = chromosome[0:mid]
        str2 = chromosome[mid:]
        x1 = self.binaryArrayToNum(str1)
        x2 = self.binaryArrayToNum(str2)
        if  (x1+x2) <= 64 :
            if (12*x1 + 8* x2 < 600) :
                result = 24*3*x1 +16*4*x2
        return result
    # 选择
    def selection(self):
        """
        选择
        """
        randomNum = 0
        sumFitness = 0
        resulCodes = []
        adaptiveValue = [0] * self.count
        for i in range(self.count) :
            #每个基因的适应度值和种群的总适应度值
            adaptiveValue[i] = self.fitness(self.population[i])
            sumFitness += adaptiveValue[i]
        for i in range(self.count) :
            #每个个体的适应度概率
            adaptiveValue[i] = adaptiveValue[i] /sumFitness
        for i in range(self.count):
            #产生随机概率
            randomNum = random.randint(1,99)
            randomNum = randomNum /100
            sumFitness = 0
            # 轮盘赌选确定区间
            for j in range(len(self.population)):
                if randomNum >sumFitness and randomNum <= sumFitness + adaptiveValue[j] :
                    resulCodes.append(self.population[j])
                    self.population.pop(j)
                    break
                else :
                    sumFitness += adaptiveValue[j]
        return resulCodes
    #遗传算法交叉
    def crossover(self,parents) :
        """
        染色体交叉，繁衍，生成下一代种群
        """
        #新出生的孩子，最终回被加入存活下来的父母之中，形成新一代的种群
        children = []
        # 需要新产生的孩子量
        target_count = self.count - len(parents)
        # 繁殖
        while len(children) < target_count :
            male = random.randint(0,len(parents)-1)
            female = random.randint(0,len(parents)-1)
            if male != female :
                #随机选取交叉点
                cross_pos = random.randint(0,self.length)
                male  = parents[male]
                female = parents[female]
                child = male[0:cross_pos] + female[cross_pos:]
                children.append(child)
        #经过繁殖之后，孩子和父母的数量与原始种群数量相等
        #更新种群
        self.population = parents +children
    def mutation(self):
        """
        变异
        对种群中的所有个体，根据变异概率随机改变个体中的某个基因
        """
        
        for i in range(len(self.population)):
            if random.random() < self.mutation_rate :
                mutationPoint = random.randint(0,self.length-1)
                newcode = list(self.population[i])
                newcode[mutationPoint] = ('0' if newcode[mutationPoint]=='1' else '1')
                self.population[i] = ''.join(newcode)
    
    def result(self) :
        """
        获得当前代的最优值，这里取得是每天利益最大值时的编码
        """
        max = 0
        lastCode = ''
        for chromosome in ga.population:
            if self.fitness(chromosome) > max:
                max = self.fitness(chromosome)
                lastCode = chromosome
        print('每天获得最大利益为:%d,获得最大利益时基因编码为:%s'%(max,lastCode))
        str1 = lastCode[0:6]
        str2 = lastCode[6:]
        x1 = self.binaryArrayToNum(str1)
        x2 = self.binaryArrayToNum(str2)
        print('x1的值为:%d,x2的值为:%d'%(x1,x2))
        
if __name__ == '__main__':
    # 染色体长度为12， 种群数量为200
    ga = GA(12, 200)
    # 200次进化迭代
    for x in range(150):
         ga.evolve()
         print('第%d次进化：'%(x))
         ga.result()
