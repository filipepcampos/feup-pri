import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay

def get_pr(filename):
    with open(filename) as file:
        lines = file.readlines()
        precision = [float(i) for i in lines[0].split(",")]
        recall = [float(i) for i in lines[1].split(",")]
        return precision, recall


def plot_comparison(filename1, filename2, output_filename="pr.pdf", label1="System A", label2="System B"):
    pA, rA = get_pr(filename1)
    pB, rB = get_pr(filename2)


    fig, ax = plt.subplots()
    dispA = PrecisionRecallDisplay(pA, rA)
    dispB = PrecisionRecallDisplay(pB, rB)
    ax = plt.gca()
    ax.set_xlim(0,1.1)
    ax.set_ylim(0,1.1)
    dispA.plot(ax=ax, label=label1)
    dispB.plot(ax=ax, label=label2)

    plt.legend(loc="upper right")
    plt.savefig(output_filename)

comparison = [
    ("query1/Enhanced/precision_recall_values.csv", "query1/GridSearch/precision_recall_values.csv"),
    ("query2/Baseline/precision_recall_values.csv", "query2/GridSearch/precision_recall_values.csv"),
    ("query3/Enhanced C/precision_recall_values.csv", "query3/GridSearch/precision_recall_values.csv"),
    ("query4/Enhanced C/precision_recall_values.csv", "query4/GridSearch/precision_recall_values.csv")
]

for i, (A, B) in enumerate(comparison, start=1):
    plot_comparison(A,B, f"query{i}_comparison.pdf")