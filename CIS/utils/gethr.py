import numpy as np
import math

def gethr(sig, fs,f0):
    fs = 2000
    sig_o = (sig-np.mean(sig))/(np.max(sig)-np.min(sig))
    sig_o[np.argwhere(np.abs(sig_o)<0.8*np.max(np.abs(sig_o)))] = 0
    crit_ind = len(sig_o) + np.round(0.5455*fs)
    c_sig = np.correlate(sig_o,sig_o,mode = "full")[len(sig_o)-1:]
    F0 = np.round(fs/f0)
    F0_range = np.arange((F0-np.round(F0/2)),(F0+np.round(F0/2)+1))
    tmpind = len(sig)+F0_range
    if tmpind[0] <crit_ind:
        ids = np.argwhere(tmpind>=crit_ind)
        tmpind = tmpind[ids].reshape(-1)
    else:
        tmpind = np.concatenate((np.arange(crit_ind,tmpind[0]-1), tmpind))

    if tmpind[-1]>len(c_sig):
        ids = np.argwhere(tmpind<=len(c_sig))
        tmpind = tmpind[ids].reshape(-1)

    tmp = c_sig[tmpind]
    val,ind = np.max(tmp)
    P0 = tmpind[ind]-len(sig)
    hr = 1/(P0/fs)
    hrp = 1/hr
    
    return hrp,hr
