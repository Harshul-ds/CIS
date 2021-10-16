clear;
addpath(genpath('.\'));
data_path= 'Michigan_Heart_Sounds\';
annot_data_path='..\annotation\';
addpath(genpath(data_path));
rng('default');
%% parameters
dbs = 'MH';
% dbs='PASCAL';
files=GetFilesList_MH(data_path);
delta=25e-3; %for evaluation metrics
Fs=2000;
global debug;
debug=1;
%% method 
noise_dur=0.2;
for j=8:length(files)
    tic;
%     [sig,fs]=GetWavefile(data_path,dbs,files{j});
    % Downsample to 2kHz
    
%     sig=sig(1:10*fs);
%     t_sig=length(sig)/fs;
    t_sig = 1e2;
    [S1_locations_final, S2_locations_final] = estimate_s1s2(files{j});
    [Begin,End,Event] = GetAnnotations_MH(annot_data_path,files{j});
    
    inds=find(End>t_sig);
    Event(inds)=[];
    Begin(inds)=[];
    End(inds)=[];
    
    [S1TP(j), S1TN(j), S1FP(j), S2TP(j), S2TN(j), S2FP(j)] = TPTNFS_aihighway( Begin,End,Event,S1_locations_final,S2_locations_final);
    
    [S1_Se(j),S1_Pp(j),S1_FS(j),S2_Se(j),S2_Pp(j),S2_FS(j),far_S1,missed_S1,far_S2,missed_S2] = FS_Physionet2(Begin,End,Event,S1_locations_final,S2_locations_final,delta);
    
    toc;
    disp([j, S1_Se(j),S1_Pp(j),S1_FS(j),S2_Se(j),S2_Pp(j),S2_FS(j)]);
end