#coding=utf-8 
class Gragh():
    def __init__(self,nodes,sides):
        '''
        nodes 表示点
        sides 表示边

        '''
        self.sequense = {}
        self.side=[]
        for node in nodes:
            for side in sides:
                u,v=side
                if node ==u:
                    self.side.append(v)
                elif node == v:
                    self.side.append(u)
            self.sequense[node] = self.side
            self.side=[]
        print(self.sequense)


    '''
    # Depth-First-Search 
    '''
    def DFS(self,node0):
        queue,order=[],[]
        queue.append(node0)
        while queue:
            v = queue.pop()
            order.append(v)
            for w in self.sequense[v]:
                if w not in order and w not in queue: 
                    queue.append(w)
        return order

    '''
     beadth-First-Search
    '''
    def BFS(self,node0):
        queue,order = [],[]
        queue.append(node0)
        order.append(node0)
        while queue:
            v = queue.pop(0)
            for w in self.sequense[v]:
                if w not in order:
                    order.append(w)
                    queue.append(w)
        return order


def main():  
    nodes = [i+1 for i in range(8)]

    sides=[(1, 2),
        (1, 3),
        (2, 4),
        (2, 5),
        (4, 8),
        (5, 8),
        (3, 6),
        (3, 7),
        (6, 7)]
    G = Gragh(nodes,sides)
    print("广度优先搜索检索:%s"%G.DFS(1))
    print("深度优先搜索检索:%s"%G.BFS(1))

if __name__ == "__main__":
    main() 