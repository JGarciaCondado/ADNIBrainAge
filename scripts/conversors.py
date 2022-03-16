import pandas as pd
import numpy as np
import datetime

#Load data
phase = 2
df_metadata = pd.read_csv('../DATA/adni%d_mri.csv'%phase, index_col=0)\
                .drop(['TYPECONVERSOR', 'CONVERSIONDATE'], axis=1)

# Load patient assesments
cols_a = ['RID', 'EXAMDATE',
          'DXCHANGE', 'DIAGNOSIS']
df_assesment = pd.read_csv(
    'DXSUM_PDXCONV_ADNIALL.csv', usecols=cols_a)
df_assesment.dropna(subset=['EXAMDATE'], inplace=True)

# Get all patients in phase
rids = list(set(df_metadata['RID'].tolist()))
df_assesment_pts = df_assesment[df_assesment['RID'].isin(rids)].copy()

# Homogonise diagnosis data and remove nans due to Phase1
df_assesment_pts['DIAGNOSIS'] = df_assesment_pts.pop('DIAGNOSIS').fillna(df_assesment_pts.pop('DXCHANGE'))
df_assesment_pts['DIAGNOSIS'].replace({4.0: 2.0, 5.0: 3.0, 7.0:1.0, 8.0: 2.0}, inplace=True)
df_assesment_pts.dropna(inplace=True)
df_assesment_pts.sort_values(by=['RID', 'EXAMDATE'], inplace=True)

# Apply conversion diagnosis variables given by ADNIGO2
def conversor_types(current_diag, new_diag):
    # Keep diagnosis
    if current_diag == new_diag:
        return current_diag
    # CN to MCI
    elif current_diag == 1.0 and new_diag == 2.0:
        return 4.0
    # MCI to AD
    elif current_diag == 2.0 and new_diag == 3.0:
        return 5.0
    # CN to AD
    elif current_diag == 1.0 and new_diag == 3.0:
        return 6.0
    # MCI to CN
    elif current_diag == 2.0 and new_diag == 1.0:
        return 7.0
    # AD to MCI
    elif current_diag == 3.0 and new_diag == 2.0:
        return 8.0
    # AD to CN
    elif current_diag == 3.0 and new_diag == 1.0:
        return 9.0

# Find conversions and time of conversion for each
conversor_info = []
conversion_date_info = []
for rid in rids:
    df_pt = df_assesment_pts[df_assesment_pts['RID']==rid]
    exam_dates = df_pt['EXAMDATE'].tolist()
    diagnosis = df_pt['DIAGNOSIS'].tolist()
    # Compare diagnosis to diagnosis when image was taken 
    initial_diagnosis = df_metadata.at[df_metadata.index[df_metadata['RID']==rid][0], 'DIAGNOSIS']
    image_date = datetime.datetime.strptime(df_metadata.at[df_metadata.index[df_metadata['RID']==rid][0], 'SCANDATE'],
                                            '%Y-%m-%d')
    conversion_date = None
    current_conversor_type = initial_diagnosis
    for date, diag in zip(exam_dates, diagnosis):
        # If diagnosis is before image taken ignore
        if datetime.datetime.strptime(date, '%Y-%m-%d') < image_date:
            continue
        elif initial_diagnosis != diag:
            conversor_type = conversor_types(initial_diagnosis, diag)
            # Check wether already detected this conversion if not update
            if conversor_type != current_conversor_type:
                conversion_date = date
                current_conversor_type = conversor_type
        # Save last exam date as conversion date if no conversion
        elif current_conversor_type < 3.5:
            conversion_date = date
    conversor_info.append(current_conversor_type)
    conversion_date_info.append(conversion_date)

df_conversors = pd.DataFrame(list(zip(rids, conversor_info, conversion_date_info)),
                             columns=['RID', 'TYPECONVERSOR', 'CONVERSIONDATE'])

# Store all information in metadata
df_metadata = df_metadata.merge(df_conversors, on=['RID'])
df_metadata.to_csv('../DATA/adni%d_mri.csv'%phase)
