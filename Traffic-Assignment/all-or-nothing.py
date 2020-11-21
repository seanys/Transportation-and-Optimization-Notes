import pandas as pd

class Schedule(object):
    '''规划思路：全部是按照历史规划'''
    @staticmethod
    def pointToAll(ver_start):
        '''获得点到全部顶点的路径和距离'''
        _list, record = [ver_start],{ver_start : {"distance":0, "front_ver":-1} }
        # 初步计算一下节点（）
        while len(_list) > 0:
            new_list = []
            for front_ver in _list:
                all_sub_arc = ALL_VERTEXES[front_ver]["sub_arc"]
                for sub_arc in all_sub_arc:
                    sub_ver = ALL_EDGES[sub_arc]["tail_ver"]
                    if sub_ver not in record.keys():
                        record[sub_ver] = {
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
        unsearched = [i for i in range(len(ALL_VERTEXES)) if i != ver_start]
        while current_layer != []:
            temp_current_layer = []
            # print(current_layer)
            for i in range(len(ALL_VERTEXES)):
                for j in current_layer:
                    if record[i]["front_ver"] == j:
                        route = record[j]["route"] + [i]
                        record[i]["route"] = route
                        record[i]["edges"] = Schedule.getEdges(route)
                        temp_current_layer.append(i)
                        unsearched.remove(i)
            current_layer = deepcopy(temp_current_layer)
  
class AllOrNothing():
    '''全有全无规划算法'''
    def __init__():
        pass

    def loadNetwork():
        '''加载网络情况'''
        pass

    def loadDemands():
        '''加载交通需求情况'''
        pass

    def allOrNothing():
        '''计算分配后的结果'''
        pass

if __name__ == '__main__':
    pass
