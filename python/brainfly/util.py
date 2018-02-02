"""
Utility functions for brainfly
"""
import numpy as np


def intlist(array):
    """Round an array to the nearest integer and make it into a list
    Args:
        array (np.ndarray): numpy array
    Returns:
        (list): integers
    """
    return np.around(array).astype(int).tolist()


def lerp(current, goal, t):
    """Linearly interpolate between current and goal
    Args:
        current (number-like): starting position
        goal (number-like): final destination
        t (float): number in [0, 1]. 
                   At t=0, the function will return current
                   At t=1, the function will return goal
    Returns:
        (float): the position at time t
    """
    return current + (goal - current) * t


def subsample_frequencies(freqs, width=4):
    """Subsample features from the frequency domain
    First smooths the frequencies and then subsamples it
    Args:
        freqs (np.ndarray): vector of power at each frequency
        width (int): smoothing window size
    Returns:
        (np.ndarray): subsampled frequencies of size len(freqs) // 4
    """
    width = int(np.ceil(len(freqs) / width))
    weights = np.ones(width) / width
    result = np.array([np.convolve(freqs[:, i], weights, 'same')[::width] for i in range(freqs.shape[1])]).T
    return result
