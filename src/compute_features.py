from pathlib import Path
import yaml
import numpy as np
import pandas as pd
import pickle

feature_processor = {
        'Mean': lambda data: np.mean(data['magnitude'].values),
        'Std': lambda data: np.std(data['magnitude'].values)
        }

if __name__ == "__main__":
    params = yaml.safe_load(open("params.yaml"))["features"]
    output_dir = Path('features')
    output_dir.mkdir(exist_ok=True)

    feature_db = []
    print(f"Computing {params['list']}")

    for file in Path('data').glob('*.pkl'):
        with open(file, 'rb') as f:
            data, label = pickle.load(f)
        feature_row = {}
        feature_row['oid'] = file.stem
        feature_row['label'] = label
        for feature_name in params['list']:
            feature_row[feature_name] = feature_processor[feature_name](data)
        feature_db.append(feature_row)
    feature_db = pd.DataFrame(feature_db).set_index('oid')
    feature_db.to_csv(output_dir / 'feature_table.csv')
