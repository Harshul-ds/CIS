function locations_final = location_postprocess(locations,estHRP)

i=1;count=1;
while i<length(locations)
    if locations(i+1)-locations(i)>estHRP
        locations_final(count)=locations(i);
        i=i+1;
        flag=1;
    else
        locations_final(count)=(locations(i)+locations(i+1))/2;
        i=i+2;
        flag=0;
    end
    count=count+1;
end
if flag
    locations_final(count)=locations(i);
end