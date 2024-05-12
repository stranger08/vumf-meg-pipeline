#! /bin/bash

## export variables
export SUBJECTS_DIR=/home/s8/Documents/VU/dataset/subjects_dir/freesurfer/
export SUBJECT=sub-V1008

nii_path=/home/s8/Documents/VU/dataset/origin/$SUBJECT/anat
cd $nii_path
filename=${SUBJECT}_space-CTF_T1w.nii
recon-all -subjid $SUBJECT -i $filename -openmp 12

#! /bin/bash

export SUBJECTS_DIR=/home/s8/Documents/VU/dataset/subjects_dir/freesurfer/

recon-all -subjid $SUBJECT -all -notal-check -openmp 12