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

infile = "reddit_submissions_vaccine_barriers.csv"
outfile = "vaccine_barriers_manually_labeled.csv"
indata = read_data_from_file(infile)
outdata = []
outdata = read_data_from_file(outfile)
remaining_data = []
outdata_ids = [i['id'] for i in outdata]
for row in indata:
    if row['id'] not in outdata_ids:
        remaining_data.append(row)
random.shuffle(remaining_data)
idx = 0
outdata_idx = len(outdata)
while True:
    if len(outdata) == len(indata):
        break
    row = remaining_data[idx]
    response = input(f"{row['title']} \n[E]ffectivness, [S]ide effects, [A]vailability, [N]/A, [H]ighlight problem, [U]ndo, [Q]uit\n")
    response = response.strip().lower()
    if response in ["e", "s", "a", "n", "h"]:
        row['manual_label'] = response
        if outdata_idx == len(outdata):
            outdata.append(row)
        elif outdata_idx < len(outdata):
            outdata[idx] = row
        else:
            raise RuntimeError("some index thing happened.")
        save_data_to_file(outdata, outfile)
        idx += 1
        outdata_idx +=1
    elif response == "u":
        idx -= 1
        outdata_idx -= 1
    elif response == "q":
        break
