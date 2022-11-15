# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        prog = 'Evaluation',
        description = 'Evaluate metrics for a given query and relevant documents'
    )
    parser.add_argument('qrels_file')
    parser.add_argument('query_url')
    parser.add_argument('output_dir')
    parser.add_argument('-n', default=10, required=False)
    return parser.parse_args()

args = get_args()

qrels_file = args.qrels_file
query_url = args.query_url
output_dir = args.output_dir
n_documents = args.n

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(qrels_file).readlines()))
# Get query results from Solr instance
results = requests.get(query_url).json()['response']['docs']

with open(f'{output_dir}/top_documents.txt', 'w') as file:
    for doc in results[:n_documents]:
        file.write(doc['title'] + '\n')

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)

@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['title'] in relevant
        ]) / idx 
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values)

@metric
def p20(results, relevant, n=20):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['title'] in relevant])/n

@metric
def p15(results, relevant, n=15):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['title'] in relevant])/n

@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['title'] in relevant])/n

@metric
def p5(results, relevant, n=5):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['title'] in relevant])/n

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)

# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p5': 'Precision at 5 (P@5)',
    'p10': 'Precision at 10 (P@10)',
    'p15': 'Precision at 15 (P@15)',
    'p20': 'Precision at 20 (P@20)',
}

# Calculate all metrics 
metrics_results = [
    [evaluation_metrics[m], calculate_metric(m, results, relevant)]
    for m in evaluation_metrics
]
# Export results as LaTeX table
df = pd.DataFrame([['Metric','Value']] + metrics_results)
with open(f'{output_dir}/results.tex','w') as tf:
    tf.write(df.style.hide(axis="index").to_latex())
# Export to csv for internal use
df.to_csv(f'{output_dir}/results.csv', header=False, index=False)

# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list
precision_values = [
    len([
        doc 
        for doc in results[:idx]
        if doc['title'] in relevant
    ]) / idx 
    for idx, _ in enumerate(results, start=1)
]

recall_values = [
    len([
        doc for doc in results[:idx]
        if doc['title'] in relevant
    ]) / len(relevant)
    for idx, _ in enumerate(results, start=1)
]

precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

# Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
recall_values = sorted(set(recall_values))

# Extend matching dict to include these new intermediate steps
for idx, step in enumerate(recall_values):
    if step not in precision_recall_match:
        if recall_values[idx-1] in precision_recall_match:
            precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
        else:
            precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
ax = plt.gca()
ax.set_xlim(0,1.1)
ax.set_ylim(0,1.1)
disp.plot(ax=ax)
plt.savefig(f'{output_dir}/precision_recall.pdf')
