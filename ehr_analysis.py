### This module contains functions to parse and analyze patient data
from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List

T = str


def parse_data(filename: str) -> Dict[str, List[T]]:
    """I have used a dictionary where each patient's data
    can be accessed using PatientID so that the computational
    complexity is lower than using a list. I can access records
    using PatientID with O(1) complexity."""
    """The complexity of this parser is better since we add the data 
    to a dictionary as we read it. This parser likely has complexity
    O(3N)"""
    patient_dict = {}  # 1
    with open(filename) as f:  # 1
        for line in f:  # N for number of records
            fields = line.split("\t")  # N times
            patient_dict[fields[0]] = fields[1:]  # N times
    return patient_dict


# We access the above patient_dict to return number of
# patients older than input age
def num_older_than(age: int) -> int:
    """returns number of patients older than given age"""
    """The big O notationa for this is O(6N)"""
    count = 0  # 1
    for key, vals in patient_dict.items():  # Everything in this loop happens N times
        patient = patient_dict[key]  # 1
        age_str = patient[1]  # 1
        if key.isnumeric():
            time_diff = datetime.now() - datetime.strptime(
                age_str, "%Y-%m-%d %H:%M:%S.%f"
            )  # 1
            years = time_diff.total_seconds() / 31536000  # 1
            if years > age:  # 1 in dictionaries
                count += 1  # 1
    return count


def sick_patients(lab: str, gt_lt: str, value: int) -> List[str]:
    """returns patient ID with characteristics input for lab test"""
    """Complexity is O(5N)"""
    list_of_pid = []
    # first go through dictionary and find patients with provided labs
    # this has the advantage of returning only unique patient IDs
    for key, vals in lab_dict.items():  # N
        if vals[1] == lab:  # 1 in dictionaries
            if gt_lt == "<":  # 1
                if int(float(vals[2])) < value:  # 1
                    list_of_pid.append(key)  # 1
            elif gt_lt == ">":
                if int(float(vals[2])) > value:
                    list_of_pid.append(key)
            else:
                raise ValueError("Please enter < or > as the second argument.")
    return list_of_pid


if __name__ == "__main__":
    ## Here we import the data into a dictionary
    patient_dict = parse_data("PatientCorePopulatedTable.txt")
    lab_dict = parse_data("LabsCorePopulatedTable.txt")
    print(sick_patients("CBC: MCHC", ">", 37))
