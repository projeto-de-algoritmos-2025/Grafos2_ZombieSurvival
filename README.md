# Grafos2_ZombieSurvival
 
**Projeto de Algoritmos - Grafos 2**

## Sobre o Projeto

Este projeto implementa uma **visualização interativa de algoritmos de caminho mais curto** em grafos, utilizando uma temática de sobrevivência zumbi para tornar o aprendizado mais envolvente. O objetivo é comparar visualmente o comportamento dos algoritmos **Dijkstra** e **A*** em cenários de busca de rotas.

Link da apresentação do projeto: [Grafos2_ZombieSurvival](https://youtu.be/2qDmSdwQDoo)

### Missão

Você está em um mundo pós-apocalíptico infestado de zumbis. Sua missão é encontrar o caminho mais seguro (com menor número de zumbis) do **"Abrigo Seguro"** até o **"Laboratório da Cura"**, navegando por uma rede de cidades interconectadas.

## Funcionalidades

- ✅ **Geração automática de mapas**: Cria grafos aleatórios com cidades e conexões
- ✅ **Visualização em tempo real**: Acompanhe o progresso dos algoritmos passo a passo
- ✅ **Comparação de algoritmos**: Alterne entre Dijkstra e A* para ver as diferenças

## Como Usar

### Controles
- **`ESPAÇO`**: Gerar um novo mapa aleatório
- **Mouse**: Clique nos botões para alternar entre algoritmos

### Interface
- **Nós verdes**: Abrigo Seguro (início) e caminho final
- **Nó vermelho**: Laboratório da Cura (destino)
- **Nós amarelos**: Locais visitados pelo algoritmo
- **Nós roxos**: Locais considerados (apenas no A*)
- **Nós cinzas**: Locais não explorados
- **Números nas arestas**: Quantidade de zumbis no caminho
- **Números nos nós**: Distância acumulada do início

## Tecnologias Utilizadas

- **Python 3.x**
- **Pygame**: Interface gráfica e visualização
- **NetworkX**: Manipulação e criação de grafos
- **Heapq**: Implementação de fila de prioridade
- **Random**: Geração de mapas aleatórios
- **Math**: Cálculos de distância euclidiana

## Pré-requisitos

```bash
Python 3.7+
```

## Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/projeto-de-algoritmos-2025/Grafos2_ZombieSurvival.git
cd Grafos2_ZombieSurvival
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o programa**
```bash
python main.py
```

### Características do Grafo
- **15 cidades** por mapa 
- **Conexões baseadas em proximidade** (máximo 350 pixels)
- **Valores de risco** aleatórios (10-100 zumbis por rota)
- **Garantia de conectividade** entre todos os pontos

---
Autores

<table>
  <tr>
    <td align="center"><a href="https://github.com/MM4k"><img style="border-radius: 60%;" src="https://github.com/MM4k.png" width="200px;" alt=""/><br /><sub><b>Marcelo Makoto</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/EnzoEmir"><img style="border-radius: 60%;" src="https://github.com/EnzoEmir.png" width="200px;" alt=""/><br /><sub><b>Enzo Emir</b></sub></a><br /></td>
  </tr>
</table>
