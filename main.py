import networkx as nx
import matplotlib.pyplot as plt

nxgraph = nx.read_weighted_edgelist(
    "i2.txt", create_using=nx.Graph(), nodetype=int)
pos = nx.spring_layout(nxgraph)
nx.draw_networkx(nxgraph, with_labels=True, pos=pos,
                 node_size=700, node_color="blue")
nx.draw_networkx_edge_labels(
    nxgraph, pos=pos, edge_labels=nx.get_edge_attributes(nxgraph, 'weight'))
plt.axis("off")
plt.show()


def dijkstra(graph, start, end):
    # Prazan dict koji sadrzi distance
    distances = {}
    # Lista tacaka na putu do trenutne tacke
    predecessors = {}

    # svi cvorovi kroz koje treba proci
    to_assess = graph.keys()

    # Inicijalno postavljanje svih covorova na beskonacnu vrednost
    for node in graph:
        distances[node] = float('inf')
        predecessors[node] = None

    # Postaviti pocetnu kolekciju trajno oznacenih cvorova na prazno
    sp_set = []

    # Postavi distancu pocetnog cvora da bude 0
    distances[start] = 0

    # Dok imamo covorova kroz koje je potrebno iterirati
    while len(sp_set) < len(to_assess):

        # Izbrisati sve cvorove koji imaju beskonacnu vrednost
        still_in = {node: distances[node]
                    for node in [node for node in
                                 to_assess if node not in sp_set]}

        # Nadji najblizi cvor -> trenutnog covora
        closest = min(still_in, key=distances.get)

        # Dodaj ga u kolekciju oznacenih cvorova
        sp_set.append(closest)

        # Za svakog `komsiju` najblizeg covora
        for node in graph[closest]:
            # Ako mozemo naci kracu distancu
            if distances[node] > distances[closest] +\
                    graph[closest][node]:

                # Dodaj kracu distancu
                distances[node] = distances[closest] +\
                    graph[closest][node]

                predecessors[node] = closest

    """
    Nakon zavrsetka petlje, potrebno je izracunati krajnju putanju
    Ovo cinimo tako sto se vracamo u nazad kroz prethodnike
    """
    path = [end]
    while start not in path:
        path.append(predecessors[path[-1]])

    # Vrati putanju u redosledu `pocetak -> kraj` zajedno sa `cenom`
    return path[::-1], distances[end]


if __name__ == '__main__':
    graph = {
        '1': {'2': 1, '4':  1},
        '2': {'1': 1, '4':  1, '3':  2},
        '3': {'2': 2, '4': 1, '5': 1, '6': 1},
        '4': {'1':  1, '2':  1, '3': 1, '5': 2, '6': 15},
        '5': {'3': 1, '4': 2, '6': 1},
        '6': {'3': 1, '4': 15, '5': 1}
    }
    path, distance = dijkstra(graph, start='1', end='6')
    print(f'PUT: {path}')
    print(f'NAJKRACA PUTANJA {distance}')
