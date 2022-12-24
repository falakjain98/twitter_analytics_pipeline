"""!pip install -q transformers
!pip install -q sentencepiece
!pip install -q textblob
!pip install -q emot"""

import pandas as pd

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from emot.emo_unicode import UNICODE_EMOJI

from textblob import TextBlob
from transformers import pipeline

# remove hashtags
def hashtags(text):
  hash = re.findall(r"#(\w+)", text)
  return hash

# remove mentions
def mentions(text):
  mention = re.findall(r"@(\w+)", text)
  return mention

# translate emoji
def emoji(text):
  for emot in UNICODE_EMOJI:
    if text == None:
      text = text
    else:
      text = text.replace(emot, "_".join(UNICODE_EMOJI[emot].replace(",", "").replace(":", "").split()))
    return text

# remove retweet username and tweeted at @username
def remove_users(tweet):
  '''Takes a string and removes retweet and @user information'''
  tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) 
  # remove tweeted at
  return tweet

# remove links
def remove_links(tweet):
  '''Takes a string and removes web links from it'''
  tweet = re.sub(r'http\S+', '', tweet) # remove http links
  tweet = re.sub(r'bit.ly/\S+', '', tweet) # remove bitly links
  tweet = tweet.strip('[link]') # remove [links]
  return tweet

def clean_html(text):
  html = re.compile('<.*?>')#regex
  return html.sub(r'',text)

# remove non ascii character
def non_ascii(s):
  return "".join(i for i in s if ord(i)<128)

def lower(text):
  return text.lower()

# remove email address
def email_address(text):
  email = re.compile(r'[\w\.-]+@[\w\.-]+')
  return email.sub(r'',text)

# remove stopwords
def removeStopWords(str):
# select english stopwords
  cachedStopWords = set(stopwords.words("english"))
# add custom words
  cachedStopWords.update(('and','I','A','http','And','This','When','It','These','these','regards','email'))
# remove stop words
  new_str = ' '.join([word for word in str.split() if word not in cachedStopWords or word=='not' or word=='very']) 
  return new_str

def remove_(tweet):
  tweet = re.sub('([_]+)', "", tweet)
  return tweet

# apply all functions and perform sentiment analysis
def clean_data_nlp(df):
    # apply all the functions above
    df['hashtag'] = df.tweet.apply(func = hashtags)
    df['mention'] = df.tweet.apply(func = mentions)
    df['new_tweet'] = df.tweet.apply(func = emoji)
    df['new_tweet'] = df.new_tweet.apply(func = remove_users)
    df['new_tweet'] = df.new_tweet.apply(func = clean_html)
    df['new_tweet'] = df.new_tweet.apply(func = remove_links)
    df['new_tweet'] = df.new_tweet.apply(func = non_ascii)
    df['new_tweet'] = df.new_tweet.apply(func = lower)
    df['new_tweet'] = df.new_tweet.apply(func = email_address)
    df['new_tweet'] = df.new_tweet.apply(func = removeStopWords)
    df['new_tweet'] = df.new_tweet.apply(func = clean_html)
    df['new_tweet'] = df.new_tweet.apply(func = remove_)

    # Using a specific model for sentiment analysis
    specific_model = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment")

    df['prediction'] = df['new_tweet'].apply(lambda x: (specific_model(x)[0]['label'],specific_model(x)[0]['score']))
    df['score'] = df['prediction'].apply(lambda x: round(x[1],2))
    df['sentiment'] = df['prediction'].apply(lambda x: x[0])
    df['sentiment'] = df['sentiment'].map({'LABEL_2':2,'LABEL_1':1,'LABEL_0':0})
    df['subjectivity'] = df['new_tweet'].apply(lambda x: round(TextBlob(x).sentiment.subjectivity,2))
    df.drop(columns = ['prediction'], inplace = True)
    return (df)