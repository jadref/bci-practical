"""
Feedback phase for a BCI experiment

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
    """Force a matplotlib figure to redraw itself, inside a compute loop"""
    if fig is None: fig=plt.gcf()
    fig.canvas.draw()
    plt.pause(1e-3) # wait for draw.. 1ms


def test(text, n_targets=10, repetitions=5):
    """
    Online feedback phase

    Args:
    - text: handle to Text object
    - n_targets: Number of iterations to do
    - repetitions: Number of times each letter occurs per iteration
    """
    letters = list(string.ascii_uppercase)
    letter2idx = {l: i for i, l in enumerate(letters)}

    # Make sure all classification events are retrieved
    bufhelp.MAXEVENTHISTORY = 800
    bufhelp.sendEvent('experiment.start', 1)
    for target in range(n_targets):
        _, state = bufhelp.buffer_newevents('classifier.prediction', timeout_ms=0, state=None)
        flashes = np.zeros((len(letters), len(letters)*repetitions))
        text.set(text='Think of your target letter\nand get ready', color='green',
                 fontsize=14)
        drawnow()
        plt.pause(2)
        text.set(text='')
        drawnow()
        plt.pause(1)
        for i, letter in enumerate(np.random.permutation(letters*repetitions)):
            flashes[letter2idx[letter], i] = 1
            text.set(text=letter, color='white', fontsize=120)
            drawnow()
            bufhelp.sendEvent('stimulus.type', 'test')
            plt.pause(0.1)
        text.set(text='')
        # Wait for classifier
        plt.pause(3)

        predictions, _ = bufhelp.buffer_newevents('classifier.prediction', state=state, timeout_ms=5000)
        # Make sure the predictions are in the right order
        predictions = sorted(predictions, key=lambda p: p.sample)
        if len(predictions) != flashes.shape[1]:
            print('Too few predictions found..., removing last trials')
            flashes = flashes[:, :len(predictions)]
    
        predictions = np.array([p.value[0] for p in predictions])
        # Compute inner product of each letter
        similarities = flashes @ predictions
        # Pick the letter with the highest similarity
        letter = np.argmax(similarities)
        text.set(text=letters[letter], fontsize=120, color='blue')
        plt.pause(2)
    bufhelp.sendEvent('experiment.end', 1)


def setup_experiment():
    """
    Intialize the environment for the experiment

    Returns:
    the window
    """
    bufhelp.connect()

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
    test(text)


if __name__ == '__main__':
    run_experiment()
