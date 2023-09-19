import tweepy
import openai
import discord_bot
import templates
import credentials
import sys

# Check which account to post to
possible_accounts = ["king", "entrepreneur", "fraudster", "billionaire"]
account = sys.argv[1].strip()
print(account + " : ")
assert account in possible_accounts

# API keyws that yous saved earlier
exec(f"api_key = credentials.{account}_api_key")
exec(f"api_secrets = credentials.{account}_api_secrets")
exec(f"access_token = credentials.{account}_access_token")
exec(f"access_secret = credentials.{account}_access_secret")
exec(f"bearer_token = credentials.{account}_bearer")
 
# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(
    bearer_token,
    api_key,
    api_secrets,
    access_token,
    access_secret,
    wait_on_rate_limit=True
)

openai.api_key_path = "/home/anon/.secret"

llm4 = "gpt-4-0613"

def generate_tweet(account):
    filename = f"ListFiles/{account}.txt"
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Check if the file is not empty
    try:
        line_number = int(lines[0])
        name = lines[line_number]
    except:
        print("Couldn't retreive a person")
        return

    lines[0] = str(line_number+1) + "\n"
    with open(filename, 'w') as file:
        file.writelines(lines)

    # Get Midjourney image
    image = discord_bot.main("/imagine", credentials.channel_id, name)

    my_template = templates.template(account, name.strip())

    # Generate twitter thread
    response = openai.ChatCompletion.create(
        model=llm4,
        messages=[{"role": "system", "content": my_template}],
    )

    # Process twitter thread
    tweet_content = response.choices[0].message.content.strip()
    tweets = tweet_content.split("######")
    print(tweet_content)
    
    # Upload image to twitter
    media_id = api.media_upload(filename=image).media_id_string
    print(media_id)

    # Upload thread
    response = client.create_tweet(text=tweets[0], media_ids=[media_id])
    prev_tweet_id = response.data['id']

    for tweet in tweets[1:]:
        response = client.create_tweet(text=tweet, in_reply_to_tweet_id=prev_tweet_id)
        prev_tweet_id = response.data['id']

if len(sys.argv) < 2:
    print("You need an argument of which account to post to")
    exit()


generate_tweet(account)