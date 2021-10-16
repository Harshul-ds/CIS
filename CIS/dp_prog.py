#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal import find_peaks

def dp_prog(lp_res,avg,delta):

    assert not any(np.isnan(lp_res)), 'First argument can not have NaN in its element'
    
    lamb = 1
    lmin = np.floor((1-delta)*avg).astype(np.int)
    lmax = np.floor((1+delta)*avg).astype(np.int)
    cost_sig = np.zeros((len(lp_res), ))
    loc_sig = np.zeros((len(lp_res), ))
    cost = np.zeros((lmax-lmin+1, ))
    for i in range(lmax+1, len(lp_res)):
        for j in range(lmin, lmax):
            cost[j-lmin] = cost_sig[i-j]-lamb*lp_res[i-j]
        l1 = np.argwhere(cost == np.min(cost))
        loc_sig[i] = i-lmin-l1[0]+1
        cost_sig[i] = np.min(cost)

    k = 0
    last_sig = np.array([cost_sig[np.max(np.clip(np.arange(len(cost_sig)-2*lmax,
                                                 len(cost_sig)), 0, np.inf)).astype(np.int)]])
    l12 = np.argwhere(last_sig == np.min(last_sig))[0]
    last_loc = len(cost_sig)-2*lmax+l12[0]-1
    indices = np.array([last_loc], dtype=np.int)
    while k == 0:
        if loc_sig[indices[0]]<lmax+20000:
            break
        indices = np.append(indices, loc_sig[indices[0]].astype(np.int))

    gci = np.zeros((len(lp_res),))
    gci[indices] = 1
    s2sum = np.zeros((2*np.int(avg/2)+1, ))

    for i in range(-np.int(avg/2),np.int(avg/2)):
        ids = indices+i
        ids = ids[np.argwhere(ids<len(lp_res))]
        s2sum[i+np.int(avg/2)] = np.mean(lp_res[ids])

    i1 = np.round(np.linspace(0, 1, 6)*len(s2sum)); i1[0] = 1
    pksloc, _ = find_peaks(s2sum)
    pksval = s2sum[pksloc]
    indr = np.argwhere((pksloc>=i1[3]) & (pksloc<=i1[5])).reshape(-1)
    indl = np.argwhere((pksloc>=i1[0]) & (pksloc<=i1[2])).reshape(-1)

    if len(indl)==0:
        v = np.max(pksval[indr])
        id = np.argmax(pksval[indr])
        s2loc = pksloc[indr[id]]-np.round(avg/2).astype(np.int)
    elif len(indr)==0:
        v = np.max(pksval[indl])
        id = np.argmax(pksval[indl])
        s2loc = pksloc[indl[id]]-np.round(avg/2).astype(np.int)
    else:
        if np.max(pksval[indr])>np.max(pksval[indl]):
            v = np.max(pksval[indr])
            id = np.argmax(pksval[indr])
            s2loc = pksloc[indr[id]]-np.round(avg/2).astype(np.int)
        else:
            v = np.max(pksval[indl])
            id = np.argmax(pksval[indl])
            s2loc = pksloc[indl[id]]-np.round(avg/2)

    if s2loc>0:
        indices_s1 = indices; indices_s2 = indices+s2loc
        indices_s2 = indices_s2[indices_s2>len(lp_res)]
        indices_s2 = indices_s2[indices_s2<0]
    else:
        indices_s2 = indices; indices_s1 = indices+s2loc
        indices_s1 = indices_s1[indices_s1<len(lp_res)]
        indices_s1 = indices_s1[indices_s1>0]

    
    return gci, cost_sig, loc_sig, indices_s1, indices_s2

