def read_csv_skipping_rows(csv_path, skip_ratio):
    # Read every Nth line of a csv file. 
    # For example to read very 10th line, run read_csv_skipping_rows('my_file.csv',10)
    
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    
    len_of_file = file_len(csv_path)
    print ('file length %d, reading 1 in %d...' %(len_of_file, skip_ratio))    
    skipped = np.setdiff1d(np.arange(len_of_file), np.arange(0,len_of_file,10))
    
    df = pd.read_csv(csv_path, skiprows=skipped)
    print('Done.')
    return df
