# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 15:53:42 2018

@author: NIA-VISI16
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 09:46:23 2018

@author: NIA-VISI16

Copyright (C) 2014-2018 The HDF Group
Copyright (C) 2014 John Evans

This example code illustrates how to access and visualize a LaRC CALIPSO file 
in file in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    python CAL_LID_L2_VFM-ValStage1-V3-02.2011-12-31T23-18-11ZD.hdf.v.py

The HDF file must be in your current working directory.

Tested under: Python 2.7.14 :: Anaconda custom (64-bit)
Last updated: 2018-05-22
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from astropy.time import Time
from pyhdf.SD import SD, SDC
from matplotlib import colors
import datetime
import time
#from grain import Grain
from pkg_resources import resource_filename
DEFAULT_LEAP_SECONDS = resource_filename(__name__, 'leap-seconds')#check using this name 

#from mpl_toolkits.basemap 
#import Basemap
#class Grain(object):

#CALIPSO_EPOCH = datetime(1993, 1, 1)

output_csv_filename="output.csv"
outputfile=open(output_csv_filename,'w')

FILE_NAME = 'C:/Users/defadmin/Desktop/Medha_Majety/vfm_plot/CAL_LID_L2_VFM-Standard-V4-10.2014-02-13T05-20-10ZD_Subset.hdf'
FILE_NAME2 = 'C:/Users/defadmin/Desktop/Medha_Majety/vfm_plot/CAL_LID_L1-Standard-V4-10.2014-02-13T05-20-10ZD_Subset (2)'

# Identify the data field.
DATAFIELD_NAME = 'Feature_Classification_Flags'

hdf = SD(FILE_NAME, SDC.READ)
        
# Read dataset.
data2D = hdf.select(DATAFIELD_NAME)
data = data2D[:,:]

# Read geolocation datasets.
latitude = hdf.select('Latitude')
lat = latitude[:]
longitude = hdf.select('Longitude')
lon= longitude[:]
profile_Time= hdf.select('Profile_Time')
time= profile_Time[:]        
feature_classification_flags = hdf.select('Feature_Classification_Flags')
flags= feature_classification_flags[:]
profile_time_Level1 = hdf.select('Profile_Time')
time_l1= profile_time_Level1[:]
#altitude = hdf.select('Feature_Classification_Flags')
#alt=altitude[:]

# Extract Feature Type only (1-3 bits) through bitmask.
#data = data & 7
mask=np.uint16(0b0000000000000111)
strat_aero=data&mask
strat_aero_indices=np.where(strat_aero==4)
#[x,y]=np.where(strat_aero==4,[x,y])

mask=np.uint16(0b0000010000000100)
volcanic_ash=data&mask
volcanic_ash_indices=np.where(volcanic_ash==1028)
print(volcanic_ash_indices)

#Making a header and then reading it into the csv file
output_header='Name,Latitude,Longitude,Time,Altitude,Description\n'
outputfile.write(output_header)
print(output_header)
#Converts unix time to standard datetime, and appends all the values to an empty array: time_array
'''
#timestamp_offset=78787965879
j=0
time_array = []
for j in range (0,103):
    timestamp = time[volcanic_ash_indices[0][j]][0]
    #value = datetime.datetime.fromtimestamp(timestamp+timestamp_offset)
    value = datetime.datetime.fromtimestamp(timestamp)
    value = add_offsetyears(value,)
    #print(value.strftime('%Y+23-%m-%d %H:%M:%S'))
    time_array.append(value.strftime('%Y-%m-%d %H:%M:%S'))
    #print (time_array[j])
    j =j+1
'''
'''
j=0
time_array = []
for j in range (0,103):
    timestamp = time[volcanic_ash_indices[0][j]][0]
    value=datetime.utcfromtimestamp(timestamp)
    time_array.append(value)
    print (time_array[j])
    j =j+1
#utc = datetime(1980, 1, 6) + timedelta(seconds=1092121243.0 - (35 - 19))
    '''
#

j=0
time_array = []
timestamp_array = []
for j in range (0,103):
    timestamp = time[volcanic_ash_indices[0][j]][0]
    timestamp_array.append(timestamp)
    value = datetime.datetime.fromtimestamp(timestamp)
    #print(value.strftime('%Y-%m-%d %H:%M:%S'))
    time_array.append(value.strftime('%Y-%m-%d %H:%M:%S'))
    #print (time_array[j])
    j =j+1

