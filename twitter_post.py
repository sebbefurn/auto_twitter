import tweepy
import openai
import discord_bot
import templates
import credentials
import sys
import random

# Make sure of right arguments
if len(sys.argv) < 3:
    print("You need an argument of which account to post to and an argument of what kind of post it is")
    exit()

# Get system arguments
account = sys.argv[1].strip()
post_type = sys.argv[2].strip()

possible_accounts = ["king", "entrepreneur", "fraudster", "billionaire"]
assert account in possible_accounts

possible_post_types = ["thread", "quote"]
assert post_type in possible_post_types

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

def get_image_prompt(tweet_content):
    my_template = templates.image_prompt_template(tweet_content)
    response = openai.ChatCompletion.create(
        model=llm4,
        messages=[{"role": "system", "content": my_template}],
    )
    return response.choices[0].message.content.strip()

def get_name_sequential(account):
    filename = f"ListFiles/{account}.txt"
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Check if name at index (line_number)
    try:
        line_number = int(lines[0])
        name = lines[line_number]
    except:
        print("Couldn't retreive a person")
        return

    lines[0] = str(line_number+1) + "\n"
    with open(filename, 'w') as file:
        file.writelines(lines)

    return name.strip()

def get_name_random(account):
    filename = f"ListFiles/{account}.txt"
    with open(filename, 'r') as file:
        names = file.readlines()[1:]

    # Check if the file is not empty
    name_index = random.randint(0,len(names)-1)

    return names[name_index].strip()

def generate_tweet(account):
    # Get name
    name = get_name_sequential(account)

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

def quote_tweet(account):
    # Get the name of the person to quote
    name = get_name_random(account)

    # The template to feed into GPT-4 to create the tweet
    my_template = templates.quote_template(name)

    # Generate tweet content
    response = openai.ChatCompletion.create(
        model=llm4,
        messages=[{"role": "system", "content": my_template}],
    )
    tweet_content = response.choices[0].message.content.strip()
    # Generate an image prompt based on the quote and person
    image_prompt = get_image_prompt(tweet_content)
    # Generate the image
    image = discord_bot.main("/imagine", credentials.channel_id, image_prompt)
    # Upload the image to twitter
    media_id = api.media_upload(filename=image).media_id_string
    # Tweet it!
    client.create_tweet(text=tweet_content, media_ids=[media_id])

if post_type == "thread":
    generate_tweet(account)
elif post_type == "quote":
    quote_tweet(account)