from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List
import pytest
from ehr_analysis import Patient, Lab, parse_data, num_older_than, sick_patients


def test_parsing():
    test_patient_dict, test_lab_dict = parse_data(
        "lab_test_file.txt", "patient_test_file.txt", True
    )
    check_list = []
    for p in test_patient_dict:
        check_list.append(test_patient_dict[p].id)
    assert check_list == [
        "B7E9FC4C-5182-4A34-954E-CEF5FC07E96D",
        "DA6CECFF-DE13-4C4C-919F-64E1A2B76C9D",
        "135C831F-7DA5-46C0-959C-EBCBD8810B43",
    ]


def test_Patient_Class():
    """Testing the functionality ot our patient class"""
    test_patient_dict, test_lab_dict = parse_data(
        "lab_test_file.txt", "patient_test_file.txt", True
    )
    assert test_patient_dict["135C831F-7DA5-46C0-959C-EBCBD8810B43"].gender == "Male"
    assert test_patient_dict["135C831F-7DA5-46C0-959C-EBCBD8810B43"].age == 50.97

    assert test_patient_dict[
        "135C831F-7DA5-46C0-959C-EBCBD8810B43"
    ].dob == datetime.strptime("1971-05-13 04:40:05.623000", "%Y-%m-%d %H:%M:%S.%f")

    assert test_patient_dict["135C831F-7DA5-46C0-959C-EBCBD8810B43"].race == "White"

    assert (
        test_patient_dict["135C831F-7DA5-46C0-959C-EBCBD8810B43"].age_at_first_admit
        == 21.96
    )


def test_Lab_Class():
    """testing the functionality of our lab class"""
    test_patient_dict, test_lab_dict = parse_data(
        "lab_test_file.txt", "patient_test_file.txt", True
    )
    sample_lab_obj = test_lab_dict["DA6CECFF-DE13-4C4C-919F-64E1A2B76C9D"][0]
    assert sample_lab_obj.p_id == "DA6CECFF-DE13-4C4C-919F-64E1A2B76C9D"
    assert sample_lab_obj.name == "CBC: RED BLOOD CELL COUNT"
    assert sample_lab_obj.value == 4.7
    assert sample_lab_obj.lab_date == datetime.strptime(
        "1950-12-19 23:49:31.047000", "%Y-%m-%d %H:%M:%S.%f"
    )


def test_num_older_than():
    """testing num_older_than functionality of ehr_analysis"""
    test_patient_dict = parse_data("lab_test_file.txt", "patient_test_file.txt", False)
    assert num_older_than(test_patient_dict, 45) == 2


def test_sick_patients():
    """Testing the sick patients function"""
    test_patient_dict, test_lab_dict = parse_data(
        "lab_test_file.txt", "patient_test_file.txt", True
    )

    assert sick_patients(test_patient_dict, "CBC: ABSOLUTE LYMPHOCYTES", ">", 15) == [
        "B7E9FC4C-5182-4A34-954E-CEF5FC07E96D"
    ]


if __name__ == "__main__":
    pytest.main(["test.py"])
