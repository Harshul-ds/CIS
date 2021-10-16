function [A0] = denoising(data_path, fileName)
%% Load a signal
FS=2000;
addpath(data_path);
% inputfileName = 'inputs.txt';
% FID = fopen(inputfileName);
% data = textscan(FID,'%s');
% fclose(FID);
% stringData = string(data{:});
% inBucket = stringData(2);

inBucket = string(data_path);
%inBucket = "s3://aih-audio-visualization-dev/MichiganDS/"; % S3 bucket to read files from

file = (inBucket + fileName);
[sigO,fs]=audioread(file);
info = audioinfo(file);
if info.NumChannels > 1
    sigO = sigO(:,1);
end
%[sigO,fs]=audioread('/home/shailesh/Jayadeva/Normal/Sridhar/Sridhar.m4a');

% if fs ~= 2000
%     sigR=resample(sigO,FS,fs);
% else
%     sigR = sigO;
% end
sigR = sigO;
%figure; 
%subplot(2,1,1); plot(sigO); grid on; title('Original signal'); axis tight; 
%subplot(2,1,2); plot(sigR); title('Original signal resampled'); 
%axis tight; grid on;
%audiowrite('/home/shailesh/Jayadeva/Normal/Sridhar/resampled.wav',sigR,FS);

%% Multilevel Wavelet decomposition
sig=sigR;
[C,L] = wavedec(sig,5,'coif5');
%[C,L] = wavedec(sigN20,5,'db1');

% coefficients of all components are concatenated in C; L lengths of each component

% Extracting approximation coeffs
cA5 = appcoef(C,L,'coif5',5);

% Extracting detail coeffs
cD5 = detcoef(C,L,5);
cD4 = detcoef(C,L,4);
cD3 = detcoef(C,L,3);
cD2 = detcoef(C,L,2);
cD1 = detcoef(C,L,1);

% Reconstructing the approximations and details
A1 = wrcoef('a',C,L,'coif5',1);
A2 = wrcoef('a',C,L,'coif5',2);
A3 = wrcoef('a',C,L,'coif5',3);
A4 = wrcoef('a',C,L,'coif5',4);
A5 = wrcoef('a',C,L,'coif5',5);

D1 = wrcoef('d',C,L,'coif5',1);
D2 = wrcoef('d',C,L,'coif5',2);
D3 = wrcoef('d',C,L,'coif5',3);
D4 = wrcoef('d',C,L,'coif5',4);
D5 = wrcoef('d',C,L,'coif5',5);

%subplot(6,1,1); plot(A4); title('Approximation A4')
%subplot(6,1,2); plot(D1); title('Detail D1')
%subplot(6,1,3); plot(D2); title('Detail D2')
%subplot(6,1,4); plot(A5); title('Detail D3')
%subplot(6,1,5); plot(D4); title('Detail D4')
%subplot(6,1,6); plot(D5); title('Detail D5')

%% Adaptive thresholding - D4

% condition-wise estimation of threshold of D4
med75 =prctile(D4, 75); % Level of noise present 
m = mean(D4);
v = var(D4);
% syms T;
% T = piecewise(med75 < v, med75*[1-(v-med75)] , med75 > v & med75 < m, med75, med75 > m, med75+(med75-m));
if med75 < v
    T = med75*(1-(v-med75));
    disp("Low level noise, threshold adapted accordingly");
elseif med75 > v && med75 < m
    T=med75;
    disp("mid level noise, threshold adapted accordingly");
else med75 > m
    T=med75+(med75-m);
    disp("high level noise, threshold adapted accordingly")
end

%% Threshold rescaling - D4

M=median(D4); % median of absolute value of detail coefficients at level 4
noiseVariance=M/0.6745; 
T_rescaled=T*noiseVariance; %rescale of estimated threshold value based on mln  

%% Applying threshold - D4

alpha=1;
if med75 <= v
    beta=1.3;
else
    beta=1.4;
end
%beta=2;

T1=alpha*T_rescaled;
T2=beta*T_rescaled;
%figure(100);plot(D4); hold on
D4((T1 < abs(D4)) & (abs(D4) < T2)) = (D4((T1 < abs(D4)) & (abs(D4) < T2)).^3/T2.^2);
D4(abs(D4) < T1) = 0;


%% Adaptive thresholding - D5

% condition-wise estimation of threshold of D4
med75 =prctile(D5, 75); % Level of noise present 
m = mean(D5);
v = var(D5);
% syms T;
% T = piecewise(med75 < v, med75*[1-(v-med75)] , med75 > v & med75 < m, med75, med75 > m, med75+(med75-m));
if med75 < v
    T = med75*(1-(v-med75));
    disp("Low level noise, threshold adapted accordingly");
elseif med75 > v && med75 < m
    T=med75;
    disp("mid level noise, threshold adapted accordingly");
else med75 > m
    T=med75+(med75-m);
    disp("high level noise, threshold adapted accordingly");
end

%% Threshold rescaling - D5

M=median(D5); % median of absolute value of detail coefficients at level 4
noiseVariance=M/0.6745; 
T_rescaled=T*noiseVariance; %rescale of estimated threshold value based on mln  

%% Applying threshold - D5

alpha=1;
if med75 <= v
    beta=1.3;
else
    beta=1.4;
end
%beta=2;

T1=alpha*T_rescaled;
T2=beta*T_rescaled;

figure(101);plot(D5); hold on
D5((T1 < abs(D5)) & (abs(D5) < T2)) = (D5((T1 < abs(D5)) & (abs(D5) < T2)).^3/T2.^2);
D5(abs(D5) < T1) = 0;


%% Reconstructing the original signal
%D5=0*D5;
C=[D4;D5];
L=[length(D4);length(D5)];
A0 = waverec(C,L,'coif5');
figure,
subplot(2,1,1); plot(A0); subplot(2,1,2); plot(sig);%subplot(3,1,3); plot(sigO);

%% writing of denoised signal 
%audiowrite(outFolder + tenantId + '_' + fileName + '_' +'denoised.wav', A0 ,FS);

end
