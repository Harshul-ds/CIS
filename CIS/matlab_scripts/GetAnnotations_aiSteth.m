function [ Begin,End,Event] = GetAnnotations_aiSteth(data_path,filename)
%GETANNOTATIONFILE Summary of this function goes here
%   Detailed explanation goes here

[~,~,raw] = xlsread([data_path, filename]) ;
Begin = cell2mat(raw(2:end,3));
Event = string(cell2mat(raw(2:end,2)));
End = cell2mat(raw(2:end,4));

end
 
