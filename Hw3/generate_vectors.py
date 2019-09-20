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

def get_avg(context_dict):
 key_list = context_dict.keys()
 print("The voc size is:")
 size = len(key_list)
 sum = 0
 for key in key_list:
  sum = sum + len(context_dict[key])
 print("The total sum is:",sum)
 average = sum/size
 print("The average is:",average)
 return average

def count_context(word,context):
 count = 0
 for pair in context:
   if pair[0] == word:
    count = count + 1
 return count

def calc_bm25(word,context):
 """ This function arguments are the word and the 
     list of words' context """
 k = 1.5
 b = 0.75
 count = count_context(word,context)
 size = len(context)
 average = get_avg(context_dict)
 numerator = (k+1)*count
 denominator = count + k*( (1-b) + b*(size/average))
 bm25 = numerator / denominator
 return bm25

def bm25_dict(context_dict):
 key_list = context_dict.keys()
 vector_dic = {}
 for key in key_list: # Each key is a pair
  context = context_dict[key]
  vector_dict[key] = bm25_vector(context_dict,context)
 return vector_dic

def bm25_vector(context_dict,context):
 key_list = context_dict.keys()
 dimension = len(key_list)
 vector = np.zeros(dimension, dtype=float)
 sum = 0
 for i in range(dimension): #For each word calculate bm25 with that context
  vector[i] = calc_bm25(key_list[i][0],context) 
  sum = sum + vector[i]
 vector = vector / sum
 return vector 

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
   #vectors_dict = create_vdict(vocabulary) #Create vector's dictionary
   context_dict = get_cdict(vocabulary,lemma_list) #Get ocurrences's dictionary
   word = "crecer" 
   entry = get_entry(word,vocabulary)
   context = context_dict[entry]
   bm25wv = bm25_vector(context_dict,context)

   """ Raw count frequency """
   #count_freq(vocabulary,vectors_dict,context_dict) #Raw frequency 
   #save_data(vectors_dict,"count_vectors.pkl")
   """ EOWC frequency """
   #eowc_freq(vocabulary,vectors_dict,context_dict) #EOWC frequency
   #save_data(vectors_dict,"eowc_vectors.pkl")
   """ BM25 frequency """
   #vectors_dict = bm25_freq(context_dict)
   #save_data(vectors_dict,"eowc_vectors.pkl")

