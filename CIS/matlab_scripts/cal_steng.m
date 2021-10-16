function [out]= cal_steng (sig, Nlen, Nshift)


% k*Nshift+1:k*Nshift+Nlen

% ind=1:Nshift:length(sig)-2*Nlen;
% indall=[ind];
% for j=1:Nlen-1
%     indall=[indall; indall(end,:)+1];
% end
% sig_seg=sig(indall);
% out=mean(sig_seg.^2,1);

out1=filtfilt(ones(1,Nlen)/100,1,sig.^2);
out=out1(1:Nshift:end);

