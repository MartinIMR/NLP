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
  from nltk.corpus import stopwords
  sw = stopwords.words("spanish")
  clean_sentences = []
  for sentence in sentences:
   print("-------ORIGINAL SENTENCE--------")
   print(sentence)
   print("------END-------")
   tokens = nltk.word_tokenize(sentence)
   print("---------- RAW TOKENS-------")
   print(tokens)
   print("----------END-------")
   tokens = [word for word in tokens if word not in sw] 
   print("----------NO SW TOKENS-------")
   print(tokens)
   print("----------END-------")
   new_sentence = []
   for token in tokens:
    cleaned = re.sub("![a-záéíóúñü]","",token)
    if(token != ""):
     new_sentence.append(cleaned)
   new_sentence = " ".join(new_sentence)
   print("-------CLEAN SENTENCE--------")
   print(new_sentence)
   print("------END-------")
   clean_sentences = cleaned_sentences + new_sentence
  return clean_sentences


def lemmatization(pairs):
  from pickle import load 
  input = open("lemmas.pkl","rb")
  lemmas = load(input)
  input.close()
  lemma_dict = []
  for pair in pairs:
    key = pair[0]+" "+pair[1][0] #Word and category
    if key in lemmas: 
     lemma = lemmas[key]
     lemma_dict.append(lemma)
  return lemma_dict

def get_context(word,source):
  window = 8
  bound = len(source)
  moves = (window//2)
  context_list = []
  for index in range(bound):
    if word == source[index]:
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

def get_context_dict(vocabulary,lemma_dict):
  cont_dict = {}
  for i in range(len(vocabulary)):
    entry = vocabulary[i]
    cont_dict[entry] = get_context(entry,lemma_dict)
  return cont_dict

def create_vdict(vocabulary):
 dimension = len(vocabulary) #Dimension of the vector
 vec_dict = {}
 #for each word set a vector in dictionary
 for word in vocabulary:
  vec_dict[word] = np.zeros(dimension, dtype=int)
 return vec_dict


if __name__=='__main__':
  file_name = "e960401_mod.htm"
  r_sentences = tokenize(file_name) #Getting the text string
  clean_sentences = clean_tokens(r_sentences)
  #tagged_words = tag_sentences(r_sentences) #Tag sentences
  #lemma_dict = lemmatization(tagged_words)
  #vocabulary = sorted(set(lemma_dict))
  #vectors_dictionary = create_vdict(vocabulary) #Create vector's dictionary
  #context_dictionary = get_context_dict(vocabulary,lemma_dict)