l=0
m=time_array[l]
for l in range (0,103):    
    def find_nearest(time_l1, m):
        time_l1 = np.asarray(time_l1)
        idx = (np.abs(time_l1 - m)).argmin()
        return time_l1[idx]
        print(find_nearest(time_l1, value))
        # 0.568743859261
    l+=1
'''
j=0
time_array = []
for j in range (0,103):
    timestamp = time[volcanic_ash_indices[0][j]][0]
    value = datetime.datetime.fromtimestamp(timestamp)
    #print(value.strftime('%Y-%m-%d %H:%M:%S'))
    time_array.append(value.str('%Y-%m-%d %H:%M:%S'))
    #print (time_array[j])
    j =j+1
'''
#Takes the second array, which is the feature classification flags, and finds which chunk of atmosphere it's located under
#and then manipulates the index value accordingly to find the altitude
#appends it to an empty array: altitude_array
altitude_array = []
i=0
for i in range (0,103):
    #for dim1 in (volcanic_ash_indices[1]):
        #if volcanic_ash_indices[1][i]>=1 and (volcanic_ash_indices[1][i]<=165):
        #type='high'
        if volcanic_ash_indices[1][i]>=1 and volcanic_ash_indices[1][i]<=55:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 55-volcanic_ash_indices[1][i]
            altitude= ((30.1-20.2)/54)*alt_temp
            altitude=altitude+20.2
            altitude_array.append(altitude)
            print (altitude,"test 1")
            

        elif volcanic_ash_indices[1][i]>=55 and volcanic_ash_indices[1][i]<=110:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 110-volcanic_ash_indices[1][i]
            altitude= ((30.1-20.2)/54)*alt_temp
            altitude=altitude+20.2
            altitude_array.append(altitude)
            print (altitude,"test 2")
            
        
        elif volcanic_ash_indices[1][i]>=111 and volcanic_ash_indices[1][i]<=165:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 165-volcanic_ash_indices[1][i]
            altitude= ((30.1-20.2)/54)*alt_temp
            altitude=altitude+20.2
            altitude_array.append(altitude)
            print (altitude,"test 3")
            
                
    #else:
     #   if volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=1165:
      #      type='medium'
        elif volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=365:
              volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
              alt_temp= 365-volcanic_ash_indices[1][i]
              altitude= ((20.1-8.2)/199)*alt_temp
              altitude=altitude+8.2
              altitude_array.append(altitude)
              print (altitude,"test 4")
              

        elif volcanic_ash_indices[1][i]>=366 and volcanic_ash_indices[1][i]<=565:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 565-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude=altitude+8.2
            altitude_array.append(altitude)
            print (altitude,"test 5")
            
        
        elif volcanic_ash_indices[1][i]>=566 and volcanic_ash_indices[1][i]<=765:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 765-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude=altitude+8.2
            altitude_array.append(altitude)
            print (altitude,"test 6")
            

        elif volcanic_ash_indices[1][i]>=766 and volcanic_ash_indices[1][i]<=965:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 965-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude=altitude+8.2
            altitude_array.append(altitude)
            print (altitude,"test 7")
            
                                    
        elif volcanic_ash_indices[1][i]>=966 and volcanic_ash_indices[1][i]<=1165:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 1165-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude=altitude+8.2
            altitude_array.append(altitude)
            print (altitude,"test 8")
             #if volcanic_ash_indices[1][i]>=1166 & volcanic_ash_indices[1][i]<=5515:
        #   type='low'
        elif volcanic_ash_indices[1][i]>=1166 and volcanic_ash_indices[1][i]<=1455:
             volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
             alt_temp= 1455-volcanic_ash_indices[1][i]
             altitude= ((8.2--0.5)/289)*alt_temp
             altitude=altitude+-0.5
             altitude_array.append(altitude)
             print (altitude,"test 9") 
             
        elif volcanic_ash_indices[1][i]>=1456 and volcanic_ash_indices[1][i]<=1745:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 1745-volcanic_ash_indices[1][i]
               altitude= ((8.2--0.5)/289)*alt_temp
               altitude=altitude+-0.5
               altitude_array.append(altitude)
               print (altitude,"test 10") 
               
        elif volcanic_ash_indices[1][i]>=1746 and volcanic_ash_indices[1][i]<=2035:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 2035-volcanic_ash_indices[1][i]
               altitude= ((8.2--0.5)/289)*alt_temp
               altitude=altitude+-0.5
               altitude_array.append(altitude)
               print (altitude,"test 11") 
               
        elif volcanic_ash_indices[1][i]>=2036 and volcanic_ash_indices[1][i]<=2325:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 2325-volcanic_ash_indices[1][i]
               altitude= ((8.2--0.5)/289)*alt_temp
               altitude=altitude+-0.5
               altitude_array.append(altitude)
               print (altitude,"test 12") 
               
        elif volcanic_ash_indices[1][i]>=2326 and volcanic_ash_indices[1][i]<=2615:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 2615-volcanic_ash_indices[1][i]
               altitude= ((8.2--0.5)/289)*alt_temp
               altitude=altitude+-0.5
               altitude_array.append(altitude)
               print (altitude,"test 13")  
               
        elif volcanic_ash_indices[1][i]>=2616 and volcanic_ash_indices[1][i]<=2905:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 2905-volcanic_ash_indices[1][i]
               altitude= ((8.2--0.5)/289)*alt_temp
               altitude=altitude+-0.5
               altitude_array.append(altitude)
               print (altitude,"test 14")    
               
        elif volcanic_ash_indices[1][i]>=2906 and volcanic_ash_indices[1][i]<=3195:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 3195-volcanic_ash_indices[1][i]
               altitude= ((8.2--0.5)/289)*alt_temp
               altitude=altitude+-0.5
               altitude_array.append(altitude)
               print (altitude,"test 15")   
               
        elif volcanic_ash_indices[1][i]>=3196 and volcanic_ash_indices[1][i]<=3485:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 3485-volcanic_ash_indices[1][i]
               altitude= ((8.2--0.5)/289)*alt_temp
               altitude=altitude+-0.5
               altitude_array.append(altitude)
               print (altitude,"test 16")   
             
        elif volcanic_ash_indices[1][i]>=3486 and volcanic_ash_indices[1][i]<=3775:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 3775-volcanic_ash_indices[1][i]
            altitude= ((8.2--0.5)/289)*alt_temp
            altitude=altitude+-0.5
            altitude_array.append(altitude)
            print (altitude,"test 17")
             
        elif volcanic_ash_indices[1][i]>=3776 and volcanic_ash_indices[1][i]<=4065:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4065-volcanic_ash_indices[1][i]
            altitude= ((8.2--0.5)/289)*alt_temp
            altitude=altitude+-0.5
            altitude_array.append(altitude)
            print (altitude,"test 18")
             
        elif volcanic_ash_indices[1][i]>=4066 and volcanic_ash_indices[1][i]<=4355:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4355-volcanic_ash_indices[1][i]
            altitude= ((8.2--0.5)/289)*alt_temp
            altitude=altitude+-0.5
            altitude_array.append(altitude)
            print (altitude,"test 19")
             
        elif volcanic_ash_indices[1][i]>=4356 and volcanic_ash_indices[1][i]<=4645:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4645-volcanic_ash_indices[1][i]
            altitude= ((8.2--0.5)/289)*alt_temp
            altitude=altitude+-0.5
            altitude_array.append(altitude)
            print (altitude,"test 20")
             
        elif volcanic_ash_indices[1][i]>=4646 and volcanic_ash_indices[1][i]<=4935:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4935-volcanic_ash_indices[1][i]
            altitude= ((8.2--0.5)/289)*alt_temp
            altitude=altitude+-0.5
            altitude_array.append(altitude)
            print (altitude,"test 21")
             
        elif volcanic_ash_indices[1][i]>=4936 and volcanic_ash_indices[1][i]<=5225:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 5225-volcanic_ash_indices[1][i]
            altitude= ((8.2--0.5)/289)*alt_temp
            altitude=altitude+-0.5
            altitude_array.append(altitude)
            print (altitude,"test 22")
             
        elif volcanic_ash_indices[1][i]>=5226 and volcanic_ash_indices[1][i]<=5515:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 5515 -volcanic_ash_indices[1][i]
            altitude= ((8.2--0.5)/289)*alt_temp
            altitude=altitude+-0.5
            altitude_array.append(altitude)
            print (altitude,"test 23") 
            
