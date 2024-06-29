
# Ideia inicial: 
# Ler todo o arquivo de entrada colocando cada vértice em uma lista e ordenando as dimenções da caixinha.
# Após, descobrir quem é a maior/menor caixa.
# Depois, comparar cada caixinha da lista entre si vendo cque mcabe em quem.
# Montar grafo :)

# O que fiz:
# Li todo o arquivo e já ordenei as dimensões em decrescente
# Montei o grafo já fazendo comparações
# Próximas tarefas:
# Queria criar os grafos igual o sor (com as dimensões não ordenadas)
# Método para descobrir a maior sequência de caixas (provavelmente usando dfs)

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

## >>> Main <<3
if __name__ == "__main__":
    caminho_arquivo = 'catalogos/caso00010.txt'

    g = Digraph(caminho_arquivo)

    #for v in g.getVerts():
    #    print(f"{v}: ", end="")
    #    for w in g.getAdj(v):
    #        print(f"{w} ", end="")
    #    print()
    #print()
    
    # Código DOT do grafo, coloque no site http://www.webgraphviz.com/ para
    # visualizar o grafo e suas ligações :)
    print(g.toDot())
