import sys
import os
import numpy as np
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

def perform_negsel(train_file, test_file, alphabet='file://english.train', n=10, r=4):
    command = f'java -jar negsel2.jar -alphabet {alphabet} -self {train_file} -n {n} -r {r} -c -l < {test_file}'
    stream = os.popen(command)
    data = [float(line.rstrip()) for line in stream.readlines()]
    result = []
    result = [1 if num > 0 else 0 for num in data]
    print(result)
    return result

def main():
    for r in range(1,10):
        print(r)
        print(np.mean(perform_negsel('english.train', 'english.test', r = r)))
    

if __name__ == '__main__':
    main()

 