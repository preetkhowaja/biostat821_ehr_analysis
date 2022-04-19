from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List
import sqlite3
from sqlite3 import Error
from ehr_analysis import Patient, Lab, parse_data, num_older_than, sick_patients


class SQL:
    def __init__(self) -> None:
        self.p_dict = None
        self.lab_dict = None
        self.connection = None
        pass

    def create_connection(self, db_file):
        """Creates db file connection where tables are stored"""
        try:
            self.connection = sqlite3.connect(db_file)
        except self.connection.Error as e:
            print(e)
        return self.connection

    def create_tables(self):
        """Create Patient Table from patient objects"""
        c = self.connection.cursor()
        c.execute(
            """CREATE TABLE Patients (
            id text,
            gender text,
            dob real,
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

    def insert_into_patient(self, patient_dict):
        """Insert fields into patient table"""
        self.p_dict = patient_dict
        entries = []
        for key, val in self.p_dict.items():
            entry = []
            entry.append(val.id)
            entry.append(val.gender)
            entry.append(val.dob)
            entry.append(val.race)
            entries.append(entry)
        c2 = self.connection.cursor()
        c2.executemany(""" INSERT INTO Patients VALUES (?,?,?,?)""", entries)
        self.connection.commit()
        self.connection.close()
        pass

    def insert_into_lab(self, lab_dict):
        """Insert into labs table"""
        pass


def main(patient_file, lab_file):
    """Takes the lab and patient files and converts them to dictionaries.
    Then it adds every object to a SQL able"""
    patient_dictionary, lab_dictionary = parse_data(lab_file, patient_file, True)
    start_db = SQL()
    start_db.create_connection("PatientDatabase")
    start_db.create_tables()
    start_db.insert_into_patient(patient_dictionary)


if __name__ == "__main__":
    main("PatientCorePopulatedTable.txt", "LabsCorePopulatedTable.txt")
