import pygame
import networkx as nx

# Configurações e cores
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
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

# Função de desenho
def draw(screen, font, graph, start_node, end_node):
    screen.fill(BLACK)

    # Desenha as estradas
    for u, v, data in graph.edges(data=True):
        pos_u = graph.nodes[u]['pos']
        pos_v = graph.nodes[v]['pos']
        pygame.draw.line(screen, GRAY, pos_u, pos_v, 2)
        risk_text = font.render(str(data['risk']), True, WHITE)
        mid_pos = ((pos_u[0] + pos_v[0]) / 2, (pos_u[1] + pos_v[1]) / 2 - 20)
        screen.blit(risk_text, mid_pos)
    
    for node, data in graph.nodes(data=True):
        pos = data['pos']
        color = BLUE

        if node == start_node:
            color = GREEN
        elif node == end_node:
            color = RED
        
        pygame.draw.circle(screen, color, pos, 15)
        city_text = font.render(node, True, WHITE)
        screen.blit(city_text, (pos[0] - city_text.get_width() // 2, pos[1] + 20))

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Visualização do Mapa")
    font = pygame.font.SysFont('Consolas', 18)

    game_map = create_map()
    START_NODE = "Abrigo"
    END_NODE = "Laboratório (Cura)"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(screen, font, game_map, START_NODE, END_NODE)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()