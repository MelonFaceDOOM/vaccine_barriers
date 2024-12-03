import time
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from config import VSM_CREDENTIALS

def main():
   get_samples()

def get_samples():
    """get representative sample of tweets & reddit submissions"""
    conn = psycopg2.connect(**VSM_CREDENTIALS)
    # create_indices(conn)
    get_tweets(conn, "tweets_10k.csv")
    print("tweets saved")
    get_reddit_submissions(conn, "reddit_submissions_10k.csv")
    print("reddit submissions saved")
    get_reddit_comments(conn, "reddit_comments_10k.csv")
    print("reddit comments saved")
    conn.close()
    
def get_other_data():
    df = pd.read_csv("tweets_10k_labeled.csv")
    tweet_vaccine_barrier_count = len(df[df['cgpt_response']=="True"])
    df = pd.read_csv("reddit_submissions_10k_labeled.csv")
    reddit_submission_vaccine_barrier_count = len(df[df['cgpt_response']=="True"])
    df = pd.read_csv("reddit_comments_10k_labeled.csv")
    reddit_comment_vaccine_barrier_count = len(df[df['cgpt_response']=="True"])
    
    conn = psycopg2.connect(**VSM_CREDENTIALS)
    cur = conn.cursor()
    cur.execute("""SELECT COUNT(*) FROM tweet""")
    count = cur.fetchone()[0]
    projected_total_vaccine_barrier_count = (tweet_vaccine_barrier_count/10_000) * count
    print('total tweets', count)
    print('tweet vaccine barrier count in 10k', tweet_vaccine_barrier_count)
    print('projected total tweet vaccine barrier count', projected_total_vaccine_barrier_count)
    cur.execute("""SELECT COUNT(*) FROM reddit_submission""")
    count = cur.fetchone()[0]
    projected_total_vaccine_barrier_count = (reddit_submission_vaccine_barrier_count/10_000) * count
    print('total reddit submissions', count)
    print('reddit submission vaccine barrier count in 10k', reddit_submission_vaccine_barrier_count)
    print('projected total reddit submission vaccine barrier count', projected_total_vaccine_barrier_count)
    cur.execute("""SELECT COUNT(*) FROM reddit_comment""")
    count = cur.fetchone()[0]
    projected_total_vaccine_barrier_count = (reddit_comment_vaccine_barrier_count/10_000) * count
    print('total reddit_comments', count)
    print('reddit comment vaccine barrier count in 10k', reddit_comment_vaccine_barrier_count)
    print('projected total reddit submission vaccine barrier count', projected_total_vaccine_barrier_count)
    cur.close()
    conn.close()
    
def create_indices(conn):
    cur = conn.cursor()
    t1 = time.perf_counter()
    cur.execute("""CREATE INDEX idx_tweet_date_entered_btree ON tweet USING btree (date_entered);""")
    t2 = time.perf_counter()
    print(f"Tweet index created: {t2-t1:.1f}")
    cur.execute("""CREATE INDEX idx_reddit_submission_created_utc_btree ON reddit_submission USING btree (created_utc);""")
    t3 = time.perf_counter()
    print(f"Reddit Submission index created: {t3-t2:.1f}")
    cur.execute("""CREATE INDEX idx_reddit_comment_created_utc_btree ON reddit_comment USING btree (created_utc);""")
    t4 = time.perf_counter()
    print(f"Reddit Comment index created: {t4-t3:.1f}")
    conn.commit()
    cur.close()
    
def get_tweets(conn, save_location):
    """split into 10_000 buckets, get 1 post per bucket"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        WITH ranked_data AS (
        SELECT *, 
               NTILE(10000) OVER (ORDER BY date_entered) AS bucket
        FROM tweet
        WHERE is_en = True
        ),
        sampled_data AS (
            SELECT DISTINCT ON (bucket) *
            FROM ranked_data
            ORDER BY bucket, RANDOM() -- Select one random row per bucket
        )
        SELECT *
        FROM sampled_data;
        """
    )
    tweets = cur.fetchall()
    df = pd.DataFrame(tweets)
    df.to_csv(save_location, encoding='utf-8', index=False)
    cur.close()
    
def get_reddit_submissions(conn, save_location):
    """split into 10_000 buckets, get 1 post per bucket"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        WITH ranked_data AS (
        SELECT *, 
               NTILE(10000) OVER (ORDER BY created_utc) AS bucket
        FROM reddit_submission
        WHERE is_en = True
        ),
        sampled_data AS (
            SELECT DISTINCT ON (bucket) *
            FROM ranked_data
            ORDER BY bucket, RANDOM() -- Select one random row per bucket
        )
        SELECT *
        FROM sampled_data;
        """
    )
    tweets = cur.fetchall()
    df = pd.DataFrame(tweets)
    df.to_csv(save_location, encoding='utf-8', index=False)
    cur.close()
    
def get_reddit_comments(conn, save_location):
    """split into 10_000 buckets, get 1 post per bucket"""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        WITH ranked_data AS (
        SELECT *, 
               NTILE(10000) OVER (ORDER BY created_utc) AS bucket
        FROM reddit_comment
        WHERE is_en = True
        ),
        sampled_data AS (
            SELECT DISTINCT ON (bucket) *
            FROM ranked_data
            ORDER BY bucket, RANDOM() -- Select one random row per bucket
        )
        SELECT *
        FROM sampled_data;
        """
    )
    tweets = cur.fetchall()
    df = pd.DataFrame(tweets)
    df.to_csv(save_location, encoding='utf-8', index=False)
    cur.close()

if __name__ == "__main__":
    main()
