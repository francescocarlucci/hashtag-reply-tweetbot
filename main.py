import tweepy

def get_credentials():

    credentials = {}

    with open('credentials.txt', 'r') as credentials_file:
        for line in credentials_file:
           (key, val) = line.split(':')
           credentials[key] = val.rstrip('\n')

    return credentials

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

def main():

    credentials = get_credentials()

    oauth = tweepy.OAuthHandler(credentials['pk'], credentials['sk'])
    oauth.set_access_token(credentials['pt'], credentials['st'])

    session = tweepy.API(oauth)

    since_id = get_since_id()

    try:

        for tweet in session.search(q="coronavirus", lang="it", result_type="recent", count=1, since_id=int(since_id)):

            tweet_id = tweet.id

            session.update_status(status = '#andratuttobene :)', in_reply_to_status_id = tweet_id, auto_populate_reply_metadata=True)

            update_log([ tweet_id, tweet.user.name ])

        update_since_id(tweet_id)

    except:
        print("Ops, something went wrong!")

if __name__ == '__main__':
    main()
