
#function [out]= cal_steng (sig, Nlen, Nshift)


#out1=filtfilt(ones(1,Nlen)/100,1,sig.^2);
#out=out1(1:Nshift:end);

from scipy.signal import filtfilt
import numpy as np

def cal_steng(sig, Nlen, Nshift):
    out1= filtfilt(np.ones((np.int(Nlen),))/100,1,sig**2)
    #Considers elements from 1 to end with a shift of Nshift
    out=out1[::Nshift]
    return out
