import pygame
import networkx as nx
import heapq
import time
import random
import math

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 100, 255)

def create_map(num_cities=15):
    G = nx.Graph()

    MIN_SEPARATION_DISTANCE = 150
    
    start_node_name = "Abrigo Seguro"
    end_node_name = "Laboratório da Cura"
    
    node_positions = []

    start_pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
    G.add_node(start_node_name, pos=start_pos)
    node_positions.append(start_pos)

    end_pos = (0,0)
    while True:
        end_pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
        distance = math.sqrt((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)
        if distance > MIN_SEPARATION_DISTANCE * 2:
            G.add_node(end_node_name, pos=end_pos)
            node_positions.append(end_pos)
            break

    city_names = [
        "Base Eagle", "Porto Seguro", "Vila Esperança", "Fortaleza Beta",
        "Hospital Central", "Torre de Rádio", "Centro Comercial", "Estação de Trem",
        "Ponte Sul", "Fazenda Miller", "Usina Elétrica", "Cruzamento Perigoso",
        "Aeroporto Abandonado", "Subúrbios", "Represa", "Observatório"
    ]
    num_remaining_cities = min(num_cities - 2, len(city_names))
    selected_names = random.sample(city_names, num_remaining_cities)

    for city_name in selected_names:
        tries = 0
        while tries < 100:
            pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
            is_far_enough = True
            for existing_pos in node_positions:
                distance = math.sqrt((pos[0] - existing_pos[0])**2 + (pos[1] - existing_pos[1])**2)
                if distance < MIN_SEPARATION_DISTANCE:
                    is_far_enough = False
                    break
            if is_far_enough:
                G.add_node(city_name, pos=pos)
                node_positions.append(pos)
                break
            tries += 1

    all_nodes = list(G.nodes(data=True))
    max_connection_distance = 350

    for i in range(len(all_nodes)):
        for j in range(i + 1, len(all_nodes)):
            node1_name, data1 = all_nodes[i]
            node2_name, data2 = all_nodes[j]
            pos1, pos2 = data1['pos'], data2['pos']
            distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
            if distance < max_connection_distance:
                risk = random.randint(10, 100)
                G.add_edge(node1_name, node2_name, risk=risk)
    
    if not nx.is_connected(G):
        components = list(nx.connected_components(G))
        main_component = max(components, key=len)
        for component in components:
            if component != main_component:
                node_from_main = random.choice(list(main_component))
                node_from_other = random.choice(list(component))
                risk = random.randint(50, 150)
                G.add_edge(node_from_main, node_from_other, risk=risk)

    return G

def dijkstra(graph, start_node, end_node):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {node: None for node in graph.nodes}
    pq = [(0, start_node)]
    visited = set()
    yield {'visited': visited, 'current_node': start_node, 'predecessors': predecessors}
    while pq:
        current_risk, current_node = heapq.heappop(pq)
        if current_risk > distances[current_node]: continue
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

def draw(screen, font, graph, dijkstra_state, start_node, end_node, final_path):
    screen.fill(BLACK)
    for u, v, data in graph.edges(data=True):
        pos_u, pos_v = graph.nodes[u]['pos'], graph.nodes[v]['pos']
        pygame.draw.line(screen, GRAY, pos_u, pos_v, 2)
        risk_text = font.render(str(data['risk']), True, WHITE)
        mid_pos = ((pos_u[0] + pos_v[0]) / 2, (pos_u[1] + pos_v[1]) / 2 - 20)
        screen.blit(risk_text, mid_pos)
    if final_path:
        for i in range(len(final_path) - 1):
            pos1, pos2 = graph.nodes[final_path[i]]['pos'], graph.nodes[final_path[i+1]]['pos']
            pygame.draw.line(screen, GREEN, pos1, pos2, 5)
    for node, data in graph.nodes(data=True):
        pos = data['pos']
        color = BLUE
        if 'visited' in dijkstra_state and node in dijkstra_state['visited']: color = YELLOW
        if 'current_node' in dijkstra_state and node == dijkstra_state['current_node']: color = RED
        if node == start_node: color = GREEN
        elif node == end_node: color = RED
        if final_path and node in final_path: color = GREEN
        pygame.draw.circle(screen, color, pos, 15)
        city_text = font.render(node, True, WHITE)
        screen.blit(city_text, (pos[0] - city_text.get_width() // 2, pos[1] + 20))

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Missão: A Cura Zumbi")
    font = pygame.font.SysFont('Consolas', 18)

    game_map = create_map(num_cities=12)
    
    START_NODE = "Abrigo Seguro"
    END_NODE = "Laboratório da Cura"
    
    print(f"Missão iniciada: Encontrar o caminho de '{START_NODE}' para '{END_NODE}'")
    
    STEP_DELAY = 0.5
    last_step_time = 0

    dijkstra_generator = dijkstra(game_map, START_NODE, END_NODE)
    dijkstra_state = {}
    final_path = []
    algorithm_finished = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not algorithm_finished and time.time() - last_step_time > STEP_DELAY:
            last_step_time = time.time()
            try:
                dijkstra_state = next(dijkstra_generator)
            except StopIteration:
                algorithm_finished = True
                print("Algoritmo finalizado.")
                predecessors = dijkstra_state.get('predecessors', {})
                current = END_NODE
                if current in predecessors or current == START_NODE:
                    while current is not None:
                        final_path.insert(0, current)
                        current = predecessors.get(current)
                    if not final_path or final_path[0] != START_NODE:
                        print("Não foi possível encontrar um caminho.")
                        final_path = []
        
        draw(screen, font, game_map, dijkstra_state, START_NODE, END_NODE, final_path)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()