function [x,fs]=GetWavefile_aiSteth(data_path,name)
[x,fs]=audioread([data_path, name]);
info = audioinfo([data_path, name]);
if info.NumChannels > 1
    x = x(:,1);
end
end