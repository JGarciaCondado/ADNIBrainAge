#!/bin/bash

project_path=$1
cd ${project_path}

#Create tsv file with header for each value to store
#echo "Subject  Vscale  GM_norm  WM_norm  vscf_norm  pgrey_norm" >> DATA/processed_data.tsv

# TODO put commands inside this
#for subject in $(ls SUBJECTS/)
#do
#    cd ${project_path}/SUBJECTS/${subject}
#done

# Use SienaX to segment and normalize by brain size
subject=sub002
cd SUBJECTS/${subject}

#sienax ${subject}_T1w.nii -o ${subject}_sienax -B "-B -f 0.1 -s -m" -d -r -S "i 20"
vscale=$(grep VSCALING ${subject}_sienax/report.sienax | awk '{ print $2 }') 
gm_scale=$(grep GREY ${subject}_sienax/report.sienax | awk '{ print $2 }') 
wm_scale=$(grep WHITE ${subject}_sienax/report.sienax | awk '{ print $2 }')
vcsf_scale=$(grep vcsf ${subject}_sienax/report.sienax | awk '{ print $2 }')
pgrey_scale=$(grep pgrey ${subject}_sienax/report.sienax | awk '{ print $2 }')

echo "${subject}  ${vscale}  ${gm_scale}  ${wm_scale}  ${vcsf_scale}  ${pgrey_scale}" >> ${project_path}/DATA/processed_data.tsv
#Useful command to check slicesdir *.nii TODO after to check all correct segmentation
