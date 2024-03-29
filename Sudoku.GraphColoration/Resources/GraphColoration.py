import numpy as np
from timeit import default_timer
import networkx as nx
import matplotlib.pyplot as plt


def is_valid(grid, row, col, num):
    # Vérifier si num est présent dans la ligne spécifiée
    if num in grid[row]:
        return False

    # Vérifier si num est présent dans la colonne spécifiée
    if num in grid[:, col]:
        return False

    # Vérifier si num est présent dans le bloc 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r, c] == num:
                return False
    return True


def sudoku_to_graph(grid, color_list):
    graph = nx.Graph()
    attrs = {}
    pos = {}
    color_map = []
    k = 0
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            graph.add_node(k)
            attrs[k] = {"position": (row, column), "value": grid[row, column], "color": "black"}
            pos[k] = (column, 8 - row)
            color_map.append("black")
            k += 1
    nx.set_node_attributes(graph, attrs)

    for node_1 in graph.nodes:  # general rules
        i1, j1 = graph.nodes[node_1]["position"]
        for node_2 in graph.nodes:
            i2, j2 = graph.nodes[node_2]["position"]
            if (i1 == i2) & (j1 == j2):  # same position
                continue
            elif i1 == i2:  # same row
                graph.add_edge(node_1, node_2)
            elif j1 == j2:  # same column
                graph.add_edge(node_1, node_2)
            elif (i1 // 3 == i2 // 3) & (j1 // 3 == j2 // 3):  # same box
                graph.add_edge(node_1, node_2)
            else:
                continue

    for node in graph.nodes:  # specific links
        value = graph.nodes[node]["value"]
        if value > 0:
            for other_node in graph.nodes:
                other_value = graph.nodes[other_node]["value"]
                if (other_value > 0) & (other_value != value):
                    graph.add_edge(node, other_node)
                if (other_value > 0) & (other_value == value):
                    if node != other_node:
                        for other_neighbor in graph[other_node]:
                            graph.add_edge(node, other_neighbor)

    nx.draw(graph, pos, node_color=color_map)
    plt.savefig("test.png")

    return graph


def graph_to_sudoku(graph, color_dict):
    sudoku_grid = np.zeros((9, 9), dtype=int)

    for node in graph:
        row, column = graph.nodes[node]["position"]
        sudoku_grid[row, column] = color_dict[graph.nodes[node]["color"]]

    return sudoku_grid


def get_saturated_degree(graph, node):
    res = 0
    already_seen_colors = []
    for neighbor in graph[node]:
        neighbor_color = graph.nodes[neighbor]["color"]
        if neighbor_color != "black":
            if already_seen_colors.count(neighbor_color) == 0:
                already_seen_colors.append(neighbor_color)
                res += 1
    return res


def get_most_used_color(graph):
    colors = {
        "red": 0,
        "blue": 0,
        "green": 0,
        "yellow": 0,
        "purple": 0,
        "orange": 0,
        "brown": 0,
        "pink": 0,
        "grey": 0
    }

    most_used_color = "red"
    for node in graph.nodes:
        node_color = graph.nodes[node]["color"]
        if node_color != "black":
            colors[node_color] += 1
            if colors[node_color] > colors[most_used_color]:
                most_used_color = node_color

    print(most_used_color)
    return most_used_color


def assign_color(graph, node, color_number, color_list):
    already_seen_colors = []
    if node < 0:
        return
    for neighbor in graph[node]:
        neighbor_color = graph.nodes[neighbor]["color"]
        if neighbor_color != "black":
            if already_seen_colors.count(neighbor_color) == 0:
                already_seen_colors.append(neighbor_color)

    color_number_copy = 0
    if len(already_seen_colors) == color_number:
        print(color_number)
        print("color_list[color_number]", color_list[color_number])
        graph.nodes[node]["color"] = color_list[color_number]
        color_number_copy = color_number + 1

    else:
        # get most used color from graph
        print("unusedcolor")
        most_used_color = get_most_used_color(graph)
        graph.nodes[node]["color"] = most_used_color

    return color_number_copy

def solve_graph(graph, color_list):
    color_number = 1
    number_of_colored_nodes = 0

    while number_of_colored_nodes < 81:
        max_saturated_degree = -1
        max_index = -1
        for node in graph.nodes:
            if graph.nodes[node]["color"] == "black":
                saturated_degree = get_saturated_degree(graph, node)
                if saturated_degree > max_saturated_degree:
                    max_saturated_degree = saturated_degree
                    max_index = node
                elif saturated_degree == max_saturated_degree:
                    if len(graph[node]) > len(graph[max_index]):
                        max_index = node


        print(max_index)
        color_number = assign_color(graph, max_index, color_number, color_list)
        number_of_colored_nodes += 1


def solve_sudoku(grid, row=0, col=0):
    color_list = ["black",  # 0
                  "red",  # 1
                  "blue",  # 2
                  "green",  # 3
                  "yellow",  # 4
                  "purple",  # 5
                  "orange",  # 6
                  "brown",  # 7
                  "pink",  # 8
                  "grey"]  # 9
    color_dict = {
        "black": 0,
        "red": 1,
        "blue": 2,
        "green": 3,
        "yellow": 4,
        "purple": 5,
        "orange": 6,
        "brown": 7,
        "pink": 8,
        "grey": 9
    }

    graph = sudoku_to_graph(grid, color_list)
    solve_graph(graph, color_list)

    solved_sudoku = graph_to_sudoku(graph, color_dict)
    grid = solved_sudoku

    print(grid)

    return True  # TODO: Remove when done


# Définir `instance` uniquement si non déjà défini par PythonNET
if 'instance' not in locals():
    instance = np.array([
        [0, 0, 0, 0, 9, 4, 0, 3, 0],
        [0, 0, 0, 5, 1, 0, 0, 0, 7],
        [0, 8, 9, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 8],
        [0, 6, 0, 2, 0, 1, 0, 5, 0],
        [1, 0, 2, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 0, 0, 5, 2, 0],
        [9, 0, 0, 0, 6, 5, 0, 0, 0],
        [0, 4, 0, 9, 7, 0, 0, 0, 0]
    ], dtype=int)

start = default_timer()
# Exécuter la résolution de Sudoku
if solve_sudoku(instance):
    # print("Sudoku résolu par backtracking avec succès.")
    result = instance  # `result` sera utilisé pour récupérer la grille résolue depuis C#
else:
    print("Aucune solution trouvée.")
execution = default_timer() - start
print("Le temps de résolution est de : ", execution * 1000, " ms")
