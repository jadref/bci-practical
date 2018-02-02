"""
Plot the signals generated during the calibration phase.
Uses the processed_data generated from training.py
"""
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('../signalProc')
sys.path.append('../plotting')
sys.path.append('../utilities')
import bufhelp
from image3d import image3d
from readCapInf import readCapInf


MIN_FREQ = 5
MAX_FREQ = 32
CAPFILE = 'cap_tmsi_mobita_10ch.txt'


if __name__ == '__main__':
    with open('processed_data.pkl', 'rb') as f:
        data = pickle.load(f)

    # Load the locations from the capfile
    Cname, _, xy, _, _ = readCapInf(CAPFILE)

    data, events, hdr = data['X'], data['events'], data['hdr']

    # Only use the relevant frequencies
    freqs = np.linspace(0, hdr.fSample/2, len(data[0]))
    data = [d[(MIN_FREQ <= freqs) & (freqs <= MAX_FREQ)] for d in data]
    freqs = freqs[(freqs >= MIN_FREQ) & (freqs <= MAX_FREQ)]

    X = np.array(data)
    y = np.concatenate([e.value for e in events])
    
    # Average over trials
    mean_left = X[y==0].mean(0)
    mean_right = X[y==1].mean(0)

    # Plot the data
    X = np.dstack([mean_left, mean_right])
    image3d(X, dim=1, xlabel='Frequency (Hz)', plotpos=xy, xvals=freqs,
            yvals=Cname, zlabel=['LH', 'RH'], ticklabs='sw', ylabel='Power')
    plt.show()
