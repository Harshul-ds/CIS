#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 15:13:12 2021

@author: at3ee
"""
import numpy as np

def hrp(sig,fs,f0):
    """
    

    Parameters
    ----------
    sig : float
        recorded signal.
    fs : int32
        sampling freq in hz.
    f0 : int32
        a rough estimate of what the pitch freq (hz) can be.

    Returns
    -------
    hrp : float
        heart rate period in seconds.
    hr : float
        hr: heart rate in hz.

    """
    sig = sig.reshape(-1)
    sig_o = sig
    sig[np.abs(sig)<0.4*np.max(np.abs(sig))] = 0
    
    crit_ind = len(sig)+np.round(0.5455*fs); # corr to 110bpm 60/110 = .5455
    c_sig = np.correlate(sig, sig, "full")
    F0 = np.round(fs/f0);
    F0_range = np.arange((F0-np.round(F0/2)),(F0+np.round(F0/2)))
    tmpind = len(sig)+F0_range
    if tmpind[0]<crit_ind:
        ids, = np.where(tmpind >= crit_ind)
        tmpind = tmpind[ids]
    else:
        tmpind = np.concatenate((np.arange(crit_ind,tmpind[0]), tmpind))
        

    if tmpind[-1] > len(c_sig):
        ids, = np.where(tmpind <= len(c_sig))
        tmpind = tmpind[ids]

    # [tmpind(1) tmpind(end) length(c_sig)]
    tmp = c_sig[tmpind]

    ind = np.argmax(tmp)
    P0 = tmpind[ind]-len(sig)
    hr = 1/(P0/fs)
    hrp = 1/hr
    
    return hr, hrp