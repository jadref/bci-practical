import sys
sys.path.append('../../python/signalProc')
import pickle

import numpy as np

import bufhelp
import preproc
import linear

if __name__ == '__main__':
    f = pickle.load(open('training_data.pkl', 'rb'))
    data = f['data']
    events = f['events']
    hdr = f['hdr']

    data = preproc.detrend(data)
    # data, _ = preproc.badchannelremoval(data)

    # this line causes memory errors
    # data is of shape (1300, 60, 4)
    # spatial filtering tries to create eye(78_000)
    # data = preproc.spatialfilter(data)

    data = preproc.spectralfilter(data, (0, 1, 14, 15),
                                  hdr.fSample)

    data, events, _ = preproc.badtrailremoval(data, events)
    data = np.array(data).reshape(len(data), -1)
    print('data shape:', data.shape)
    events = np.array([e.value[0] for e in events])
    events[events==0] = -1
    classifier = linear.fit(data, events)
    pickle.dump(classifier, open('classifier.pkl', 'wb'))
