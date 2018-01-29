import pickle
import sys
sys.path.append('../signalProc')
sys.path.append('../plotting')
sys.path.append('../utilities')
from image3d import image3d
from readCapInf import readCapInf
import bufhelp
import matplotlib.pyplot as plt
import numpy as np

MIN_FREQ = 5
MAX_FREQ = 32


if __name__ == '__main__':
    with open('processed_data.pkl', 'rb') as f:
        data = pickle.load(f)
    Cname, _, xy, _, _ = readCapInf('cap_tmsi_mobita_10ch.txt')
    data, events, hdr = data['X'], data['events'], data['hdr']
    X = np.array(data)
    freqs = np.linspace(5, 32, X.shape[1])
    y = np.concatenate([e.value for e in events])
    mean_left = X[y==0].mean(axis=0)
    mean_right = X[y==1].mean(axis=0)
    X = np.dstack([mean_left, mean_right])
    image3d(X, dim=1, plotpos=xy, xvals=freqs, yvals=Cname, ticklabs='all')
    # _, axs = plt.subplots(5, 2)
    # for i, ax in enumerate(axs.flatten()):
    #     ax.set_title(i+1)
    #     ax.plot(freqs, mean_left[:, i], label='left')
    #     ax.plot(freqs, np.repeat(mean_left.mean(0)[i], len(freqs)), label='left_average')
    #     ax.plot(freqs, mean_right[:, i], label='right')
    #     ax.plot(freqs, np.repeat(mean_right.mean(0)[i], len(freqs)), label='right_average')
    # plt.legend()
    plt.show()
