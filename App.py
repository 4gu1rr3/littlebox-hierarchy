import os
from time import process_time
# Função para ler os arquivos e ordenar as dimensões das caixas
def leitor(caminho_arquivo):
    caixas = []
    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            # Dividir a linha em três números inteiros concatenados
            dimensoes = list(map(int, linha.strip().split()))
            # Ordenar as dimensões em ordem decrescente
            dimensoes.sort(reverse=True)
            # Adicionar as dimensões ordenadas à lista de caixas
            caixas.append(dimensoes)
    return caixas

# Classe Graph
class Graph:
    def __init__(self, *args):
        self.graph = {}
        self.vertices = set()
        self.caixas = []
        if len(args) == 1:
            self.__readFromFile(args[0])
       
    def __readFromFile(self, filename):
        self.caixas = leitor(filename)
        for i in range(len(self.caixas)):
            for j in range(len(self.caixas)):
                if i != j and self.__cabeDentro(self.caixas[i], self.caixas[j]):
                    self.addEdge(str(i), str(j))

    def __cabeDentro(self, caixa1, caixa2):
        # Verifica se todas as dimensões da caixa1 são menores que as dimensões da caixa2
        return all(c1 < c2 for c1, c2 in zip(caixa1, caixa2))

    def addEdge(self, v, w):
        self.addToList(v, w)

    def addToList(self, v, w):
        lista = self.graph[v] if v in self.graph else []
        lista.append(w)
        self.graph[v] = lista
        self.vertices.add(v)
        self.vertices.add(w)
                
    def getAdj(self, v):
        return self.graph[v] if v in self.graph else []

    def getVerts(self):
        return self.vertices
    
# Classe Digraph herdada de Graph
class Digraph(Graph):
    def addEdge(self, v, w):
        super().addToList(v, w)

    def toDot(self):
        NEWLINE = '\n'
        sb = "digraph {" + NEWLINE
        sb += "rankdir = TB;" + NEWLINE
        sb += "node [shape = ellipse];" + NEWLINE
        for v in sorted(self.getVerts()):
            label = ' '.join(map(str, self.caixas[int(v)]))
            sb += f'{v} [label="{label}"]' + NEWLINE
        for v in sorted(self.getVerts()):
            for w in self.getAdj(v):
                sb += v + " -> " + w + NEWLINE
        sb += "}" + NEWLINE
        return sb

## Função de caminhamento
class DepthFirstSearch:
    def __init__(self, g, s):
        self.s = s
        self.marked = {}
        self.edgeTo = {}
        self.depth = {}  # Dicionário para armazenar a profundidade de cada vértice
        self.__dfs(g, s, 0)  # Começa a busca com profundidade 0

    def hasPathTo(self, v):
        return v in self.marked

    def pathTo(self, v):
        if not self.hasPathTo(v):
            return None
        
        path = []
        while v != self.s:
            path.insert(0, v)
            v = self.edgeTo[v]
        path.insert(0, self.s)
        return path

    def __dfs(self, g, s, depth):
        self.marked[s] = True
        self.depth[s] = depth  # Armazena a profundidade do vértice s

        for w in g.getAdj(s):
            if self.depth.get(w, -1) < depth + 1:
                self.edgeTo[w] = s  # Atualiza só se o caminho for maior
                self.__dfs(g, w, depth + 1)  # Incrementa a profundidade para o próximo vértice

    def maxDepthPath(self):
        max_depth = -1
        max_depth_vertex = None
        for v in self.marked:
            if self.depth[v] > max_depth:
                max_depth = self.depth[v]
                max_depth_vertex = v
        return self.pathTo(max_depth_vertex)
    
    def maxDepth(self):
        return max(self.depth.values(), default=-1)+1

## >>> Main <<3
if __name__ == "__main__":
    start = process_time()
    caminho_arquivo = 'catalogos/caso02000.txt'

    g = Digraph(caminho_arquivo)

    maiorSeq = []
    
    maior = 0
    for vertice in g.getVerts():
        dfs = DepthFirstSearch(g, vertice)
        max_path = dfs.maxDepthPath()
        if maior < dfs.maxDepth():
            maior = dfs.maxDepth()
        if len(max_path) > len(maiorSeq):
            maiorSeq = max_path

    print("Quantidade de caixas:", maior)
    
    #for v in g.getVerts():
    #    print(f"{v}: ", end="")
    #    if dfs.hasPathTo(v):
    #        for w in dfs.pathTo(v):
    #            print(f"{w} ", end="")
    #    print()
    #print()

    #for v in g.getVerts():
    #    print(f"{v}: ", end="")
    #    for w in g.getAdj(v):
    #        print(f"{w} ", end="")
    #    print()
    #print()

    # Código DOT do grafo, coloque no site http://www.webgraphviz.com/ para
    # visualizar o grafo e suas ligações :)
    #print(g.toDot())
    end = process_time()
    t = end-start
    print("Tempo de execução: " + str(t)+"s")