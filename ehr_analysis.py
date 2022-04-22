### This module contains functions to parse and analyze patient data
from datetime import datetime, timedelta, date
from typing import Any, TypeVar, Dict, List, Tuple

# Initiating Classes for Patient and Lab
class Patient:
    def __init__(
        self, id: str, gender: str, dob: str, race: str, labs: list = None
    ) -> None:
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
        return round(time_diff.total_seconds() / 31536000, 2)

    @property
    def age_at_first_admit(self):
        """Patient age at first admission"""
        earliest_date = self.lab[0].lab_date
        for L in self.lab[1:]:
            if L.lab_date <= earliest_date:
                earliest_date = L.lab_date
        if self.lab == []:
            raise ValueError("Patient not in records")
        return round((earliest_date - self.dob).days / 365, 2)


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
) -> Tuple[Dict[str, List(Patient)], Dict[str, Any]]:

    patient_dict = {}  # 1
    lab_dict: Dict[str, List(Lab)] = {}

    # Populate lab dictionary with lab object
    with open(lab_file) as f:  # 1
        counter = 0
        for line in f:  # N for number of records
            counter += 1
            if counter == 1:
                pass
            else:
                fields = line.split("\t")
                # lab_date = datetime.strptime(fields[5][:23], "%Y-%m-%d %H:%M:%S.%f")
                lab_object = Lab(
                    fields[0], fields[2], fields[3], fields[4], fields[5][:23]
                )
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
    return patient_dict, lab_dict

# We access the above patient_dict to return number of
# patients older than input age
def num_older_than(p_dict: Dict[str, List[Patient]], age: int) -> int:
    count = 0  # 1
    for P in p_dict:
        if p_dict[P].age > age:
            count += 1
    return count


def sick_patients(
    p_dict: Dict[str, List[Patient]], lab: str, gt_lt: str, value: int
) -> list:
    list_of_patients_sick = []
    for p in p_dict:
        lab_list = p_dict[p].lab
        for labs in lab_list:
            if labs.name == lab:
                if gt_lt == "<":
                    if labs.value < value:
                        list_of_patients_sick.append(p)
                elif gt_lt == ">":
                    if labs.value > value:
                        list_of_patients_sick.append(p)
    # Make sure list is unique
    unique_list = []
    for L in list_of_patients_sick:
        if L not in unique_list:
            unique_list.append(L)
    return unique_list
