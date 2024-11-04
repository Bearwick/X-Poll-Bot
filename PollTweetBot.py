import time
from OpenAI_API import fetch_polls_openAI
from X_API import post_tweet
from Storage import setFileName, write_json

def fetch_polls(polls_to_fetch):
    try:
        return fetch_polls_openAI(polls_to_fetch)
    
    except Exception as e:
        print(f"Error fetching polls: {e}")

def create_tweet(poll):
    tweet = {}
    tweet_text = poll["text"]
    tweet_options = poll["options"]
    tweet_duration = 120

    if len(tweet_text) > 280:
        # Decide how to handle it
        return
    
    for option in tweet_options:
        if len(option) > 25:
            # Decide how to handle it
            return

    tweet["text"] = tweet_text
    tweet["poll"] = {"duration_minutes": tweet_duration, "options": tweet_options}
    # create a tweet that has a question and a poll for answers
    return tweet

def post_polls(polls, polls_per_day):
    # Check if polls is None or doesn't contain expected data
    
    for poll in polls["polls"]: # NoneType object is not subscriptable
        tweet = create_tweet(poll)
        rate_limit_reached, sleep_time = post_tweet(tweet)
        if rate_limit_reached:
            time.sleep(sleep_time)
        else:
            write_json(poll["text"])
            time.sleep(24*3600//polls_per_day)


if __name__ == "__main__":
    setFileName("questions.json")
    running = True
    while running:
        polls_per_day = 6
        polls_to_fetch = 10
        polls = fetch_polls(polls_to_fetch)

        if polls is None or "polls" not in polls:    
            print("Error: polls data is missing or not in the correct format.")
            running = False
        else:  
            post_polls(polls, polls_per_day)
