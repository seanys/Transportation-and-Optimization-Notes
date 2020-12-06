class Edge(object):
    def __init__(self, u, v, w):
        self.source = u
        self.sink = v  
        self.capacity = w
    def __repr__(self):
        return "%s->%s:%s" % (self.source, self.sink, self.capacity)

class FlowNetwork(object):
    def __init__(self):
        self.adj = {}
        self.flow = {}
 
    def addVertex(self, vertex):
        self.adj[vertex] = []
 
    def getEdges(self, v):
        return self.adj[v]
 
    def addEdge(self, u, v, w=0):
        if u == v:
            raise ValueError("u == v")
        edge = Edge(u,v,w)
        redge = Edge(v,u,0)
        edge.redge = redge
        redge.redge = edge
        self.adj[u].append(edge)
        self.adj[v].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0
 
    def findPath(self, source, sink, path):
        if source == sink:
            return path
        for edge in self.getEdges(source):
            residual = edge.capacity - self.flow[edge]
            if residual > 0 and edge not in path:
                result = self.findPath( edge.sink, sink, path + [edge]) 
                if result != None:
                    return result
 
    def maxFlow(self, source, sink):
        path = self.findPath(source, sink, [])
        while path != None:
            residuals = [edge.capacity - self.flow[edge] for edge in path]
            flow = min(residuals)
            for edge in path:
                self.flow[edge] += flow
                self.flow[edge.redge] -= flow
            path = self.findPath(source, sink, [])
        return sum(self.flow[edge] for edge in self.getEdges(source))

if __name__ == "__main__":
    g = FlowNetwork()
    [g.addVertex(v) for v in "sopqrt"]
    g.addEdge('s','o',3)
    g.addEdge('s','p',3)
    g.addEdge('o','p',2)
    g.addEdge('o','q',3)
    g.addEdge('p','r',2)
    g.addEdge('r','t',3)
    g.addEdge('q','r',4)
    g.addEdge('q','t',2)
    print("最大流:%s"%(g.maxFlow('s','t')))
