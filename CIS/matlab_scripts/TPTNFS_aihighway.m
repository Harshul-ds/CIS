function [S1TP, S1TN, S1FP, S2TP, S2TN, S2FP] = TPTNFS_aihighway(Begin,End,Event,s1,s2)

S1TP=0;S1TN=0;S1FP=0;S2TP=0;S2TN=0;S2FP=0;
S1count=0;S2count=0;
for i=1:length(Event)
   
    if strcmp(Event{i},'S1')
% % %         Begin(i) End(i) from S1_detect - S1TP else S1TN
        ind=find(s1>=Begin(i) & s1<=End(i));
        if ~isempty(ind)
            S1TP=S1TP+1;
        else
            S1TN=S1TN+1;
        end
        S1count=S1count+1;
    elseif strcmp(Event{i},'S2')
% % %         Begin(i) End(i) from S1_detect - S1TP else S1TN
        ind=find(s2>=Begin(i) & s2<=End(i));
        if ~isempty(ind)
            S2TP=S2TP+1;
        else
            S2TN=S2TN+1;
        end
        S2count=S2count+1;
    else
       disp('None'); 
    end
    
end
S1FP=length(s1)-S1TP;S2FP=length(s2)-S2TP;

