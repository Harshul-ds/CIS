import os
import random
import scipy
import librosa
import numpy as np
import torch
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
import importlib
import matplotlib.pyplot as plt
from librosa import display
import time

from pathlib import Path
from scipy import signal
from scipy.ndimage import gaussian_filter1d


def bandpass_filter(sig, Fs=4096):

    # Normalized passband edge
    # frequencies w.r.t. Nyquist rate
    # Pass band frequency in Hz
    fp = np.array([20, 400])
    # Stop band frequency in Hz
    fs = np.array([10, 500])
    # Pass band ripple in dB
    Ap = 0.4
    # Stop band attenuation in dB
    As = 50
    wp = fp/(Fs/2)
    ws = fs/(Fs/2)
    N, wc = signal.cheb2ord(wp, ws, Ap, As)

    h = signal.cheby2(N, As, wc, 'bandpass', output="sos")
    sig_f = signal.sosfilt(h, sig)

    return sig_f


def compute_referene_frame(sig, win_length, hop_length, filt_len):
    # 
    inst_energy = scipy.signal.medfilt(np.log(1+np.abs(sig)), filt_len)
    ind = [np.argmax(inst_energy[int(2*len(sig)//5): int(3*len(sig)//5)]) + int(2*len(sig)//5), np.argmax(inst_energy[int(3*len(sig)//5): int(4*len(sig)//5)]) + int(3*len(sig)//5)]
    # ref_frame = int(ind//hop_length + 1)
    # ind = [np.argmax(inst_energy[int(3*len(sig)//5): int(4*len(sig)//5)]) + int(3*len(sig)//5)]
    
    ref_frame = [int(i//hop_length + 1) for i in ind]
    return ref_frame

def compute_spectral_coherence(filename, fs, win_length, hop_length, n_fft, device="cpu"):
    x, _ = librosa.load(filename, sr=fs)
    signal_length = len(x)
    Nw = np.ceil(len(x)/(hop_length))
    pad_len = int(Nw+1)*int(hop_length) - signal_length
    x = np.pad(x, (pad_len//2, pad_len - pad_len//2), 'constant', constant_values=(0, 0))
    # x = librosa.util.fix_length(x, int(Nw+1)*hop_length)
    filt_len = 127
    
    ref_frame = compute_referene_frame(x, win_length, hop_length, filt_len)
    C_ = np.zeros((321, 33))
    for rf in ref_frame:
        # C = np.zeros((321, 15))
        C = np.zeros((321, 33))
        for m in range(rf-2,rf+2):
            C_m = []
            for n in range(int(Nw+1)):
                x_ = x[m*hop_length: m*hop_length+win_length]
                y_ = x[(n)*(hop_length): (n)*(hop_length)+win_length]
                f, Cxy = signal.coherence(x_, y_, n_fft, nperseg=64)
                Cxy[np.isnan(Cxy)] = 0
                if n==m:
                   Cxy=np.zeros(Cxy.shape)
                Cxy = gaussian_filter1d(Cxy, 3)
                C_m.append(np.array([Cxy])) #[:15]
            # C.append(torch.tensor(np.array(C_m).squeeze(), dtype=torch.float32, device="cuda:0"))
            C_m_ = np.array(C_m).squeeze()
            C_m_ = (C_m_-np.min(C_m_))/(np.max(C_m_)-np.min(C_m_))
            C_m_[C_m_<np.percentile(C_m_, 95)] = 0
            C += C_m_
            
        C_ += (C-np.min(C))/(np.max(C)-np.min(C))

    return torch.tensor(C_, dtype=torch.float32, device=device), f

def mse_loss_for_variable_length_data():
    def loss_function(ipt, target, n_frames):
        """Calculate the MSE loss for variable length dataset.
        """
        E = 1e-7
        n_frames_list=[]
        n_frames_list.append(n_frames)
        with torch.no_grad():
            masks = []
            for n_frames in n_frames_list:

                masks.append(torch.ones((n_frames[0], target.size(2)), dtype=torch.float32))  # the shape is (T, F)

            binary_mask = pad_sequence(masks, batch_first=True).to(ipt.device)
        

        masked_ipt = ipt * binary_mask
        masked_target = target * binary_mask
        return ((masked_ipt - masked_target) ** 2).sum() / (binary_mask.sum() + E)

    return loss_function



def mcd(C, C_hat):
    """C and C_hat are NumPy arrays of shape (T, D),
    representing mel-cepstral coefficients.

    """
    K = 10 / torch.log(10) * torch.sqrt(2)
    return K * torch.mean(torch.sqrt(torch.sum((C - C_hat) ** 2, axis=1)))


def prepare_empty_dir(dirs, resume=False):
    """
    if resume experiment, assert the dirs exist,
    if not resume experiment, make dirs.

    Args:
        dirs (list): directors list
        resume (bool): whether to resume experiment, default is False
        print(dir_path)
    """
    
    for dir_path in dirs:

        if resume:
            assert dir_path.exists()
        else:
            dir_path.mkdir(parents=True, exist_ok=True)

class ExecutionTime:
    """
    Usage:
        timer = ExecutionTime()
        <Something...>
        print(f"Finished in {timer.duration()} seconds.")
    """

    def __init__(self):
        self.start_time = time.time()

    def duration(self):
        return time.time() - self.start_time
    
def initialize_config(module_cfg):

    module = importlib.import_module(module_cfg["module"])
    return getattr(module, module_cfg["main"])(**module_cfg["args"])

if __name__ == '__main__':
    train_dataset="../train_files.txt"
    train_f_paths = [line.rstrip('\n') for line in open(train_dataset, "r")]
    noise_path_folder = "../wav_babble/"
    idx = 3
    train_snr_val =  ["_5db", "_10db", "_15db"]
    noisy_f_name = str(noise_path_folder + train_f_paths[idx] + train_snr_val[1] + ".wav")
    fs = 4096
    win_length = 512
    hop_length = 64
    n_fft = 2048
    C, f = compute_spectral_coherence(noisy_f_name, fs, win_length, hop_length, n_fft)
    plt.imshow(C.T, cmap="magma")
    plt.show()
    



