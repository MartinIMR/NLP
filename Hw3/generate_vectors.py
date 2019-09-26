import nltk
import numpy as np

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

def idf_vector(vocabulary,context_dict):
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
 len_vec = create_lenvec(context_dict) # This is the same for all words (Calculate once)
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

if __name__=='__main__':
   lemma_list = load_data("words/lemma_list.pkl")
   vocabulary = load_data("words/vocabulary.pkl")
   context_dict = load_data("vectors/context_dict.pkl") #Get ocurrences's dictionary
   bm25_dict = create_bm25dict(vocabulary,context_dict)
   normalized_bm25 = create_nbm25dict(vocabulary,bm25_dict)
   
