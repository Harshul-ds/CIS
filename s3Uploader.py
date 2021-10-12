#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3, os, sys, shutil, glob
from botocore.exceptions import NoCredentialsError

from keys import ACCESS_KEY, SECRET_KEY
    

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
#tenantId = str(sys.argv[1])
#fileName = str(sys.argv[2])

def main(tenantId, fileName): 

    # rootFolder = "/home/ubuntu/CIS/Visualizations/"
    with open('inputs.txt', 'r') as file:
        input_lines = [line.strip() for line in file]
        rootFolder=input_lines[0]
    outFolder = rootFolder + tenantId + '/'
    
    for file in os.listdir(outFolder):
        if file.endswith(".jpg"):
            os.remove(os.path.join(outFolder, file))
        if file.endswith(".avi"):
            os.remove(os.path.join(outFolder, file))
        if fileName in file:
            upload_file_bucket = "aisteth-audio-visualization-dev"
            upload_file_key = tenantId + '/' + str(file)  
            upload_to_aws(outFolder + file, upload_file_bucket, upload_file_key)
        
    # if upload_to_aws is True:
    #     shutil.rmtree(outFolder)
    #     print("Cleanup Completed")
