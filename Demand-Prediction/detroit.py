import xlrd
import csv
import math
import pandas as pd
import numpy as np
from pandas import read_csv
from copy import deepcopy

def Detroit():
    ALL_DATA = xlrd.open_workbook("data/城镇基础数据.xlsx")
    ALL_CITY_TABLE = ALL_DATA.sheets()[2]
    town_to_town = []
    for i in range(25):
        town_to_town.append([])
        row = ALL_CITY_TABLE.row_values(i+2)
        for j in range(25):
            town_to_town[i].append(row[j+1])
    # print(town_to_town)
    last_town_to_town = deepcopy(town_to_town)
    
    demands = pd.read_csv("result/需求和吸引量预测.csv")
    O_2025,D_2025 = [],[]
    for i in range(demands.shape[0]):
        O_2025.append(demands["2025 Generate"][i])
        D_2025.append(demands["2025 Attract"][i])

    alpha,last_alpha= [1 for i in range(25)],[1 for i in range(25)]
    beta,last_beta = [1 for i in range(25)],[1 for i in range(25)]
    F,last_F = 1,1
    change_val = 1000
    iterated_times = 0
    # while change_val > 1:
    while change_val > 0.000001:
        for i in range(25):
            alpha[i] = O_2025[i]/getSumO(i,town_to_town)
            beta[i] = D_2025[i]/getSumD(i,town_to_town)
        F = sum(O_2025)/getAll(town_to_town)
        for i in range(25):
            for j in range(25):
                # O i D j
                town_to_town[j][i] = last_town_to_town[j][i] * alpha[i] * alpha[j] / F
        
        change_val = abs(F-last_F) + getChange(last_alpha,alpha) + getChange(last_beta,beta)
        last_F = F
        last_alpha = deepcopy(alpha)
        last_beta = deepcopy(beta)
        last_town_to_town = deepcopy(town_to_town)

        iterated_times = iterated_times + 1

        print(change_val)
    print(iterated_times)
    
    with open("data/2025_ODs.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["OD"]+[_ for _ in range(25)]])
        for i in range(25):
            val = ["%0.1f"%item for item in town_to_town[i]]
            writer.writerows([[i] + val])

def Detroit35():
    ALL_DATA = xlrd.open_workbook("data/城镇基础数据.xlsx")
    ALL_CITY_TABLE = ALL_DATA.sheets()[2]
    town_to_town = []
    for i in range(25):
        town_to_town.append([])
        row = ALL_CITY_TABLE.row_values(i+2)
        for j in range(25):
            town_to_town[i].append(row[j+1])
    # print(town_to_town)
    last_town_to_town = deepcopy(town_to_town)
    
    demands = pd.read_csv("result/需求和吸引量预测.csv")
    O_2035,D_2035 = [],[]
    for i in range(demands.shape[0]):
        O_2035.append(demands["2035 Generate"][i])
        D_2035.append(demands["2035 Attract"][i])

    alpha,last_alpha= [1 for i in range(25)],[1 for i in range(25)]
    beta,last_beta = [1 for i in range(25)],[1 for i in range(25)]
    F,last_F = 1,1
    change_val = 1000
    iterated_times = 0
    # while change_val > 1:
    while change_val > 0.000001:
        for i in range(25):
            alpha[i] = O_2035[i]/getSumO(i,town_to_town)
            beta[i] = D_2035[i]/getSumD(i,town_to_town)
        F = sum(O_2035)/getAll(town_to_town)
        for i in range(25):
            for j in range(25):
                # O i D j
                town_to_town[j][i] = last_town_to_town[j][i] * alpha[i] * alpha[j] / F
        
        change_val = abs(F-last_F) + getChange(last_alpha,alpha) + getChange(last_beta,beta)
        last_F = F
        last_alpha = deepcopy(alpha)
        last_beta = deepcopy(beta)
        last_town_to_town = deepcopy(town_to_town)

        iterated_times = iterated_times + 1

        print(change_val)

    print(iterated_times)
    with open("data/2035_ODs.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["OD"]+[_ for _ in range(25)]])
        for i in range(25):
            val = ["%0.1f"%item for item in town_to_town[i]]
            writer.writerows([[i] + val])

def getChange(last_arr,_arr):
    change_val = 0
    for i in range(len(_arr)):
        change_val = change_val + abs(_arr[i] - last_arr[i])
    return change_val

def getSumD(i,town_to_town):
    _sum = 0
    for j in range(25):
        _sum = _sum + town_to_town[j][i]
    return _sum

def getSumO(i,town_to_town):
    return sum(town_to_town[i])

def getAll(town_to_town):
    _sum = 0
    for j in range(25):
        _sum = _sum + sum(town_to_town[j])
    return _sum

if __name__ == '__main__':
    Detroit()
    Detroit35()
