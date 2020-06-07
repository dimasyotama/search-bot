import nltk
import random
import string
import re, string, unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import wikipedia as wk
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")
# nltk.download('punkt') 
# nltk.download('wordnet')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

welcome_input = ("Hello","hello","Hi","hi","Sup","sup","What's up","what's up","Hey Bud","hey","Hey")
welcome_respon = ["hi","Hi","hey","Hei","hei","Hei There","hello","I am glad! You are talking to me"]
def welcome(user_response):
    for word in user_response.split():
        if word.lower() in welcome_input:
            return random.choice(welcome_respon)

data = open('HR.txt','r',errors = 'ignore')
raw = data.read()
raw = raw.lower()
sent_tokens = nltk.sent_tokenize(raw)

def Normalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    #word tokenization
    word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    
    #remove ascii
    new_words = []
    for word in word_token:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    
    #Remove tags
    rmv = []
    for w in new_words:
        text=re.sub("&lt;/?.*?&gt;","&lt;&gt;",w)
        rmv.append(text)
        
    #pos tagging and lemmatization
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    lmtzr = WordNetLemmatizer()
    lemma_list = []
    rmv = [i for i in rmv if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
        lemma_list.append(lemma)
    return lemma_list

def generate_response(user_response):
    robo_response = ""
    sent_tokens.append(user_response)
    TfidfVectorize = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
    tfidf = TfidfVectorize.fit_transform(sent_tokens)
    #vals = cosine_similarity(tfidf[-1], tfidf)
    vals = linear_kernel(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0) or "tell me about" or "search" in user_response:
        print("Checking Wikipedia")
        if user_response:
            robo_response = wikipedia_data(user_response) + "\n"
            return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

def wikipedia_data(input):
    reg_ex = re.search('tell me about (.*)', input)
    try:
        if reg_ex:
            topic = reg_ex.group(1)
            wiki = wk.summary(topic, sentences = 3)
            return wiki
    except Exception as e:
            print("No content has been found")

flag=True
print("My name is BOTSEARCH and I'm a searchbot. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response = user_response.lower()
    if(user_response not in ['bye','shutdown','exit', 'quit']):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("BOTSEARCH : You are welcome..")
        else:
            if(welcome(user_response)!=None):
                print("BOTSEARCH : "+welcome(user_response))
            else:
                print("BOTSEARCH : ",end="")
                print(generate_response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("BOTSEARCH : Bye!!! ")