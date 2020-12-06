import pandas as pd
import csv
from line_search import LineSearch
from copy import deepcopy
import numpy as np

def getID(i,j):
    return "%05d%05d"%(i,j)

def loadFlow():
    '''加载整个的'''
    flow = {}
    with open("User-Equilibrium-Project&Line-Search/SiousFalls/flow.txt", "r") as f:  # 打开文件
        data = f.readlines()  # 读取文件
        for i in range(0,24):
            all_lines = ""
            for j in range(5):
                all_lines = all_lines + data[i*7 + j + 1].replace("\n","").replace(" ","")
            j = 0
            for item in all_lines.split(";"):
                split_res = item.split(":")
                if len(split_res) > 1:
                    flow[getID(i+1,j+1)] = float(split_res[1])
                    j = j + 1
    return flow

def loadNetwork():
    '''加载网络'''
    df = pd.read_csv("User-Equilibrium-Project&Line-Search/SiousFalls/network.csv")
    vertexes = {}
    for i in range(1,25):
        vertexes[i] = {
            "id":i,
            "sub_arc":[]
        }
    edges = {}
    for i in range(df.shape[0]):
        _id = getID(df["init_node"][i],df["term_node"][i])
        vertexes[df["init_node"][i]]["sub_arc"].append(_id)
        edges[_id] = {
            "front_ver":df["init_node"][i],
            "tail_ver":df["term_node"][i],
            "capacity":df["capacity"][i],
            "length":df["length"][i],
            "free_flow_time":df["free_flow_time"][i],
            "flow_time":df["free_flow_time"][i],
            "current_flow":0
        }
    return vertexes,edges


ALL_VERTEXES,ALL_EDGES = loadNetwork()
ALL_FLOWS = loadFlow()

def timeA(key,v_a):
    '''计算时间t_a'''
    t_0 = ALL_EDGES[key]["free_flow_time"]
    C_a = ALL_EDGES[key]["capacity"]
    return t_0*(1+0.15*pow(v_a/C_a,4))

def funFW(alpha,args=np.array([])):
    res = 0
    for key in ALL_EDGES:
        t_0 = ALL_EDGES[key]["free_flow_time"]
        c_a = ALL_EDGES[key]["capacity"]
        x_a_n = ALL_EDGES[key]["current_flow"]
        y_a_n = ALL_EDGES[key]["auxiliary_flow"]
        res += t_0*(x_a_n+alpha*(y_a_n-x_a_n)+0.03*pow(x_a_n+alpha*(y_a_n-x_a_n),5)/pow(c_a,4))
    return res

def dfunFW(alpha,args=np.array([])):
    res = 0
    for key in ALL_EDGES:
        t_0 = ALL_EDGES[key]["free_flow_time"]
        c_a = ALL_EDGES[key]["capacity"]
        x_a_n = ALL_EDGES[key]["current_flow"]
        y_a_n = ALL_EDGES[key]["auxiliary_flow"]
        res += t_0*(y_a_n-x_a_n)*(1+0.15*pow(x_a_n+alpha*(y_a_n-x_a_n),4)/pow(c_a,4))
    return res

class AssignmentFlow():
    def __init__(self):
        self.main()

    def main(self):
        '''求解分配情况'''
        self.allOrNothing()
        while True:
            self.changeFlowTime(time_key="flow_time",flow_key="current_flow")
            self.allOrNothing(flow_change_key="auxiliary_flow",time_source_key="flow_time")
            alpha = LineSearch.graidentDescent(fun=funFW,dfun=dfunFW,theta=np.array([0.1]))
            break
            # 暂时有bug
            for key in ALL_EDGES:
                ALL_EDGES[key]["current_flow"] = ALL_EDGES[key]["current_flow"] + alpha*(ALL_EDGES[key]["auxiliary_flow"] - ALL_EDGES[key]["current_flow"])
            if abs(alpha) < 1:
                break
        print("最终的网络流")
        for key in ALL_EDGES:
            print("%s-%s %s"%(ALL_EDGES[key]["front_ver"],ALL_EDGES[key]["tail_ver"],ALL_EDGES[key]["current_flow"]))

    def changeFlowTime(self,time_key,flow_key):
        '''修改网络流时间'''
        for key in ALL_EDGES:
            ALL_EDGES[key][time_key] = timeA(key,ALL_EDGES[key][flow_key])

    def allOrNothing(self,flow_change_key="current_flow",time_source_key="free_flow_time"):
        '''按照某个标准进行流量分配'''
        for key in ALL_EDGES:
            ALL_EDGES[key][flow_change_key] = 0
        for i in range(1,25):
            record = self.shortestPath(i,time_source_key)
            for key in record:
                route = record[key]["route"]
                target_ver = record[key]["id"]
                if len(route) == 1: continue
                for j in range(len(route)-1):
                    start_ver,end_ver = route[j],route[j+1]
                    _id = getID(start_ver,end_ver)
                    ALL_EDGES[_id][flow_change_key] += ALL_FLOWS[getID(i,target_ver)]

    def shortestPath(self,ver_start,time_key="free_flow_time"):
        '''最短路径求解'''
        _list, record = [ver_start],{ver_start : {"id":ver_start, "distance":0, "front_ver":-1} }
        while len(_list) > 0:
            new_list = []
            for front_ver in _list:
                all_sub_arc = ALL_VERTEXES[front_ver]["sub_arc"]
                for sub_arc in all_sub_arc:
                    sub_ver = ALL_EDGES[sub_arc]["tail_ver"]
                    if sub_ver not in record.keys():
                        record[sub_ver] = {
                            "id" : sub_ver,
                            "distance" : ALL_EDGES[sub_arc][time_key] + record[front_ver]["distance"],
                            "front_arc" : sub_arc,
                            "front_ver" : front_ver
                        }
                        new_list.append(sub_ver)
                        continue
                    new_distance = ALL_EDGES[sub_arc][time_key] + record[front_ver]["distance"]
                    if new_distance  < record[sub_ver]["distance"]:
                        record[sub_ver]["distance"] = new_distance
                        record[sub_ver]["front_ver"] = front_ver
                        new_list.append(sub_ver)
            _list = deepcopy(new_list)

        current_layer = [ver_start]
        record[ver_start]["route"] = [ver_start]
        record[ver_start]["edges"] = []
        unsearched = [i for i in ALL_VERTEXES.keys() if i != ver_start]
        while current_layer != []:
            temp_current_layer = []
            for i in ALL_VERTEXES.keys():
                for j in current_layer:
                    if record[i]["front_ver"] == j:
                        route = record[j]["route"] + [i]
                        record[i]["route"] = route
                        # record[i]["edges"] = Schedule.getEdges(route)
                        temp_current_layer.append(i)
                        unsearched.remove(i)
            current_layer = deepcopy(temp_current_layer)
        # for key in record:
        #     print(record[key])
        return record



if __name__ == "__main__":
    AssignmentFlow()
