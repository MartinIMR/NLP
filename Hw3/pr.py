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

if __name__=='__main__':
  file_name = "e960401_mod.htm"
  r_sentences = tokenize(file_name) #Getting the text string 
  tagged_words = tag_sentences(r_sentences) #Tag sentences
  print("Tagged list has:",len(tagged_words)," elements")
  print(tagged_words[:200])
