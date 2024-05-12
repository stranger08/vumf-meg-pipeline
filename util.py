import csv
import numpy as np

SUBJECTS_LIST_FILE = 'subject-ids.csv'

def load_subjects_list():
    data = []
    with open(SUBJECTS_LIST_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return np.array(data).flatten()
