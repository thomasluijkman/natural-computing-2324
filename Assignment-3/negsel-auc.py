import sys
import os
import numpy as np
from sklearn.metrics import roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import json

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

def plot_roccurve_with_auc(fpr, tpr, filename, title=""):
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

def plot_auc_scores(r_values, auc_scores, filename, test_nr):
    parent_dir = "/".join(filename.split('/')[:-1])
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    plt.figure()
    plt.plot(r_values, auc_scores)
    plt.xlabel("r value")
    plt.ylabel("AUC Score")
    plt.grid()
    plt.title(f"AUC scores for test{test_nr} file for different r-values")
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
        plot_roccurve_with_auc(fpr, tpr, filename, title)

# We select 7, because length of the shortest syscall is 7
chunk_length = 7
    
def process_cert_train_file(filepath, write_to):
    f = open(filepath, "r")
    content = ''.join(f.read().split("\n"))
    f.close()
    chunks = [content[0+i:chunk_length+i] for i in range(0, len(content), chunk_length)]
    if len(chunks[-1]) < chunk_length:
        chunks[-1] = content[-chunk_length:]
    resulting_string = '\n'.join(chunks)
    new_train_file = open(write_to, "w")
    new_train_file.write(resulting_string)
    new_train_file.close()

def process_cert_test_file(filepath, write_to, index_json_file):
    f = open(filepath, "r")
    content = f.read().split("\n")
    f.close()
    resulting_chunks = []
    indexing = {}
    for i, line in enumerate(content):
        if line == "":
            continue
        line_chunks = [line[i:chunk_length+i] for i in range(0, len(line), chunk_length)]
        current_result_length = len(resulting_chunks)
        indexing[i] = [current_result_length + chunk_idx for chunk_idx in range(len(line_chunks))]
        if len(line_chunks[-1]) < chunk_length:
            line_chunks[-1] = line[-chunk_length:]
        resulting_chunks += line_chunks
    resulting_string = '\n'.join(resulting_chunks)
    new_train_file = open(write_to, "w")
    new_train_file.write(resulting_string)
    new_train_file.close()
    index_train_file = open(index_json_file, "w")
    index_train_file.write(json.dumps(indexing))
    index_train_file.close()
    return indexing

def exercise2_cert(print_only_confusion=False, r_confusion=4):
    testfile_nr = 2
    alphabet = 'file://snd-cert.alpha'
    train_file = './syscalls/snd-cert/snd-cert.train'
    new_train_file = 'snd-cert-processed.train'
    test_file = f'./syscalls/snd-cert/snd-cert.{testfile_nr}.test'
    new_test_file = f'snd-cert-processed.{testfile_nr}.test'
    index_json_file = f'./syscalls/snd-cert/snd-cert.{testfile_nr}.json'
    labels_file = f"./syscalls/snd-cert/snd-cert.{testfile_nr}.labels"
    labels = []
    with open(labels_file) as file:
        for line in file:
            labels.append(int(line.strip()))
    process_cert_train_file(train_file, new_train_file)
    test_indexing = process_cert_test_file(test_file, new_test_file, index_json_file)
    auc_scores = []
    r_values = range(1,8)
    for r in r_values:
        cert_results_per_chunk = perform_negsel(train_file=new_train_file, test_file=new_test_file, alphabet=alphabet, n=7, r=r)
        cert_results = []
        for key in test_indexing.keys():
            cert_indeces = test_indexing[key]
            cert_values = np.array([cert_results_per_chunk[index] for index in cert_indeces])
            cert_results.append(np.mean(cert_values))
        fpr, tpr, _ = roc_curve(labels, cert_results)
        print(f"FPR: {fpr}")
        print(f"TPR: {tpr}")
        auc_roc = auc(fpr, tpr)
        auc_scores.append(auc_roc)
        title = f'ROC curve for r = {r} (AUC = {"{:.4f}".format(auc_roc)})'
        filename = f'results/ex2/cert_test{testfile_nr}_r_{r}.png'
        plot_roccurve_with_auc(fpr, tpr, filename, title)
    auc_scores_filename = f'results/ex2/cert_test{testfile_nr}_aucscores.png'
    plot_auc_scores(r_values, auc_scores, auc_scores_filename, testfile_nr)

def exercise2_unm():
    testfile_nr = 2
    alphabet_unm = 'file://snd-unm.alpha'
    train_file_unm = './syscalls/snd-unm/snd-unm.train'
    new_train_file_unm = 'snd-unm-processed.train'
    test_file_unm = f'./syscalls/snd-unm/snd-unm.{testfile_nr}.test'
    new_test_file_unm = f'snd-unm-processed.{testfile_nr}.test'
    index_json_file_unm = f'./syscalls/snd-unm/snd-unm.{testfile_nr}.json'
    labels_file_unm = f"./syscalls/snd-unm/snd-unm.{testfile_nr}.labels"
    labels_unm = []
    with open(labels_file_unm) as file:
        for line in file:
            labels_unm.append(int(line.strip()))
    process_cert_train_file(train_file_unm, new_train_file_unm)
    test_indexing_unm = process_cert_test_file(test_file_unm, new_test_file_unm, index_json_file_unm)
    auc_scores_unm = []
    r_values = range(7,8)
    for r in r_values:
        unm_results_per_chunk = perform_negsel(train_file=new_train_file_unm, test_file=new_test_file_unm, alphabet=alphabet_unm, n=7, r=r)
        unm_results = []
        for key in test_indexing_unm.keys():
            unm_indeces = test_indexing_unm[key]
            unm_values = np.array([unm_results_per_chunk[index] for index in unm_indeces])
            unm_results.append(np.mean(unm_values))
        fpr, tpr, _ = roc_curve(labels_unm, unm_results)
        print(f"FPR: {fpr}")
        print(f"TPR: {tpr}")
        auc_roc = auc(fpr, tpr)
        auc_scores_unm.append(auc_roc)
        title = f'ROC curve for r = {r} (AUC = {"{:.4f}".format(auc_roc)})'
        filename = f'results/ex2/unm_test{testfile_nr}_r_{r}.png'
        plot_roccurve_with_auc(fpr, tpr, filename, title)
    auc_scores_filename = f'results/ex2/unm_test{testfile_nr}_aucscores.png'
    plot_auc_scores(r_values, auc_scores_unm, auc_scores_filename, testfile_nr)

if __name__ == '__main__':
    exercise1()
    exercise2_cert()
    exercise2_unm()