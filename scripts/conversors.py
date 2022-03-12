import pandas as pd
import numpy as np

#Load data
phase = 3
df_metadata = pd.read_csv('../DATA/adni%d_mri.csv'%phase, index_col=0)

# Load patient assesments
cols_a = ['RID', 'EXAMDATE',
          'DXCHANGE', 'DIAGNOSIS']
df_assesment = pd.read_csv(
    'DXSUM_PDXCONV_ADNIALL.csv', usecols=cols_a)
df_assesment.dropna(subset=['EXAMDATE'], inplace=True)

# Get all patients in phase
rid = df_metadata['RID'].tolist()
df_assesment_pts = df_assesment[df_assesment['RID'].isin(rid)]
df_last_assesment= df_assesment_pts.drop_duplicates('RID', keep='last')

# Merge DXCHANGE and DIAGNOSIS column and homogenise diagnosis
df_last_assesment = df_last_assesment.copy()
df_last_assesment['LASTDIAGNOSIS'] = df_last_assesment.pop('DIAGNOSIS').fillna(df_last_assesment.pop('DXCHANGE'))
df_last_assesment['LASTDIAGNOSIS'].replace({4.0: 2.0, 5.0: 3.0, 8.0: 2.0}, inplace=True)
df_last_assesment.rename(columns={'EXAMDATE': 'LASTEXAMDATE'}, inplace=True)

# Merge and add wether there was a conversion
df_metadata = df_metadata.merge(df_last_assesment, on=['RID'])
df_metadata['CONVERSOR'] = df_metadata['DIAGNOSIS'] != df_metadata['LASTDIAGNOSIS']

# Apply conversion diagnosis variables given by ADNIGO2
def conversor_types(row):
    # Keep diagnosis
    if row['DIAGNOSIS'] == row['LASTDIAGNOSIS']:
        return row['DIAGNOSIS']
    # CN to MCI
    elif row['DIAGNOSIS'] == 1.0 and row['LASTDIAGNOSIS'] == 2.0:
        return 4.0
    # MCI to AD
    elif row['DIAGNOSIS'] == 2.0 and row['LASTDIAGNOSIS'] == 3.0:
        return 5.0
    # CN to AD
    elif row['DIAGNOSIS'] == 1.0 and row['LASTDIAGNOSIS'] == 3.0:
        return 6.0
    # MCI to CN
    elif row['DIAGNOSIS'] == 2.0 and row['LASTDIAGNOSIS'] == 1.0:
        return 7.0
    # AD to MCI
    elif row['DIAGNOSIS'] == 3.0 and row['LASTDIAGNOSIS'] == 2.0:
        return 8.0
    # AD to CN
    elif row['DIAGNOSIS'] == 3.0 and row['LASTDIAGNOSIS'] == 1.0:
        return 9.0

df_metadata['TYPECONVERSOR'] = df_metadata.apply(lambda row: conversor_types(row), axis=1)

df_metadata.to_csv('../DATA/adni%d_mri.csv'%phase)
