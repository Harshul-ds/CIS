function [S1_Se,S1_Pp,S1_FS,S2_Se,S2_Pp,S2_FS,...
    far_S1,missed_S1,far_S2,missed_S2] = FS_Physionet(Begin,End,Event,s1,s2,delta)
%% ref: Performance of an open-source heart sound segmentation algorithm on eight independent databases
idxs=contains(Event,'S1');
[S1_Se,S1_Pp,S1_FS,far_S1,missed_S1]=ComputeMetrics(Begin(idxs),End(idxs),s1,delta);

idxs=contains(Event,'S2');
[S2_Se,S2_Pp,S2_FS,far_S2,missed_S2]=ComputeMetrics(Begin(idxs),End(idxs),s2,delta);

end

function [Se,Pp,FS,far,missed]=ComputeMetrics(beg,ends,detected,delta)

TP=0;
FP=0;
FN=0;
missed=[];
far=[];
if(isempty(beg))
    FP=FP+length(detected);
else
    cen=(beg(1)+ends(1))/2;
    N2=sum(detected<beg(1));
    if(N2>0)
        FP=FP+N2;
        far=[far cen];
    end
end


for i=1:length(beg)
    cen=(beg(i)+ends(i))/2;
    N1=sum(beg(i)<detected & detected<ends(i));
    if(i~=length(beg))
        last_beg=beg(i+1);
    else
        last_beg=length(beg);
    end
    N2=sum(detected>ends(i) & detected<last_beg);
    if(N1>0)
        TP=TP+1;
        if(N1>1)
            FP=FP+N1-1;
            inds=beg(i)<detected & detected<ends(i);
            far=[far;detected(inds)];
        end
    else
        FN=FN+1;
        missed=[missed cen];
    end
%     if(N2>0)
%         FP=FP+N2;
%         inds=detected>ends(i) & detected<last_beg;
%         if ~isempty(inds)
%             far=[far;detected(inds)];
%         end
%     end
end

Se=TP*100/(TP+FN);
Pp=TP*100/(TP+FP);
FS=2*Se*Pp/(Se+Pp);

end
