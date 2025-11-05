from Graph import Graph
from parse_json_graph import parse_graph
from Car import ElectricCar

def main():
    graph = parse_graph()
    saida = -1
    eCar = ElectricCar(4)

    while saida != 0:
        print("1-Imprimir Grafo")
        print("2-Desenhar Grafo")
        print("3-Imprimir  nodos de Grafo")
        print("4-A*")
        print("5-Gulosa")
        print("6-DFS")
        print("7-BFS")
        print("0-Saír")

        saida = int(input("introduza a sua opcao-> "))
        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            print(graph.adjacency_lists_dict)
            l = input("prima enter para continuar")
        elif saida == 2:
            graph.desenha()
        elif saida == 3:
            print(graph.adjacency_lists_dict.keys())
            l = input("prima enter para continuar")

        elif saida == 4:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")

            eCar.assign_location(inicio)
            print(graph.procura_aStar(inicio, fim, eCar))
            l = input("prima enter para continuar")

        elif saida == 5:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")
            print(graph.greedy(inicio, fim))
            l = input("prima enter para continuar")
        elif saida == 6:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")
            print(graph.procura_DFS(inicio, fim))
            l = input("prima enter para continuar")
        elif saida == 7:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")
            print(graph.procura_BFS(inicio, fim))
            l = input("prima enter para continuar")
        else:
            print("you didn't add anything")
            l = input("prima enter para continuar")


if __name__ == "__main__":
    main()
