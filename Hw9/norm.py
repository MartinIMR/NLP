import nltk
import os

def tokenize(file):
  file = open(file,encoding="Latin-1")
  raw = file.read()
  file.close()
  #Get list of sentences
  sent_tokenizer = nltk.data.load("nltk:tokenizers/punkt/spanish.pickle")
  sentences = sent_tokenizer.tokenize(raw)
  return sentences

def remove_stopwords(text): #Input is a list of sentences
  from nltk.corpus import stopwords
  sw = stopwords.words("spanish")
  no_stopwords = []
  for sentence in text:
    words = sentence.split() 
    new_sentence = []
    for word in words: 
      if( word not in sw): 
        new_sentence.append(word.lower())
    new_sentence = " ".join(new_sentence)
    no_stopwords.append(new_sentence)
  return no_stopwords

def remove_nowords(text):
  import re
  new_text = []
  for sentence in text:
    words = sentence.split()
    new_sentence = []
    for word in words:
      new_word = re.sub("[^a-záéíóúñü]","",word) #Leave only simple words
      if(new_word != ""):
        new_sentence.append(new_word)
    new_sentence = " ".join(new_sentence)
    new_text.append(new_sentence)
  return new_text

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

  """
  for review in reviews:
    review = remove_stopwords(review)
  """
