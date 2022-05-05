import pandas as pd
from functools import reduce

#Load metadata
phase = 3
cols_meta = ['RID']
df_metadata = pd.read_csv('../DATA/adni%d_mri.csv'%phase, usecols=cols_meta)
rids_meta = set(df_metadata['RID'].tolist())

# Preprocesing of dataframes to obtain desired patients
def process_dataframe(file_name, cols, rids, phase):
    df = pd.read_csv(file_name, usecols=cols)
    df.columns= [column.upper() for column in df.columns]
    df = df[df['PHASE']=='ADNI%d' % phase]
    df = df[df['RID'].isin(rids)]
    df = df.sort_values(by=['RID', 'USERDATE'])
    df = df.drop_duplicates(subset='RID', keep='first')
    df = df.drop(['PHASE', 'USERDATE'], axis=1)
    return df

# Import MMSE data
cols_mmse = ['Phase', 'RID', 'USERDATE', 'MMSCORE']
df_mmse = process_dataframe('../ASSESMENT/MMSE.csv', cols_mmse, rids_meta, phase)

# Import MoCA data
cols_moca = ['Phase', 'RID', 'USERDATE', 'TRAILS', 'CUBE', 'CLOCKCON',
       'CLOCKNO', 'CLOCKHAN', 'LION', 'RHINO', 'CAMEL', 'DIGFOR', 'DIGBACK',
       'LETTERS', 'SERIAL1', 'SERIAL2', 'SERIAL3', 'SERIAL4', 'SERIAL5', 'REPEAT1',
       'REPEAT2', 'FFLUENCY', 'ABSTRAN', 'ABSMEAS', 'DELW1', 'DELW2',
       'DELW3', 'DELW4', 'DELW5', 'DATE', 'MONTH', 'YEAR', 'DAY', 'PLACE',
       'CITY']
df_moca = process_dataframe('../ASSESMENT/MOCA.csv', cols_moca, rids_meta, phase)

# Requires computation of score
df_moca['LETTERS'] = [1 if total <= 1 else 0 for total in df_moca['LETTERS']]
cols_serial = ['SERIAL1', 'SERIAL2', 'SERIAL3', 'SERIAL4', 'SERIAL5']
df_moca['SERIAL'] = df_moca[cols_serial].sum(axis=1)
df_moca['SERIAL'] = df_moca['SERIAL'].map({0:0, 1:1, 2:2, 3:2, 4:3, 5:3})
df_moca['FFLUENCY'] = [1 if total >= 11 else 0 for total in df_moca['FFLUENCY']]
delayed_cat = ['DELW1', 'DELW2', 'DELW3', 'DELW4', 'DELW5']
for cat in delayed_cat:
    df_moca[cat] = [1 if val == 1 else 0 for val in df_moca[cat]]
cols_score = [ 'TRAILS', 'CUBE', 'CLOCKCON', 'CLOCKNO', 'CLOCKHAN',
       'LION', 'RHINO', 'CAMEL', 'DIGFOR', 'DIGBACK', 'LETTERS', 'SERIAL',
       'REPEAT1', 'REPEAT2', 'FFLUENCY', 'ABSTRAN', 'ABSMEAS', 'DELW1', 'DELW2',
       'DELW3', 'DELW4', 'DELW5', 'DATE', 'MONTH', 'YEAR', 'DAY', 'PLACE',
       'CITY']
df_moca['MOCASCORE'] = df_moca[cols_score].sum(axis=1)

# Import CDR data
cols_cdr = ['Phase', 'RID', 'USERDATE', 'CDGLOBAL']
df_cdr = process_dataframe('../ASSESMENT/CDR.csv', cols_cdr, rids_meta, phase)

# Import ADAS-cog data
cols_adas = ['Phase', 'RID', 'USERDATE', 'TOTSCORE']
df_adas = process_dataframe('../ASSESMENT/ADAS_ADNIGO23.csv', cols_adas, rids_meta, phase)
df_adas = df_adas.rename(columns={'TOTSCORE':'ADASSCORE'})

# Import FAQ data
cols_faq = ['Phase', 'RID', 'USERDATE', 'FAQTOTAL']
df_faq = process_dataframe('../ASSESMENT/FAQ.csv', cols_faq, rids_meta, phase)

# Import UWNeuropsych data
cols_uwneuropsych = ['PHASE', 'RID', 'USERDATE', 'ADNI_MEM', 'ADNI_EF']
df_uwneuropsych = process_dataframe('../ASSESMENT/UWNPSYCHSUM_12_13_21.csv', cols_uwneuropsych, rids_meta, phase)

dfs = [df_mmse, df_cdr, df_adas, df_faq, df_moca[['RID', 'MOCASCORE']], df_uwneuropsych]
df_final = reduce(lambda left,right: pd.merge(left,right,on='RID'), dfs)
df_final.to_csv('../DATA/adni%d_neuropsych.csv'%phase)
