# This module tests all the functionalities in the ehr_analysis
from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List
from ehr_analysis import parse_data, num_older_than, sick_patients, patient_age


def test():
    patient_dictionary_desired = {
        "PatientID   ": [
            "PatientName ",
            "PatientGender   ",
            "PatientDateofBirth ",
            "PatientRace",
        ],
        "123": ["Preet   ", "Female ", " 1997-05-08 02:45:40.547 ", "Asian"],
        "456": ["Liam Reese  ", "Male    ", "1969-11-28 11:39:49.197", "White"],
    }

    assert parse_data("patient_sample.txt") == patient_dictionary_desired


if __name__ == "__main__":
    test()
