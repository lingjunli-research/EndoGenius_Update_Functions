# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 14:05:27 2023

@author: lawashburn
"""

import csv
import pandas as pd
import os

MS2_path = r"D:\EndoGenius_Updates\v1.0.3_SLbuild\pt01_new_rawfile_formatting\input\MS2_eval_short.ms2"
output_directory = r"D:\EndoGenius_Updates\v1.0.3_SLbuild\pt01_new_rawfile_formatting\output"

######## Extracting sample name ###############
backslash_index1 = MS2_path.rfind('\\')
backslash_index2 = MS2_path.rfind('/')

if backslash_index1 > backslash_index2:
    backslash_index = backslash_index1
elif backslash_index2 >= backslash_index1:
    backslash_index = backslash_index2

base_file_path = MS2_path[0:(backslash_index+1)]

tissue_type = MS2_path.replace(base_file_path,'')
tissue_type = tissue_type.replace('.ms2','')

#########Start formatting################
with open(MS2_path) as input:
    lst = [line.strip() for line in input] #appending each entry of the raw file to a list

new_list= []
final_lst = []
final_lst.append(['m/z', 'resolution', 'charge', 'intensity', 'MS2','scan_number','precursor_charge','retention time'])
ms2_list = []

new = lst

for i in new:
    new_list.append(i.split())
    if '@' in i:
        x = i.split()
        for y in x:
            if '@' in y:
                ms2 = y[0:y.index('@')]
                ms2_list.append(str(ms2))

header_list = new_list[0:26]
new_list = new_list[26:] # starts from line 26 to remove the first few header lines so that program could proceed
seperation_list = []
RT_list = []
scan_number_list = []    
precursor_charge_list = []

##This section is for extracting info from first scan

for i in header_list:
    if 'S' in i:
        scan_number_list.append(i[1])
    if 'Z' in i:
        precursor_charge_list.append(i[1])
    if 'RetTime' in i:
        RT_list.append(i[2])

##This section is for extracting info for the rest of the scans
for i in range(len(new_list)):
    if 'RetTime' in new_list[i]:
        RT_list.append(new_list[i][2])
    if 'PrecursorInt' in new_list[i]:
        seperation_list.append(i+2)
    if 'S' in new_list[i]:
        scan_number_list.append(new_list[i][1])
    if 'Z' in new_list[i]:
        precursor_charge_list.append(new_list[i][1])

seperation_pairs = []
start = 0
for i in range(int(len(seperation_list)/2)):
    seperation_pairs.append((seperation_list[i+start],seperation_list[i+start+1]))
    start +=1 
 
update_index = 0
for start,end in seperation_pairs:
    start += update_index
    end += update_index
    new_list[start:end] = '-'
    update_index -= (end-start-1)

ms2_list_index = 0
scan_number_index = 0
precursor_charge_index = 0
ret_time_index = 0

for element in new_list:
    if element == '-':
        ms2_list_index+=1
        scan_number_index+=1
        precursor_charge_index+=1
        ret_time_index+=1
        continue   
    element.append(ms2_list[ms2_list_index])
    element.append(scan_number_list[scan_number_index])
    element.append(precursor_charge_list[precursor_charge_index])
    element.append(RT_list[ret_time_index])
    final_lst.append(element)

final_list_formatted = []

incorrect_entries = ['S','I','Z']

for entry in final_lst:
    if entry[0] not in incorrect_entries:
        final_list_formatted.append(entry)

out_name = output_directory + '\\'+tissue_type+'_formatted.txt'
with open(out_name,'w') as output:
    for i in final_list_formatted:
        for j in i:
            output.write(str(j + ','))
        output.write('\n')

