import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import csv
from pandas import DataFrame,Series
# from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def corrGust():
    coor_names = ['GDP（亿元）', '工业总产值（亿元）', '全社会固定资产投资（亿元）', '人均可支配收入（元）', '户籍人口（万人）', '在岗人数（万人）']
    demand_names = ['全方式旅客发送量（万人次）', '全方式旅客吸引量（万人次）']
    demand0_df = pd.read_csv("data/%s.csv"%demand_names[0])
    demand1_df = pd.read_csv("data/%s.csv"%demand_names[1])
    for coor_name in coor_names:
        coor_df = pd.read_csv("data/%s.csv"%coor_name)
        all_corr_gust1,all_corr_gust2 = [],[]
        for i in range(25):
            coor_data = coor_df["Town%s"%i]
            all_corr_gust1.append(demand0_df["Town%s"%i].corr(coor_data))
            all_corr_gust2.append(demand1_df["Town%s"%i].corr(coor_data))

            # if coor_name == "人均可支配收入（元）" and i < 3:
            #     plt.scatter(demand, coor_data)
            #     plt.title('corr_gust :' + str(demand.corr(coor_data)), fontproperties='SimHei') #给图写上title
            #     plt.show()
        total = 0
        for item in all_corr_gust1:
            total = total + item
        print("%0.4f" % (total/25))

        total = 0
        for item in all_corr_gust2:
            total = total + item
        print("%0.4f" % (total/25))

def newPlot():
    data_ori = pd.read_csv("data/人均可支配收入（元）.csv")
    print(data_ori)
    sns.set_theme(color_codes = True)
    sns.jointplot(x = "Year", y = "Town0", data = data_ori, kind="reg")
    plt.show()

def multiplePlot():
    coor_names = ['GDP（亿元）', '工业总产值（亿元）', '全社会固定资产投资（亿元）', '人均可支配收入（元）', '户籍人口（万人）', '在岗人数（万人）']
    coor_names_en = ['GDP', 'Industry', 'Investment', 'Income', 'Household', 'On Job']
    demand_names = ['全方式旅客发送量（万人次）', '全方式旅客吸引量（万人次）']
    demand0_df = pd.read_csv("data/%s.csv"%demand_names[0])
    demand1_df = pd.read_csv("data/%s.csv"%demand_names[1])
    for i in range(25):
        demand = demand0_df["Town%s"%i] + demand1_df["Town%s"%i]
        reg_data = pd.DataFrame(demand)
        reg_data["Demand"] = demand
        for j in range(len(coor_names)):
            coor_df = pd.read_csv("data/%s.csv"%coor_names[j])
            reg_data[coor_names_en[j]] = coor_df["Town%s"%i]
            # print(reg_data[coor_names_en[j]])

        g = sns.PairGrid(reg_data, y_vars=["Demand"], x_vars = ['GDP', 'Industry', 'Investment'], height=5)
        # g = sns.PairGrid(reg_data, y_vars=["Demand"], x_vars = ['Income', 'Household', 'On Job'], height=5)
        g.map(sns.regplot, color=".3",  x_jitter=.1)
        g.add_legend()
        # g.set(ylim=(-1, 11), yticks=[0, 5, 10])
        
        # print(reg_data["Investment"])
        # sns.pairplot(reg_data, x_vars=['GDP', 'Industry', 'Investment'], y_vars="Demand", kind = 'reg')
        # sns.pairplot(reg_data, x_vars=['Income', 'Household', 'On Job'], y_vars="Demand", kind = 'reg')
        plt.show()


def multipleRegression():
    coor_names = ['GDP（亿元）', '工业总产值（亿元）', '全社会固定资产投资（亿元）', '人均可支配收入（元）', '户籍人口（万人）', '在岗人数（万人）']
    coor_names_en = ['GDP', 'Industry', 'Investment', 'Income', 'Household', 'On Job']
    demand_names = ['全方式旅客发送量（万人次）', '全方式旅客吸引量（万人次）']
    demand0_df = pd.read_csv("data/%s.csv"%demand_names[0])
    demand1_df = pd.read_csv("data/%s.csv"%demand_names[1])
    with open("result/需求和吸引量预测.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows([["ID","2025 Generate","2025 Attract","2035 Generate","2035 Attract"]])
    for i in range(25):
        demand = demand0_df["Town%s"%i] + demand1_df["Town%s"%i]
        reg_data = pd.DataFrame(demand)
        reg_data["Demand0"] = demand0_df["Town%s"%i]
        reg_data["Demand1"] = demand1_df["Town%s"%i]
        for j in range(len(coor_names)):
            coor_df = pd.read_csv("data/%s.csv"%coor_names[j])
            reg_data[coor_names_en[j]] = coor_df["Town%s"%i]
        
        X = reg_data.loc[:,('Investment', 'Income', 'Household')]
        # X = reg_data.loc[:,('GDP', 'Industry', 'Investment', 'Income', 'Household', 'On Job')]
        Y0 = reg_data.loc[:,'Demand0'] # 产生量
        Y1 = reg_data.loc[:,'Demand1'] # 吸引量


        GDP_df = pd.read_csv("result/平滑预测-GDP（亿元）.csv")
        Industry_df = pd.read_csv("result/平滑预测-工业总产值（亿元）.csv")
        Investment_df = pd.read_csv("result/平滑预测-全社会固定资产投资（亿元）.csv")
        Income_df = pd.read_csv("result/平滑预测-人均可支配收入（元）.csv")
        Household_df = pd.read_csv("result/线性预测-户籍人口（万人）.csv")
        OnJob_df = pd.read_csv("result/线性预测-在岗人数（万人）.csv")

        linreg = LinearRegression() 
        model = linreg.fit(X, Y0)
        a,b,c = linreg.coef_
        k = linreg.intercept_

        generate_2025 = a*Investment_df["triple_2025"][i] + b*Income_df["triple_2025"][i] + \
            c*Household_df["2025"][i] + k
        generate_2035 = a*Investment_df["triple_2035"][i] + b*Income_df["triple_2035"][i] + \
            c*Household_df["2035"][i] + k
        # generate_2025 = a*GDP_df["triple_2025"][i] + b*Industry_df["triple_2025"][i] + \
        #     c*Investment_df["triple_2025"][i] + d*Income_df["triple_2025"][i] + \
        #         e*Household_df["2025"][i]+ f*OnJob_df["2025"][i] + k
        # generate_2035 = a*GDP_df["triple_2035"][i] + b*Industry_df["triple_2035"][i] + \
        #     c*Investment_df["triple_2035"][i] + d*Income_df["triple_2035"][i] + \
        #         e*Household_df["2035"][i]+ f*OnJob_df["2035"][i] + k

        linreg = LinearRegression() 
        model = linreg.fit(X, Y1)
        # a,b,c,d,e,f = linreg.coef_
        a,b,c= linreg.coef_
        k = linreg.intercept_

        attract_2025 = a*Investment_df["triple_2025"][i] + b*Income_df["triple_2025"][i] + \
            c*Household_df["2025"][i] + k
        attract_2035 = a*Investment_df["triple_2035"][i] + b*Income_df["triple_2035"][i] + \
            c*Household_df["2035"][i] + k

        with open("result/需求和吸引量预测.csv","a+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[i,generate_2025,attract_2025,generate_2035,attract_2035]])


if __name__ == '__main__':
    # corrGust()
    multipleRegression()
    
