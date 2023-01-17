import json
import yaml
import pandas as pd
#from joblib import load
from mlem.api import load
from sklearn.metrics import f1_score, classification_report
from train_classifier import prepare_dataset


if __name__ == "__main__":
    params = yaml.safe_load(open("params.yaml"))["train"]
    X, y, labels = prepare_dataset('features/feature_table.csv',
                                   params, train=False)
    model = load('models/dt_model')
    ypred = model.predict(X)
    metrics = {'f1_score': f1_score(y, ypred)}
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f)
    report = classification_report(y_true=y,
                                   y_pred=ypred,
                                   target_names=labels,
                                   output_dict=True)
    df_classification_report = pd.DataFrame(report).transpose()
    df_classification_report.to_csv('classification_report.csv',
                                    float_format=lambda x: f"{x:0.4f}")
