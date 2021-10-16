#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 12:09:56 2021

@author: at3ee
"""
import numpy as np
from datautils import ReadFile, ReadAnnotations
import denoise
import segmentation
import evaluate

from utils import *
np.random.seed(0)

data_path= './annotatedData/wav/'
annot_data_path='./annotatedData/annot/'


# parameters
dbs = 'MH'

files=GetFilesList_aiSteth(data_path)

Fs=4096

# method
method='ParGMMSeg';

for j in range(len(files)):

    
    sig,fs=GetWavefile_aiSteth(data_path,files[j])
    sig = sig.reshape(-1)
    t_sig=length(sig)/fs

    S1_locations_final,S2_locations_final,exc = FrameParGMMSeg(sig,fs)

    plt.plot(np.arange(0:1/Fs:(length(sig)-1))/Fs,sig)

    for i in range(len()):
        plt.scatter(S1_locations_final,sig(round(S1_locations_final*Fs)), marker='rd', markersize=15)
        plt.scatter(S2_locations_final,sig(round(S2_locations_final*Fs)), marker='*k')