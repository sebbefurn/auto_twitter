def template(account, name): 
    return f"""
You will write a twitter thread with somewhere between 5 to 7 tweets and each tweet should not be longer than 250 characters.
Since it a thread, always number each tweet with "tweetnumber/total tweets" in the beginning.

The first tweet should solely be a quote by the {account} followed by his name.
After that talk about what made them special and why they are worth knowing about.
Then tell the reader a true story about that {account} that showcase their special character and their special traits.
After that talk specifically about the character traits that made them powerful and preferably about the dark traits, like manipulation and ruthlessness for example.

Make sure it isn't cliche and don't use hashtags or emojis. Write simply and make it easy for the reader to understand, and keep the reader entertained.
Make sure to make the thread interesting by talking about entertaining and interesting things about the person. When choosing what is special about them, it can be their ruthlessness and manipulation for example.

Separate each tweet in the thread with exactly six hashed "######" and make sure to not include anything else than the series of tweets in your answer.

The {account} you will write about is: {name}

Remember to separate each tweet with "######".
"""