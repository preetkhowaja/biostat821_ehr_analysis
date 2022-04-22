from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List, Tuple, Any
import sqlite3
from sqlite3 import Error
from ehr_analysis import Patient, Lab, parse_data, num_older_than, sick_patients


class SQL:
    def __init__(self) -> None:
        pass

    def create_connection(self, db_file: str):
        """Creates db file connection where tables are stored"""
        self.connection = sqlite3.connect(db_file)
        return self.connection

    def create_tables(self) -> None:
        """Create Patient Table from patient objects"""
        c = self.connection.cursor()
        c.execute(
            """CREATE TABLE Patients (
            id text,
            gender text,
            dob real,
            age integer,
            race text
        )"""
        )
        c.execute(
            """CREATE TABLE Labs (
            p_id text,
            name text,
            value integer,
            units text,
            lab_date real
        )"""
        )
        self.connection.commit()

    def insert_into_patient(self, patient_dict: Dict[str, List[Patient]]) -> None:
        """Insert fields into patient table"""
        self.p_dict = patient_dict
        entries = []
        for key, val in self.p_dict.items():
            time_diff = datetime.now() - val.dob
            age = round(time_diff.total_seconds() / 31536000, 2)
            entry = []
            entry.append(val.id)
            entry.append(val.gender)
            entry.append(val.dob)
            entry.append(age)
            entry.append(val.race)
            entries.append(entry)
        c2 = self.connection.cursor()
        c2.executemany(""" INSERT INTO Patients VALUES (?,?,?,?,?)""", entries)
        self.connection.commit()

    def insert_into_lab(self, lab_dict: Dict[str, List[Lab]]) -> None:
        """Insert into labs table"""
        self.l_dict = lab_dict
        entries2 = []
        for key, val in self.l_dict.items():
            for each_lab in val:
                entry = []
                entry.append(each_lab.p_id)
                entry.append(each_lab.name)
                entry.append(each_lab.value)
                entry.append(each_lab.units)
                entry.append(each_lab.lab_date)
                entries2.append(entry)
        c2 = self.connection.cursor()
        c2.executemany(""" INSERT INTO Labs VALUES (?,?,?,?,?)""", entries2)
        self.connection.commit()


def main(
    patient_file: str, lab_file: str
) -> Tuple[Dict[str, Patient], Dict[str, List[Lab]]]:
    """Takes the lab and patient files and converts them to dictionaries.
    Then it adds every object to a SQL able"""
    patient_dictionary, lab_dictionary = parse_data(lab_file, patient_file, True)
    start_db = SQL()
    start_db.create_connection("PatientDatabase")
    start_db.create_tables()
    start_db.insert_into_patient(patient_dictionary)
    start_db.insert_into_lab(lab_dictionary)
    return patient_dictionary, lab_dictionary


def num_older_than(age_given: int):
    connection_age = sqlite3.connect("PatientDatabase")
    age_cur = connection_age.cursor()
    age_cur.execute("SELECT id FROM Patients WHERE age > ?", (age_given,))
    rows = age_cur.fetchall()
    return len(rows)


def sick_patients(lab: str, gt_lt: str, value: int) -> list:
    conn_sick = sqlite3.connect("PatientDatabase")
    sick_cursor = conn_sick.cursor()
    if gt_lt == ">":
        sick_cursor.execute(
            "SELECT p_id FROM Labs WHERE name = ? AND value > ?", (lab, value)
        )
        sick_patients = sick_cursor.fetchall()
    elif gt_lt == "<":
        sick_cursor.execute(
            "SELECT p_id FROM Labs WHERE name = ? AND value < ?", (lab, value)
        )
        sick_patients = sick_cursor.fetchall()
    return sick_patients


