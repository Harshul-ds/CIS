function x=addnoise(x,type,params)

switch type
    case 'imp_noise'
         for j=1:params.nums
             start=randi(length(x)-params.dur,1);
             inds=rand(params.dur,1)<0.5;
             msig=max(abs(x));
             noise=inds*msig(1)-(1-inds)*msig(1);
             x(start:start+params.dur-1)=noise;
         end
        
        
    case 'awgn'
           x=awgn(x,params.SNR,'measured');
    case 'gamma_noise'
        x=x+params.gain*trnd(params.gamma,length(x),1);
end
  