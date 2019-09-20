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

def create_vdict(vocabulary):
 dimension = len(vocabulary) #Dimension of the vector
 vec_dict = {}
 #for each word set a vector in dictionary
 for pair in vocabulary:
  vec_dict[pair] = np.zeros(dimension, dtype=int)
 return vec_dict

def get_cdict(vocabulary,lemma_list):
  cont_dict = {}
  for i in range(len(vocabulary)):
    entry = vocabulary[i]
    cont_dict[entry] = get_context(entry,lemma_list)
  return cont_dict

def count_freq(vocabulary,v_dict,c_dict):
 for i in range(len(vocabulary)):
  key = vocabulary[i]
  vector = v_dict[key]
  context = c_dict[key]
  for pair in context:
   index = vocabulary.index(pair)
   vector[index] = vector[index] + 1

def eowc_freq(vocabulary,v_dict,c_dict):
 for i in range(len(vocabulary)):
  key = vocabulary[i]
  vector = v_dict[key]
  context = c_dict[key]
  total_words = len(context)
  for pair in context:
   index = vocabulary.index(pair)
   vector[index] = vector[index] + 1
  vector = vector/total_words

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

  
if __name__=='__main__':
   lemma_list = load_data("lemma_list.pkl")
   vocabulary = load_data("vocabulary.pkl")
   vectors_dict = create_vdict(vocabulary) #Create vector's dictionary
   context_dict = get_cdict(vocabulary,lemma_list) #Get ocurrences's dictionary
   """ Raw count frequency """
   #count_freq(vocabulary,vectors_dict,context_dict) #Raw frequency 
   #save_data(vectors_dict,"count_vectors.pkl")
   """ EOWC frequency """
   eowc_freq(vocabulary,vectors_dict,context_dict) #EOWC frequency
   save_data(vectors_dict,"eowc_vectors.pkl")
