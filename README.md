# EHR Analysis

In the module ehr_analysis.py, we parse data from input files and perform data analysis on them.

## Data parsing

Define a function `parse_data(filename: str) -> ???` that reads and parses the data files. Choose appropriate data structures such that the expected analyses (below) are efficient.

Include a module docstring describing your rationale for choosing these data structures.

Include a function docstring analyzing the computational complexity of the data parser.

## Analysis

Define the following functions to interrogate the data. In each one, include a function docstring describing its computational complexity _at runtime_ (i.e. after parsing into the global data structures).

### Old patients

The function `num_older_than(age, ???)` should take the data and return the number of patients older than a given age (in years). For example,

```python
>> num_older_than(51.2)
52
```

### Sick patients

The function `sick_patients(lab, gt_lt, value, ???)` should take the data and return a (unique) list of patients who have a given test with value above (">") or below ("<") a given level. For example,

```python
>> sick_patients("METABOLIC: ALBUMIN", ">", 4.0)
["FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "64182B95-EB72-4E2B-BE77-8050B71498CE"]
```

