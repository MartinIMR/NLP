from Modules import Files
from Modules import Norm
import nltk
import numpy as np
from bs4 import BeautifulSoup

def obtain_articles(file_name):
  file = open(file_name,encoding="utf-8")
  text = file.read()
  file.close()
  articles = text.split("<h3>")
  del articles[0]
  return articles

def tokenize(fname):
  f = open(fname,encoding="utf-8")
  t = f.read()
  articles = t.split("<h3>")
  #Remove the first article
  del articles[0]
  clean_articles = []
  sent_tokenizer = nltk.data.load("nltk:tokenizers/punkt/spanish.pickle")
  for article in articles:
    soup = BeautifulSoup(article,"lxml")
    text_article = soup.get_text()
    sentences = sent_tokenizer.tokenize(text_article)
    del sentences[-1] #Erase the last item
    #Convert to string again and append
    new_article = " ".join(sentences)
    clean_articles.append(new_article)
  return clean_articles

def clean_tokens(articles):
  import re
  from nltk.corpus import stopwords
  sw = stopwords.words("spanish")
  clean_articles = []
  for article in articles:
   tokens = nltk.word_tokenize(article)
   tokens = [token.lower() for token in tokens]
   tokens = [word for word in tokens if word not in sw] 
   new_article = []
   for token in tokens:
    cleaned = re.sub("[^(a-záéíóúñü)]","",token) #Leave only simple words
    if(cleaned != ""):
     new_article.append(cleaned)
   new_article = " ".join(new_article)
   clean_articles.append(new_article)
  return clean_articles

def tag_sentences(sentences):
  from pickle import load
  input = open("Data/tagger.pkl","rb")
  tagger = load(input)
  input.close()
  tagged = []
  for sent in sentences:
    tokens = nltk.word_tokenize(sent)
    s_tagged = tagger.tag(tokens)
    tagged = tagged + s_tagged
  return tagged

def lemmatize_articles(articles):
  from pickle import load
  input = open("Data/olemmas.pkl","rb")
  lemmas = load(input)
  input.close()
  lemmatized_articles = []
  for article in articles:
    lemmatized = []
    words = nltk.word_tokenize(article)
    words = [ word.lower() for word in words ]
    for word in words:
     if word in lemmas:
       lemma = lemmas[word]
       lemmatized.append(lemma)
     else:
       lemmatized.append(word)
    lemmatized = " ".join(lemmatized) 
    lemmatized_articles.append(lemmatized)
  return lemmatized_articles

def lemmatization(pairs):
  from pickle import load 
  input = open("Data/lemmas.pkl","rb")
  lemmas = load(input)
  input.close()
  lemma_list = []
  for pair in pairs:
    word = pair[0]
    category = pair[1][0]
    key = word+" "+category #Word and category
    if key in lemmas: 
     tuple = (lemmas[key],category.lower())
     lemma_list.append(tuple)
    else:
     tuple = (word,category.lower())
     lemma_list.append(tuple)
  return lemma_list

def get_vocabulary(lemma_list):
 vocabulary = set(lemma_list)
 vocabulary = sorted(vocabulary, key = lambda tup:tup[0])
 return vocabulary

def get_cdict(vocabulary,lemma_list):
  cont_dict = {}
  for i in range(len(vocabulary)):
    entry = vocabulary[i]
    cont_dict[entry] = get_context(entry,lemma_list)
  return cont_dict

def get_context(pair,source):
  word = pair[0]
  window = 8
  bound = len(source)
  moves = (window//2)
  context_list = []
  for index in range(bound):
    if word == source[index][0]:
     min = index - moves
     max = index + moves + 1
     if min < 0:
      min = 0
     if max > bound:
      max = bound
     ady_list = []
     for i in range(min,max): #Ocurrences
       if i != index:
        ady_list.append(source[i]) 
     context_list = context_list + ady_list 
  return context_list

   
if __name__=='__main__':
    file_name = "Data/e960401_mod.htm"
    articles = obtain_articles(file_name)

    """
    for i in range(len(articles)):
      article = articles[i]
      print("Articulo crudo:")
      print(article)
      article = Norm.remove_tags(article)
      print("Articulo sin etiquetas:")
      print(article)
      article = Norm.tokenize(article)
      article = Norm.lower(article)
      article = Norm.remove_stopwords(article)
      article = Norm.remove_nowords(article)
       
    readed_articles = tokenize(file_name) #Each element(article) is a list of strings
    clean_articles = clean_tokens(readed_articles) #Removing stopwords, and no words.
    lemmatized_articles = lemmatize_articles(clean_articles) #Lemmatize each article
    text_file = open("Output.txt", "w")
    text_file.write("Purchase Amount: %s" % TotalAmount)
    text_file.close()
    for i in range len(lemmatized_articles): 
    """  