i=i+1


#putting together all of the latitude, longitude, altitude, and time values
#and then reading it and writing it in a seperate csv file
i=0
a=0
b=0
for i in range (0,103):
    #c=volcanic_ash_indices[0][a]
    #d=volcanic_ash_indices[1][b]
    #print(lat[dim0][i],',',lon[dim0][i],',',time[dim0][i],",",flags[c][d])
    output_arr=[i, lat[volcanic_ash_indices[0][i]][0], lon[volcanic_ash_indices[0][i]][0], time_array[i],altitude_array[i], 'Vol Ash']
    output_string=','.join(map(str,output_arr))
    print(output_string)
    outputfile.write(output_string)
    outputfile.write('\n')
    #print('Latitude:',lat[dim0][i],'Longitude:',lon[dim0][i],'Time:',time_array)
   #for dim1 in volcanic_ash_indices[0]:
    i=i+1
    a=a+1
    b=b+1

outputfile.close()   



'''
#i=0
#for dim1 in (volcanic_ash_indices[1]):
 #   print (volcanic_ash_indices[1][i])
  #  i=i+1
i=0
while i<= len(volcanic_ash_indices[1])-1:
    if volcanic_ash_indices[1][i]>=1 and (volcanic_ash_indices[1][i]<=165):
        type='high'
        if volcanic_ash_indices[1][i]>=1 and volcanic_ash_indices[1][i]<=55:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 55-volcanic_ash_indices[1][i]
            altitude= ((30.1-20.2)/54)*alt_temp
            print ("test 1",volcanic_ash_indices[1][i])
            continue

        else:
            if volcanic_ash_indices[1][i]>=55 and volcanic_ash_indices[1][i]<=110:
                volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
                alt_temp= 110-volcanic_ash_indices[1][i]
                altitude= ((30.1-20.2)/54)*alt_temp
                print ("test 2",volcanic_ash_indices[1][i])
                break

            else: 
                if volcanic_ash_indices[1][i]>=111 and volcanic_ash_indices[1][i]<=165:
                    volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
                    alt_temp= 165-volcanic_ash_indices[1][i]
                    altitude= ((30.1-20.2)/54)*alt_temp
                    print ("test 3",volcanic_ash_indices[1][i])
                    break

    else:
        if volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=1165:
            type='medium'
            if volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=365:
                volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
                alt_temp= 365-volcanic_ash_indices[1][i]
                altitude= ((20.1-8.2)/199)*alt_temp
                print ("test 4",volcanic_ash_indices[1][i])
                break

            else:
                if volcanic_ash_indices[1][i]>=366 and volcanic_ash_indices[1][i]<=565:
                    volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
                    alt_temp= 565-volcanic_ash_indices[1][i]
                    altitude= ((20.1-8.2)/199)*alt_temp
                    print ("test 5",volcanic_ash_indices[1][i])
                    break
        
                else :
                    if volcanic_ash_indices[1][i]>=566 and volcanic_ash_indices[1][i]<=765:
                        volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
                        alt_temp= 765-volcanic_ash_indices[1][i]
                        altitude= ((20.1-8.2)/199)*alt_temp
                        print ("test 6",volcanic_ash_indices[1][i])
                        break
            #print (volcanic_ash_indices[1][0])

                    else: 
                        if volcanic_ash_indices[1][i]>=766 and volcanic_ash_indices[1][i]<=965:
                            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
                            alt_temp= 965-volcanic_ash_indices[1][i]
                            altitude= ((20.1-8.2)/199)*alt_temp
                            print ("test 7",volcanic_ash_indices[1][i])
                            break

                        else:
                            if volcanic_ash_indices[1][i]>=966 and volcanic_ash_indices[1][i]<=1165:
                                volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
                                alt_temp= 1165-volcanic_ash_indices[1][i]
                                altitude= ((20.1-8.2)/199)*alt_temp
                                print ("test 8",volcanic_ash_indices[1][i])
                                break
print ("Altitude:",volcanic_ash_indices[1][i],altitude)      
i+=1

#THIS IS THE CODE FOR THE ALTITUDE
altitude_array = []
i=0
for i in range (0,103):
    #for dim1 in (volcanic_ash_indices[1]):
        #if volcanic_ash_indices[1][i]>=1 and (volcanic_ash_indices[1][i]<=165):
        #type='high'
        if volcanic_ash_indices[1][i]>=1 and volcanic_ash_indices[1][i]<=55:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 55-volcanic_ash_indices[1][i]
            altitude= ((30.1-20.2)/54)*alt_temp
            altitude_array.append(altitude)
            print (altitude,"test 1")
            

        elif volcanic_ash_indices[1][i]>=55 and volcanic_ash_indices[1][i]<=110:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 110-volcanic_ash_indices[1][i]
            altitude= ((30.1-20.2)/54)*alt_temp
            altitude_array.append(altitude)
            print (altitude,"test 2")
            
        
        elif volcanic_ash_indices[1][i]>=111 and volcanic_ash_indices[1][i]<=165:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 165-volcanic_ash_indices[1][i]
            altitude= ((30.1-20.2)/54)*alt_temp
            altitude_array.append(altitude)
            print (altitude,"test 3")
            
                
    #else:
     #   if volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=1165:
      #      type='medium'
        elif volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=365:
              volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
              alt_temp= 365-volcanic_ash_indices[1][i]
              altitude= ((20.1-8.2)/199)*alt_temp
              altitude_array.append(altitude)
              print (altitude,"test 4")
              

        elif volcanic_ash_indices[1][i]>=366 and volcanic_ash_indices[1][i]<=565:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 565-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude_array.append(altitude)
            print (altitude,"test 5")
            
        
        elif volcanic_ash_indices[1][i]>=566 and volcanic_ash_indices[1][i]<=765:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 765-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude_array.append(altitude)
            print (altitude,"test 6")
            

        elif volcanic_ash_indices[1][i]>=766 and volcanic_ash_indices[1][i]<=965:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 965-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude_array.append(altitude)
            print (altitude,"test 7")
            
                                    
        elif volcanic_ash_indices[1][i]>=966 and volcanic_ash_indices[1][i]<=1165:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 1165-volcanic_ash_indices[1][i]
            altitude= ((20.1-8.2)/199)*alt_temp
            altitude_array.append(altitude)
            print (altitude,"test 8")
            
        
       #if volcanic_ash_indices[1][i]>=1166 & volcanic_ash_indices[1][i]<=5515:
        #   type='low'
        if volcanic_ash_indices[1][i]>=1166 and volcanic_ash_indices[1][i]<=1455:
             volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
             alt_temp= 1455-volcanic_ash_indices[1][i]
             volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
              
        if volcanic_ash_indices[1][i]>=1456 and volcanic_ash_indices[1][i]<=1745:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 1745-volcanic_ash_indices[1][i]
               volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
                
        if volcanic_ash_indices[1][i]>=1746 and volcanic_ash_indices[1][i]<=2035:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 2035-volcanic_ash_indices[1][i]
               volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
                
        if volcanic_ash_indices[1][i]>=2036 and volcanic_ash_indices[1][i]<=2325:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 2325-volcanic_ash_indices[1][i]
               volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
                
        if volcanic_ash_indices[1][i]>=2326 and volcanic_ash_indices[1][i]<=2615:
               volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
               alt_temp= 2615-volcanic_ash_indices[1][i]
               volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
                
        if volcanic_ash_indices[1][i]>=2616 and volcanic_ash_indices[1][i]<=2905:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 2905-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=2906 and volcanic_ash_indices[1][i]<=3195:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 3195-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=3196 and volcanic_ash_indices[1][i]<=3485:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 3485-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=3486 and volcanic_ash_indices[1][i]<=3775:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 3775-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=3776 and volcanic_ash_indices[1][i]<=4065:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4065-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=4066 and volcanic_ash_indices[1][i]<=4355:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4355-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=4356 and volcanic_ash_indices[1][i]<=4645:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4645-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=4646 and volcanic_ash_indices[1][i]<=4935:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 4935-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=4936 and volcanic_ash_indices[1][i]<=5225:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 5225-volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp
             
        if volcanic_ash_indices[1][i]>=5226 and volcanic_ash_indices[1][i]<=5515:
            volcanic_ash_indices[1][i]=volcanic_ash_indices[1][i]-1
            alt_temp= 5515 -volcanic_ash_indices[1][i]
            volcanic_ash_indices[1][i]= ((8.2--0.5)/289)*alt_temp  
'''     
'''   
index=len(strat_aero_indices)-1
while index>0:
    strat_data=data[strat_aero_indices[index]]
    mask=np.uint16(0b0000010000000000)
    # mask=1024
    volcano_flags=strat_data&mask
    if volcano_flags[strat_aero_indices[index]]==1024:
        print('found volcanic ash at index:',index)
    index=index-1

mask=np.uint16(0b0000010000000100)
data=np.uint16 (0b0111110001111100)
mtest1=np.uint16(np.left_shift(mask,8))
dtest1=np.uint16(np.left_shift(data,8))
data=dtest1&mtest1


if data==mtest1:
    print("it works")
    mtest2=np.uint16(np.right_shift(mask,8))
    dtest2=np.uint16(np.right_shift(data,8))
    data=mtest2&dtest2
    if data==mtest2:
        print("it works pt2")
'''
# Subset latitude values for the region of interest (40N to 62N).
# See the output of CAL_LID_L2_VFM-ValStage1-V3-02.2011-12-31T23-18-11ZD.hdf.py example.
#lat = lat[3500:4000]
size = lat.shape[0]
    
