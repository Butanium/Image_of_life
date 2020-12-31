import skimage.io as img
import numpy as np
import matplotlib
import json
import matplotlib.pyplot as plt
from time import process_time


matplotlib.use("TkAgg")

colors = {'red': np.array([255, 0, 0]), 'green': np.array([0, 255, 0]), 'blue': np.array([0, 0, 255]),
          'black': np.zeros(3, int), 'white': np.array([255, 255, 255])}
with open('parameters.json') as parameters:
    data = json.load(parameters)
    death_color = colors[data['death_color']]
    img_file = data['img_file']
    tolerance = data['tolerance']
    rules = data['rules']
    delta_t = data["delta_t"]
    nb_iterations = data["iterations"]
fig, ax = plt.subplots()
ax.cla()
plt.gca().axes.get_yaxis().set_visible(False)
plt.gca().axes.get_xaxis().set_visible(False)

inp_image = img.imread("input_images/" + img_file)
# inp_image = np.random.random((20,20,3))
# inp_image*=255
# inp_image = inp_image.astype(int)
dimensions = [len(inp_image), len(inp_image[0]), 3]
m1 = np.zeros(dimensions, dtype=int)
for i in range(dimensions[0]):
    for j in range(dimensions[1]):
        for k in range(dimensions[2]):
            m1[i][j][k] = inp_image[i][j][k]
state_matrix_l = [m1, np.zeros(dimensions, dtype=int)]
occup_list = [[0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]


def is_cell_alive(l, c, state_matrix):
    return sum(abs(state_matrix[l][c][i] - death_color[i]) for i in range(3)) > tolerance


def get_neighbours(l, c, state_matrix):
    global occup_list
    global dimensions
    global death_color
    nb_alive_neighbours = 0
    nb_dead_neighbours = 0
    new_color = np.zeros(3, int)
    d_color = np.zeros(3, int)

    for i in occup_list:
        if not ((0 <= l + i[0] < dimensions[0]) and (0 <= c + i[1] < dimensions[1])):
            continue
        if is_cell_alive(l + i[0], c + i[1], state_matrix):
            new_color += state_matrix[l + i[0]][c + i[1]]
            nb_alive_neighbours += 1
        else:
            nb_dead_neighbours += 1
            d_color += state_matrix[l + i[0]][c + i[1]]
    return nb_alive_neighbours, nb_dead_neighbours, new_color // nb_alive_neighbours if nb_alive_neighbours != 0 else \
        new_color, d_color if nb_dead_neighbours == 0 else d_color // nb_dead_neighbours


# plt.pause(1)
# ax.imshow(inp_image)
# plt.pause(5)

# Todo function that make an alive color a dead color by * deltas by a constant

def refresh(index_matrix):
    global state_matrix_l
    state_matrix = state_matrix_l[index_matrix]
    new_matrix = state_matrix_l[1 - index_matrix]
    for l in range(dimensions[0]):
        for c in range(dimensions[1]):
            nb_a_neighbours, nb_d_neighbours, new_color, d_color = get_neighbours(l, c, state_matrix)
            if is_cell_alive(l, c, state_matrix):
                if nb_a_neighbours in rules['death']:
                    new_matrix[l][c] = (death_color + nb_d_neighbours * d_color) // (nb_d_neighbours + 1)
                else:
                    new_matrix[l][c] = (state_matrix[l][c] + new_color * nb_a_neighbours) // (nb_a_neighbours + 1)
            else:
                if nb_a_neighbours in rules['birth']:
                    new_matrix[l][c] = new_color
                else:
                    new_matrix[l][c] = (state_matrix[l][c] + nb_d_neighbours * d_color) // (nb_d_neighbours + 1)


index = 0
ax.imshow(state_matrix_l[0].astype('uint8'))
plt.pause(.1)
input("enter anything to start")
deltas = []
for i in range(nb_iterations):
    ax.imshow(state_matrix_l[i % 2].astype('uint8'))
    # t = process_time()
    plt.pause(delta_t)
    ax.cla()
    # deltas.append(process_time()-t)
    ax.set_title("frame {}".format(i))
    t = process_time()
    refresh(i % 2)
    deltas.append(process_time()-t)
import pickle

with open('debug_data.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(deltas, filehandle)
