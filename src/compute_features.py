from pathlib import Path
import yaml
import pandas as pd
import pickle


if __name__ == "__main__":
    params = yaml.safe_load(open("params.yaml"))["features"]
    output_dir = Path('features')
    output_dir.mkdir(exist_ok=True)

    feature_db = []
    print(f"Computing {params['list']}")

    for file in Path('data').glob('*.pkl'):
        with open(file, 'rb') as f:
            data, label = pickle.load(f)
        oid = file.stem
        features = {}
        features['label'] = label
        feature_db.append(pd.DataFrame(features, index=oid))
    pd.concat(feature_db).to_csv(output_dir / 'feature_table.csv')