# You can visualize other blocks by changing subset parameters.
#  data2d = data[3500:3999, 0:164]    # 20.2km to 30.1km
#  data2d = data[3500:3999, 165:1164] #  8.2km to 20.2km

# data2d = data[3500:4000, 1165:]  # -0.5km to  8.2km
#data2d = data[3500:4000, 1165:]  # -0.5km to  8.2km
data2d = data[:, 1165:]  # -0.5km to  8.2km
data3d = np.reshape(data2d, (size, 15, 290))
data = data3d[:,0,:]

# Focus on cloud (=2) data only.
data[data > 2] = 0;
data[data < 2] = 0;
data[data == 2] = 1;

# Generate altitude data according to file specification [1].
alt = np.zeros(290)

# You can visualize other blocks by changing subset parameters.
#  20.2km to 30.1km
# for i in range (0, 54):
#       alt[i] = 20.2 + i*0.18;
#  8.2km to 20.2km
# for i in range (0, 199):
#       alt[i] = 8.2 + i*0.06;
# -0.5km to 8.2km
for i in range (0, 289):
    alt[i] = -0.5 + i*0.03


alt1=(39.79567, 39.49629, 39.196907, 38.897522, 38.59814, 38.29876, 37.99938, 37.699997, 37.400616, 37.101234, 36.801853, 36.502472, 36.20309, 35.90371, 35.604324, 35.304943, 35.00556, 34.70618, 34.4068, 34.107418, 33.808037, 33.508656, 33.209274, 32.909893, 32.61051, 32.311127, 32.011745, 31.712366, 31.412983, 31.113602, 30.81422, 30.51484, 30.215458, 29.975952, 29.796324, 29.616693, 29.437065, 29.257437, 29.077806, 28.898178, 28.71855, 28.53892, 28.359291, 28.179663, 28.000032, 27.820404, 27.640776, 27.461147, 27.281517, 27.101889, 26.92226, 26.74263, 26.563002, 26.383373, 26.203743, 26.024115, 25.844486, 25.664856, 25.485228, 25.3056, 25.125969, 24.94634, 24.766712, 24.587084, 24.407454, 24.227825, 24.048197, 23.868567, 23.688938, 23.50931, 23.32968, 23.150051, 22.970423, 22.790792, 22.611164, 22.431536, 22.251907, 22.072277, 21.892649, 21.71302, 21.53339, 21.353762, 21.174133, 20.994503, 20.814875, 20.635246, 20.455616, 20.275988, 20.156235, 20.09636, 20.036482, 19.976606, 19.916729, 19.856853, 19.796978, 19.7371, 19.677225, 19.617348, 19.557472, 19.497595, 19.43772, 19.377844, 19.317966, 19.258091, 19.198214, 19.138338, 19.07846, 19.018585, 18.958708, 18.898832, 18.838957, 18.77908, 18.719204, 18.659327, 18.599451, 18.539574, 18.479698, 18.419823, 18.359945, 18.30007, 18.240192, 18.180317, 18.12044, 18.060564, 18.000687, 17.940811, 17.880936, 17.821058, 17.761183, 17.701305, 17.64143, 17.581553, 17.521677, 17.461802, 17.401924, 17.342049, 17.282171, 17.222296, 17.162418, 17.102543, 17.042667, 16.98279, 16.922915, 16.863037, 16.803162, 16.743284, 16.683409, 16.623531, 16.563656, 16.50378, 16.443903, 16.384027, 16.32415, 16.264275, 16.204397, 16.144522, 16.084646, 16.024769, 15.964892, 15.905016, 15.84514, 15.785264, 15.725388, 15.665511, 15.605635, 15.545758, 15.485882, 15.426005, 15.36613, 15.306253, 15.246377, 15.186501, 15.126624, 15.066748, 15.006871, 14.946995, 14.887119, 14.827243, 14.767366, 14.70749, 14.647614, 14.587737, 14.527861, 14.467984, 14.408109, 14.348232, 14.288356, 14.228479, 14.168603, 14.1087265, 14.04885, 13.988974, 13.929098, 13.869222, 13.809345, 13.749469, 13.689592, 13.629716, 13.5698395, 13.509963, 13.450088, 13.390211, 13.330335, 13.270458, 13.210582, 13.150705, 13.090829, 13.030952, 12.971077, 12.911201, 12.851324, 12.791448, 12.731571, 12.671695, 12.611818, 12.551942, 12.492066, 12.43219, 12.3723135, 12.312437, 12.252561, 12.192684, 12.132808, 12.072931, 12.013056, 11.953179, 11.893303, 11.833426, 11.77355, 11.713674, 11.653797, 11.593921, 11.534045, 11.474169, 11.414292, 11.354416, 11.294539, 11.234663, 11.174787, 11.114911, 11.055035, 10.995158, 10.935282, 10.875405, 10.815529, 10.755652, 10.695776, 10.6359005, 10.576024, 10.516148, 10.456271, 10.396395, 10.336518, 10.276642, 10.216765, 10.15689, 10.097013, 10.037137, 9.977261, 9.917384, 9.857508, 9.797631, 9.737755, 9.677879, 9.618003, 9.558126, 9.49825, 9.438374, 9.378497, 9.318621, 9.258744, 9.198869, 9.138992, 9.079116, 9.019239, 8.959363, 8.899487, 8.83961, 8.779734, 8.719858, 8.659982, 8.600105, 8.540229, 8.480352, 8.420476, 8.3605995, 8.300723, 8.240848, 8.19594, 8.166001, 8.136064, 8.106126, 8.076187, 8.046249, 8.016311, 7.986373, 7.9564347, 7.9264965, 7.8965583, 7.86662, 7.836682, 7.8067436, 7.776806, 7.7468677, 7.7169294, 7.686991, 7.657053, 7.627115, 7.5971766, 7.5672383, 7.5373006, 7.5073624, 7.477424, 7.447486, 7.4175477, 7.3876095, 7.3576713, 7.3277335, 7.2977953, 7.267857, 7.237919, 7.2079806, 7.1780424, 7.148104, 7.118166, 7.088228, 7.05829, 7.028352, 6.9984136, 6.9684753, 6.938537, 6.908599, 6.8786607, 6.848723, 6.8187847, 6.7888465, 6.7589083, 6.72897, 6.699032, 6.6690936, 6.6391554, 6.6092176, 6.5792794, 6.549341, 6.519403, 6.4894648, 6.4595265, 6.4295883, 6.39965, 6.3697124, 6.339774, 6.309836, 6.2798977, 6.2499595, 6.2200212, 6.190083, 6.160145, 6.130207, 6.100269, 6.0703306, 6.0403924, 6.010454, 5.980516, 5.9505777, 5.9206395, 5.890702, 5.8607635, 5.8308253, 5.800887, 5.770949, 5.7410107, 5.7110724, 5.681134, 5.6511965, 5.6212583, 5.59132, 5.561382, 5.5314436, 5.5015054, 5.471567, 5.441629, 5.411691, 5.381753, 5.3518147, 5.3218765, 5.2919383, 5.262, 5.232062, 5.2021236, 5.172186, 5.1422477, 5.1123095, 5.082371, 5.052433, 5.022495, 4.9925566, 4.9626184, 4.9326806, 4.9027424, 4.872804, 4.842866, 4.8129277, 4.7829895, 4.7530513, 4.723113, 4.6931753, 4.663237, 4.633299, 4.6033607, 4.5734224, 4.543484, 4.513546, 4.4836082, 4.45367, 4.423732, 4.3937936, 4.3638554, 4.333917, 4.303979, 4.2740407, 4.244103, 4.2141647, 4.1842265, 4.1542883, 4.12435, 4.094412, 4.0644736, 4.0345354, 4.0045977, 3.9746592, 3.9447212, 3.914783, 3.8848448, 3.8549066, 3.8249686, 3.7950304, 3.7650921, 3.735154, 3.705216, 3.6752777, 3.6453395, 3.6154013, 3.5854633, 3.555525, 3.5255868, 3.4956486, 3.4657106, 3.4357724, 3.4058342, 3.375896, 3.345958, 3.3160198, 3.2860816, 3.2561433, 3.2262053, 3.1962671, 3.166329, 3.1363907, 3.1064527, 3.0765145, 3.0465763, 3.016638, 2.9867, 2.9567618, 2.9268236, 2.8968854, 2.8669474, 2.8370092, 2.807071, 2.7771327, 2.7471948, 2.7172565, 2.6873183, 2.65738, 2.6274421, 2.597504, 2.5675657, 2.5376275, 2.5076895, 2.4777513, 2.447813, 2.4178748, 2.3879368, 2.3579986, 2.3280604, 2.2981222, 2.2681842, 2.238246, 2.2083077, 2.1783695, 2.1484315, 2.1184933, 2.088555, 2.0586169, 2.028679, 1.9987407, 1.9688025, 1.9388644, 1.9089261, 1.878988, 1.8490498, 1.8191117, 1.7891736, 1.7592354, 1.7292973, 1.699359, 1.669421, 1.6394827, 1.6095446, 1.5796064, 1.5496683, 1.5197301, 1.489792, 1.4598538, 1.4299157, 1.3999774, 1.3700393, 1.3401011, 1.310163, 1.2802248, 1.2502867, 1.2203485, 1.1904104, 1.1604722, 1.130534, 1.1005958, 1.0706577, 1.0407195, 1.0107814, 0.9808432, 0.950905, 0.92096686, 0.8910287, 0.86109054, 0.8311524, 0.8012142, 0.77127606, 0.7413379, 0.71139973, 0.6814616, 0.6515234, 0.62158525, 0.5916471, 0.5617089, 0.53177077, 0.5018326, 0.47189447, 0.4419563, 0.41201815, 0.38208, 0.35214183, 0.32220367, 0.2922655, 0.26232734, 0.23238918, 0.20245102, 0.17251286, 0.1425747, 0.112636544, 0.08269838, 0.05276022, 0.022822062, -0.0071161, -0.03705426, -0.066992424, -0.09693058, -0.12686874, -0.1568069, -0.18674506, -0.21668322, -0.24662139, -0.27655956, -0.3064977, -0.33643585, -0.36637402, -0.39631218, -0.42625034, -0.4561885, -0.6208484, -0.92023003, -1.2196116, -1.5189933, -1.8183749)
    
# Contour the data on a grid of latitude vs. pressure
latitude, altitude = np.meshgrid(lat, alt)


# Make a color map of fixed colors.
cmap = colors.ListedColormap(['white', 'blue', 'blue'])

# Define the bins and normalize.
bounds = np.linspace(0,2,3)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


long_name = 'Feature Type (Bits 1-3) in Feature Classification Flag'
basename = os.path.basename(FILE_NAME)
plt.contourf(latitude, altitude, np.rot90(data,1), cmap=cmap)
plt.title('{0}\n{1}'.format(basename, long_name))
plt.xlabel('Latitude (degrees north)')
plt.ylabel('Altitude (km)')

fig = plt.gcf()

# Create a second axes for the discrete colorbar.
ax2 = fig.add_axes([0.93, 0.2, 0.01, 0.6])
cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, boundaries=bounds)
cb.ax.set_yticklabels(['Others','', 'Cloud'], fontsize=6)

# plt.show()
pngfile = "{0}.v.py.png".format(basename)
fig.savefig(pngfile)
    
