import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Clean data
cols = ['PHASE', 'RID', 'SITEID', 'VISCODE', 'VISCODE2']
df = pd.read_csv('MRI_DATA/MRI3META.csv', usecols=cols)

# Seperate by Phase
df_adni2 = df[df['PHASE'] == 'ADNI2']
df_adni3 = df[df['PHASE'] == 'ADNI3']

# Obtain screening for new and rolling over pts
df_adni2_sc = df_adni2[df_adni2['VISCODE'].isin(['v02', 'v06'])]
df_adni3_sc = df_adni3[df_adni3['VISCODE'].isin(['init', 'sc'])]

# Remove duplicate patients
df_adni2_sc = df_adni2_sc.drop_duplicates(subset='RID')
df_adni3_sc = df_adni3_sc.drop_duplicates(subset='RID')

# Keep only sites with high numbers
min_pt_adni2 = 20
adni2_pt_sites = df_adni2_sc['SITEID'].tolist()
sites_thr_adni2 = [x for x in set(adni2_pt_sites)
                   if adni2_pt_sites.count(x) > min_pt_adni2]
df_adni2_clean = df_adni2_sc[df_adni2_sc['SITEID'].isin(sites_thr_adni2)]
min_pt_adni3 = 25
adni3_pt_sites = df_adni3_sc['SITEID'].tolist()
sites_thr_adni3 = [x for x in set(adni3_pt_sites)
                   if adni3_pt_sites.count(x) > min_pt_adni3]
df_adni3_clean = df_adni3_sc[df_adni3_sc['SITEID'].isin(sites_thr_adni3)]

# Load roster data
cols_r = ['Phase', 'RID', 'SITEID', 'PTID']
df_roster = pd.read_csv('ENROLLMENT/ROSTER.csv', usecols=cols_r)

# Add PTID information to csv
df_roster_adni2 = df_roster[df_roster['Phase'] == 'ADNI2']
df_adni2_clean = df_adni2_clean.merge(df_roster_adni2, on=['RID', 'SITEID'])\
                               .drop('PHASE', axis=1)
df_roster_adni3 = df_roster[df_roster['Phase'] == 'ADNI3']
df_adni3_clean = df_adni3_clean.merge(df_roster_adni3, on=['RID', 'SITEID'])\
                               .drop('PHASE', axis=1)

# Full list of all MRI images
df_mrilist = pd.read_csv('MRI_DATA/MRILIST.csv')
df_mrilist_3T = df_mrilist[df_mrilist['MAGSTRENGTH'] == 3.0]

# Keep patients that we are interested in
PTIDs3 = df_adni3_clean['PTID'].tolist()
df_mrilist_pts3 = df_mrilist_3T[df_mrilist_3T['SUBJECT'].isin(PTIDs3)]
PTIDs2 = df_adni2_clean['PTID'].tolist()
df_mrilist_pts2 = df_mrilist_3T[df_mrilist_3T['SUBJECT'].isin(PTIDs2)]

# Keep only intial visits
df_mrilist_sc3 = df_mrilist_pts3[df_mrilist_pts3['VISIT']
                                 .isin(['ADNI3 Initial Visit-Cont Pt',
                                        'ADNI Screening'])]
df_mrilist_sc2 = df_mrilist_pts2[df_mrilist_pts2['VISIT']
                                 .isin(['ADNI2 Screening MRI-New Pt',
                                        'ADNI2 Screening-New Pt',
                                        'ADNI2 Initial Visit-Cont Pt'])]

# Keep only the relevant sequences
sequences3 = ['Accelerated Sagittal MPRAGE_ND', 'Accelerated Sagittal MPRAGE',
              'Sagittal 3D Accelerated MPRAGE',
              'Sagittal 3D Accelerated MPRAGE_REPEAT', '3D MPRAGE',
              'Accelerated Sagittal MPRAGE_MPR_Tra',
              'Accelerated Sag IR-FSPGR',
              'Accelerated Sagittal MPRAGE_MPR_Cor',
              'Accelerated Sagittal MPRAGE Phase A-P',
              'Accelerated Sagittal IR-FSPGR']
sequences2 = ['SAG IR-SPGR', 'Accelerated SAG IR-FSPGR', 'Sag IR-SPGR',
              'MPRAGE SENSE2', 'MPRAGE GRAPPA2', 'MPRAGE_S2_DIS3D',
              'Accelerated Sag IR-FSPGR', 'MPRAGE', 'Sag IR-FSPGR',
              'Accelerated SAG IR-SPGR', 'Accelerated Sag IR-SPGR',
              'MPRAGE_GRAPPA2', 'MPRAGE repeat']
df_mrilist_images3 = df_mrilist_sc3[df_mrilist_sc3['SEQUENCE'].isin(
    sequences3)]
