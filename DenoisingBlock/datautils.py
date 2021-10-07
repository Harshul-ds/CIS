import os
import librosa
import numpy as np
import torch
from torch.utils.data import Dataset
from scipy import signal
import matplotlib.pyplot as plt
import librosa.display as display
from utils import bandpass_filter, compute_spectral_coherence 
import random

class IRMDataset(Dataset):
    def __init__(self,
                 clean_train_dataset="../Data/clean_val_files_.txt",
                 clean_val_dataset="../Data/clean_val_files_.txt",
                 noisy_train_dataset="../Data/noisy_val_files_.txt",
                 noisy_val_dataset="../Data/noisy_val_files_.txt",                       
                 test_dataset="../Data/BLE_test_files.txt",
                 snr_list="../Data/snr_val.txt",
                 offset=700,
                 limit=None,
                 mode="train",
                 fs=4096,
                 device="cpu"
                 ):

        super().__init__()
        assert mode in ["train", "validation", "test"], "mode parameter must be one of 'train', 'validation', and 'test'."
        self.clean_train_f_paths = [line.rstrip('\n') for line in open(clean_train_dataset, "r")]
        self.clean_val_f_paths = [line.rstrip('\n') for line in open(clean_val_dataset, "r")]
        self.train_f_paths = [line.rstrip('\n') for line in open(noisy_train_dataset, "r")]
        self.val_f_paths = [line.rstrip('\n') for line in open(noisy_val_dataset, "r")]
        self.test_f_paths = [line.rstrip('\n') for line in open(test_dataset, "r")]
        self.snr_list = [line.rstrip('\n') for line in open(snr_list, "r")]
        self.mode = mode
        self.clean_path_folder = "../Data/wav_clean/"
        self.noise_path_folder = "../Data/wav_babble/"
        self.test_path_folder = "../Data/wav_BLE/"
        self.train_snr_val =  ["_0db", "_5db", "_10db", "_15db"]
        self.val_snr_val = ["_[-]5db", "_0db", "_5db", "_10db", "_15db"]
        # self.test_snr_val = ["_0db", "_5db", "_10db", "_15db"]
        self.fs = 4096
        self.win_length = 512
        self.hop_length = 64
        self.n_fft = 2048
        self.device = device

        if mode=="train":
            self.length = len(self.train_f_paths)
        elif mode=="validation":
            self.length = len(self.val_f_paths)
        else:
            self.length = len(self.test_f_paths)
        # self.Nw = 5*fs
        self.offset = offset
        
    def load_file(file_path, sr=4096):
        basename_text = os.path.basename(os.path.splitext(file_path)[0])
        y, _ = librosa.load(file_path, sr=sr)
        return {
            "name": basename_text,
            "y": y
        }

    def __len__(self):
        return self.length

    def __getitem__(self, idx):

        if self.mode == "train":
            clean_f_name = str(self.clean_path_folder + self.clean_train_f_paths[idx])
            noisy_f_name = str(self.noise_path_folder + self.train_f_paths[idx])
            clean_y, _ = librosa.load(clean_f_name, sr=4096)
            noisy_y, _ = librosa.load(noisy_f_name, sr=4096)
            noisy_y = bandpass_filter(noisy_y)
            noise_y = noisy_y - clean_y
            clean_mag, _ = librosa.magphase(librosa.stft(clean_y, n_fft=2048, hop_length=64, win_length=512))
            noise_mag, _ = librosa.magphase(librosa.stft(noise_y, n_fft=2048, hop_length=64, win_length=512))
            noisy_mag, _ = librosa.magphase(librosa.stft(noisy_y, n_fft=2048, hop_length=64, win_length=512))
            mask = np.sqrt(clean_mag ** 2 / (clean_mag + noise_mag) ** 2)
            n_frames = int(clean_mag.shape[1])
            C, _ = compute_spectral_coherence(noisy_f_name, self.fs, self.win_length, self.hop_length, self.n_fft, self.device)
                                              
            return torch.tensor(noisy_mag.T, dtype=torch.float32), C, torch.tensor(clean_mag.T), torch.tensor(mask.T), n_frames

        elif self.mode == "validation":
            clean_f_name = str(self.clean_path_folder + self.clean_train_f_paths[idx])
            snr_val = self.snr_list[idx]
            noisy_f_name = str(self.noise_path_folder + self.val_f_paths[idx])
            clean_y, _ = librosa.load(clean_f_name, sr=4096)
            noisy_y, _ = librosa.load(noisy_f_name, sr=4096)
            noisy_y = bandpass_filter(noisy_y)
            noise_y = noisy_y - clean_y
            C, _ = compute_spectral_coherence(noisy_f_name, self.fs, self.win_length, self.hop_length, self.n_fft, self.device)
            return noisy_y, C, clean_y, noisy_f_name, snr_val

        else:
            noisy_f_name = str(self.test_path_folder + self.test_f_paths[idx])
            noisy_y, _ = librosa.load(noisy_f_name, sr=4096)
            noisy_y = bandpass_filter(noisy_y)
            C, _ = compute_spectral_coherence(noisy_f_name, self.fs, self.win_length, self.hop_length, self.n_fft, self.device)
                        
            return noisy_y, C, noisy_f_name

if __name__ == '__main__':
    # dataset = wavDataset()
    dataset = IRMDataset()
    res = next(iter(dataset))
    print(res[0].shape)
    print(res[1].shape)
    # print(res[2].shape)
    fig1 = plt.figure(1, figsize=(10, 10))
    ax1 = fig1.add_subplot(211)
    ax2 = fig1.add_subplot(212)
    img1 = display.specshow(librosa.amplitude_to_db(res[0].squeeze().T, ref=np.max),
                                                            y_axis='log', x_axis='time', ax=ax1)
    ax1.set_title('Power spectrogram for noisy_y')
    fig1.colorbar(img1, ax=ax1, format="%+2.0f dB")

    img2 = display.specshow(librosa.amplitude_to_db(res[1].squeeze().T, ref=np.max),
                                                            y_axis='log', x_axis='time', ax=ax2)
    ax2.set_title('Power spectrogram for clean_y')
    fig1.colorbar(img2, ax=ax2, format="%+2.0f dB")
    # # noise_dataset="/home/at3ee/Desktop/Phonocardiogram/files_10db.txt"
    # # noise_f_paths = [line.rstrip('\n') for line in open(noise_dataset, "r")]
    # # noisy_y, _ = librosa.load('/media/at3ee/Backup Plus/wav_10db/'+noise_f_paths[8], sr=14400)
    # f, Cxy = signal.coherence(res[1][:2000], res[1][6000:8000], 4096, nperseg=256)
    # plt.semilogy(f, Cxy)
    # plt.xlabel('frequency [Hz]')
    # plt.ylabel('Coherence')
    # plt.show()
