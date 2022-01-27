#!/bin/bash

#Usage TODO

#Image folders
image_folder=$1

# Command useful to unstack all of the subject images
# mv **/**/**/**/*.nii ./

#Obtain patient lits
ls ${image_folder} | awk '{ print $1 }' > DATA/patient_list.txt

mkdir -p SUBJECTS

count=1

for i in $(cat DATA/patient_list.txt)
do
    subject_code=sub$(printf "%03d" $count)
	
    #In this .tsv file you can trace the original subject code and the new BIDS one
	echo "${subject_code}	${i:5:10}" >> DATA/participants.tsv

    cp ${image_folder}/${i} SUBJECTS/${subject_code}_T1w.nii.gz

	count=$[$count +1]
done
