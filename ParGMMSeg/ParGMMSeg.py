#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:26:09 2021

@author: at3ee
"""
import nuumpy as np

from FrameParGMMSeg import  FrameParGMMSeg

def ParGMMSeg(sig, Fs = 4096):
    """
    Parametric GMM Segmentation of PCD signal

    Parameters
    ----------
    sig : TYPE
        DESCRIPTION.
    Fs : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    sig  =  sig.reshape(-1)
    sig  =  sig/np.max(np.abs(sig))
    Nw = 5*Fs
    s1_loc = np.array(np.array([]))
    s2_loc = np.array([])
    offset = Nw/4
    sig = np.concatenate((np.zeros(offset), sig, np.zeros(offset+Nw)))
    seq = np.array([])
    st = offset+1
    while st+Nw+offset < len(sig):
        s1, s2, ss = FrameParGMMSeg(sig[st-offset:st+Nw+offset], Fs)
        s1 = s1[s1>offset]; s2 = s2[s2>offset]
        s1 = s1-offset; s2 = s2-offset
        s1 = s1[s1<(Nw)]; s2 = s2[s2<(Nw)]
        
        if s1.size == 0:
            s1_loc = np.concatenate((s1_loc, s1+st-offset))
            s2_loc = np.concatenate((s2_loc, s2+st-offset))

        seq = np.concatenate((seq,ss))
        st = st+Nw

    s1 = s1[s1>0]
    s2 = s2[s2>0]
    s1 = s1[s1<len(sig)]
    s2 = s2[s2<len(sig)]
    s1_loc = s1_loc/Fs
    s2_loc = s2_loc/Fs
