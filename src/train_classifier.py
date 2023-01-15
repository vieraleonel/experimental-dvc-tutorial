from pathlib import Path
import yaml
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from joblib import dump


def prepare_dataset(dataset_path, params, train=True):
    features = pd.read_csv(dataset_path, index_col=0)
    string_labels = features['label'].values
    encoder = LabelEncoder().fit(string_labels)
    labels = encoder.transform(string_labels)
    features_numeric = features.drop('label', axis=1).values
    X_train, X_test, y_train, y_test = train_test_split(features_numeric, labels,
                                                        train_size=params['train_size'],
                                                        random_state=params['split_seed'])
    if train:
        X, y = X_train, y_train
    else:
        X, y = X_test, y_test
    return X, y, list(encoder.classes_)


def train_dt(X, y, params):
    print(f"Training with {params}")
    clf = DecisionTreeClassifier(max_depth=params["max_depth"],
                                 criterion=params["criterion"])
    return clf.fit(X, y)


if __name__ == "__main__":
    output_dir = Path('models')
    output_dir.mkdir(exist_ok=True)
    params = yaml.safe_load(open("params.yaml"))["train"]
    X, y, _ = prepare_dataset('features/feature_table.csv', params, train=True)
    model = train_dt(X, y, params)
    dump(model, output_dir / 'model.joblib')
