#!/bin/bash

#Useful command to check slicesdir *.nii TODO after to check all correct segmentation

sienax subject2.nii -B "-B -f 0.1 -s -m" -d -r -S "i 20"
