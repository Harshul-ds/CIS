function [gci, cost_sig, loc_sig, indices_s1 indices_s2]=dp_prog(lp_res,avg,delta)

if ~isempty(find(isnan(lp_res)==1))
    error('First argument can not have NaN in its element');
end

lamb=1;
lmin=floor((1-delta)*avg);
lmax=floor((1+delta)*avg);
cost_sig=zeros(1,numel(lp_res));
loc_sig=zeros(1,numel(lp_res));
for i=lmax+1:numel(lp_res)
    for j=lmin:lmax
        cost(j-lmin+1)=cost_sig(i-j)-lamb*lp_res(i-j);
    end
    l1=find(cost==min(cost));
    loc_sig(i)=i-lmin-l1(1)+1;
%     if(loc_sig(loc_sig(i))>0)
%     if(lp_res(loc_sig(i))<.3*lp_res(loc_sig(loc_sig(i))))
%         loc_sig(i)=loc_sig(loc_sig(i));
%     end
%     end
    cost_sig(i)=min(cost);
end
k=0;
last_sig=cost_sig(max(1,numel(cost_sig)-2*lmax):numel(cost_sig));
l12=find(last_sig==min(last_sig));
last_loc=numel(cost_sig)-2*lmax+l12(1)-1;
indices=[last_loc];
while(k==0)
    if loc_sig(indices(1))<lmax+20
        break;
    end
    indices=[loc_sig(indices(1))  indices];
end
gci=zeros(1,numel(lp_res));
gci(indices)=1;


%%%%%%%%%%%
for i=-round(avg/2):1:round(avg/2)

    ids=indices+i;
    ids(find(ids>length(lp_res)))=[];
    ids(find(ids>length(lp_res)))=[];
    s2sum(i+round(avg/2)+1)=mean(lp_res(ids));
    
end
i1=round([0:.2:1]*length(s2sum));i1(1)=1;
[pksval,pksloc]=findpeaks(s2sum);
indr=(find(pksloc>=i1(4) & pksloc<=i1(6)));indl=(find(pksloc>=i1(1) & pksloc<=i1(3)));
% max(pksval(indr))
% max(pksval(indl))
if isempty(indl)
%     disp('r1');
    [v, id]=max(pksval(indr));
    s2loc=pksloc(indr(id))-round(avg/2);
elseif isempty(indr)
%     disp('l1');
    [v, id]=max(pksval(indl));
    s2loc=pksloc(indl(id))-round(avg/2);
else
    if max(pksval(indr))>max(pksval(indl))
%         disp('r');
        [v, id]=max(pksval(indr));
        s2loc=pksloc(indr(id))-round(avg/2);
    else
%         disp('l');
        [v, id]=max(pksval(indl));
        s2loc=pksloc(indl(id))-round(avg/2);
    end
end
% indr
% v
% id
% s2loc
% figure(101);plot(-round(avg/2):1:round(avg/2),s2sum);title(s2loc);
if s2loc>0
    indices_s1=indices;indices_s2=indices+s2loc;
    indices_s2(indices_s2>length(lp_res))=[];
    indices_s2(indices_s2<1)=[];
else
    indices_s2=indices;indices_s1=indices+s2loc;
    indices_s1(indices_s1>length(lp_res))=[];
    indices_s1(indices_s1<1)=[];
end
