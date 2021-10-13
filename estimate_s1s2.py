from libsmop import *
# estimate_s1s2.m

    
@function
def estimate_s1s2(tenantId=None,fileName=None,*args,**kwargs):
    varargin = estimate_s1s2.varargin
    nargin = estimate_s1s2.nargin

    dfile=concat([datestr(now,'mm-dd-yyyy'),'.txt'])
# estimate_s1s2.m:2
    
    diary(dfile)
    
    inputfileName='inputs.txt'
# estimate_s1s2.m:5
    FID=fopen(inputfileName)
# estimate_s1s2.m:6
    data=textscan(FID,'%s')
# estimate_s1s2.m:7
    fclose(FID)
    stringData=string(data[arange()])
# estimate_s1s2.m:9
    rootFolder=stringData(1)
# estimate_s1s2.m:10
    outFolder=(rootFolder + tenantId + '/')
# estimate_s1s2.m:11
    # create if directory doesnt exist
    if logical_not(exist(outFolder,'dir')):
        mkdir(outFolder)
    
    FS=2000
# estimate_s1s2.m:18
    framelen=5
# estimate_s1s2.m:19
    
    wlen=round(dot(framelen,FS))
# estimate_s1s2.m:20
    BPM0=72
# estimate_s1s2.m:21
    F0=BPM0 / 60
# estimate_s1s2.m:21
    st_winlen=0.05
# estimate_s1s2.m:22
    st_winshift=1 / FS
# estimate_s1s2.m:23
    st_Nlen=round(dot(st_winlen,FS))
# estimate_s1s2.m:24
    st_Nshift=round(dot(st_winshift,FS))
# estimate_s1s2.m:25
    delta=0.01
# estimate_s1s2.m:26
    
    A0=denoising(tenantId,fileName)
# estimate_s1s2.m:28
    sig=copy(A0)
# estimate_s1s2.m:29
    #[sig,fs]=audioread(file);
#[sig,fs]=audioread("/home/ubuntu/CIS/Sridhar.m4a");
    if size(sig,1) < size(sig,2):
        sig=sig.T
# estimate_s1s2.m:33
    
    if size(sig,2) > 1:
        sig=sig(arange(),1)
# estimate_s1s2.m:36
    
    #sig=resample(sig,FS,fs);sigo=sig;
    
    S1_detect=dot(0,sig)
# estimate_s1s2.m:41
    S2_detect=dot(0,sig)
# estimate_s1s2.m:42
    HRPall=[]
# estimate_s1s2.m:43
    for i in arange(1,length(sig) - wlen + 1,round(wlen / 2)).reshape(-1):
        #     disp(['Segment starting at ' num2str(i/FS) 'sec']);
        sigseg=sig(arange(i,i + wlen - 1))
# estimate_s1s2.m:47
        HRP,HR=gethr(sigseg,FS,F0,nargout=2)
# estimate_s1s2.m:48
        HRPall=concat([[HRPall],[HRP]])
# estimate_s1s2.m:48
        sigseg=concat([[zeros(round(dot(HRP,FS)),1)],[sigseg]])
# estimate_s1s2.m:49
        st_eng=cal_steng(sigseg,st_Nlen,st_Nshift)
# estimate_s1s2.m:50
        #     PitchPeriod_inFrames=round(2*HRP/st_winshift);
#     zero_st_eng=[zeros(PitchPeriod_inFrames,1); st_eng];
        ll,cs,loc_sig,ind1s,ind2s=dp_prog(st_eng,round(HRP / st_winshift),delta,nargout=5)
# estimate_s1s2.m:53
        #     figure(99);
#     subplot(411);plot(sigseg);title([HRP HR]);axis tight;
#     hold on;stem(ind1s,ones(1,length(ind1s)),'r');
#     hold on;stem(ind2s,ones(1,length(ind2s)),'m');hold off;
#     subplot(412);plot([1:length(st_eng)]*st_winshift,st_eng);axis tight;
#     subplot(413); plot(cs); axis tight
#     subplot (414); stem(ll); axis tight
#     pause
        ind1s=ind1s - round(dot(HRP,FS)) + 1
# estimate_s1s2.m:66
        ind1s[ind1s < 1]=[]
# estimate_s1s2.m:66
        S1_detect[i - 1 + ind1s]=S1_detect(i - 1 + ind1s) + 1
# estimate_s1s2.m:67
        ind2s=ind2s - round(dot(HRP,FS)) + 1
# estimate_s1s2.m:69
        ind2s[ind2s < 1]=[]
# estimate_s1s2.m:69
        S2_detect[i - 1 + ind2s]=S2_detect(i - 1 + ind2s) + 1
# estimate_s1s2.m:70
    
    #############
    i=length(sig) - wlen + 1
# estimate_s1s2.m:76
    sigseg=sig(arange(i,i + wlen - 1))
# estimate_s1s2.m:77
    HRP,HR=gethr(sigseg,FS,F0,nargout=2)
# estimate_s1s2.m:78
    HRPall=concat([[HRPall],[HRP]])
# estimate_s1s2.m:78
    sigseg=concat([[zeros(round(dot(HRP,FS)),1)],[sigseg]])
# estimate_s1s2.m:79
    st_eng=cal_steng(sigseg,st_Nlen,st_Nshift)
