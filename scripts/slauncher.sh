#!/bin/bash


#
#SBATCH -J anat # A single job name for the array
#SBATCH -n 1 # Number of cores
#SBATCH -p medium # Partition
#SBATCH --mem 8000 # Memory request
#SBATCH -o LOG/anat_%A_%a.out # Standard output
#SBATCH -e LOG/anat_%A_%a.err # Standard error

export FSLOUTPUTTYPE=NIFTI_GZ

cd /home/jorga/ADNIBrainAge
phase=ADNI2
patients=( ${phase}/SUBJECTS/* )

mainRoot=/home/jorga/ADNIBrainAge
patient="${patients[${SLURM_ARRAY_TASK_ID}]}"
patientname=$( basename $patient )


echo "*********************"
echo "$patientname"
echo "*********************"

singularity exec /home/biocruces/comp-neuro/compneuro_wICA_AROMA.simg ${mainRoot}/process_data.sh ${mainRoot}/${phase} $patientname
