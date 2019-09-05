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

def clean_tokens(sentences):
  clean_sentences = []
  for sentence in sentences:
    print("-------SENTENCE--------")
    print(sentence)
    print("------END-------")
    tokens = nltk.word_tokenize(sentence)
    print("----------TOKENS-------")
    print(tokens)
    print("----------END-------")
    new_sentence = ""
    for token in tokens:
      new_sentence = []
      cleaned = re.sub("![a-záéíóúñü]","")

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

if __name__=='__main__':
  file_name = "e960401_mod.htm"
  r_sentences = tokenize(file_name) #First tokenization (Remove tags and tokenize)
  c_sentences = clean_tokens(r_sentences) #Remove non words and stopwords
  #tagged_words = tag_sentences(r_sentences) #Tag sentences
