import subprocess
from pathlib import Path
import pandas as pd

lines = []
with open('tasks.csv') as file:
    for l in file.readlines():
        split = l.strip().split(',')
        lines.append((split[0], split[1], ",".join(split[2:])))

index = {}
for (query_name, version_name, url) in lines:
    if(query_name.startswith("#")):
        continue
    Path(f'{query_name}/{version_name}').mkdir(parents=True, exist_ok=True)
    print(f'Evaluating {query_name}/{version_name}')
    process = subprocess.Popen(['python3', 'evaluate.py', f'{query_name}/relevant.txt', url, f'{query_name}/{version_name}'])
    process.wait()
    index[query_name] = [version_name] if query_name not in index else index[query_name] + [version_name]

# Build comparisons
for query_name, versions in index.items():
    # Top document comparison
    df = pd.DataFrame()
    df['Rank'] = [i+1 for i in range(10)]
    for version_name in versions:
        df[version_name] = [l.strip() for l in open(f'{query_name}/{version_name}/top_documents.txt').readlines()]
    
    with open(f'{query_name}/top_documents.tex', 'w') as file:
        file.write(df.style.hide(axis="index").to_latex())
    
    # Metric comparison
    df = pd.read_csv(f'{query_name}/{versions[0]}/results.csv')
    header = ['Model'] + list(df['Metric'].values)
    df = pd.DataFrame(columns=header)
    for i, version_name in enumerate(versions):
        version_df = pd.read_csv(f'{query_name}/{version_name}/results.csv')
        df.loc[i+1] = [version_name] + list(version_df['Value'].values)
    
    with open(f'{query_name}/results.tex', 'w') as file:
        file.write(df.style.hide(axis="index").to_latex())
    
    
        
