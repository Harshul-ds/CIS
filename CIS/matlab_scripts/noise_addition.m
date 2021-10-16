function [sig] = noise_addition(sig0, dB)

% Adds student-t noise

S = mean(sig0.^2);
SNR = 10^(dB/10);
v = trnd(5, 1, length(sig0));
v = v./(mean(v.^2));
sig  = sig0 + (S/SNR)*v;
end