import numpy as np
import pandas as pd


def read_csv_skipping_rows(csv_path, skip_ratio):
    # Read every Nth line of a csv file. 
    # For example to read very 10th line, run read_csv_skipping_roxws('my_file.csv',10)
    
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    
    len_of_file = file_len(csv_path)
    print ('file length %d, reading 1 in %d...' %(len_of_file, skip_ratio))    
    skipped = np.setdiff1d(np.arange(len_of_file), np.arange(0, len_of_file, skip_ratio))
    
    df = pd.read_csv(csv_path, skiprows=skipped)
    print('Done.')
    return df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(add_help=True, description="Make a trimmed dataset")
    parser.add_argument('in_csv', type=str,
                         help='The Path to csv file')

    parser.add_argument('output', type=str, help='Oputout of the trimmed csv')
    parser.add_argument('-s', "--skip_ratio", default=10, type=int, help='Do not write images')

    args = parser.parse_args()

    return_value = read_csv_skipping_rows(args.in_csv, args.skip_ratio)
    return_value.to_csv(args.output)





