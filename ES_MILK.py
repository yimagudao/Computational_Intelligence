# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 17:50:21 2018

@author: moulf
"""

import random
import math 

class ES() :
    def __init__(self,count):
        self.count = count
        self.population = self.gen_population(count)
    def gen_population(self,count):
        return [self.gen_chromosome() for i in range(count)]
    def gen_chromosome(self):
        chromosome = []
        chromosome.append(random.randint(0,64))
        chromosome.append(random.randint(0,64))
        chromosome.append(random.random())
        chromosome.append(random.random())
        return chromosome


if __name__ == '__main__':
    es = ES(10)
    