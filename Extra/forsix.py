from Modules import Files
from Modules import Norm
import nltk

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

def get_vocabulary(lemma_list):
 vocabulary = set(lemma_list)
 vocabulary = sorted(vocabulary, key = lambda tup:tup[0])
 return vocabulary




if __name__ == "__main__":
  document_name = "Data/e960401_mod.htm"
  file = open(document_name, encoding = "UTF-8")
  document = file.read() #Open the document
  file.close()
  raw = Norm.remove_tags(document) #Remove the tags


  tokens = Norm.tokenize(raw) #Tokenize process 
  print("There are", len(tokens),"tokens.")
  print("Raw tokens:",tokens[:20])


  tokens = Norm.lower(tokens)
  tokens = Norm.remove_nowords(tokens)  #Get only words
  print("There are", len(tokens)," cleaned tokens.")
  print("Tokens after removing no words:",tokens[:20])


  tokens = Norm.remove_stopwords(tokens) #Remove stopwords
  print("There are", len(tokens)," after removing stopwords.")
  print("Tokens after removing stopwords:",tokens[:20])

  tokens = Norm.tag_text(tokens)
  print("There are", len(tokens)," tagged tokens.")
  print("These are the tags:",tokens[:20])
  print("Lets see if the tokens are still avaliable:")
  print(tokens[:20])

  tokens = Norm.lemmatize(tokens) 
  print("There are", len(tokens) ," after lemmatization.")
  print("These are the lemmatizated tokens:",tokens[:20])

  #Obtain frequencies with nltk
  simple = [pair[0] for pair in tokens]
  text = nltk.Text(simple) # Convert to type text
  fdist = nltk.FreqDist(text)
  vocabulary = sorted(fdist.keys()) #Get vocabulary
  mini = vocabulary[:30]
  for word in mini:
    print("Word:",word)
    print("Frequency:",fdist[word]) 
