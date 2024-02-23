import sys
import os
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

def gen_labels_ex1(results_a, results_b):
    combined_results = np.concatenate([results_a, results_b])
    labels = np.zeros(len(combined_results))
    labels[:len(results_a)] = 0
    labels[len(results_a):] = 1
    return (combined_results, labels)

def perform_negsel(train_file, test_file, 
                    alphabet='file://english.train', n=10, r=4, save_results=False):
    command = f'java -jar negsel2.jar -alphabet {alphabet} -self {train_file} -n {n} -r {r} -c -l < {test_file}'
    stream = os.popen(command)
    data = [float(line.strip()) for line in stream.readlines()]
    return data

def plot_auc(fpr, tpr, filename, title=""):
    parent_dir = "/".join(filename.split('/')[:-1])
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    plt.figure()
    plt.plot(fpr, tpr, color='red', lw=2)
    plt.plot([0,1],[0,1], color='black', linestyle='--')
    plt.xlim([-0.01,1.01])
    plt.ylim([-0.01,1.01])
    plt.grid()
    plt.title(title)
    plt.savefig(filename)

def exercise1():
    for r in range(1,10):
        print(f'Performing negative selection on English and Tagalog strings... (r={r})')
        english_results = perform_negsel('english.train', 'english.test', r=r)
        tagalog_results = perform_negsel('english.train', 'tagalog.test', r=r)
        combined, labels = gen_labels_ex1(english_results, tagalog_results)
        fpr, tpr, _ = roc_curve(labels, combined)
        auc_roc = auc(fpr, tpr)
        title = f'ROC curve for r = {r} (AUC = {"{:.4f}".format(auc_roc)})'
        filename = f'results/ex1/english-tagalog_r_{r}.png'
        plot_auc(fpr, tpr, filename, title)
    

def exercise2():
    pass
    

if __name__ == '__main__':
    exercise1()
    exercise2()

 