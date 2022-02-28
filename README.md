# EHR Analysis

To access data from this repository, ensure you have the .txt files downloaded. The file to be run first is ehr_analysis.py. This loads your data and allows you the following functionalities:


1. **Number of patients older than**

You can use the function num_older_than(number) which takes an integer input and returns the number of patients in your file older than that input age.

2. **Sick Patients**

Use the function sick_patients(test_type, gt_lt, value) which takes a test type, a greater than or less than sign and a numerical value and returns the patient IDs for which this condition holds true. For example,

```sick_patients('URINALYSIS: WHITE BLOOD CELLS', '>', 1)```


3. **Patient's Age on Admission**

Use the function pateint_age(patientID) to obtain the input patient's age on first admission. For example;

```patient_age('1A8791E3-A61C-455A-8DEE-763EB90C9B2C')```

