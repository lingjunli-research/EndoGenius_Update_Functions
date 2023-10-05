# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 11:15:15 2023

@author: lawashburn
"""

import pandas as pd
import csv

results_directory = r"C:\Users\lawashburn\Documents\EndoGeniusDistributions\version_assessment_output\EndoGenius_v1.0.2\pt4_InnoWizard\rawDB_rawMS\2021_0817_CoG_1"
formatted_spectra_path = r"D:\EndoGenius_Updates\v1.0.3_SLbuild\pt01_new_rawfile_formatting\output\2021_0817_CoG_1_formatted_RT_old.txt"
output_directory = r"D:\EndoGenius_Updates\v1.0.3_SLbuild\pt02_output"
fragment_error = 0.02

backslash_index1 = results_directory.rfind('\\')
backslash_index2 = results_directory.rfind('/')

if backslash_index1 > backslash_index2:
    backslash_index = backslash_index1
elif backslash_index2 >= backslash_index1:
    backslash_index = backslash_index2

base_file_path = results_directory[0:(backslash_index+1)]

tissue_type = results_directory.replace(base_file_path,'')

final_target_results_path = results_directory + '\\final_results__target.csv'
final_target_results = pd.read_csv(final_target_results_path)

sequence_log = []
mz_log = []
z_log = []
rt_log = []
peaks_count_log = []
peak_list_log = []

formatted_spectra = pd.read_csv(formatted_spectra_path, sep=",",skiprows=[0], names= ['m/z','resolution','charge','intensity','MS2','scan_number','precursor_charge','retention time','null'])

for row in final_target_results.index:
    peak_summary = []
    
    sequence = final_target_results['Peptide'][row]
    scan = final_target_results['Scan'][row]
    
    sequence_formatted = sequence.replace('(Glu->pyro-Glu)','(pyroGlu)')
    sequence_formatted = sequence_formatted.replace('(Gln->pyro-Glu)','(pyroGlu)')
    
    sample_fragment_path = results_directory + '\\fragment_matches\\' + sequence_formatted + '_' + str(scan) + '_fragment_report.csv'
    
    sample_fragment = pd.read_csv(sample_fragment_path)
    
    sample_fragment_filtered = sample_fragment[sample_fragment['Fragment error (Da)'] <= fragment_error]

    spectra_scan_filtered = formatted_spectra[formatted_spectra['scan_number'] == scan]
    rt = spectra_scan_filtered['retention time'].iloc[0]

    for line in sample_fragment_filtered.index:

        frag_name = sample_fragment_filtered['ion'][line]
        frag_mz = sample_fragment_filtered['Fragment actual m/z'][line]
        frag_z = sample_fragment_filtered['Fragment actual charge'][line]
        frag_int = sample_fragment_filtered['Fragment actual intensity'][line]        
        summary = frag_name + ':' + str(frag_mz) + ':' + str(frag_z) + ':' + str(frag_int)
        peak_summary.append(summary)

    
    mz = sample_fragment_filtered['Precursor actual m/z'].iloc[0]
    z = sample_fragment_filtered['Precursor actual charge'].iloc[0]
    length = len(sample_fragment_filtered)
    
    sequence_log.append(sequence)
    mz_log.append(mz)
    z_log.append(z)
    peaks_count_log.append(length)
    peak_list_log.append(peak_summary)
    rt_log.append(rt)
    
individual_library = pd.DataFrame(
    {'Sequence': sequence_log,
     'm/z': mz_log,
     'z': z_log,
     'RT':rt_log,
     'peak count': peaks_count_log,
     'peak list':peak_list_log
    })

output_path = output_directory + '\\spectral_library_' + tissue_type + '.csv'
with open(output_path,'w',newline='') as filec:
        writerc = csv.writer(filec)
        individual_library.to_csv(filec,index=False)