import skimage.io as img
import numpy as np
import matplotlib
import json
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


colors = {'red': [255, 0, 0], 'green': [0, 255, 0], 'blue': [0, 0, 255], 'black': [0] * 3, 'white': [255] * 3}
with open('parameters.json') as parameters:
    data = json.load(parameters)
    death_color = colors[data['death_color']]
    img_file = data['img_file']
    tolerance = data['tolerance']

fig, ax = plt.subplots()
ax.cla()
inp_image = img.imread("test2.png")
dimensions = [len(inp_image), len(inp_image[0]), 3]
state_matrix_l = [inp_image, np.zeros(dimensions, dtype=int)]
occup_list = [[0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]


def is_cell_alive(l, c, state_matrix):
    return sum(abs(state_matrix[l][c][i] - death_color[i]) for i in range(3)) > tolerance


def get_neighbours(l, c, state_matrix):
    global occup_list
    global dimensions
    nb_neighbours = 0
    new_color = np.zeros(3, int)
    death_color = np.zeros(3, int)
    for i in occup_list:
        if not ((0 <= l + i[0] < dimensions[0]) and (0 <= c + i[1] < dimensions[1])):
            continue
        if is_cell_alive(l + i[0], c + i[1], state_matrix):
            new_color += state_matrix[l + i[0]][c + i[1]]
            nb_neighbours += 1
        else:
            death_color += state_matrix[l + i[0]][c + i[1]]
    return nb_neighbours, new_color // nb_neighbours
# plt.pause(1)
# ax.imshow(inp_image)
# plt.pause(5)


def refresh(index_matrix):
    global state_matrix_l
    change = False
    state_matrix = state_matrix_l[index_matrix]
    new_matrix = state_matrix_l[1-index_matrix]
    for l in range(dimensions[0]):
        for c in range(dimensions[1]):
            nb_neighbours, new_color = get_neighbours(l, c, state_matrix)
            if is_cell_alive(l, c, state_matrix):
                if nb_neighbours in (2,3):
                    new_matrix[l][c] = (new_matrix[l][c] + new_color) // 2
                else:


    return change
