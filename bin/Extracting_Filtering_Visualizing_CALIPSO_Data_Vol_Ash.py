# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:43:22 2018

@author: NIA-VISI16
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 15:53:42 2018

@author: NIA-VISI16
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 09:46:23 2018

@author: NIA-VISI16


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
import math
#from grain import Grain
from pkg_resources import resource_filename



DIFFERENCE_BETWEEN_TIMES = 0.744
#from mpl_toolkits.basemap 
#import Basemap
#class Grain(object):

#CALIPSO_EPOCH = datetime(1993, 1, 1)
#Intializes two blank arrays: one for the actual attuenuated backscatter values
#The other for the indices of where the attenuated backscatter values are located
#making an output csv file to transfer all the python code to and then writing
att_back_arr=[]
att_back_arr_indices=[]
output_csv_filename="output.csv"
outputfile=open(output_csv_filename,'w')
#LID_LEV2 = 'C:/Users/defadmin/Desktop/Medha_Majety/vfm_plot/CAL_LID_L2_VFM-Standard-V4-10.2014-02-13T05-20-10ZD_Subset.hdf'
LID_LEV2 = '../data/CAL_LID_L2_VFM-Standard-V4-10.2014-02-13T05-20-10ZD_Subset.hdf'
LID_LEV1 = '../data/CAL_LID_L1-Standard-V4-10.2014-02-13T05-20-10ZD.hdf'

# Identify the data field.
DATAFIELD_NAME = 'Feature_Classification_Flags'

read_L2 = SD(LID_LEV2, SDC.READ)
process_L1=True
try:
    read_L1 = SD(LID_LEV1, SDC.READ)
    profile_time_Level1 = read_L1.select('Profile_Time')
    time_l1= profile_time_Level1[:]
    attenuated_backscatter = read_L1.select('Total_Attenuated_Backscatter_532')
    att_back = attenuated_backscatter[:]
except Exception as e:
    print('LID_LEV1 granule not in ../data. Skipping lookup of Total_Attenuated_Backscatter_532 in: '+LID_LEV1)
    process_L1=False     
# Read dataset.
data2D = read_L2.select(DATAFIELD_NAME)
data = data2D[:,:]

# Read geolocation datasets.
#selects for latitude
latitude = read_L2.select('Latitude')
lat = latitude[:]
#selects for longitude
longitude = read_L2.select('Longitude')
lon= longitude[:]
#selects for profile time(level 2)
profile_Time= read_L2.select('Profile_Time')
time= profile_Time[:]       
#selects for feautre classification flags 
feature_classification_flags = read_L2.select('Feature_Classification_Flags')
flags= feature_classification_flags[:]
#selects for UTC time (level 2)
profile_UTC_time = read_L2.select('Profile_UTC_Time')
profile_UTC = profile_UTC_time[:]
#altitude = hdf.select('Feature_Classification_Flags')
#alt=altitude[:]

# Extract Feature Type only (1-3 bits) through bitmask.
#data = data & 7
mask=np.uint16(0b0000000000000111)
strat_aero=data&mask
#Strat_aero is the first filter to identify volcanic ash, and it is located in bit 2, so 100 or 4
#Find the indices where there is stratospheric aerosol using a numpy command
strat_aero_indices=np.where(strat_aero==4)

#next step in filtering: volcanic ash
#locating in bit 1 so 10000000000, but to ensure that strat_aero is still being selected, you must do
#10000000100
mask=np.uint16(0b0000010000000100)
volcanic_ash=data&mask
volcanic_ash_indices=np.where(volcanic_ash==1028)
print(volcanic_ash_indices)

#Making a header and then reading it into the csv file
output_header='Name,Latitude,Longitude,Time,Altitude,Description\n'
outputfile.write(output_header)
print(output_header)
#Converts tai time to utc, and appends all the values to an empty array: time_array
def TAItoUTC(tai_time_value):

    #Convert float in TAI93 (since 1JAN93 epoch) to UTC in isot format

    t93 = Time('1993-01-01T00:00:00.000', format='isot', scale='utc')

    epoch93 = t93.gps

    tai93time = Time(tai_time_value+epoch93, format='gps', scale="utc")

    utc_time=tai93time.isot

    return utc_time
#intializing a blank time array, converting tai to utc
#And then appending that array with utc time converted values
time_array = []

num_indices=len(volcanic_ash_indices[1])
for j in range (0,num_indices):
    time2 = TAItoUTC(time[volcanic_ash_indices[0][j]][0])
    time_array.append(time2)
print (time_array)

