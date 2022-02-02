### This module contains functions to parse and analyze patient data
from datetime import datetime, timedelta, date


def parse_data(filename: str):
    """I have used a dictionary where each patient's data
    can be accessed using PatientID"""
    patient_dict = {}
    with open(filename) as f:
        for line in f:
            fields = line.split()
            patient_dict[fields[0]] = fields[1:]
    del patient_dict["\ufeffPatientID"]
    return patient_dict


## Here we import the data into a dictionary
patient_dict = parse_data("PatientCorePopulatedTable.txt")
lab_dict = parse_data("LabsCorePopulatedTable.txt")

# We access the above patient_dict to return number of
# patients older than input age
def num_older_than(age):
    """returns number of patients older than given age"""
    count = 0
    for vals in patient_dict:
        patient = patient_dict[vals]
        age_str = patient[1] + patient[2]
        time_diff = datetime.now() - datetime.strptime(age_str, "%Y-%m-%d%H:%M:%S.%f")
        years = time_diff.total_seconds() / 31536000
        if years > age:
            count += 1
    print(count)


# def sick_patients(lab, gt_lt, value):


# parse_data("PatientCorePopulatedTable.txt")
# num_older_than(63)
print(lab_dict)
