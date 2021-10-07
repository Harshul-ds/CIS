import argparse
import json
import torch
import torch.nn as nn
from model import LSTM_model
from scipy.io.wavfile import write
import datetime




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Configuration file...')
    parser.add_argument('Config_file',
                        metavar='PATH',
                        type=str,
                        help='the path to file containing configuration')
    args = parser.parse_args()

    f = open(args.Config_file)

    config = json.load(f)
    print(config)
    
    # Create model
    model_config = config["model"]
    model = LSTM_model(model_config[0], model_config[0], device)

    # Load data    
    noisy_f_name = str(test_path_folder + test_f_paths[idx])
    noisy_y, _ = librosa.load(noisy_f_name, sr=4096)
    noisy_y = bandpass_filter(noisy_y)
    
    # Feature extraction
    fs = 4096
    C, _ = compute_spectral_coherence(noisy_f_name, fs, win_length, hop_length, n_fft, device)
    noisy_y = noisy_y.reshape(-1).numpy()
    # noisy_y = bandpass_filter(noisy_y)
    noisy_mag, noisy_phase = librosa.magphase(librosa.stft(noisy_y, n_fft=2048, hop_length=64, win_length=512))
    noisy_mag_tensor = torch.tensor(noisy_mag.T, device=self.device, dtype=torch.float32).unsqueeze(0) # (batch_size, T, F)
    assert noisy_mag_tensor.dim() == 3
    
    pred_mask, attention_vector = model(C, noisy_mag_tensor)
    
    pred_clean_mag_tensor = noisy_mag_tensor * pred_mask
    
    pred_clean_mag = torch.t(pred_clean_mag_tensor.squeeze(0)).detach().cpu().numpy()  # (F, T)
    pred_clean_y_s = librosa.istft(pred_clean_mag * noisy_phase, hop_length=64, win_length=512)

    min_len = min(len(noisy_y), len(pred_clean_y_s))
    noisy_y = noisy_y[:min_len]
    pred_clean_y = pred_clean_y_s[:min_len]
    write('predicted_output.wav', fs, pred_clean_y)  # Save as WAV file 
    

    

