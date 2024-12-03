import os
import csv
import pandas as pd
from openai import OpenAI
from config import OPENAI_API_KEY

OPENAI_CLIENT = OpenAI(api_key=OPENAI_API_KEY)
JOB_DESCRIPTION = open("job_description.txt", 'r').read()
PROMPT_TEMPLATE = open("prompt_template.txt").read()

def label_vaccine_barriers():
    """labels vaccine barrier categories on reddit submissions titles."""
    output = "reddit_submissions_vaccine_barriers.csv"
    prompt_template = open("prompt_barrier_categories.txt", 'r', encoding="utf-8").read()
    df = pd.read_csv("reddit_submissions_10k.csv", encoding='utf-8')
    if os.path.isfile(output):
        already_completed = pd.read_csv(output, encoding="utf-8")
        df = df[~df['id'].isin(already_completed['id'].to_list())]
    for index, row in df.iterrows():
        post_text = row['title']
        formatting_text = {"post_type": "reddit submission title",
                           "post_text": post_text}
        formatted_prompt = prompt_template.format(**formatting_text)
        response = single_prompt_response(formatted_prompt)
        if index % 100 == 0:
            print(index)
            print(formatted_prompt)
            print("CHAT GPT RESPONSE:", response)
        row['cgpt_response'] = response
        row_dict = row.to_dict()        
        save_results_to_file(output, row_dict)
def call_cgpt():
    for input_filename, output_filename, post_type, post_text_column in [
        ("tweets_10k.csv", "tweets_10k_labeled.csv", "tweet", "tweet_text"),
        ("reddit_submissions_10k.csv", "reddit_submissions_10k_labeled.csv", "reddit submission title", "title"),
        ("reddit_comments_10k.csv", "reddit_comments_10k_labeled.csv", "reddit comment text", "body")
    ]:
        df = pd.read_csv(input_filename, encoding="utf-8")
        if os.path.isfile(output_filename):
            already_completed = pd.read_csv(output_filename, encoding="utf-8")
            df = df[~df['id'].isin(already_completed['id'].to_list())]
            # print(already_completed['id'].to_list())
            # print(df['id'].tolist()[:10])
        # print(input_filename, len(df))
        for index, row in df.iterrows():
            if post_text_column == "body":
                post_text = row[post_text_column][:500] # first 500 chars for reddit comment body
            else:
                post_text = row[post_text_column]
            formatting_text = {"post_type": post_type,
                               "post_text": post_text}
            formatted_prompt = PROMPT_TEMPLATE.format(**formatting_text)
            response = single_prompt_response(formatted_prompt)
            if index % 100 == 0:
                print(post_type, index)
                print(formatted_prompt)
                print("CHAT GPT RESPONSE:", response)
            row['cgpt_response'] = response
            row_dict = row.to_dict()        
            save_results_to_file(output_filename, row_dict)
        
def single_prompt_response(prompt):
    """create a chatgpt instance, feed it one single prompt, and return the reply"""
    
    # temperature = get_temperature()
    # top_p = get_top_p()
    # presence_penalty = get_presence_penalty()
    # frequency_penalty = get_frequency_penalty()
    completion = OPENAI_CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": JOB_DESCRIPTION},
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response

def save_results_to_file(file_path, row_dict):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row_dict.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)

        
if __name__ == "__main__":
    label_vaccine_barriers()

