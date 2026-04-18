import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

stop_words = set(stopwords.words("english"))

# preprocess
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return tokens

# compare overlap
def compare_overlap(user_message, possible_response):
    return len(set(user_message) & set(possible_response))

# extract nouns
def extract_nouns(tagged_message):
    nouns = []
    for token in tagged_message:
        if token[1].startswith("N"):
            nouns.append(token[0])
    return nouns