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

def get_context(word,source):
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

def get_cdict(vocabulary,lemma_list):
  cont_dict = {}
  for i in range(len(vocabulary)):
    entry = vocabulary[i]
    cont_dict[entry] = get_context(entry,lemma_list)
    print("The word:",entry," has the following context list:")
    print(cont_dict[entry])
  return cont_dict

def create_vdict(vocabulary):
 dimension = len(vocabulary) #Dimension of the vector
 vec_dict = {}
 #for each word set a vector in dictionary
 for word in vocabulary:
  vec_dict[word] = np.zeros(dimension, dtype=int)
 return vec_dict

def get_vocabulary(lemma_list):
 vocabulary = []
 for pair in lemma_list:
  vocabulary.append(pair[0])
 vocabulary = sorted(set(vocabulary))
 return vocabulary

def get_vectors(vocabulary,v_dict,c_dict):
 for i in range(len(vocabulary)):
  entry = vocabulary[i]
  vector = v_dict[entry]
  context = c_dict[entry]
  for pair in context:
  category = pair[1]


if __name__=='__main__':
  file_name = "e960401_mod.htm"
  r_sentences = tokenize(file_name) #Getting the text string
  clean_sentences = clean_tokens(r_sentences) #Removing stopwords, and no words.
  tagged_words = tag_sentences(clean_sentences) #Tag sentences
  lemma_list = lemmatization(tagged_words) #Lemmatization
  vocabulary = get_vocabulary(lemma_list) #Obtain vocabulary
  vectors_dict = create_vdict(vocabulary) #Create vector's dictionary
  context_dict = get_cdict(vocabulary,lemma_list) #Get ocurrences's dictionary
  vectors_dict = get_vectors() 
