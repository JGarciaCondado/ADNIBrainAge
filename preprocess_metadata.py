import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('MRI_DATA/MRI3META.csv')

# Clean data
cols = ['PHASE', 'ID', 'RID', 'SITEID', 'VISCODE', 'VISCODE2']
df = df[cols]

# Seperate by Phase
df_adni2 = df[df['PHASE'] == 'ADNI2']
df_adni3 = df[df['PHASE'] == 'ADNI3']

# Obtain screening or baseline
df_adni2_sc = df_adni2[df_adni2['VISCODE'] == 'v02']
df_adni3_sc = df_adni3[df_adni3['VISCODE'].isin(['init', 'sc'])]

# Keep only sites with high numbers
min_pt_adni2 = 15
adni2_pt_sites = df_adni2_sc['SITEID'].tolist()
sites_thr_adni2 = [x for x in set(adni2_pt_sites) \
                   if adni2_pt_sites.count(x) > min_pt_adni2]
df_adni2_clean = df_adni2_sc[df_adni2_sc['SITEID'].isin(sites_thr_adni2)]
min_pt_adni3 = 25
adni3_pt_sites = df_adni3_sc['SITEID'].tolist()
sites_thr_adni3 = [x for x in set(adni3_pt_sites) \
                   if adni3_pt_sites.count(x) > min_pt_adni3]
df_adni3_clean = df_adni3_sc[df_adni3_sc['SITEID'].isin(sites_thr_adni3)]

# Convert patient RID which is unique to PTID which may change depending on site
# TODO add PTID column to adni3 clean (will need to remove duplicates)
df_roster = pd.read_csv('ENROLLMENT/ROSTER.csv')
df_roster_adni2 = df_roster[df_roster['Phase'] == 'ADNI2']
RIDs = df_adni2_clean['RID'].tolist()
df_roster_adni2_clean = df_roster_adni2[df_roster_adni2['RID'].isin(RIDs)]
df_roster_adni3 = df_roster[df_roster['Phase'] == 'ADNI3']
RIDs = df_adni3_clean['RID'].tolist()
df_roster_adni3_clean = df_roster_adni3[df_roster_adni3['RID'].isin(RIDs)]

# Full list of all MRI images
df_mrilist = pd.read_csv('MRI_DATA/MRILIST.csv')
df_mrilist_3T = df_mrilist[df_mrilist['MAGSTRENGTH'] == 3.0]

# TODO repeat for ADNI2 careful with visit and sequence type check that adni 2 initial vist dont also have adni screening

# Keep patients that we are interested in
PTIDs = df_roster_adni3_clean['PTID'].tolist()
df_mrilist_pts = df_mrilist_3T[df_mrilist_3T['SUBJECT'].isin(PTIDs)]
#print(df_mrilist_pts)
# print(set(df_mrilist_pts['VISIT'].tolist()))

# Keep only intial visitis to ADNI3
df_mrilist_sc = df_mrilist_pts[df_mrilist_pts['VISIT'].isin(['ADNI3 Initial Visit-Cont Pt', 'ADNI Screening'])]
continuing_ptids = set(df_mrilist_sc[df_mrilist_sc['VISIT'] == 'ADNI3 Initial Visit-Cont Pt']['SUBJECT'])
#print(len(df_mrilist_sc))
#print(continuing_ptids)
#df_mrilist_sc[df_mrilist_sc['SUBJECT'].isin(continuing_ptids)].to_csv('continuing.csv')
#print(df_mrilist_sc[(df_mrilist_sc['VISIT'] == 'ADNI Screening') \
#                    & (df_mrilist_sc['SUBJECT'].isin(list(continuing_ptids)))])
#df_mrilist_sc = df_mrilist_sc.drop(df_mrilist_sc[(df_mrilist_sc['VISIT'] == 'ADNI Screening') \
#                    & (df_mrilist_sc['SUBJECT'].isin(continuing_ptids))])
#print(len(df_mrilist_sc))

# Keep only the relevant sequences 
sequences = ['Accelerated Sagittal MPRAGE_ND', 'Accelerated Sagittal MPRAGE',
             'Sagittal 3D Accelerated MPRAGE', 'Sagittal 3D Accelerated MPRAGE_REPEAT',
             '3D MPRAGE', 'Accelerated Sagittal MPRAGE_MPR_Tra', 'Accelerated Sag IR-FSPGR',
             'Accelerated Sagittal MPRAGE_MPR_Cor', 'Accelerated Sagittal MPRAGE Phase A-P',
             'Accelerated Sagittal IR-FSPGR']
df_mrilist_images = df_mrilist_sc[df_mrilist_sc['SEQUENCE'].isin(sequences)]

# TODO what to do with repeated images?
pts_multiple_images = [pt for pt in PTIDs if df_mrilist_images['SUBJECT'].tolist().count(pt) > 1]
df_repeated_images = df_mrilist_images[df_mrilist_images['SUBJECT'].isin(pts_multiple_images)]
print(df_repeated_images)
# TODO one single csv with all relevant info fusing PHASE, RID, SITEID, PTID, VISCODE, VISCODE2, PTID, VISIT, SEQUENCE, SCANDAT, STUDYID, SERIESID, IMAGEUID
