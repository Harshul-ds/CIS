#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing required modules 
from zipfile import ZipFile 
from os.path import basename
import os 
#tenantId = "apollo"
#fileName = "14"
# tenantId = str(sys.argv[1])
# fileName = str(sys.argv[2])



def get_all_file_paths(directory): 
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        filepath = [ fi for fi in files if fi.endswith((".jpg", ".avi", ".wav")) ]
        for filename in filepath: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            
            file_paths.append(filepath) 
      
    # returning all file paths 
    return file_paths   		 

def main(tenantId, fileName): 
    # path to folder which needs to be zipped 
    with open('inputs.txt', 'r') as file:
        input_lines = [line.strip() for line in file]
        rootFolder=input_lines[0]
    inDir = rootFolder + tenantId  
    directory = inDir
  
    # calling function to get all file paths in the directory 
    file_paths = get_all_file_paths(directory) 
  
    # printing the list of all files to be zipped 
    print('Following files will be zipped:') 
    for file_name in file_paths: 
        print(file_name) 
  
    # writing files to a zipfile 
    with ZipFile(inDir + "/" + tenantId + "_" + fileName + '_5seconds_visualization' + '_assests.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths: 
            zip.write(file, basename(file)) 
  
    print('All files zipped successfully!')         
  
  
# main() 