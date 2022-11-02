from pathlib import Path
import yaml
import pandas as pd
import pickle
import turbofats


if __name__ == "__main__":
    params = yaml.safe_load(open("params.yaml"))["features"]
    output_dir = Path('features')
    output_dir.mkdir(exist_ok=True)

    feature_db = []
    print(f"Computing {params['list']}")
    calculator = turbofats.FeatureSpace(feature_list=params['list'])

    for file in Path('data').glob('*.pkl'):
        with open(file, 'rb') as f:
            lc, label = pickle.load(f)
            lc['oid'] = file.stem
            lc.set_index('oid', inplace=True)
        lc_features = calculator.calculate_features(lc)
        lc_features['label'] = label
        feature_db.append(lc_features)
    pd.concat(feature_db).to_csv(output_dir / 'feature_table.csv')
