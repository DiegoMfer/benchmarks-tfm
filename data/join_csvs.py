import glob
import pandas as pd
import os

# Get all CSV files in the data directory
csv_files = glob.glob(os.path.join(os.path.dirname(__file__), '*.csv'))

# Read and concatenate all CSVs
all_dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    df['source_file'] = os.path.basename(file)
    # Add 'tool' column based on file name
    if 'rdfgraphgen' in file:
        df['tool'] = 'rdfgraphgen'
    elif 'lubm' in file:
        df['tool'] = 'lubm'
    elif 'rudof' in file:
        df['tool'] = 'rudof'
    else:
        df['tool'] = 'unknown'
    # Drop columns if they exist
    for col in ['entities', 'universities']:
        if col in df.columns:
            df = df.drop(columns=[col])
    all_dfs.append(df)

joined_df = pd.concat(all_dfs, ignore_index=True)

# Save the joined CSV
joined_df.to_csv(os.path.join(os.path.dirname(__file__), 'all_benchmarks_joined.csv'), index=False)
print(f"Joined {len(csv_files)} CSV files into all_benchmarks_joined.csv")
