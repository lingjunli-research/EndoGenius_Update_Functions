# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:13:10 2023

@author: lawashburn
"""

import pandas as pd
import os
import seaborn as sns

shuffle_db_path = r"D:\Manuscripts\2023_fractionated_spectral_library\SL_build_results_processed\Brain_OG_F3F9\Shuffle_database.csv"
target_db_path = r"D:\Manuscripts\2023_fractionated_spectral_library\SL_build_results_processed\Brain_OG_F3F9\target_list.csv"
processed_results_path = r"D:\Manuscripts\2023_fractionated_spectral_library\SL_build_results_processed"
samples_processed = ['Brain_OG','PO']
mods = ['Amidated','Sulfo','Oxidation','Glu->pyro-Glu','Gln->pyro-Glu']
number_mods = [0,1,2,3]

shuffle_db = pd.read_csv(shuffle_db_path)
target_db = pd.read_csv(target_db_path)

shuffle_db['Sequence (no modifications)'] = shuffle_db['Sequence'].str.replace(r"\(.*?\)", "", regex=True)
shuffle_db = shuffle_db.drop(columns=['Precursor theoretical monoisotopic mass'])

target_list = target_db['Sequence'].values.tolist()
shuffle_db_filtered = shuffle_db[shuffle_db['Sequence (no modifications)'].isin(target_list)]

dirlist = [ item for item in os.listdir(processed_results_path) if os.path.isdir(os.path.join(processed_results_path, item)) ]

coverage_df = shuffle_db_filtered

for directory in dirlist:
    for sample in samples_processed:
        if sample in directory:
            primary_dir_path = processed_results_path + '\\' + directory
            dirlist2 = [ item for item in os.listdir(primary_dir_path) if os.path.isdir(os.path.join(primary_dir_path, item)) ]
            for val in dirlist2:
                results_path = processed_results_path + '\\' + directory + '\\' + val + '\\final_results__target.csv'
                results = pd.read_csv(results_path)
                if len(results)>0:
                    new_results_df = pd.DataFrame()
                    new_results_df['Sequence'] = results['Peptide']
                    new_results_df[val] = 'X'
                    new_results_df = new_results_df.drop_duplicates(subset='Sequence')
                    coverage_df = coverage_df.merge(new_results_df, on='Sequence',how='left')
                else:
                    pass

cov_cal_w_mods_df = coverage_df[coverage_df.iloc[:, 2:].notnull().any(axis=1)]
cov_cal_w_mods_df = cov_cal_w_mods_df.drop_duplicates(subset='Sequence')

percent_coverage_w_mods = (len(cov_cal_w_mods_df)/len(coverage_df))*100
print('Percent coverage including PTMs: ' + str(percent_coverage_w_mods))

cov_cal_wo_mods_df = coverage_df[coverage_df.iloc[:, 2:].notnull().any(axis=1)]
cov_cal_wo_mods_df = cov_cal_wo_mods_df.drop_duplicates(subset='Sequence (no modifications)')
percent_coverage_wo_mods = (len(cov_cal_wo_mods_df)/len(target_db))*100
print('Percent coverage (backbone only): ' + str(percent_coverage_wo_mods))

cov_cal_w_mods_df['modifications'] = cov_cal_w_mods_df['Sequence'].str.findall(r'\((.*?)\)').str.join(', ')

mod_counts = []

for mod in mods:
    mod_count = cov_cal_w_mods_df['modifications'].str.contains(mod).sum()
    mod_counts.append(mod_count)

mod_summary_df = pd.DataFrame({'Mod':mods,'Mod count':mod_counts})
cov_cal_w_mods_df['Number of Mods'] = cov_cal_w_mods_df['Sequence'].str.count('\(')

mod_number_occurance = []

for a in number_mods:
    count = cov_cal_w_mods_df.loc[cov_cal_w_mods_df['Number of Mods'] == a, 'Number of Mods'].count()
    mod_number_occurance.append(count)

number_mods_df = pd.DataFrame({'Number modifications':number_mods,'Occurances':mod_number_occurance})
sns.set_palette("Spectral")
plot_number_mods = sns.barplot(number_mods_df, y="Number modifications", x="Occurances", orient="h")

type_mods_df = pd.DataFrame({'PTM':mods,'Occurances':mod_counts})
plot_mod_type = sns.barplot(type_mods_df, y="PTM", x="Occurances", orient="h")