# Imports

# Constants
fs = 250
trlen_ms = 750

# Functions

def algorithms_brainfly():
    algorithms = {}
    algorithms['ms2samp'] = lambda x : (x*fs)/1000.0
    algorithms['s2amp'] = lambda x : x*fs