import nltk
import numpy as np
import math as mt

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

def conditional_entropy_dict(vocabulary,marginal_list,marginal_dict):
  dimension = len(vocabulary)
  entropy_dict = {}
  for i in range(dimension): #First word
    word1 = vocabulary[i]
    entropy_vector = np.zeros(dimension, dtype=float)
    vec1_prob = marginal_dict[word1] # A vector of probability for first word P(w11,w-i1)
    pw10 = marginal_list[i][0] 
    pw11 = marginal_list[i][1]
    for j in range(dimension): #Second word
      word2 = vocabulary[j]
      pw20 = marginal_list[j][0]
      pw21 = marginal_list[j][1]
      pw11w21 = vec1_prob[j]
      pw11w20 = pw11 - pw11w21 
      pw10w21 = pw21 - pw11w21
      pw10w20 = pw10 - pw10w21

      hw1w2 = ( pw10w20*mt.log(pw10w20) + pw11w20*mt.log(pw11w20) ) / ( -pw20 ) \
            - ( pw10w21*mt.log(pw10w21) + pw11w21*mt.log(pw11w21) ) / ( pw21 ) 
      entropy_vector[j] = hw1w2
    entropy_dict[word1] = entropy_vector
  return entropy_dict

def create_idfvect(vocabulary,context_dict):
  dimension = len(vocabulary)
  vector = np.log(np.full(dimension,dimension+1, dtype=float) + 1)
  print(vector)
  for i in range(dimension):
    k = 0
    word = vocabulary[i]
    for key in context_dict.keys():
     context = context_dict[key]
     if word in context:
      k = k + 1
    vector[i] = vector[i]/k
  return vector


def create_lenvec(vocabulary,context_dict):
  """ This function create a vector, each position is the length of its context"""
  dimension = len(vocabulary)
  len_vector = np.zeros(dimension, dtype=int)
  for i in range(dimension):
    key = vocabulary[i]
    len_vector[i] = len(context_dict[key]) #The length of the i-context
  return len_vector

def create_cvector(vocabulary,context):
  dimension = len(vocabulary)
  ct_vector = np.zeros(dimension, dtype=int) #Each position is a word
  for i in range(dimension):
    word = vocabulary[i] # Actually this is a pair, the real word is in word[0]
    if word in context: # Only do the for if the word is inside
     count = 0
     for pair in context:
       if pair == word:
         count = count + 1
     ct_vector[i] = count
  return ct_vector 
 
def create_bm25dict(vocabulary,context_dict):
 k = 1.5
 b = 0.75
 dimension = len(vocabulary)
 len_vec = create_lenvec(vocabulary,context_dict) # This is the same for all words (Calculate once)
 average = np.sum(len_vec)/dimension # The same for all words (Calculate once) 
 modified = k * ( (1 - b) + (b*len_vec) ) # The same
 bm25_dict = {}
 for i in range(dimension):
   pair = vocabulary[i] # pair[0] <=> Word in the i-position <=> i-word 
   context = context_dict[pair] # i-word's context
   count_vector = create_cvector(vocabulary,context)# Get the i-word's context count vector
   numerator = count_vector * (k + 1) # i-word's numerator vector
   denominator = count_vector + modified[i] # i-word's denominator vector
   bm25_vector = np.divide(numerator,denominator) # i-word's bm25 vector 
   bm25_dict[pair] = bm25_vector
 return bm25_dict 

def create_nbm25dict(vocabulary,bm25_dict):
  dimension = len(vocabulary)
  normalized = {}
  for i in range(dimension):
    pair = vocabulary[i]
    normalized[pair] = bm25_dict[pair]/np.sum(bm25_dict[pair]) 
  return normalized 

def get_marginal_list(vocabulary,lem_sent):
  dimension = len(vocabulary)
  total_sent = len(lem_sent)
  marginal_list = []
  for i in range(dimension):
    ocurrences = 0
    word = vocabulary[i][0]
    for sent in lem_sent: 
      sent_tokens = nltk.word_tokenize(sent)
      if word in sent_tokens:
        ocurrences = ocurrences + 1
    probability = ocurrences/total_sent
    tuple = ( (1 - probability) , probability ) # First position P(w=0), secong P(w=1) 
    marginal_list.append(tuple)
  return marginal_list

def get_marginal_dict(vocabulary,lem_sents):
  dimension = len(vocabulary)
  total_sent = len(lem_sent)
  lem_list = []
  for sentence in lem_sents:# Convert sentence to list for a faster search
    lem_list.append(nltk.word_tokenize(sentence))
  marginal_dict = {}
  for i in range(dimension): #For each word in vocabulary
    vector = np.zeros(dimension ,dtype = int) #Create the vector for the i-word
    w1 = vocabulary[i][0] #First word
    for s in range(total_sent): #Search the first word in each sentence
      sentence = lem_list[s]
      if w1 in sentence: # If in, then iterate for every word in vocabulary
        for j in range(dimension): 
          w2 = vocabulary[j][0]
          if w2 in sentence: #If both words in, then increment vector's pos
            vector[j] = vector[j] + 1
    vector = vector/total_sent
    marginal_dict[vocabulary[i]] = vector
  return marginal_list

if __name__=='__main__':
   """
   lemma_list = load_data("words/lemma_list.pkl")
   vocabulary = load_data("words/vocabulary.pkl")
   context_dict = load_data("vectors/context_dict.pkl") #Get ocurrences's dictionary
   bm25_dict = create_bm25dict(vocabulary,context_dict)
   save_data(bm25_dict,"vectors/bm25_dict.pkl")
   normalized_bm25 = create_nbm25dict(vocabulary,bm25_dict)
   save_data(normalized_bm25,"vectors/normalized_dict.pkl")
   idf_vector = create_idfvect(vocabulary,context_dict)
   save_data(idf_vector,"vectors/idf_vector.pkl")
   """
   vocabulary = load_data("words/vocabulary.pkl")
   lem_sent = load_data("words/lemmatized_sentences.pkl")
   marginal_list = get_marginal_list(vocabulary,lem_sent)
   save_data(marginal_list,"words/marginal_list.pkl")
   marginal_vectors = get_marginal_dict(vocabulary,lem_sent)
   save_data(marginal_vectors,"words/marginal_dict.pkl")
