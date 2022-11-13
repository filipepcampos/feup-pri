import subprocess
from pathlib import Path

lines = []
with open('tasks.csv') as file:
    lines = [tuple(l.strip().split(',')) for l in file.readlines()]

for (query_name, version_name, url) in lines:
    Path(f'{query_name}/{version_name}').mkdir(parents=True, exist_ok=True)
    print(f'Evaluating {query_name}/{version_name}')
    process = subprocess.Popen(['python3', 'evaluate.py', f'{query_name}/relevant.txt', url, f'{query_name}/{version_name}'])
    process.wait()