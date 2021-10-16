function files = GetAnnotList_aiSteth(data_path)
%GETFILESLIST Summary of this function goes here
%   Detailed explanation goes here

files=dir([data_path]);
files={files.name};
end

