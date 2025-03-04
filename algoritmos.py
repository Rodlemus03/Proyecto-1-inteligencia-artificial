import numpy as np
import heapq
from collections import deque
import time  
def contar_nodos(maze):
    return np.sum(maze != 1)  # Cuenta todas las celdas que no son paredes

def get_neighbors(position, maze):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = []
    for dr, dc in directions:
        r, c = position[0] + dr, position[1] + dc
        if 0 <= r < maze.shape[0] and 0 <= c < maze.shape[1] and maze[r, c] != 1:
            neighbors.append((r, c))
    return neighbors

def medir_rendimiento(algoritmo, maze, start, goal, heuristic=None):
    start_time = time.time()
    if heuristic:
        path, nodos_recorridos = algoritmo(maze, start, goal, heuristic)
    else:
        path, nodos_recorridos = algoritmo(maze, start, goal)
    end_time = time.time()
    
    tiempo_ejecucion = end_time - start_time
    pasos = len(path) if path else 0
    
    return path, pasos, tiempo_ejecucion, nodos_recorridos  # Devolvemos nodos recorridos



def bfs(maze, start, goal):
    queue = deque([(start, [start])])
    visited = set()
    nodos_recorridos = 0  #  Contador de nodos recorridos
    while queue:
        (current, path) = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1  #  Aumentar contador
        if current == goal:
            return path, nodos_recorridos  #  Devolver nodos recorridos
        for neighbor in get_neighbors(current, maze):
            queue.append((neighbor, path + [neighbor]))
    return None, nodos_recorridos

def dfs(maze, start, goal):
    stack = [(start, [start])]
    visited = set()
    nodos_recorridos = 0
    while stack:
        (current, path) = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1
        if current == goal:
            return path, nodos_recorridos
        for neighbor in get_neighbors(current, maze):
            stack.append((neighbor, path + [neighbor]))
    return None, nodos_recorridos

def greedy_search(maze, start, goal, heuristic):
    priority_queue = [(heuristic(start, goal), start, [start])]
    visited = set()
    nodos_recorridos = 0
    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1
        if current == goal:
            return path, nodos_recorridos
        for neighbor in get_neighbors(current, maze):
            heapq.heappush(priority_queue, (heuristic(neighbor, goal), neighbor, path + [neighbor]))
    return None, nodos_recorridos

def a_star(maze, start, goal, heuristic):
    priority_queue = [(0 + heuristic(start, goal), 0, start, [start])]
    visited = set()
    nodos_recorridos = 0
    while priority_queue:
        _, cost, current, path = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1
        if current == goal:
            return path, nodos_recorridos
        for neighbor in get_neighbors(current, maze):
            new_cost = cost + 1
            heapq.heappush(priority_queue, (new_cost + heuristic(neighbor, goal), new_cost, neighbor, path + [neighbor]))
    return None, nodos_recorridos

def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


