import numpy as np

def location_postprocess(locations, estHRP, flag=0):
    i=0
    count=0
    locations_final = np.zeros((len(locations),))
    while i<len(locations)-1:
        if (locations[i+1]-locations[i])>estHRP:
            locations_final[count]=locations[i]
            i=i+1
            flag=1
        else:
            locations_final[count]=(locations[i]+locations[i+1])/2
            i=i+2
            flag=0

        count=count+1

    if flag:
        locations_final[count]=locations[i]

    return locations_final
