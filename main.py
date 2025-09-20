import pygame
import networkx as nx
import heapq
import time

# Configurações e cores
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 100, 255)

# Criação do mapa (grafo)
def create_map():
    G = nx.Graph()

    # Adiciona nós
    cities = {
        "Abrigo": (100, 360),
        "Hospital": (300, 150),
        "Centro": (400, 400),
        "Posto Militar": (700, 200),
        "Ponte": (550, 550),
        "Laboratório (Cura)": (950, 600)
    }
    for city, pos in cities.items():
        G.add_node(city, pos=pos)

    # Adiciona arestas com pesos (risco)
    roads = [
        ("Abrigo", "Hospital", 10),
        ("Abrigo", "Centro", 25),
        ("Hospital", "Posto Militar", 40),
        ("Centro", "Hospital", 15),
        ("Centro", "Ponte", 30),
        ("Centro", "Posto Militar", 50),
        ("Posto Militar", "Laboratório (Cura)", 60),
        ("Ponte", "Laboratório (Cura)", 20)
    ]
    for road in roads:
        G.add_edge(road[0], road[1], risk=road[2])

    return G

# Dijkstra
def dijkstra(graph, start_node, end_node):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {node: None for node in graph.nodes}
    pq = [(0, start_node)]
    visited = set()

    yield {'visited': visited, 'current_node': start_node, 'predecessors': predecessors}

    while pq:
        current_risk, current_node = heapq.heappop(pq)

        if current_risk > distances[current_node]:
            continue
        
        visited.add(current_node)

        yield {'visited': visited, 'current_node': current_node, 'predecessors': predecessors}

        if current_node == end_node:
            print("Caminho encontrado!")
            return

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                risk = graph[current_node][neighbor]['risk']
                new_risk = distances[current_node] + risk

                if new_risk < distances[neighbor]:
                    distances[neighbor] = new_risk
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (new_risk, neighbor))

# Função de desenho
def draw(screen, font, graph, dijkstra_state, start_node, end_node, final_path):
    screen.fill(BLACK)

    # Desenha as estradas
    for u, v, data in graph.edges(data=True):
        pos_u = graph.nodes[u]['pos']
        pos_v = graph.nodes[v]['pos']
        pygame.draw.line(screen, GRAY, pos_u, pos_v, 2)
        # Escreve o risco na estrada
        risk_text = font.render(str(data['risk']), True, WHITE)
        mid_pos = ((pos_u[0] + pos_v[0]) / 2, (pos_u[1] + pos_v[1]) / 2 - 20)
        screen.blit(risk_text, mid_pos)
    
    # Caminho final (se encontrado)
    if final_path:
        for i in range(len(final_path) - 1):
            pos1 = graph.nodes[final_path[i]]['pos']
            pos2 = graph.nodes[final_path[i+1]]['pos']
            pygame.draw.line(screen, GREEN, pos1, pos2, 5)

    for node, data in graph.nodes(data=True):
        pos = data['pos']
        color = BLUE

        if node in dijkstra_state['visited']:
            color = YELLOW
        if node == dijkstra_state['current_node']:
            color = RED
        if node == start_node:
            color = GREEN
        elif node == end_node:
            color = RED
        
        if final_path and node in final_path:
            color = GREEN

        pygame.draw.circle(screen, color, pos, 15)
        city_text = font.render(node, True, WHITE)
        screen.blit(city_text, (pos[0] - city_text.get_width() // 2, pos[1] + 20))

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dijkstra")
    font = pygame.font.SysFont('Consolas', 18)

    game_map = create_map()
    START_NODE = "Abrigo"
    END_NODE = "Laboratório (Cura)"
    
    # Controle de velocidade
    STEP_DELAY = 0.5
    last_step_time = 0

    # Inicialização do algoritmo
    dijkstra_generator = dijkstra(game_map, START_NODE, END_NODE)
    dijkstra_state = {}
    final_path = []
    algorithm_finished = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Avança um passo no algoritmo de acordo com o delay
        if not algorithm_finished and time.time() - last_step_time > STEP_DELAY:
            last_step_time = time.time()
            try:
                dijkstra_state = next(dijkstra_generator)
            except StopIteration:
                algorithm_finished = True
                print("Algoritmo finalizado.")
                predecessors = dijkstra_state['predecessors']
                current = END_NODE
                while current is not None:
                    final_path.insert(0, current)
                    current = predecessors.get(current)
                if final_path[0] != START_NODE:
                    print("Não foi possível encontrar um caminho.")
                    final_path = []
        
        draw(screen, font, game_map, dijkstra_state, START_NODE, END_NODE, final_path)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()