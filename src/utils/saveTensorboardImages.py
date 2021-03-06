# -*- coding: future_fstrings -*-
from __future__ import print_function, division, absolute_import
import numpy as np
import re
from matplotlib import pyplot as plt
import os
import csv
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from os import listdir
from os.path import isfile, join
import glob

SAVE_PATH="/home/finuxs/TFM/write/imagesWriting/tensorboard/comparison/val/unlossPredicted/"
save = 'unlossPredicted.png'
files = [f for f in sorted(glob.iglob(SAVE_PATH + "*.csv")) if isfile(join(SAVE_PATH, f))]
loss = np.zeros((len(files), 101))
epoch = np.zeros((len(files), 101))
print(files)
cnt=0

for i in range(len(files)):
    idx = 0
    with open(os.path.join(SAVE_PATH, files[i]), "r") as f:
        csv_reader = csv.DictReader(f,delimiter=',')
        line_count = 0
        print(f)
        for row in csv_reader:
            epoch[i,idx] = row["Step"]
            if cnt == 1:
                loss[i,idx] = 2.0*float(row["Value"])
            elif cnt == 3:
                loss[i,idx] = 0.75*float(row["Value"])
            else:
                loss[i,idx] = row["Value"]
            idx += 1

        loss[i] = savgol_filter(loss[i], 51, 3)  # window size 51, polynomial order 3

    cnt = cnt +1

    plt.plot(epoch[i], loss[i])
#plt.legend(['hidden GRU', 'hidden LSTM', 'repeated GRU', 'repeated LSTM'], loc='upper right')
#plt.legend(['hidden No Residual', 'hidden Residual', 'repeated No Residual', 'repeated Residual'], loc='upper right')
plt.legend(['erd repeated GRU Residual', 'simple residual repeated LSTM', 'martinez repeated GRU', 'srivastava repeated LSTM'], loc='upper right')
#plt.legend(["even","none","window 2","window 3"], loc="upper right")
plt.title('Validation Loss vs Epoch')
plt.xlabel('Epoch')
plt.ylabel('Validation Loss')
plt.tight_layout()
plt.savefig(os.path.join(SAVE_PATH,save))
plt.draw()
plt.close()

