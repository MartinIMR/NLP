import nltk
import os

data_path = "Data/"
tagger_name = "tagger.pkl"
lemmas_name = "olemmas.pkl"

def remove_tags(raw_text):
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(raw_text,"lxml")
  no_tags = soup.get_text()
  return no_tags

def tokenize(text_string):
  tokens = nltk.word_tokenize(text_string)
  return tokens

def lower(tokens):
  lower_case = [word.lower() for word in tokens]
  return lower_case

def lower_sentences(sentences):
  lower_case = []
  for sentence in sentences:
    sentence = sentence.split()
    lower_case.append([word.lower() for word in sentence])
  return lower_case

def remove_stopwords(tokens):
  from nltk.corpus import stopwords
  stop_words = stopwords.words("spanish")
  no_stopwords = [word for word in tokens if word not in stop_words]
  return no_stopwords

def tokenize_sentences(text_string): #Returns a list of sentences 
  sent_tokenizer = nltk.data.load("nltk:tokenizers/punkt/spanish.pickle")
  sentences = sent_tokenizer.tokenize(text_string)
  return sentences

def remove_stopwords_sentences(sentences): #Input is a list of sentences
  from nltk.corpus import stopwords
  stop_words = stopwords.words("spanish")
  no_stopwords = []
  for sentence in sentences:
    sentence = sentence.split() 
    new_sentence = [word for word in sentence if word not in stop_words]
    new_sentence = " ".join(new_sentence)
    no_stopwords.append(new_sentence)
  return no_stopwords

def remove_nowords(tokens):
  import re
  no_words = []
  for token in tokens:
    new_token = re.sub("[^a-záéíóúñü]","",token) #Leave only simple words
    if( new_token != "" ):
      no_words.append(new_token)
  return no_words

def remove_nowords_sentences(sentences):
  import re
  new_text = []
  for sentence in sentences:
    words = sentence.split()
    new_sentence = []
    for word in words:
      new_word = re.sub("[^a-záéíóúñü]","",word) #Leave only simple words
      if(new_word != ""):
        new_sentence.append(new_word)
    new_sentence = " ".join(new_sentence)
    new_text.append(new_sentence)
  return new_text

def tag_text(tokens): #A list of tag in the word position 
  from pickle import load
  input = open(data_path+tagger_name,"rb")
  tagger = load(input)
  input.close()
  tagged_text = tagger.tag(tokens)
  tagged_text = [(pair[0],pair[1].lower()) for pair in tagged_text]
  print("First 50 pairs:",tagged_text[:50])
  return tagged_text
  """
  tagged_text = []
  for word in tokens:
    tagged = tagger.tag(words)
    sentence_tags = [pair[1].lower() for pair in tagged]
    text_tags.append(sentence_tags)
  return tagged_text
  """

def lemmatize(tokens):
  from pickle import load
  input = open(data_path+lemmas_name,"rb")
  lemmas = load(input)
  input.close()
  print("Read tokens:",tokens[:20])
  lemmatized = []
  for word in tokens:
    if word[0] in lemmas:
      lemma = lemmas[word[0]]
      new_pair = (lemma,word[1])
      lemmatized.append(new_pair)
    else:
      lemmatized.append(word)

  print("Lemmatized list:",lemmatized[:20])
  #lemmatized = " ".join(lemmatized) 
  return lemmatized


"""
if __name__ == "__main__":
  folder = "moviles/"
  reviews = []
  for filename in os.listdir(folder): #Open each file
    review = tokenize(folder+filename)
    reviews.append(review)
  normalized = []
  print(reviews[0])
  nostp = remove_stopwords(reviews[0])
  print("\nNo stopwords:")
  print(nostp)
  cleaned = remove_nowords(nostp)
  print("\nCleaned:")
  print(cleaned)
  text_tags = tag_text(cleaned)
  print("Lemmatized:")
  lemmatized = lemmatize(cleaned)
  print(lemmatized)
  for review in reviews:
    review = remove_stopwords(review)
"""
