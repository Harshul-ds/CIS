function files = GetFilesList_aiSteth(data_path)
%GETFILESLIST Summary of this function goes here
%   Detailed explanation goes here

files=dir([data_path '*.wav']);
files={files.name};
end

