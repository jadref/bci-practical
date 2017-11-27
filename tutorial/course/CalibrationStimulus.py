"""
Calibration phase for a BCI experiment
Shows a target letter in green and briefly shows all letters

Author: Joris van Vugt (s4279859)
"""
import string
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../../python/signalProc')
import bufhelp


def drawnow(fig=None):
    "force a matplotlib figure to redraw itself, inside a compute loop"
    if fig is None: fig=plt.gcf()
    fig.canvas.draw()
    plt.pause(1e-3) # wait for draw.. 1ms


def calibrate(text, n_targets=10, repetitions=5):
    """
    Calibration phase

    Args:
    - window: Render the stimuli to this window
    - n_targets: Number of iterations with a random target letter to do
    - repetitions: Number of times each letter occurs per iteration
    """
    letters = list(string.ascii_uppercase)
    target_letters = np.random.choice(letters, size=n_targets)
    bufhelp.sendEvent('experiment.start', 1)
    for target in target_letters:
        text.set(text=target, color='green')
        drawnow()
        plt.pause(2)
        text.set(text='')
        drawnow()
        plt.pause(1)
        for letter in np.random.permutation(letters*repetitions):
            text.set(text=letter, color='white')
            drawnow()
            stimulus_name = int(letter == target)
            bufhelp.sendEvent('stimulus.type', stimulus_name)
            plt.pause(0.1)
    bufhelp.sendEvent('experiment.end', 1)


def setup_experiment():
    """
    Intialize the environment for the experiment

    Returns:
    the window
    """
    hostname = 'localhost'
    port = 1972
    bufhelp.connect(hostname, port)

    plt.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    ax.set_axis_off()
    ax.set_facecolor('black')
    text = ax.text(0, 0, 'STARTING', color='white', fontsize=120,
                   ha='center', va='center')
    drawnow()
    return text


def run_experiment():
    """Run the entire experiment"""
    text = setup_experiment()
    calibrate(text)


if __name__ == '__main__':
    run_experiment()
