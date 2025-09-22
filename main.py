import pygame
import networkx as nx
import heapq
import time
import random
import math

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

COLOR_BACKGROUND = (28, 32, 36)
COLOR_PANEL_BG = (42, 48, 54)
COLOR_TEXT = (210, 210, 210)
COLOR_TEXT_SECONDARY = (140, 140, 140)
COLOR_BORDER = (80, 88, 96)
COLOR_EDGE = (60, 66, 72)

COLOR_NODE_DEFAULT = (180, 180, 180)
COLOR_START = (76, 175, 80)
COLOR_END = (244, 67, 54)
COLOR_VISITED = (255, 193, 7)
COLOR_CONSIDERED = (156, 39, 176)  
COLOR_PATH = (76, 175, 80)

def create_map(num_cities=15):
    G = nx.Graph()

    MIN_SEPARATION_DISTANCE = 150
    STATUS_AREA_HEIGHT = 100
    GAME_AREA_HEIGHT = SCREEN_HEIGHT - STATUS_AREA_HEIGHT
    
    start_node_name = "Abrigo Seguro"
    end_node_name = "Laboratório da Cura"
    
    node_positions = []

    start_pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, GAME_AREA_HEIGHT - 50))
    G.add_node(start_node_name, pos=start_pos)
    node_positions.append(start_pos)

    end_pos = (0,0)
    while True:
        end_pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, GAME_AREA_HEIGHT - 50))
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
            pos = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, GAME_AREA_HEIGHT - 50))
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

def dijkstra(graph, start_node, end_node, status_messages):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {node: None for node in graph.nodes}
    pq = [(0, start_node)]
    visited = set()
    yield {'visited': visited, 'current_node': start_node, 'predecessors': predecessors, 'distances': distances}
    while pq:
        current_risk, current_node = heapq.heappop(pq)
        if current_risk > distances[current_node]: continue
        visited.add(current_node)
        yield {'visited': visited, 'current_node': current_node, 'predecessors': predecessors, 'distances': distances}
        if current_node == end_node:
            total_cost = distances[end_node]
            status_messages.append(">> Caminho encontrado!")
            status_messages.append(f">> Você encontrou {total_cost} zumbis até o Laboratório. Boa sorte, vai precisar...")
            return
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                risk = graph[current_node][neighbor]['risk']
                new_risk = distances[current_node] + risk
                if new_risk < distances[neighbor]:
                    distances[neighbor] = new_risk
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (new_risk, neighbor))

def heuristic(node1, node2, graph):
    pos1 = graph.nodes[node1]['pos']
    pos2 = graph.nodes[node2]['pos']
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def a_star(graph, start_node, end_node, status_messages):
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0
    
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start_node] = heuristic(start_node, end_node, graph)
    
    predecessors = {node: None for node in graph.nodes}
    pq = [(f_score[start_node], start_node)]
    visited = set()
    considered = set()  
    
    yield {'visited': visited, 'considered': considered, 'current_node': start_node, 'predecessors': predecessors, 'distances': g_score}
    
    while pq:
        current_f, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        yield {'visited': visited, 'considered': considered, 'current_node': current_node, 'predecessors': predecessors, 'distances': g_score}
        
        if current_node == end_node:
            total_cost = g_score[end_node]
            status_messages.append(">> Caminho encontrado com A*!")
            status_messages.append(f">> Você encontrou {int(total_cost)} zumbis até o Laboratório. Boa sorte, vai precisar...")
            return
        
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                considered.add(neighbor)
                
                risk = graph[current_node][neighbor]['risk']
                tentative_g_score = g_score[current_node] + risk
                
                if tentative_g_score < g_score[neighbor]:
                    predecessors[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_node, graph)
                    heapq.heappush(pq, (f_score[neighbor], neighbor))

