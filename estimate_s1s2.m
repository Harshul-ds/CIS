function estimate_s1s2(tenantId,fileName)
dfile=[datestr(now,'mm-dd-yyyy'),'.txt']; % logfile
diary(dfile); %dairy for logging

inputfileName = 'inputs.txt';
FID = fopen(inputfileName);
data = textscan(FID,'%s');
fclose(FID);
stringData = string(data{:});
rootFolder = stringData(1); 
outFolder = (rootFolder + tenantId + "/");

% create if directory doesnt exist
if ~exist(outFolder, 'dir') % create o/p directory if it doesn't exist
       mkdir(outFolder);
end

FS=2000;
framelen=5; % in sec
wlen=round(framelen*FS);
BPM0=72;F0=BPM0/60;
st_winlen=0.05;
st_winshift=1/FS;
st_Nlen=round(st_winlen*FS);
st_Nshift=round(st_winshift*FS);
delta=0.01; % percentage of tolerance 

[A0]=denoising(tenantId, fileName);
sig = A0;
%[sig,fs]=audioread(file);
%[sig,fs]=audioread("/home/ubuntu/CIS/Sridhar.m4a");
if size(sig,1)<size(sig,2)
    sig=sig';
end
if size(sig,2)>1
    sig=sig(:,1);
end

%sig=resample(sig,FS,fs);sigo=sig;

S1_detect=0*sig;
S2_detect=0*sig;
HRPall=[];
for i=1:round(wlen/2):length(sig)-wlen+1
   
%     disp(['Segment starting at ' num2str(i/FS) 'sec']);
    sigseg=sig(i:i+wlen-1);
    [HRP,HR]=gethr(sigseg,FS,F0);HRPall=[HRPall; HRP];
    sigseg=[zeros(round(HRP*FS),1); sigseg];
    st_eng = cal_steng (sigseg, st_Nlen, st_Nshift);
%     PitchPeriod_inFrames=round(2*HRP/st_winshift);
%     zero_st_eng=[zeros(PitchPeriod_inFrames,1); st_eng];
    [ll, cs, loc_sig, ind1s ind2s]=dp_prog(st_eng,round(HRP/st_winshift),delta);

    
    
%     figure(99);
%     subplot(411);plot(sigseg);title([HRP HR]);axis tight;
%     hold on;stem(ind1s,ones(1,length(ind1s)),'r');
%     hold on;stem(ind2s,ones(1,length(ind2s)),'m');hold off;
%     subplot(412);plot([1:length(st_eng)]*st_winshift,st_eng);axis tight;
%     subplot(413); plot(cs); axis tight
%     subplot (414); stem(ll); axis tight
%     pause
    
    ind1s=ind1s-round(HRP*FS)+1;ind1s(ind1s<1)=[];
    S1_detect(i-1+ind1s)=S1_detect(i-1+ind1s)+1;
    
    ind2s=ind2s-round(HRP*FS)+1;ind2s(ind2s<1)=[];
    S2_detect(i-1+ind2s)=S2_detect(i-1+ind2s)+1;

   
end

%%%%%%%%%%%%%
i=length(sig)-wlen+1;
sigseg=sig(i:i+wlen-1);
[HRP,HR]=gethr(sigseg,FS,F0);HRPall=[HRPall; HRP];
sigseg=[zeros(round(HRP*FS),1); sigseg];
st_eng = cal_steng (sigseg, st_Nlen, st_Nshift);
%     PitchPeriod_inFrames=round(2*HRP/st_winshift);
%     zero_st_eng=[zeros(PitchPeriod_inFrames,1); st_eng];
[ll, cs, loc_sig, ind1s ind2s]=dp_prog(st_eng,round(HRP/st_winshift),delta);

% figure(99);
% subplot(411);plot(sigseg);title([HRP HR]);axis tight;
% hold on;stem(ind1s,ones(1,length(ind1s)),'r');
% hold on;stem(ind2s,ones(1,length(ind2s)),'m');hold off;
% subplot(412);plot([1:length(st_eng)]*st_winshift,st_eng);axis tight;
% subplot(413)outputBucketURL; plot(cs); axis tight
% subplot(414); stem(ll); axis tight
% % pause

ind1s=ind1s-round(HRP*FS);ind1s(ind1s<1)=[];
S1_detect(i-1+ind1s)=S1_detect(i-1+ind1s)+1;

ind2s=ind2s-round(HRP*FS)+1;ind2s(ind2s<1)=[];
S2_detect(i-1+ind2s)=S2_detect(i-1+ind2s)+1;

video = VideoWriter(outFolder + tenantId + '_' + fileName + '_' +'5seconds_visualization','Motion JPEG AVI'); %create the video object
video.FrameRate=1;
open(video);
figure(100);

subplot(211);plot([1:length(sig)]/FS,sig);hold on;
% stem([1:length(sig)]/FS,S1_detect,'r');stem([1:length(sig)]/FS,S2_detect,'m');
for i=1:wlen:length(sig)
   
    if i+wlen-1<length(sig)
        
        subplot(211);plot([i:i+wlen-1]/FS,sig(i:i+wlen-1),'k');
        subplot(212);plot([i:i+wlen-1]/FS,sig(i:i+wlen-1));hold on;
        S1 = stem([i:i+wlen-1]/FS,S1_detect(i:i+wlen-1)>0,'r');
	    S2 = stem([i:i+wlen-1]/FS,S2_detect(i:i+wlen-1)>0,'b');hold off
        legend([S1, S2], {'S1','S2'}, 'Location','northeast', 'NumColumns',1);
        legend boxoff;
        %pause
        baseFileName = sprintf('%s_%s_frame%02d.jpg',tenantId, string(fileName), i);
        %fullFileName = fullfile(outBucket, baseFileName);
        localFileName = fullfile(outFolder, baseFileName);
        %imwrite(getframe(gcf).cdata, fullFileName)
        imwrite(getframe(gcf).cdata, localFileName)

        %I = readimage(imds, sprintf('%2d.png', i));
        frame=getframe(gcf);     
        %I = imread(fullFileName);
        writeVideo(video,frame);
    end
end

close(video);

%zip(outFolder + tenantId + '_assets',{'*.jpg','*.png', '*.avi'}, outFolder);

%[status,cmdout] = system(sprintf('aws s3 cp %s%s_%s_5frames_visualization.avi %s',outFolder, tenantId, fileName, outBucket)); % python clean up 1) zip, cleanup, mp4

subplot(211);

S1_locations=sort(find(S1_detect>0)/FS);
S2_locations=sort(find(S2_detect>0)/FS);
Med_HRP=median(HRPall);
tmp = location_postprocess(S1_locations,0.8*Med_HRP);
S1_locations_final = location_postprocess(tmp,0.8*Med_HRP);
tmp = location_postprocess(S2_locations,0.8*Med_HRP);
S2_locations_final = location_postprocess(tmp,0.8*Med_HRP);
%[S1TP, S1TN, S1FP, S2TP, S2TN, S2FP]=evaluate_s1_s2(GTfile,S1_locations_final,S2_locations_final);
%S1acc = (S1TP + S1TN)/(S1TP + S1TN + S1FP)*100;
%S2acc = (S2TP + S2TN)/(S2TP + S2TN + S2FP)*100;
%s = struct("S1_identification_accuracy", round(S1acc), "S2_identification_accuracy", round(S2acc));
%accuracy=jsonencode(s)


% figure(100);
% subplot(211);hold on;stem(S1_locations_final,ones(1,length(S1_locations_final)),'r');
% stem(S2_locations_final,ones(1,length(S2_locations_final)),'m');
% hold off;
end
