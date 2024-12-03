# check how many rows are in mutlilabel.csv
import pandas as pd

df = pd.read_csv("data/multilabel.csv")

def convert_values(submission_ids, col, value):
    """for a given list of [subsmission_ids], change all of their [col] values to [value]"""
    for i in submission_ids:
        if i not in df['id'].tolist():
            raise ValueError(f"id {i} doesn't exist in data")
        else:
            df.loc[df['id']==i, col]=value


def donotcallthis():
    ## EXAMPLE USAGE FOR INDIVIDUAL ROWS
    changes = [
        (["pu59ni"], "Mandates", False),
        (["pl8yosm"], "Logistics", False), 
        (["p06nv2"], "Mandates", False)
    ]
    for i in changes:
        convert_values(i[0], i[1], i[2])
    df.to_csv("multilabel_fixed.csv", index=False)


def print_category(category_name):
    filtered = df[df[category_name]==True]
    filtered_true = filtered[filtered['Negative']==True]
    filtered_false = filtered[filtered['Negative']==False]
    problem_highlighted = filtered[filtered['Highlight Problem']==True]
    print("="*30, category_name, "where Negative True", "="*30)
    for idx, row in filtered_true.iterrows():
        print(row['id'], row['title'])
    print("="*30, category_name, "where Negative False", "="*30)
    for idx, row in filtered_false.iterrows():
        print(row['id'], row['title'])
    print("="*30, category_name, "where Problem Highlighted", "="*30)
    for idx, row in problem_highlighted.iterrows():
        print(row['id'], row['title'])
    print("="*100)
    print()

categories = ['Mandates', 'Logistics', 'Efficacy', 'Side Effects', 'Conspiracy', 'General Discussion', 'Testing']
for category in categories:
    print_category(category)
