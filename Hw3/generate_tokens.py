import nltk
import numpy as np
from bs4 import BeautifulSoup

def tokenize(fname):
  f = open(fname,encoding="utf-8")
  t = f.read()
  soup = BeautifulSoup(t,"lxml")
  text_string = soup.get_text()
  #Get list of sentences
  sent_tokenizer = nltk.data.load("nltk:tokenizers/punkt/spanish.pickle")
  sentences = sent_tokenizer.tokenize(text_string)
  return sentences

def clean_tokens(sentences):
  import re
  from nltk.corpus import stopwords
  sw = stopwords.words("spanish")
  clean_sentences = []
  for sentence in sentences:
   tokens = nltk.word_tokenize(sentence)
   tokens = [token.lower() for token in tokens]
   tokens = [word for word in tokens if word not in sw] 
   new_sentence = []
   for token in tokens:
    cleaned = re.sub("[^(a-záéíóúñü)]","",token) #Leave only simple words
    if(cleaned != ""):
     new_sentence.append(cleaned)
   new_sentence = " ".join(new_sentence)
   clean_sentences.append(new_sentence)
  return clean_sentences

def tag_sentences(sentences):
  from pickle import load
  input = open("tagger.pkl","rb")
  tagger = load(input)
  input.close()
  tagged = []
  for sent in sentences:
    tokens = nltk.word_tokenize(sent)
    s_tagged = tagger.tag(tokens)
    tagged = tagged + s_tagged
  return tagged

def lemmatization(pairs):
  from pickle import load 
  input = open("lemmas.pkl","rb")
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

def save_data(data,name):
    from pickle import dump
    output = open(name,"wb")
    dump(data,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()

def load_data(file_name):
  from pickle import load 
  input = open(file_name,"rb")
  data = load(input)
  input.close()
  return data

   
if __name__=='__main__':
    file_name = "e960401_mod.htm"
    r_sentences = tokenize(file_name) #Getting the text string
    clean_sentences = clean_tokens(r_sentences) #Removing stopwords, and no words.
    save_data(clean_sentences,"clean_sentences.pkl")
    tagged_words = tag_sentences(clean_sentences) #Tag sentences
    save_data(tagged_words,"tagged_words.pkl")
    lemma_list = lemmatization(tagged_words) #Lemmatization
    save_data(lemma_list,"lemma_list.pkl")
    vocabulary = get_vocabulary(lemma_list) #Obtain vocabulary
    save_data(vocabulary,"vocabulary.pkl")
    context_dict = get_cdict(vocabulary,lemma_list) #Get ocurrences's dictionary
    save_data(context_dict,"context_dic.pkl")

