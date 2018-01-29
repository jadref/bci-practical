import sklearn.linear_model
import skwrap

def fit(data, events, mapping=None):
    classifier = sklearn.linear_model.LogisticRegression()
    classifier = skwrap.fit(data, events, classifier, mapping, reducer='concat')
    return classifier
    
def predict(data):
    global classifier    
    return skwrap.predict(data, classifier)
