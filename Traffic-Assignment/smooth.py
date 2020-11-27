'''
参考: https://github.com/AlanConstantine/ExponentialSmoothing
'''
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv

def expSmoothing(alpha, s):
    s2 = np.zeros(s.shape)
    s2[0] = s[0]
    for i in range(1, len(s2)):
        s2[i] = alpha*s[i]+(1-alpha)*s2[i-1]
    return s2

def computeError(original, pre):
    total_error = 0
    pre = pre[2:]
    # for i in range(1,len(original)-1):
    #     total_error = original[1] - pre[]
    # for item in original[1:]:
    #     for 
        
    print("original",original[1:])
    print("pre",pre[2:])

def showData(new_year, pre_year, s_pre_double, s_pre_triple, _id, name):
    # year, time_id, number = data.T
    df = pd.read_csv("data/%s.csv" % name)
    year = df["Year"].values
    number = df["Town%s"%_id].values

    plt.figure(figsize=(14, 6), dpi=80)
    plt.plot(year, number, color='blue', label="actual value")
    plt.plot(new_year[1:], s_pre_double[2:],
             color='red', label="double predicted value")
    plt.plot(new_year[1:], s_pre_triple[2:],
             color='green', label="triple predicted value")
    plt.legend(loc='lower right')
    plt.title('Total GDP')
    plt.xlabel('year')
    plt.ylabel('number')
    plt.xticks(new_year)
    # plt.colors()
    plt.show()


def smoothingFunc(alpha,_id,name):
    pre_year = np.array([i for i in range(2020,2036)])
    df = pd.read_csv("data/%s.csv" % name)
    year = df["Year"].values
    number = df["Town%s"%_id].values
    initial_number = np.insert(number, 0, values = [number[0]-(number[1]-number[0])])

    # 一次平滑/二次平滑
    s_single = expSmoothing(alpha, initial_number)
    s_double = expSmoothing(alpha, s_single)

    a_double = 2*s_single - s_double
    b_double = (alpha/(1-alpha))*(s_single-s_double)
    s_pre_double = np.zeros(s_double.shape)
    for i in range(1, len(initial_number)):
        s_pre_double[i] = a_double[i-1] + b_double[i-1]

    for i in range(1, 17):
        pre_next_year = a_double[-1] + b_double[-1]*i
        s_pre_double = np.insert(s_pre_double, len(s_pre_double), values=np.array(
            [pre_next_year]), axis=0)

    # 三次平滑指数
    s_triple = expSmoothing(alpha, s_double)

    a_triple = 3*s_single-3*s_double+s_triple
    b_triple = (alpha/(2*((1-alpha)**2)))*((6-5*alpha)*s_single -
                                           2*((5-4*alpha)*s_double)+(4-3*alpha)*s_triple)
    c_triple = ((alpha**2)/(2*((1-alpha)**2)))*(s_single-2*s_double+s_triple)

    s_pre_triple = np.zeros(s_triple.shape)

    for i in range(1, len(initial_number)):
        s_pre_triple[i] = a_triple[i-1] + b_triple[i-1]*1 + c_triple[i-1]*(1**2)

    for i in range(1, 17):
        pre_next_year = a_triple[-1] + b_triple[-1]*i + c_triple[-1]*(i**2)
        s_pre_triple = np.insert(s_pre_triple, len(s_pre_triple), values=np.array(
            [pre_next_year]), axis=0)

    new_year = np.insert(year, len(year), values = pre_year, axis=0)

    # computeError(initial_number, s_pre_double)
    # print(new_year)
    # print(s_pre_double)
    # print(s_pre_triple)
    print(s_pre_triple)
    if s_pre_triple[26] < number[9] and alpha != 0.3:
        return False

    return [s_pre_double[16],s_pre_double[26],s_pre_triple[16],s_pre_triple[26]]
    # showData(new_year, pre_year, s_pre_double, s_pre_triple, _id, name)



if __name__ == '__main__':
    names = ['GDP（亿元）', '工业总产值（亿元）', '全社会固定资产投资（亿元）', '人均可支配收入（元）']
    for name in names:
        with open("result/平滑预测-%s.csv" % name,"w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([["Town","double_2025","double_2035","triple_2025","triple_2035","alpha"]])
        alpha = 0.5
        for i in range(25):
        # for i in range(1):
            res = smoothingFunc(alpha,i,name)
            if res != False:
                [double_2025,double_2035,triple_2025,triple_2035] = res
                with open("result/平滑预测-%s.csv" % name,"a+") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows([[i,double_2025,double_2035,triple_2025,triple_2035,alpha]])
                continue
            alpha = 0.4
            res = smoothingFunc(alpha,i,name)
            if res != False:
                [double_2025,double_2035,triple_2025,triple_2035] = res
                with open("result/平滑预测-%s.csv" % name,"a+") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows([[i,double_2025,double_2035,triple_2025,triple_2035,alpha]])
                continue
            alpha = 0.3
            res = smoothingFunc(alpha,i,name)
            [double_2025,double_2035,triple_2025,triple_2035] = res
            if res != False:
                [double_2025,double_2035,triple_2025,triple_2035] = res
                with open("result/平滑预测-%s.csv" % name,"a+") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows([[i,double_2025,double_2035,triple_2025,triple_2035,alpha]])
                continue
            alpha = 0.2
            res = smoothingFunc(alpha,i,name)
            [double_2025,double_2035,triple_2025,triple_2035] = res
            with open("result/平滑预测-%s.csv" % name,"a+") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows([[i,double_2025,double_2035,triple_2025,triple_2035,alpha]])