df_mrilist_images2 = df_mrilist_sc2[df_mrilist_sc2['SEQUENCE'].isin(
    sequences2)]

# Remove repeated images keep higher IMAGEUID, the last image taken
pts3_multiple_im = [pt for pt in PTIDs3
                    if df_mrilist_images3['SUBJECT'].tolist().count(pt) > 1]
df_repeated_images3 = df_mrilist_images3[df_mrilist_images3['SUBJECT'].isin(
    pts3_multiple_im)]
df_mrilist_images3 = df_mrilist_images3.sort_values(
    'IMAGEUID', ascending=False).drop_duplicates('SUBJECT').sort_index()
pts2_multiple_im = [pt for pt in PTIDs2
                    if df_mrilist_images2['SUBJECT'].tolist().count(pt) > 1]
df_repeated_images2 = df_mrilist_images2[df_mrilist_images2['SUBJECT'].isin(
    pts2_multiple_im)]
df_mrilist_images2 = df_mrilist_images2.sort_values(
    'IMAGEUID', ascending=False).drop_duplicates('SUBJECT').sort_index()

# Merge into a single frame
df_full_adni3 = df_adni3_clean.merge(df_mrilist_images3, left_on='PTID',
                                     right_on='SUBJECT')\
                              .drop('SUBJECT', axis=1)
df_full_adni2 = df_adni2_clean.merge(df_mrilist_images2, left_on='PTID',
                                     right_on='SUBJECT')\
                              .drop('SUBJECT', axis=1)

# Load patient assesments
cols_a = ['RID', 'PTID', 'SITEID', 'Phase',
          'VISCODE', 'VISCODE2', 'DXCHANGE', 'DIAGNOSIS']
df_assesment = pd.read_csv(
    'ASSESMENT/DXSUM_PDXCONV_ADNIALL.csv', usecols=cols_a)

# Standarize diagnosis
df_full_adni3 = df_full_adni3.merge(df_assesment, on=['RID', 'PTID', 'SITEID',
                                    'VISCODE', 'VISCODE2', 'Phase'])\
                              .drop('DXCHANGE', axis=1)
# Viscodes are different for new patients as had 3 seperate sesions: screening
# (v01), screening mri (v02) and baseline (v03). There is no recorded i
# diagnosis for v02 so use v03 baseline as recommended in ADNI documentation
df_assesment = df_assesment[df_assesment['VISCODE'].isin(['v03', 'v06'])]
df_full_adni2 = df_full_adni2.drop(['VISCODE', 'VISCODE2'], axis=1)\
                             .merge(df_assesment, on=['RID', 'PTID', 'SITEID',
                                    'Phase'])\
                             .drop('DIAGNOSIS', axis=1)
# Covnert to standard CN (1.0), MCI (2.0) and AD (3.0) labels
df_full_adni2["DXCHANGE"].replace({4.0: 2.0, 5.0: 3.0, 7.0: 1.0}, inplace=True)
df_full_adni2.rename(columns={'DXCHANGE': 'DIAGNOSIS'}, inplace=True)

# Load ADNI Merge data to get age information
cols_m = ['COLPROT', 'PTID', 'VISCODE', 'AGE', 'DX_bl', 'PTGENDER', 'Years_bl']
df_adni_merge = pd.read_csv('STUDY_DATA/ADNIMERGE.csv', usecols=cols_m)\
    .rename(columns={'COLPROT': 'Phase', 'VISCODE': 'VISCODE2'})

# Add age of patient at visit
df_full_adni2 = df_full_adni2.merge(
    df_adni_merge, on=['PTID', 'Phase', 'VISCODE2'])
df_full_adni2['AGE'] = df_full_adni2['AGE']+df_full_adni2['Years_bl']
df_full_adni2.drop('Years_bl', axis=1, inplace=True)
# Different viscode naming in csvs
df_adni_merge['VISCODE2'].replace({'bl': 'sc'}, inplace=True)
df_full_adni3 = df_full_adni3.merge(
    df_adni_merge, on=['PTID', 'Phase', 'VISCODE2'])
df_full_adni3['AGE'] = df_full_adni3['AGE']+df_full_adni3['Years_bl']
df_full_adni3.drop('Years_bl', axis=1, inplace=True)

# Save all metadata as csv
df_full_adni2.to_csv('DATA/adni2_mri.csv')
df_full_adni3.to_csv('DATA/adni3_mri.csv')
pd.concat([df_full_adni2, df_full_adni3]).to_csv('DATA/adni2and3_mri.csv')

# Save IMAGEIDs as txts
with open('DATA/adni2_mri_ids.txt', 'w') as f:
    f.write(','.join(str(i) for i in df_full_adni2['IMAGEUID']))
with open('DATA/adni3_mri_ids.txt', 'w') as f:
    f.write(','.join(str(i) for i in df_full_adni3['IMAGEUID']))