def draw(screen, fonts, graph, algorithm_state, start_node, end_node, final_path, status_messages, current_algorithm):
    screen.fill(COLOR_BACKGROUND)
    
    for u, v, data in graph.edges(data=True):
        pos_u, pos_v = graph.nodes[u]['pos'], graph.nodes[v]['pos']
        pygame.draw.aaline(screen, COLOR_EDGE, pos_u, pos_v)
        
        risk_value = str(data['risk'])
        risk_text = fonts['tiny'].render(risk_value, True, COLOR_TEXT_SECONDARY)
        
        mid_pos_x = (pos_u[0] + pos_v[0]) / 2
        mid_pos_y = (pos_u[1] + pos_v[1]) / 2 - 15
        
        text_rect = risk_text.get_rect(center=(mid_pos_x, mid_pos_y))
        screen.blit(risk_text, text_rect)

    if final_path:
        for i in range(len(final_path) - 1):
            pos1, pos2 = graph.nodes[final_path[i]]['pos'], graph.nodes[final_path[i+1]]['pos']
            pygame.draw.line(screen, COLOR_PATH, pos1, pos2, 4)

    for node, data in graph.nodes(data=True):
        pos = data['pos']
        color = COLOR_NODE_DEFAULT
        radius = 10
        
        if 'considered' in algorithm_state and node in algorithm_state['considered']: 
            color = COLOR_CONSIDERED  
        if 'visited' in algorithm_state and node in algorithm_state['visited']: 
            color = COLOR_VISITED  
        if node == start_node: 
            color = COLOR_START  
        elif node == end_node: 
            color = COLOR_END 
        if final_path and node in final_path: 
            color = COLOR_PATH 
        pygame.draw.circle(screen, color, pos, radius)

        city_text = fonts['small'].render(node, True, COLOR_TEXT)
        screen.blit(city_text, (pos[0] - city_text.get_width() // 2, pos[1] + 18))
        
        if 'distances' in algorithm_state:
            distance = algorithm_state['distances'].get(node)
            if distance is not None and distance != float('inf'):
                dist_text_str = str(int(distance))
                dist_text = fonts['tiny'].render(dist_text_str, True, COLOR_TEXT_SECONDARY)
                text_rect = dist_text.get_rect(center=(pos[0], pos[1] - 20))
                screen.blit(dist_text, text_rect)

    status_bg_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
    pygame.draw.rect(screen, COLOR_PANEL_BG, status_bg_rect)
    pygame.draw.line(screen, COLOR_BORDER, (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, SCREEN_HEIGHT - 100), 2)
    
    button_width = 120
    button_height = 30
    button_spacing = 10
    start_x = SCREEN_WIDTH - (2 * button_width + button_spacing + 20)
    start_y = SCREEN_HEIGHT - 70
    
    dijkstra_color = COLOR_START if current_algorithm == 'dijkstra' else COLOR_PANEL_BG
    dijkstra_border_color = COLOR_START if current_algorithm == 'dijkstra' else COLOR_BORDER
    dijkstra_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    pygame.draw.rect(screen, dijkstra_color, dijkstra_rect)
    pygame.draw.rect(screen, dijkstra_border_color, dijkstra_rect, 2)
    dijkstra_text = fonts['small'].render("Dijkstra", True, COLOR_TEXT)
    text_rect = dijkstra_text.get_rect(center=dijkstra_rect.center)
    screen.blit(dijkstra_text, text_rect)
    
    astar_color = COLOR_START if current_algorithm == 'astar' else COLOR_PANEL_BG
    astar_border_color = COLOR_START if current_algorithm == 'astar' else COLOR_BORDER
    astar_rect = pygame.Rect(start_x + button_width + button_spacing, start_y, button_width, button_height)
    pygame.draw.rect(screen, astar_color, astar_rect)
    pygame.draw.rect(screen, astar_border_color, astar_rect, 2)
    astar_text = fonts['small'].render("A* (Estrela)", True, COLOR_TEXT)
    text_rect = astar_text.get_rect(center=astar_rect.center)
    screen.blit(astar_text, text_rect)
    
    algo_name = "Dijkstra" if current_algorithm == 'dijkstra' else "A* (Estrela)"
    algo_indicator = fonts['default'].render(f"Algoritmo: {algo_name}", True, COLOR_TEXT)
    screen.blit(algo_indicator, (start_x, start_y - 25))
    
    y_offset = SCREEN_HEIGHT - 85
    for message in status_messages[-3:]:  
        status_text = fonts['default'].render(message, True, COLOR_TEXT)
        screen.blit(status_text, (15, y_offset))
        y_offset += 20
    
    return dijkstra_rect, astar_rect

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Missão: A Cura Zumbi")
    
    try:
        fonts = {
            'default': pygame.font.Font("VT323-Regular.ttf", 22),
            'small': pygame.font.Font("VT323-Regular.ttf", 16),
            'tiny': pygame.font.Font("VT323-Regular.ttf", 14),
        }
    except FileNotFoundError:
        print("AVISO: Fonte 'VT323-Regular.ttf' não encontrada. Usando fonte do sistema.")
        fonts = {
            'default': pygame.font.SysFont('Consolas', 18),
            'small': pygame.font.SysFont('Consolas', 14),
            'tiny': pygame.font.SysFont('Consolas', 12),
        }


    def reset(algorithm='dijkstra'):
        random.seed()
        game_map = create_map()
        status_messages = [f">> Missão: Ir de '{START_NODE}' para '{END_NODE}'."]
        
        if algorithm == 'dijkstra':
            algorithm_generator = dijkstra(game_map, START_NODE, END_NODE, status_messages)
        else:  # A*
            algorithm_generator = a_star(game_map, START_NODE, END_NODE, status_messages)
            
        algorithm_state = {}
        final_path = []
        algorithm_finished = False
        last_step_time = 0
        return game_map, algorithm_generator, algorithm_state, final_path, algorithm_finished, last_step_time, status_messages

    START_NODE = "Abrigo Seguro"
    END_NODE = "Laboratório da Cura"
    
    STEP_DELAY = 0.5
    current_algorithm = 'dijkstra'  

    game_map, algorithm_generator, algorithm_state, final_path, algorithm_finished, last_step_time, status_messages = reset(current_algorithm)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_map, algorithm_generator, algorithm_state, final_path, algorithm_finished, last_step_time, status_messages = reset(current_algorithm)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_pos = pygame.mouse.get_pos()
        
                    button_width = 120
                    button_height = 30
                    button_spacing = 10
                    start_x = SCREEN_WIDTH - (2 * button_width + button_spacing + 20)
                    start_y = SCREEN_HEIGHT - 70
                    
                    dijkstra_rect = pygame.Rect(start_x, start_y, button_width, button_height)
                    astar_rect = pygame.Rect(start_x + button_width + button_spacing, start_y, button_width, button_height)
                    
                    if dijkstra_rect.collidepoint(mouse_pos) and current_algorithm != 'dijkstra':
                        current_algorithm = 'dijkstra'
                        game_map, algorithm_generator, algorithm_state, final_path, algorithm_finished, last_step_time, status_messages = reset(current_algorithm)
                    elif astar_rect.collidepoint(mouse_pos) and current_algorithm != 'astar':
                        current_algorithm = 'astar'
                        game_map, algorithm_generator, algorithm_state, final_path, algorithm_finished, last_step_time, status_messages = reset(current_algorithm)
        
        if not algorithm_finished and time.time() - last_step_time > STEP_DELAY:
            last_step_time = time.time()
            try:
                algorithm_state = next(algorithm_generator)
            except StopIteration:
                algorithm_finished = True
                predecessors = algorithm_state.get('predecessors', {})
                current = END_NODE
                if current in predecessors or current == START_NODE:
                    while current is not None:
                        final_path.insert(0, current)
                        current = predecessors.get(current)
                    if not final_path or final_path[0] != START_NODE:
                        status_messages.append(">> ERRO: Rota para o laboratório não encontrada.")
                        final_path = []
        
        dijkstra_rect, astar_rect = draw(screen, fonts, game_map, algorithm_state, START_NODE, END_NODE, final_path, status_messages, current_algorithm)
        
        instruction_text = fonts['small'].render("Pressione [ESPAÇO] para gerar um novo mapa", True, COLOR_TEXT_SECONDARY)
        screen.blit(instruction_text, (10, 10))
        
        instruction_text2 = fonts['small'].render("Clique nos botões para trocar o algoritmo", True, COLOR_TEXT_SECONDARY)
        screen.blit(instruction_text2, (10, 30))
        
        if current_algorithm == 'astar':
            legend_y = 55
            legend_x = 10
            
            pygame.draw.circle(screen, COLOR_NODE_DEFAULT, (legend_x, legend_y), 6)
            legend_text = fonts['tiny'].render("Não explorado", True, COLOR_TEXT_SECONDARY)
            screen.blit(legend_text, (legend_x + 15, legend_y - 6))
            
            pygame.draw.circle(screen, COLOR_CONSIDERED, (legend_x + 120, legend_y), 6)
            legend_text = fonts['tiny'].render("Considerado (heurística)", True, COLOR_TEXT_SECONDARY)
            screen.blit(legend_text, (legend_x + 135, legend_y - 6))
            
            pygame.draw.circle(screen, COLOR_VISITED, (legend_x + 300, legend_y), 6)
            legend_text = fonts['tiny'].render("Visitado", True, COLOR_TEXT_SECONDARY)
            screen.blit(legend_text, (legend_x + 315, legend_y - 6))
            
            pygame.draw.circle(screen, COLOR_PATH, (legend_x + 390, legend_y), 6)
            legend_text = fonts['tiny'].render("Caminho final", True, COLOR_TEXT_SECONDARY)
            screen.blit(legend_text, (legend_x + 405, legend_y - 6))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()