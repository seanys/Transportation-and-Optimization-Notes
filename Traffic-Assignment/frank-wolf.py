import xlrd
from copy import deepcopy

def getID(i,j):
    return ("%04d%04d")%(i,j)

ALL_DATA = xlrd.open_workbook("data/hxs/Network-3.xlsx")
ALL_CONNECTION = ALL_DATA.sheets()[0]
ALL_DISTANCE = ALL_DATA.sheets()[1]
ALL_FLOW_DATA = ALL_DATA.sheets()[3]
ALL_VERTEXES,ALL_EDGES = {},{}

ALL_DELTA = []

for i in range(1,26):
    ALL_DELTA.append()
    row_connection = ALL_CONNECTION.row_values(i)
    row_distance = ALL_DISTANCE.row_values(i)
    ALL_VERTEXES[i] = {
        "id" : i,
        "sub_arc" : []
    }
    for j in range(1,26):
        if row_connection[j] == 1:
            new_key = getID(i,j)
            ALL_EDGES[new_key] = {
                "id" : new_key,
                "head_ver" : i,
                "tail_ver" : j,
                "length" : row_distance[j],
                "flow" : 0
            }
            ALL_VERTEXES[i]["sub_arc"].append(new_key)

# print(ALL_VERTEXES)
# print(ALL_EDGES)

class LineSearch():
    def __init__(self):
        pass

class TrafficAssignment():
    def __init__(self):
        self.loadFlow()
        self.allOrNothing()

    def allOrNothing(self):
        '''分配流量'''
        for i in range(1,26):
            record = self.pointToAll(i)
            for j in range(1,26):
                if i == j: continue
                # print(record[j])
                for n in range(len(record[j]['route'])-1):
                    start_ver,end_ver = record[j]['route'][n],record[j]['route'][n+1]
                    _id = getID(start_ver,end_ver)
                    ALL_EDGES[_id]["flow"] = ALL_EDGES[_id]["flow"] + self.ALL_FLOW[i][j]

        content = {}
        for i in range(1,25):
            for j in range(i+1,26):
                if getID(i,j) not in ALL_EDGES: continue
                fo = open("data/hxs/schedule-2035-3.txt", "a+")
                fo.write("%s->%s %0.2f\n"%(i,j,ALL_EDGES[getID(i,j)]["flow"]))
                fo.write("%s->%s %0.2f\n\n"%(j,i,ALL_EDGES[getID(j,i)]["flow"]))
                fo.close()


    def loadFlow(self):
        '''加载流量'''
        self.ALL_FLOW = {}
        for i in range(1,26):
            self.ALL_FLOW[i] = {}
        
        for i in range(1,26):
            row_connection = ALL_FLOW_DATA.row_values(i)
            for j in range(1,26):
                if i == j: continue
                self.ALL_FLOW[j][i] = row_connection[j]
        
        # for i in range(1,26):
        #     print(self.ALL_FLOW[i])
    
    def loadNetwork(self):


    def pointToAll(self,ver_start):
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
                            "distance" : ALL_EDGES[sub_arc]["length"] + record[front_ver]["distance"],
                            "front_arc" : sub_arc,
                            "front_ver" : front_ver
                        }
                        new_list.append(sub_ver)
                        continue
                    new_distance = ALL_EDGES[sub_arc]["length"] + record[front_ver]["distance"]
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
        return record


if __name__ == '__main__':
    TrafficAssignment()
