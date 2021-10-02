#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 19:34:15 2021

@author: at3ee
"""
import numpy as np
from scipy import signal
from scipy.signal import lfilter
from PyAstronomy import pyaC


def xewgrdel(u,
             fs = 4096,
             dy_gwlen = 0.002*200,
             dy_fwlen = 0.00045*200):
    """
    implement EW group delay epoch extraction

    Parameters
    ----------
    u : TYPE
        DESCRIPTION.
    fs : TYPE
        DESCRIPTION.
    dy_gwlen : TYPE
        DESCRIPTION.
    dy_fwlen : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    # perform group delay calculation
    
    gw = 2*np.floor(dy_gwlen*fs/2)+1            # force window length to be odd
    ghw = signal.hamming(gw)
    ghw = ghw.reshape(-1)                       # force to be a column (dmb thinks window gives a row - and he should know as he wrote it!)
    ghwn = ghw.T*np.arange(gw-1, -gw, -2)/2     # weighted window: zero in middle
    
    u2 = u**2
    yn = lfilter(ghwn,1,u2)
    yd = lfilter(ghw,1,u2)
    yd[np.abs(yd)<eps] = 10*eps                 # prevent infinities
    y = yn[gw:end]/yd[gw:end]                   # delete filter startup transient
    toff = (gw-1)/2
    fw = 2*np.floor(dy_fwlen*fs/2)+1            # force window length to be odd
    if fw>1:
        daw = signal.hamming(fw)
        y = lfilter(daw,1,y)/np.sum(daw)        # low pass filter
        toff = toff-(fw-1)/2;

    tew, sew = pyaC.zerocross1d(np.arange(len(y)), y, getIndices=True) # find zero crossings
    
    tew = tew+toff                              # compensate for filter delay and frame advance
    
    return tew, sew, y, toff