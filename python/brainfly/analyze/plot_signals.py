import pickle
import sys
sys.path.append('../signalProc')
import bufhelp
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    with open('processed_data.pkl', 'rb') as f:
        data = pickle.load(f)
    data, events = data['X'], data['events']
    X = np.array(data)
    y = np.concatenate([e.value for e in events])
    mean_left = X[y==0].mean(axis=0)
    mean_right = X[y==1].mean(axis=0)
    _, axs = plt.subplots(5, 2)
    for i, ax in enumerate(axs.flatten()):
        ax.set_title(i+1)
        ax.plot(mean_left[:, i], label='left')
        ax.plot(mean_right[:, i], label='right')
    plt.legend()
    plt.show()