#making a time array that contains the tai time
og_time_array = []
for j in range(0,num_indices):
    og_time_array.append(time[volcanic_ash_indices[0][j]][0])

    

# returns dictionary containing CAL_LID_L1 index, Profile_Time_val, attenuated_backscatter array
def find_nearest(time_l1, test_time):
    dict_out={}
    try:
        time_l1 = np.asarray(time_l1)
        idx = (np.abs(time_l1 - test_time)).argmin()
        
        dict_out['index']=idx
        dict_out['Profile_Time_val']=time_l1[idx][0]
        dict_out['attenuated_backscatter']=att_back[idx]
        #print ('CAL_LID_L1 index:',idx,'CAL_LID_L2_VFM Profile_Time:',test_time)
    except Exception as e:
        print(e,test_time)
    return dict_out
#searches through all the index values of the block and then adds the corresponding offset value
#Offsett value depends on where you are horizontally (in the three main blocks), if you are the first then the offset value is 0
#Offset value is 0.744*some constant
#that constant is multiplied by a varying coefficient
#that coefficient depends on where the block is in the row and how many rows there are in the block
for i in range (0,num_indices):
        if volcanic_ash_indices[1][i]>=1 and volcanic_ash_indices[1][i]<=55:
            test_time = og_time_array[i]
            print (test_time,"test 1")
            

        elif volcanic_ash_indices[1][i]>=55 and volcanic_ash_indices[1][i]<=110:
               test_time = float(1/3*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 2")
            
        
        elif volcanic_ash_indices[1][i]>=111 and volcanic_ash_indices[1][i]<=165:
               test_time = float(2/3*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 3")
            
                
    #else:
     #   if volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=1165:
      #      type='medium'
        elif volcanic_ash_indices[1][i]>=166 and volcanic_ash_indices[1][i]<=365:
              test_time = og_time_array[i]
              print (test_time,"test 4")
              

        elif volcanic_ash_indices[1][i]>=366 and volcanic_ash_indices[1][i]<=565:
               test_time = float(0.2*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 5")
            
        
        elif volcanic_ash_indices[1][i]>=566 and volcanic_ash_indices[1][i]<=765:
               test_time = float(0.4*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 6")
            

        elif volcanic_ash_indices[1][i]>=766 and volcanic_ash_indices[1][i]<=965:
               test_time = float(0.6*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 7") 
                                    
        elif volcanic_ash_indices[1][i]>=966 and volcanic_ash_indices[1][i]<=1165:
               test_time = float(0.8*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 8") 
        
        elif volcanic_ash_indices[1][i]>=1166 and volcanic_ash_indices[1][i]<=1455:
             test_time = og_time_array[i]
             print (test_time,"test 9") 
             
        elif volcanic_ash_indices[1][i]>=1456 and volcanic_ash_indices[1][i]<=1745:
               test_time = float(1/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 10") 
               
        elif volcanic_ash_indices[1][i]>=1746 and volcanic_ash_indices[1][i]<=2035:
               test_time = float(2/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 11")
               
        elif volcanic_ash_indices[1][i]>=2036 and volcanic_ash_indices[1][i]<=2325:
               test_time = float(3/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 12")
               
        elif volcanic_ash_indices[1][i]>=2326 and volcanic_ash_indices[1][i]<=2615:
               test_time = float(4/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 13") 
               
        elif volcanic_ash_indices[1][i]>=2616 and volcanic_ash_indices[1][i]<=2905:
               test_time = float(5/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 14")     
               
        elif volcanic_ash_indices[1][i]>=2906 and volcanic_ash_indices[1][i]<=3195:
               test_time = float(6/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 15")   
               
        elif volcanic_ash_indices[1][i]>=3196 and volcanic_ash_indices[1][i]<=3485:
               test_time = float(7/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 16")   
             
        elif volcanic_ash_indices[1][i]>=3486 and volcanic_ash_indices[1][i]<=3775:
               test_time = float(8/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 17")
             
        elif volcanic_ash_indices[1][i]>=3776 and volcanic_ash_indices[1][i]<=4065:
               test_time = float(9/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 18")
             
        elif volcanic_ash_indices[1][i]>=4066 and volcanic_ash_indices[1][i]<=4355:
               test_time = float(10/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 19")
             
        elif volcanic_ash_indices[1][i]>=4356 and volcanic_ash_indices[1][i]<=4645:
               test_time = float(11/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 20")
             
        elif volcanic_ash_indices[1][i]>=4646 and volcanic_ash_indices[1][i]<=4935:
               test_time = float(12/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 21")
             
        elif volcanic_ash_indices[1][i]>=4936 and volcanic_ash_indices[1][i]<=5225:
               test_time = float(13/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 22")
             
        elif volcanic_ash_indices[1][i]>=5226 and volcanic_ash_indices[1][i]<=5515:
               test_time = float(14/15*DIFFERENCE_BETWEEN_TIMES)
               test_time= test_time+ og_time_array[i]
               print (test_time,"test 23")
        if(process_L1):        
            nearest=find_nearest(time_l1, test_time)
            att_back_arr.append(nearest['attenuated_backscatter'])
            att_back_arr_indices.append(nearest['index'])
        #print(nearest['index'],nearest['Profile_Time_val'],nearest['attenuated_backscatter'])


#Takes the second array, which is the feature classification flags, and finds which chunk of atmosphere it's located under
#and then manipulates the index value accordingly to find the altitude
#appends it to an empty array: altitude_array
altitude_array = []
#i=0
for i in range (0,num_indices):
   
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

#putting together all of the latitude, longitude, altitude, and time values
#and then reading it and writing it in a seperate csv file

for i in range (0,num_indices):
   
    #print(lat[dim0][i],',',lon[dim0][i],',',time[dim0][i],",",flags[c][d])
    output_arr=[i, lat[volcanic_ash_indices[0][i]][0], lon[volcanic_ash_indices[0][i]][0],altitude_array[i]*1000, 'Vol Ash']
    output_string=','.join(map(str,output_arr))
    print(output_string)
    outputfile.write(output_string)
    outputfile.write('\n')
    #print('Latitude:',lat[dim0][i],'Longitude:',lon[dim0][i],'Time:',time_array)

outputfile.close()   




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

#function for writing the csv into kml
def writekml(data_dict,output_filename):
    
    
    outputfile=open(output_filename,'w')
    #hardcoding the correct header and then writing it
    header='''<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>\n'''
    outputfile.write(header)
    index=0
    #iterating through the array in order to print out all dimensions 
    for lla in data_dict['lon_lat_alt_arr']:
        placemark= '<Placemark>\n'
        #names, index,and time were all stored in a dictionary and then called on
        placemark+='<name>'+str(data_dict['names'][index])+'</name>\n'
        #the following code is to get to print your own image or icon, instead of the
        #typical thumbtack
        placemark+='<Style><IconStyle><Icon>\n'
        placemark+='<href>http://www.pngmart.com/files/4/Circle-PNG-File.png</href>\n'
        placemark+='</Icon></IconStyle><LabelStyle><scale>0</scale></LabelStyle></Style>'
        #putting the time, index, and the backscatter values into kml
        #by calling on the dictionary, what index it is, and then casting it to a string
        level1_info='\nLevel1 file not processed'
        if(process_L1):
            level1_info=" Index Value for Level 1 Data:"+str(data_dict['index value for attenuated backscatter'][index])+" All Attenuated Backscatter Values:"+str(data_dict['attenuated_backscatter'][index])
        placemark+='<description>'+"Time:"+str(data_dict['time'][index])+level1_info+'</description>'
        #sets the extrude to 0, so that the point isn't connected to the ground, appears more elevated
        placemark+='<Point><extrude>0</extrude>'
        #sets the altitude mode to absolute, which means that the poitns can float if they want
        #calls on each of the three dimensions by calling its relative location in the array
        #order is lon, lat, alt
        placemark+='<altitudeMode>absolute</altitudeMode><coordinates>'+str(lla[1])+','+str(lla[0])+','+str(lla[2])+'</coordinates></Point>\n'
        placemark+= '</Placemark>\n'
        #writes the file
        outputfile.write(placemark)
        index+=1
    outputfile.write('\n</Document>\n</kml>')
    outputfile.close()
    return
#saves into test-CALIPSO>bin> you can name the file to whatever you want to
output_filename="plotting_volcanic_ash_points_CALIPSO.kml"
#prints out all the level 1 data
#by doing the same as above, instead just calling on the dictonary and adding the backscatter, time, and names
lon_lat_alt_arr=[]
attenuated_backscatter_arr=[]
names=[]
for i in range (0,num_indices):
    lon_lat_alt_arr.append([lat[volcanic_ash_indices[0][i]][0], lon[volcanic_ash_indices[0][i]][0],altitude_array[i]*1000])
    names.append(str(i))
    attenuated_backscatter_arr.append
    #i+=1
data_dict={'lon_lat_alt_arr':lon_lat_alt_arr , 'type':'Attenuated Backscatter', 'names':names,'attenuated_backscatter':att_back_arr, 'index value for attenuated backscatter':att_back_arr_indices, 'time': time_array}
writekml(data_dict,output_filename)
    
