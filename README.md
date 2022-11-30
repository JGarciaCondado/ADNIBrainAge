# NeuropsychBrainAge

BrainAge models based on neuroimaging data have shown good accuracy for diagnostic classification. However, they have replicability issues due to site and patient variability intrinsic to neuroimaging techniques. We developped a BrainAge model trained on neuropsychological tests to identify a biomarker to distinguish stable mild cognitive impairment (sMCI) from progressive mild cognitive impairment (pMCI) to Alzheimer's disease (AD). Using a linear regressor, a BrainAge model was trained on healthy controls (CN) based on neuropsychological tests. The model was applied to sMCI and pMCI subjects to obtain predicted ages. The BrainAge delta, the predicted age minus the chronological age, was used as a biomarker to distinguish between sMCI and pMCI. We compared the model to one trained on neuroimaging features. The AUC of the ROC curve for differentiating sMCI from pMCI was 0.91. It outperforms the model trained on neuroimaging features which only obtains an AUC of 0.68. The AUC achieved is at par with the SOTA BrainAge models that use Deep Learning. The BrainAge delta was correlated with the time to conversion, the time taken for a pMCI subject to convert to AD. We suggest that the BrainAge delta trained only with neuropsychological tests is a good biomarker to distinguish between sMCI and pMCI. This opens up the possibility to study other neurological and psychiatric disorders using this technique but with different neuropsychological tests.

## Methodology

![alt text](figures/fullmodel.png)

**Overview of the BrainAge model and classification task.** **a)** Training of the BrainAge model on healthy controls with input data consisting of structural features or neuropsychological features. A total of 12 structural brain features were used, consisting of volume measured in mm3 for: white matter, grey matter, peripheral grey matter, cerebrospinal fluid, thalamus, caudate, putamen, pallidum, hippocampus, amygdala, accumbens and brainstem. A total of 6 neuropsychological features were used: MMSE, ADAS, FAQ, MoCA, ADNI Memory and ADNI Executive Function. After training the linear regressor on the healthy controls age estimation task, an age bias correction was applied to deal with the inherent bias of regression to the mean problem. **b)** Description of the classification task between stable mild cognitive impairment (sMCI) and progressive mild cognitive impairment (pMCI). First, features were extracted for each subject as with healthy controls. Then, using either neuropsychological features or structural features, the trained model and bias correction were applied to obtain a predicted age. The BrainAge delta was calculated by subtracting the chronological age from the predicted age. This delta was then used as an input to a logistic regressor to determine a threshold for labelling using a 5-fold CV scheme. **c)** Number of subjects used for training with healthy controls, the number of subjects used to test the performance of BrainAge models on unseen healthy controls, and number of sMCI and pMCI used in the classification task.

## Data

All data used came from the Alzheimer's Diseases Neuroimaging Intitative (ADNI). You can find more information on how to apply to access the data [here](https://adni.loni.usc.edu/data-samples/access-data/). The specific data uses from ADNI can be found in the **scripts/** folder.

## Citation

This is a preprint, we will update once the article is accepted for publishing.

NeuropsychBrainAge: a biomarker for conversion from mild cognitive impairment to Alzheimer's disease.
Jorge Garcia Condado, Jesus M Cortes
medRxiv 2022.11.29.22282870; doi: https://doi.org/10.1101/2022.11.29.22282870 
