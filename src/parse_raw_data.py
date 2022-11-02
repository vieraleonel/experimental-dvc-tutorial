from pathlib import Path
from zipfile import ZipFile
import pandas as pd
import pickle


def parse_lc(path):
    with ZipFile(path) as f:
        df = pd.read_csv(f.open('detections.csv'))
        df = df[['fid', 'mjd', 'magpsf_corr', 'sigmapsf_corr']]
        df = df.loc[df['fid'] == 1]
        df = df.rename(columns={'mjd': 'time',
                                'magpsf_corr': 'magnitude',
                                'sigmapsf_corr': 'error'})
        #df.columns = ['time', 'magnitude', 'error']
    return df


def scan_raw_data_folder():
    output_folder = Path('data')
    output_folder.mkdir(exist_ok=True)
    for file in Path('raw_data').rglob('*.zip'):
        lc = parse_lc(file)
        label = file.parent.stem
        with open(output_folder / f'{file.stem}.pkl', 'wb') as f:
            pickle.dump([lc, label], f, protocol=2)


if __name__ == "__main__":
    scan_raw_data_folder()
