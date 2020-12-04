#!/usr/bin/env python3
import xlrd
import csv
import math
import pandas as pd
import numpy as np
from pandas import read_csv
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
import pylab as pl
import statsmodels.api as sm


def dataProcess():
    '''获得人口数据并输出'''
    ALL_DATA = xlrd.open_workbook("data/城镇基础数据.xlsx")
    ALL_CITY_TABLE = ALL_DATA.sheets()[0]
    for i in range(0,25):
        # 初始化文件
        line_name = ['GDP（亿元）', '工业总产值（亿元）', '全社会固定资产投资（亿元）', '人均可支配收入(元)', '户籍人口（万人）', '在岗人数(万人)', '全方式旅客发送量(万人次)', '全方式旅客吸引量(万人次)']
        if i == 0:
            for name in line_name:
                with open("data/%s.csv"%name,"w") as csvfile:
                    writer = csv.writer(csvfile)
                    row = ["Num"] + ["%s"%j for j in range(2010,2020)]
                    writer.writerows([row])
        # 10年+3行
        for k in range(len(line_name)):
            value = []
            for j in range(0,10):
                row = ALL_CITY_TABLE.row_values(j + i*13 + 3)
                value.append(row[k])
            with open("data/%s.csv"%line_name[k],"a+") as csvfile:
                writer = csv.writer(csvfile)
                target = ["%s"%(i+1)] + value
                writer.writerows([target])

def dataProcessLine():
    '''获得人口数据并输出（横列）'''
    ALL_DATA = xlrd.open_workbook("data/城镇基础数据.xlsx")
    ALL_CITY_TABLE = ALL_DATA.sheets()[0]
    line_name = ['GDP（亿元）', '工业总产值（亿元）', '全社会固定资产投资（亿元）', '人均可支配收入（元）', '户籍人口（万人）', '在岗人数（万人）', '全方式旅客发送量（万人次）', '全方式旅客吸引量（万人次）']
    for i, file_name in enumerate(line_name):
        with open("data/%s.csv" % file_name,"w") as csvfile:
            writer = csv.writer(csvfile)
            first_row = ["Year"] + ["Town%s" % _ for _ in range(25)]
            writer.writerows([first_row])

        all_years = [j for j in range(2010,2020)]
        for j, year in enumerate(all_years):
            value = [year]
            for k in range(25):
                row = ALL_CITY_TABLE.row_values(k * 13 + j + 3)
                value.append(row[i + 1])
            with open("data/%s.csv" % file_name,"a+") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows([value])

def predictPeople():
    names = ["户籍人口（万人）","在岗人数（万人）"]
    for name in names:
        linePrediction(name)
    for name in names:
        exponentPrediction(name)

def linePrediction(name):
    '''线性预测模型'''
    file_name = "data/%s.csv" % name
    data = pd.read_csv(file_name)
    lrModel = LinearRegression()
    x = data[['Year']]
    with open("result/线性预测-%s.csv" % name,"w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["Town","a","b","2025","2035"]])
    for i in range(25):
        y = data[['Town%s'%i]]
        lrModel.fit(x,y)
        lrModel.score(x,y)
        prediction = lrModel.predict([[2025],[2035]])
        res = lrModel.predict([[2025],[2035]])
        a = lrModel.intercept_[0]
        b = lrModel.coef_[0][0]
        with open("result/线性预测-%s.csv" % name,"a+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[i,a,b,"%0.2f"%res[0][0],"%0.2f"%res[1][0]]])

    # plt.plot(x, y, "b")
    # plt.plot(x, a + b*x, "r")
    # plt.show()

def exponentFunc(x, a, b):
    return b * (1 + a)**(x - 2010)

def exponentPrediction(name):
    '''指数预测模型'''
    data = pd.read_csv("data/%s.csv" % name)
    x = data[['Year']].values.T[0]
    with open("result/指数预测-%s.csv" % name,"w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["Town","a","b","2025","2035"]])
    for i in range(25):
        y = data[['Town%s'%i]].values.T[0]
        [a,b], pcov = curve_fit(exponentFunc, x, y)
        with open("result/指数预测-%s.csv" % name,"a+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[i,a,b,"%0.2f"%exponentFunc(2025,a,b),"%0.2f"%exponentFunc(2035,a,b)]])

    # y1 = exponentFunc(x, a, b)
    # plt.plot(x, y, "b")
    # plt.plot(x, y1, "r")
    # plt.show()

def demandOfRail():
    df = pd.read_csv("data/铁路占比.csv")
    # print(df)
    # print(df.describe())
    # print(pd.crosstab(df["C1"],df["C2"],df["C3"],rownames=["ratio"]))
    print(df[df.columns[3:7]])
    logit = sm.Logit(df["ratio"],df[df.columns[3:7]])
    res = logit.fit()
    print(res.summary())

def demandFit():
    data = pd.read_csv("data/铁路占比-二项.csv")
    lrModel = LinearRegression()
    x = data[['C1-C3']]
    y = data[['ratio_ad']]
    lrModel.fit(x,y)
    lrModel.score(x,y)
    # prediction = lrModel.predict([[2025],[2035]])
    # print(prediction)
    # res = lrModel.predict([[2025],[2035]])
    k = lrModel.coef_[0][0]
    b = lrModel.intercept_[0]
    # print(k,b)
    # plt.plot(x, y, "b")
    # plt.plot(x, b + k*x, "r")
    # plt.show()
    distance = pd.read_csv("data/距离.csv")
    with open("result/OD铁路需求比例.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["Num"]+[i for i in range(1,26)]])
        for i in range(0,25):
            res = [i+1]
            for j in range(1,26):
                if i+1 == j:
                    res.append(0)
                    continue
                d = distance["%s"%j][i]
                res.append("%0.2f"%(1/(1+math.exp(-k*0.1017*d+b))))
            writer.writerows([res])

    ratio = pd.read_csv("result/OD铁路需求比例.csv")
    demand_2025 = pd.read_csv("result/2025_ODs.csv")
    demand_2035 = pd.read_csv("result/2035_ODs.csv")

    with open("result/铁路2025.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["Num"]+[i for i in range(1,26)]])
    with open("result/铁路2035.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["Num"]+[i for i in range(1,26)]])

    for i in range(0,25):
        res_2025 = [i+1]
        res_2035 = [i+1]
        for j in range(1,26):
            res_2025.append("%0.2f"%(ratio["%s"%j][i]*demand_2025["%s"%j][i]))
            res_2035.append("%0.2f"%(ratio["%s"%j][i]*demand_2035["%s"%j][i]))
        with open("result/铁路2025.csv","a+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([res_2025])
        with open("result/铁路2035.csv","a+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([res_2035])



if __name__ == "__main__":
    # print("success")
    # dataProcess()
    # dataProcessLine()
    # predictPeople()
    # exponentPrediction()
    # demandOfRail()
    demandFit()
