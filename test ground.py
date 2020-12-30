import matplotlib;

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

plt.plot([[1,2],[1,3]])
plt.show()
string = '5+3-2'
print(type(string))
a = string.replace('-', '+-').split('+')
print(a)
print(sum(map(int, a)))

exit()
np.random.seed(19680801)
data = np.random.random((50, 50, 50))

fig, ax = plt.subplots()

for i in range(len(data)):
    ax.cla()
    ax.imshow(data[i])
    ax.set_title("frame {}".format(i))
    # Note that using time.sleep does *not* work here!
    plt.pause(0.1)
