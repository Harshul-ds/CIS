#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import moviepy.editor as moviepy

#tenantId = "apollo"
#fileName = "14"

def conversion(tenantId, fileName):
    # tenantId = str(sys.argv[1])
    # fileName = str(sys.argv[2])
    with open('inputs.txt', 'r') as file:
        input_lines = [line.strip() for line in file]
        rootFolder=input_lines[0]
    outFolder = rootFolder + tenantId + "/"
        
    clip = moviepy.VideoFileClip(outFolder + tenantId + "_" + fileName + "_" + "5seconds_visualization.avi")
    clip.write_videofile(outFolder + tenantId + "_" + fileName + "_" + "5seconds_visualization.mp4")



