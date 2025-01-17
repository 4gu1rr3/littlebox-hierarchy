class Graph:
    def __init__(self, *args):
        self.graph = {}
        self.vertices = set()
        if len(args) == 1:
            self.__readFromFile(args[0])
       
    def __readFromFile(self, filename):
        with open(filename) as arq:
            for line in arq:
                verts = line.split()
                self.addEdge(verts[0], verts[1]) # addEdge não vai mais poder ser chamado dessa maneira
                
    # Aqui colocar método de comparação para chamar o addEdge

    def addEdge(self, v, w):
        self.addToList(v, w)
        self.addToList(w, v)

    def addToList(self, v, w):
        list = self.graph[v] if v in self.graph else []
        list.append(w)
        self.graph[v] = list
        self.vertices.add(v)
        self.vertices.add(w)
                
    def getAdj(self, v):
        return self.graph[v] if v in self.graph else []

    def getVerts(self):
        return self.vertices
    
    def toDot(self):
        edges = set()
        NEWLINE = '\n'
        sb = "graph {" + NEWLINE
        sb += "rankdir = LR;" + NEWLINE
        sb += "node [shape = circle];" + NEWLINE
        for v in sorted(self.getVerts()):
            for w in self.getAdj(v):
                edge = w + v if v > w else v + w
                if edge not in edges:
                    sb += v + " -- " + w + NEWLINE
                    edges.add(edge)
        sb += "}" + NEWLINE
        return sb


if __name__ == "__main__":

    g = Graph()

    g.addEdge("0", "1")
    g.addEdge("0", "2")
    g.addEdge("2", "1")

    g = Graph("tinyG.txt")

    for v in g.getVerts():
        print(f"{v}: ", end="")
        for w in g.getAdj(v):
            print(f"{w} ", end="")
        print()
    print()
    print(g.toDot())
