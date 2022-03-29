### This module contains functions to parse and analyze patient data
from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List
import sqlite3

# Initiating Classes for Patient and Lab
class Patient:
    def __init__(self, id: str, gender: str, dob: str, race: str, labs: list) -> None:
        self.id = id
        self.gender = gender
        self.dob = datetime.strptime(dob, "%Y-%m-%d %H:%M:%S.%f")
        self.race = race
        self.lab = labs

    def __str__(self) -> str:
        return "Patient: " + str(self.id)

    @property
    def age(self):
        """The age property"""
        time_diff = datetime.now() - self.dob
        return time_diff.total_seconds() / 31536000

    @property
    def age_at_first_admit(self):
        """Patient age at first admission"""
        earliest_date = self.labs[0].lab_date
        for L in self.labs[1:]:
            if L.lab_date <= earliest_date:
                earliest_date = L.lab_date
        if self.labs == []:
            raise ValueError("Patient not in records")
        return earliest_date - self.dob


class Lab:
    def __init__(
        self, p_id: str, name: str, value: str, units: str, lab_date: str
    ) -> None:

        self.p_id = p_id
        self.name = name
        self.value = float(value)
        self.units = units
        self.lab_date = lab_date

    def __str__(self) -> str:
        return "Lab " + self.name + " for Patient " + self.p_id


def parse_data(
    lab_file: str, patient_file: str, get_lab_dict: bool = False
):  # -> Dict[str, List[str]]:

    patient_dict = {}  # 1
    lab_dict = {}

    # Populate lab dictionary with lab object
    with open(lab_file) as f:  # 1
        counter = 0
        for line in f:  # N for number of records
            counter += 1
            if counter == 1:
                pass
            else:
                fields = line.split("\t")
                lab_date = datetime.strptime(fields[5][0:23], "%Y-%m-%d %H:%M:%S.%f")
                lab_object = Lab(fields[0], fields[2], fields[3], fields[4], lab_date)
                if lab_object.p_id in lab_dict:
                    # append to value of exisitng id
                    lab_dict[lab_object.p_id].append(lab_object)
                    pass
                else:
                    lab_dict[lab_object.p_id] = [lab_object]

    # Populate Patient dict with Patient objects
    with open(patient_file) as f:
        counter = 0
        for line in f:
            counter += 1
            if counter == 1:
                pass
            else:
                patient_list_type = line.split("\t")
                patient_ID = patient_list_type[0]
                patient_obj = Patient(
                    patient_ID,
                    patient_list_type[1],
                    patient_list_type[2],
                    patient_list_type[3],
                    lab_dict[patient_ID],
                )
                patient_dict[patient_ID] = patient_obj

    # Return dictionaries
    if get_lab_dict:
        return patient_dict, lab_dict
    else:
        return patient_dict


if __name__ == "__main__":
    ## Here we import the objects into a dictionary
    patient_file = "PatientCorePopulatedTable.txt"
    lab_file = "LabsCorePopulatedTable.txt"
    patient_dict, lab_dict = parse_data(lab_file, patient_file, get_lab_dict=True)


# We access the above patient_dict to return number of
# patients older than input age
def num_older_than(age: int) -> int:
    count = 0  # 1
    for P in patient_dict:
        if P.age > age:
            count += 1
    return count


<<<<<<< HEAD
class Lab:
    def __init__(self) -> None:
        pass


# NEED TO ADAPT TO CLASSES
# def sick_patients(lab: str, gt_lt: str, value: int) -> list:
#     """returns patient ID with characteristics input for lab test"""
#     """Complexity is O(5N)"""
#     list_of_pid = []
#     # first go through dictionary and find patients with provided labs
#     # this has the advantage of returning only unique patient IDs
#     for key, vals in lab_dict.items():  # N
#         if vals[1] == lab:  # 1 in dictionaries
#             if gt_lt == "<":  # 1
#                 if int(float(vals[2])) < value:  # 1
#                     list_of_pid.append(key)  # 1
#             elif gt_lt == ">":
#                 if int(float(vals[2])) > value:
#                     list_of_pid.append(key)
#             else:
#                 raise ValueError("Please enter < or > as the second argument.")
#     # Check if the length of the list is not more than number of observations
#     # in the data
#     assert len(list_of_pid) <= len(lab_dict)
#     return list_of_pid


# Need to create database for patient info by using INSERT


# Need to access data from database using sqlite and
# then set all attributes as properties in Patient and Lab classes
# with SQL queries using help from:
# https://docs.python.org/3/library/sqlite3.html