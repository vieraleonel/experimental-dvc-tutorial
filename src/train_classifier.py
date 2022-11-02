from pathlib import Path
import yaml
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from joblib import dump


def prepare_dataset():
    features = pd.read_csv('features/feature_table.csv', index_col=0)
    string_labels = features['label'].values
    encoder = LabelEncoder().fit(string_labels)
    labels = encoder.transform(string_labels)
    features_numeric = features.drop('label', axis=1).values
    return features_numeric, labels


def train_dt(X, y):
    params = yaml.safe_load(open("params.yaml"))["train"]
    print(f"Training with {params}")
    clf = DecisionTreeClassifier(max_depth=params["max_depth"],
                                 criterion=params["criterion"])
    return clf.fit(X, y)


if __name__ == "__main__":
    output_dir = Path('models')
    output_dir.mkdir(exist_ok=True)
    X, y = prepare_dataset()
    dump(train_dt(X, y), output_dir / 'model.joblib')
