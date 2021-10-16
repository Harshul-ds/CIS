function [hrp,hr]=gethr(sig,fs,f0)

% % % inputs:
% % % sig: recorded signal
% % % fs: sampling freq in hz
% % % f0: a rough estimate of what the pitch freq (hz) can be
% % % 
% % % Outputs:
% % % hrp: heart rate period in seconds
% % % hr: heart rate in hz

sig_o=sig; 
sig(abs(sig)<0.8*max(abs(sig)))=0;

crit_ind=length(sig)+round(0.5455*fs); %corr to 110bpm 60/110=.5455
% crit_ind=length(sig)+round(0.05*fs); %corr to 110bpm 60/110=.5455
c_sig=xcorr(sig);
F0=round(fs/f0);
F0_range=(F0-round(F0/2)):(F0+round(F0/2));
tmpind=length(sig)+F0_range;
if tmpind(1)<crit_ind
    ids=find(tmpind>=crit_ind);
    tmpind=tmpind(ids);
else
    tmpind=[crit_ind:tmpind(1)-1 tmpind];
    
end
if tmpind(end)>length(c_sig)
    ids=find(tmpind<=length(c_sig));
    tmpind=tmpind(ids);
end
% [tmpind(1) tmpind(end) length(c_sig)]
tmp=c_sig(tmpind);
% subplot(211);plot(sig_o);hold on;plot(sig,'r');hold off;
% subplot(212);plot(c_sig);hold on;plot(tmpind,tmp,'r');hold off;
[val ind]=max(tmp);
P0=tmpind(ind)-length(sig);
hr=1/(P0/fs);
hrp=1/hr;