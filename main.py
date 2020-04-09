import sys
import tweepy
from datetime import datetime

def get_credentials():

    credentials = {}

    with open('credentials.txt', 'r') as credentials_file:
        for line in credentials_file:
           (key, val) = line.split(':')
           credentials[key] = val.rstrip('\n')

    return credentials

def get_stopwords():

    with open('stopwords.txt', "r") as word:
        stop_words = word.read().split()

    return stop_words

def get_since_id():

    return open('sinceid.txt', 'r').read()

def update_since_id(tweet_id):

    update_since_id = open('sinceid.txt', 'w')
    update_since_id.write(str(tweet_id))
    update_since_id.close()

def update_log(content):

    with open('log.txt', 'a') as log:
        log.write(str(content))
        log.write(str('\n'))

def get_lastpost_date():

    return open('lastpost_date.txt', 'r').read()

def update_lastpost_date(today):

    update_lastpost_date = open('lastpost_date.txt', 'w')
    update_lastpost_date.write(str(today))
    update_lastpost_date.close()

def main():

    credentials = get_credentials()

    oauth = tweepy.OAuthHandler(credentials['pk'], credentials['sk'])
    oauth.set_access_token(credentials['pt'], credentials['st'])

    session = tweepy.API(oauth)

    since_id = get_since_id()

    today = datetime.today().strftime('%Y-%m-%d')

    lastpost_date = get_lastpost_date()

    tweet_sent = False

    stop_words = get_stopwords()

    if today == lastpost_date:

        print('You already tweeted today!')

        sys.exit(0)

    try:

        for tweet in session.search(q="coronavirus", lang="it", result_type="popular", count=100, since_id=int(since_id)):

            if tweet_sent:

                break

            tweet_id = tweet.id

            tweet_body = tweet.text

            has_stopwords = False

            # If the tweet has one of these... skip!
            for stop_word in stop_words:

                if stop_word.lower() in tweet_body.lower():

                    has_stopwords = True

            if has_stopwords:

                continue

            session.update_status(status = '#andratuttobene 🙂❤️', in_reply_to_status_id = tweet_id, auto_populate_reply_metadata=True)

            print(f"Yo! You felt a comment on: {tweet_body} (id:{tweet_id})")

            update_log([ tweet_id, tweet.user.name, tweet_body ])

            update_lastpost_date(today)

            tweet_sent = True

        update_since_id(tweet_id)

    except:
        print("Ops, something went wrong!")

if __name__ == '__main__':
    main()
