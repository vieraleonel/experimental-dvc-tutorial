import json
from joblib import load
from sklearn.metrics import f1_score
from train_classifier import prepare_dataset


if __name__ == "__main__":
    X, y = prepare_dataset()
    clf = load('models/model.joblib')
    ypred = clf.predict(X)
    metrics = {'f1_score': f1_score(y, ypred, average='macro')}
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f)
