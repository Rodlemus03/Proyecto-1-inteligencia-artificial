import matplotlib.pyplot as plt
import numpy as np
from algoritmos import (bfs, dfs, greedy_search, a_star, heuristic_manhattan, 
                        heuristic_euclidean, medir_rendimiento)

def cargar_laberinto(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    lineas = [linea.strip().replace(',', '') for linea in lineas if linea.strip()]
    longitudes = [len(linea) for linea in lineas]

    if len(set(longitudes)) > 1:
        print("❌ Error: Las líneas del laberinto tienen diferentes longitudes.")
        print(f"Longitudes detectadas: {set(longitudes)}")
        return None

    try:
        laberinto = np.array([[int(c) for c in linea] for linea in lineas])
    except ValueError as e:
        print("❌ Error al convertir los caracteres a enteros:", e)
        return None

    return laberinto

def visualizar_laberinto_con_caminos(laberinto, resultados):
    colores = {0: [1, 1, 1], 1: [0, 0, 0], 2: [0, 0, 1], 3: [1, 0, 0]}
    colores_caminos = {
        "BFS": "yellow", "DFS": "purple",
        "Greedy Manhattan": "orange", "Greedy Euclidean": "pink",
        "A_Manhattan": "green", "A_Euclidean": "cyan"
    }

    for algoritmo, (camino, pasos, tiempo, nodos_totales) in resultados.items():
        plt.figure(figsize=(6, 6))
        imagen = np.zeros((laberinto.shape[0], laberinto.shape[1], 3))

        for i in range(laberinto.shape[0]):
            for j in range(laberinto.shape[1]):
                imagen[i, j] = colores.get(laberinto[i, j], [1, 1, 1])

        plt.imshow(imagen, interpolation='nearest')

        if camino:
            camino_x = [p[1] for p in camino]
            camino_y = [p[0] for p in camino]
            plt.plot(camino_x, camino_y, color=colores_caminos[algoritmo], linewidth=1.5, label=f"{algoritmo}")

        plt.xticks([]), plt.yticks([])
        plt.title(f"{algoritmo}\nPasos: {pasos}, Tiempo: {tiempo:.6f}s\nNodos recorridos: {nodos_recorridos}", fontsize=10)
        plt.legend()
        plt.savefig(f"visualizaciones/{algoritmo}.png")
        plt.close()

    print("✅ Todas las imágenes han sido guardadas con pasos y tiempos.")

nombre_archivo = "laberintos/laberinto2-3.txt"
laberinto = cargar_laberinto(nombre_archivo)

if laberinto is not None:
    start_positions = [(r, c) for r in range(laberinto.shape[0]) for c in range(laberinto.shape[1]) if laberinto[r, c] == 2]
    goal_positions = [(r, c) for r in range(laberinto.shape[0]) for c in range(laberinto.shape[1]) if laberinto[r, c] == 3]

    if start_positions and goal_positions:
        start = start_positions[0]
        goal = goal_positions[0]

        resultados = {
            "BFS": medir_rendimiento(bfs, laberinto, start, goal),
            "DFS": medir_rendimiento(dfs, laberinto, start, goal),
            "Greedy Manhattan": medir_rendimiento(greedy_search, laberinto, start, goal, heuristic_manhattan),
            "Greedy Euclidean": medir_rendimiento(greedy_search, laberinto, start, goal, heuristic_euclidean),
            "A_Manhattan": medir_rendimiento(a_star, laberinto, start, goal, heuristic_manhattan),
            "A_Euclidean": medir_rendimiento(a_star, laberinto, start, goal, heuristic_euclidean)
        }

        for algoritmo, (camino, pasos, tiempo, nodos_recorridos) in resultados.items():
            print(f"{algoritmo}: {pasos} pasos, {tiempo:.6f} segundos, {nodos_recorridos} nodos recorridos")


        visualizar_laberinto_con_caminos(laberinto, resultados)