# estimate_s1s2.m:80
    #     PitchPeriod_inFrames=round(2*HRP/st_winshift);
#     zero_st_eng=[zeros(PitchPeriod_inFrames,1); st_eng];
    ll,cs,loc_sig,ind1s,ind2s=dp_prog(st_eng,round(HRP / st_winshift),delta,nargout=5)
# estimate_s1s2.m:83
    # figure(99);
# subplot(411);plot(sigseg);title([HRP HR]);axis tight;
# hold on;stem(ind1s,ones(1,length(ind1s)),'r');
# hold on;stem(ind2s,ones(1,length(ind2s)),'m');hold off;
# subplot(412);plot([1:length(st_eng)]*st_winshift,st_eng);axis tight;
# subplot(413)outputBucketURL; plot(cs); axis tight
# subplot(414); stem(ll); axis tight
# # pause
    
    ind1s=ind1s - round(dot(HRP,FS))
# estimate_s1s2.m:94
    ind1s[ind1s < 1]=[]
# estimate_s1s2.m:94
    S1_detect[i - 1 + ind1s]=S1_detect(i - 1 + ind1s) + 1
# estimate_s1s2.m:95
    ind2s=ind2s - round(dot(HRP,FS)) + 1
# estimate_s1s2.m:97
    ind2s[ind2s < 1]=[]
# estimate_s1s2.m:97
    S2_detect[i - 1 + ind2s]=S2_detect(i - 1 + ind2s) + 1
# estimate_s1s2.m:98
    video=VideoWriter(outFolder + tenantId + '_' + fileName + '_' + '5seconds_visualization','Motion JPEG AVI')
# estimate_s1s2.m:100
    
    video.FrameRate = copy(1)
# estimate_s1s2.m:101
    open_(video)
    figure(100)
    subplot(211)
    plot(concat([arange(1,length(sig))]) / FS,sig)
    hold('on')
    # stem([1:length(sig)]/FS,S1_detect,'r');stem([1:length(sig)]/FS,S2_detect,'m');
    for i in arange(1,length(sig),wlen).reshape(-1):
        if i + wlen - 1 < length(sig):
            subplot(211)
            plot(concat([arange(i,i + wlen - 1)]) / FS,sig(arange(i,i + wlen - 1)),'k')
            subplot(212)
            plot(concat([arange(i,i + wlen - 1)]) / FS,sig(arange(i,i + wlen - 1)))
            hold('on')
            S1=stem(concat([arange(i,i + wlen - 1)]) / FS,S1_detect(arange(i,i + wlen - 1)) > 0,'r')
# estimate_s1s2.m:113
            S2=stem(concat([arange(i,i + wlen - 1)]) / FS,S2_detect(arange(i,i + wlen - 1)) > 0,'b')
# estimate_s1s2.m:114
            hold('off')
            legend(concat([S1,S2]),cellarray(['S1','S2']),'Location','northeast','NumColumns',1)
            legend('boxoff')
            baseFileName=sprintf('%s_%s_frame%02d.jpg',tenantId,string(fileName),i)
# estimate_s1s2.m:118
            localFileName=fullfile(outFolder,baseFileName)
# estimate_s1s2.m:120
            imwrite(getframe(gcf).cdata,localFileName)
            #I = readimage(imds, sprintf('#2d.png', i));
            frame=getframe(gcf)
# estimate_s1s2.m:125
            writeVideo(video,frame)
    
    close_(video)
    #zip(outFolder + tenantId + '_assets',{'*.jpg','*.png', '*.avi'}, outFolder);
    
    #[status,cmdout] = system(sprintf('aws s3 cp #s#s_#s_5frames_visualization.avi #s',outFolder, tenantId, fileName, outBucket)); # python clean up 1) zip, cleanup, mp4
    
    subplot(211)
    S1_locations=sort(find(S1_detect > 0) / FS)
# estimate_s1s2.m:139
    S2_locations=sort(find(S2_detect > 0) / FS)
# estimate_s1s2.m:140
    Med_HRP=median(HRPall)
# estimate_s1s2.m:141
    tmp=location_postprocess(S1_locations,dot(0.8,Med_HRP))
# estimate_s1s2.m:142
    S1_locations_final=location_postprocess(tmp,dot(0.8,Med_HRP))
# estimate_s1s2.m:143
    tmp=location_postprocess(S2_locations,dot(0.8,Med_HRP))
# estimate_s1s2.m:144
    S2_locations_final=location_postprocess(tmp,dot(0.8,Med_HRP))
# estimate_s1s2.m:145
    #[S1TP, S1TN, S1FP, S2TP, S2TN, S2FP]=evaluate_s1_s2(GTfile,S1_locations_final,S2_locations_final);
#S1acc = (S1TP + S1TN)/(S1TP + S1TN + S1FP)*100;
#S2acc = (S2TP + S2TN)/(S2TP + S2TN + S2FP)*100;
#s = struct("S1_identification_accuracy", round(S1acc), "S2_identification_accuracy", round(S2acc));
#accuracy=jsonencode(s)
    
    # figure(100);
# subplot(211);hold on;stem(S1_locations_final,ones(1,length(S1_locations_final)),'r');
# stem(S2_locations_final,ones(1,length(S2_locations_final)),'m');
# hold off;
    return
    
if __name__ == '__main__':
    pass
    