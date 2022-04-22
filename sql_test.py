from datetime import datetime, timedelta, date
from typing import TypeVar, Dict, List, Tuple, Any
import sqlite3
from sqlite3 import Error
from ehr_analysis import Patient, Lab, parse_data, num_older_than, sick_patients
