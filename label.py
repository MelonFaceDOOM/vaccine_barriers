import csv
import random
import os

def read_data_from_file(file):
    if not os.path.isfile(file):
        return []
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows

def save_data_to_file(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def get_start_idx(file):
    """read length of labeled file to determine how many rows are already labeled"""
    if os.path.isfile(file):
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return len(list(reader)) - 1 # - 1 cus of header
    else:
        return 0

label_values = {"l": "Logistics", "s": "Side Effects", "e": "Efficacy", "n": "Negative", "t": "Testing", "m": "Mandates", "c": "Conspiracy", "g": "General Discussion", "r": "Reject", "h": "Highlight Problem"}
infile = "reddit_submissions_vaccine_barriers.csv"
outfile = "multilabel.csv"
indata = read_data_from_file(infile)
outdata = []
outdata = read_data_from_file(outfile)
remaining_data = []
outdata_ids = [i['id'] for i in outdata]
for row in indata:
    if row['id'] not in outdata_ids:
        remaining_data.append(row)
random.shuffle(remaining_data)
for row in outdata:
    for key, value in label_values.items():
        if value not in row.keys():
            row[value] = False # if new labels are added to this code between sessions, make that label's value be false in all exising data
working_data = outdata + remaining_data # adding outdata allows the user to undo immediately to access the previous session
idx = len(outdata)
while True:
    if idx == len(working_data):
        break
    row = working_data[idx]

    response = input(f"{row['title']} \n[E]fficacy, [S]ide effects, [L]ogistics, [N]egative, [T]esting, [M]andates, [C]onspiracy, [G]eneral Discussion, [R]eject, [H]ighlight problem, [U]ndo, [Q]uit\n")
    response = response.strip().lower()
    response = response.split(",")
    response = [i.strip() for i in response] # allows for "a,b" as well as "a, b"
    
    if response[0] == "u":
        idx -=1
        continue
    elif response[0] == "q":
        break
    elif response[0] == '':
        response = [] # instead of ['']

    response_labels = []
    redo = False
    for i in response:
        if i in label_values.keys(): 
            response_labels.append(i)
        else:
            redo = True
    if redo:
        continue

    # at this point any possible skip has not occurred and we save data
    for letter, label_name in label_values.items():
        if letter in response_labels:
            row[label_name] = True
        else:
            row[label_name] = False
    if idx == len(working_data):
        working_data.append(row)
    elif idx < len(working_data):
        working_data[idx] = row
    else:
        raise RuntimeError("some index thing happened.")

    save_data_to_file(working_data[:idx+1], outfile)
    idx += 1
