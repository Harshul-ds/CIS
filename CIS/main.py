#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import librosa
import numpy as np
from utils.gethr import gethr
from utils.cal_steng import cal_steng
from utils.location_postprocess import location_postprocess
from dp_prog import dp_prog
import matplotlib.pyplot as plt

def estimate_s1s2(y,
                  FS = 2000,
                  framelen = 5,
                  BPM0 = 72,
                  st_winlen = 0.05,
                  delta = 0.01
                  ):

    wlen = np.round(framelen*FS)
    F0 = BPM0 / 60
    st_winlen = 0.05
    st_winshift = 1 / FS
    st_Nlen = np.int(st_winlen*FS)
    st_Nshift = np.int(st_winshift*FS)
    delta = 0.01

    sig = y.reshape(-1)
    #sig = resample(sig,FS,fs);sigo = sig;
    
    S1_detect = np.zeros((len(sig), ))
    S2_detect = np.zeros((len(sig), ))
    HRP_all = np.array([])

# for i in range(1, np.int(len(sig) - wlen + 1), np.int(wlen / 2)):
#     #     disp(['Segment starting at ' num2str(i/FS) 'sec']);
#     sigseg = sig[i: i + wlen - 1]
    sigseg = sig
    # HRP, HR = gethr(sigseg,FS,F0)
    # HRP_all = np.concat((HRP_all, HRP), -1)
    HRP = 1.2
    sigseg = np.concatenate((np.zeros((np.int(HRP*FS),)),sigseg), -1)
    st_eng = cal_steng(sigseg, st_Nlen, st_Nshift)
    #     PitchPeriod_inFrames = np.round(2*HRP/st_winshift)
    #     zero_st_eng = np.concatenate((np.zeros(PitchPeriod_inFrames,1), st_eng), -1)
    ll, cs, loc_sig, ind1s, ind2s = dp_prog(st_eng, np.round(HRP / st_winshift), delta)

    ind1s = (ind1s - np.round(HRP*FS) + 1).astype(np.int)
    ind1s = ind1s[ind1s>0]
    # S1_detect[i-1+ind1s] = S1_detect[i-1+ind1s] + 1
    S1_detect[ind1s] = S1_detect[ind1s] + 1
    ind2s = (ind2s - np.round(HRP*FS) + 1).astype(np.int)
    ind2s = ind2s[ind2s>0]
    # S2_detect[i-1+ind2s] = S2_detect[i-1+ind2s] + 1
    S2_detect[ind2s] = S2_detect[ind2s] + 1
        
    S1_locations = np.sort(np.argwhere(S1_detect>0)/FS).reshape(-1)
    S2_locations = np.sort(np.argwhere(S2_detect>0)/FS).reshape(-1)
    Med_HRP = np.median(HRP_all)
    tmp = location_postprocess(S1_locations,0.8*Med_HRP)
    S1_locations_final = location_postprocess(tmp,0.8*Med_HRP);
    tmp = location_postprocess(S2_locations,0.8*Med_HRP);
    S2_locations_final = location_postprocess(tmp,0.8*Med_HRP);

    return S1_locations_final, S2_locations_final


if __name__ == '__main__':
    # Load data
    noisy_f_name  =  "AiStethRecording-8BL5_7.1_s2.wav"
    noisy_y, _  =  librosa.load(noisy_f_name, sr = 2000)
    S1_locations_final, S2_locations_final = estimate_s1s2(noisy_y)
    plt.scatter(S1_locations_final, noisy_y[S1_locations_final])
    

    
    
