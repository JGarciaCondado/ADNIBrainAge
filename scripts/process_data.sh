#!/bin/bash

project_path=$1
subject=$2
cd ${project_path}

#Create tsv file with header for each value to store
if [ ! -f DATA/processed_data.tsv ]
then
    echo "Subject Vscale Brain_norm GM_norm WM_norm vscf_norm"\
        "pgrey_norm L_Thalmus L_Caudate L_Putamen L_Palidum Brainstem"\
        "L_Hippo L_Amygdala L_Accumbens R_Thalmus R_Caudate R_Putamen"\
        "R_Palidum R_Hippo R_Amygdala R_Accumbens" >> DATA/processed_data.tsv
fi

cd SUBJECTS/${subject}
echo ${subject}

#Use SienaX to segment and normalize by brain size
sienax ${subject}_T1w.nii -o sienax -B "-B -f 0.1 -s -m" -d -r -S "i 20"

#Obtain segmented volumes of interest 
vscale=$(grep VSCALING sienax/report.sienax | awk '{ print $2 }')
brain=$(grep BRAIN sienax/report.sienax | awk '{ print $2 }')
gm_scale=$(grep GREY sienax/report.sienax | awk '{ print $2 }')
wm_scale=$(grep WHITE sienax/report.sienax | awk '{ print $2 }')
vcsf_scale=$(grep vcsf sienax/report.sienax | awk '{ print $2 }')
pgrey_scale=$(grep pgrey sienax/report.sienax | awk '{ print $2 }')

#Use FIRST to segment subcortical structures
mkdir -p first
run_first_all -i sienax/I_brain.nii.gz -o first/${subject} -b -a sienax/I2std.mat -d

#Obtain subcortical volumes of interest 
L_Thalmus=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 9.5 -u 10.5 -M -V | awk '{ print $3}')
L_Caudate=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 10.5 -u 11.5 -M -V | awk '{ print $3}')
L_Putamen=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 11.5 -u 12.5 -M -V | awk '{ print $3}')
L_Palidum=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 12.5 -u 13.5 -M -V | awk '{ print $3}')
Brainstem=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 15.5 -u 16.5 -M -V | awk '{ print $3}')
L_Hippo=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 16.5 -u 17.5 -M -V | awk '{ print $3}')
L_Amygdala=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 17.5 -u 18.5 -M -V | awk '{ print $3}')
L_Accumbens=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 25.5 -u 26.5 -M -V | awk '{ print $3}')
R_Thalmus=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 48.5 -u 49.5 -M -V | awk '{ print $3}')
R_Caudate=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 49.5 -u 50.5 -M -V | awk '{ print $3}')
R_Putamen=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 50.5 -u 51.5 -M -V | awk '{ print $3}')
R_Palidum=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 51.5 -u 52.5 -M -V | awk '{ print $3}')
R_Hippo=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 52.5 -u 53.5 -M -V | awk '{ print $3}')
R_Amygdala=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 53.5 -u 54.5 -M -V | awk '{ print $3}')
R_Accumbens=$(fslstats first/${subject}_all_fast_firstseg.nii.gz -l 57.5 -u 58.5 -M -V | awk '{ print $3}')

#Save all the data to tsv
echo "${subject} ${vscale} ${brain} ${gm_scale} ${wm_scale} ${vcsf_scale}"\
    "${pgrey_scale} ${L_Thalmus} ${L_Caudate} ${L_Putamen} ${L_Palidum} ${Brainstem}"\
    "${L_Hippo} ${L_Amygdala} ${L_Accumbens} ${R_Thalmus} ${R_Caudate} ${R_Putamen}"\
    "${R_Palidum} ${R_Hippo} ${R_Amygdala} ${R_Accumbens}" >> ${project_path}/DATA/processed_data.tsv


#Useful command to check slicesdir *.nii for correct segmentation
#Specifically for first first_roi_slicesdir *_t1.nii.gz *_all_fast_firstseg.nii.gz
