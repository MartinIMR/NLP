import nltk
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

def get_context_list(word,tagged_words):
  window = 8
  bound = len(tagged_words)
  moves = (window//2)
  context_list = []
  for pair in tagged_words:
    if word == pair[0]:
     index = tagged_words.index(pair)
     min = index - moves
     max = index + moves + 1
     if min < 0:
      min = 0
     if max > bound:
      max = bound
     ady_list = []
     print("The word index is:",index)
     for i in range(min,max): #Ocurrences
       if i != index:
         print("The word in position:",i,"is added")
         ady_list.append(tagged_words[i]) 
     context_list = context_list + ady_list 
  return context_list

if __name__=='__main__':
  file_name = "e960401_mod.htm"
  r_sentences = tokenize(file_name) #Getting the text string 
  tagged_words = tag_sentences(r_sentences) #Tag sentences
  lemma_dict = lemmatization(tagged_words)
  vocabulary = set(lemma_dict)
  lista = get_context_list("caminar",tagged_words)
  print(lista)
