import matplotlib.pyplot as plt
import pickle


with open('debug_data.data', 'rb') as filehandle:
    deltas = pickle.load(filehandle)
print(len(deltas))
plt.plot(deltas)
plt.show()