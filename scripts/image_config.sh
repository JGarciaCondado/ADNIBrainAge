#!/bin/bash

#Usage TODO

#Image folders
project_path=$1
image_folder=$2

cd ${project_path}

# Unstack all of the subject images
mkdir -p IMAGES
mv ${image_folder}/**/**/**/**/*.nii IMAGES/

#Obtain patient lits
mkdir -p DATA
ls IMAGES/ | awk '{ print $1 }' > DATA/patient_list.txt

mkdir -p SUBJECTS

count=1

for i in $(cat ${project_path}/DATA/patient_list.txt)
do

    cd ${project_path}/SUBJECTS

    subject_code=sub$(printf "%03d" $count)
    mkdir -p ${subject_code}
    cd ${subject_code}

    #In this .tsv file you can trace the original subject code and the new BIDS one
	echo "${subject_code}	${i:5:10}" >> ${project_path}/DATA/participants.tsv

    cp ${project_path}/IMAGES/${i} ${project_path}/SUBJECTS/${subject_code}/${subject_code}_T1w.nii

	count=$[$count +1]
done
