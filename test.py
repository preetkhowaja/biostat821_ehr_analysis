# This module tests all the functionalities in the ehr_analysis
import pytest
from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List
from ehr_analysis import (
    parse_data,
    num_older_than,
    sick_patients,
    patient_age,
)

# Patient File and Functionality Tests
def test():
    patient_dictionary_desired = {
        "PatientID": ["PatientGender", "PatientDateOfBirth", "PatientRace"],
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F": [
            "Male",
            "1947-12-28 02:45:40.547",
            "Unknown",
        ],
        "64182B95-EB72-4E2B-BE77-8050B71498CE": [
            "Male",
            "1952-01-18 19:51:12.917",
            "African American",
        ],
        "DB22A4D9-7E4D-485C-916A-9CD1386507FB": [
            "Female",
            "1970-07-25 13:04:20.717",
            "Asian",
        ],
        "6E70D84D-C75F-477C-BC37-9177C3698C66": [
            "Male",
            "1999-07-25 13:04:20.718",
            "White",
        ],
    }
    patient_dict = parse_data("sample_patient.txt")
    assert patient_dict == patient_dictionary_desired

    # Checking if num older than returns patients less than the number present in the dictionary
    assert num_older_than(patient_dict, 0) < (len(patient_dict) + 1)
    # Check if it returns all patients if asked for those with age older than 0
    assert num_older_than(patient_dict, 0) == 4

    # Check patient age function
    assert patient_age(patient_dict, "DB22A4D9-7E4D-485C-916A-9CD1386507FB") == 51.8


# Lab File and Functionality Tests
def test_():
    # Check lab dictionary output
    lab_dictionary = parse_data("sample_lab.txt")
    desired_lab = {
        "PatientID": ["AdmissionID", "LabName", "LabValue", "LabUnits", "LabDateTime"],
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": [
            "1",
            "URINALYSIS: RED BLOOD CELLS",
            "1.8",
            "rbc/hpf",
            "1992-07-01 01:36:17.910",
            ["1", "METABOLIC: GLUCOSE", "103.3", "mg/dL", "1992-06-30 09:35:52.383"],
            ["1", "CBC: MCH", "35.8", "pg", "1992-06-30 03:50:11.777"],
            ["1", "METABOLIC: CALCIUM", "8.9", "mg/dL", "2005-07-31 19:56:49.560"],
        ],
    }
    assert lab_dictionary == desired_lab
    # Check sick_patient function
    assert sick_patients(lab_dictionary, "URINALYSIS: RED BLOOD CELLS", ">", 0) == [
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    ]


if __name__ == "__main__":
    # test()
    pytest.main(["test.py"])
