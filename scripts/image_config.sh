#!/bin/bash

#Usage TODO

#Direcotry paths use global assigment
project_path=$1
image_folder=$2

cd ${project_path}

#Obtain patient list
mkdir -p DATA
find ${image_folder} -name "*.nii" | awk '{ print }' > DATA/patient_list.txt

# Create directory to store subject images
mkdir -p SUBJECTS

count=1

for i in $(cat ${project_path}/DATA/patient_list.txt)
do

    cd ${project_path}/SUBJECTS

    subject_code=sub$(printf "%03d" $count)
    mkdir -p ${subject_code}
    cd ${subject_code}

    #In this .tsv file you can trace the original subject code and the new BIDS one
    fname=$(basename $i)
	echo "${subject_code}	${fname:5:10}" >> ${project_path}/DATA/participants.tsv

    cp ${i} ${project_path}/SUBJECTS/${subject_code}/${subject_code}_T1w.nii

	count=$[$count +1]
done
