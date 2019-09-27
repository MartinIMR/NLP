import nltk
import numpy as np
from bs4 import BeautifulSoup

def load_data(file_name):
  from pickle import load 
  input = open(file_name,"rb")
  data = load(input)
  input.close()
  return data

def get_bm25vec(word,vocabulary,context_dict):
 k = 1.5
 b = 0.75
 dimension = len(vocabulary)
 len_vec = create_lenvec(context_dict)
 average = np.sum(len_vec)/dimension
 modified = k * ( (1 - b) + (b*len_vec) ) # The same
 pair = get_entry(word,vocabulary)

def convert_list(dict):
 list = []
 for key in dict.keys():
  tuple = (key[0],dict[key])
  list.append(tuple)
 list = sorted(list,key = lambda tup:tup[1], reverse = True)
 return list

def print_relations(entry,relations):
 word = entry[0]
 category = entry[1]
 print("The word:",word," has the following relations")
 for key in relations.keys():
   key_cat = key[1]
   if category == key_cat:
    print(key[0],":",relations[key])

def print_relation(vocabulary,vector):
  dimension = len(vocabulary)
  ordenado = []
  for i in range(dimension):
    tupla = (vector[i],i)
    ordenado.append(tupla)
  ordenado = sorted(ordenado,key = lambda tup:tup[0],reverse=True)
  for i in range(dimension//2): #Print half
    pair = ordenado[i]
    if(pair[0] == 0.0):
      break
    print(vocabulary[pair[1]][0],":",pair[0])

def search_entry(word,vocabulary):
 for i in range(len(vocabulary)):
   entry = vocabulary[i]
   if word == entry[0]:
    return entry

def cos_dict(word_key,vec_dict):
 dic_rel = {}
 word_vector = vec_dict[word_key]
 for key in vec_dict.keys():
   vector = vec_dict[key]
   coseno = np.dot(word_vector,vector) / \
   ( np.sqrt(np.sum(word_vector**2)) * np.sqrt(np.sum(vector**2)) )
   if coseno > 0:
    dic_rel[key] = coseno
 return dic_rel

def okapi_dict(word_key,vec_dict,idf_v):
 dic_rel = {}
 word_vector = vec_dict[word_key]
 for key in vec_dict.keys():
   vector = vec_dict[key]
   value = okapi_sim(word_vector,vector,idf_v) 
   if value > 0:
    dic_rel[key] = value
 return dic_rel

def okapi_sim(vec1,vec2,idf_v):
 mul_vec = np.multiply(vec1,vec2)
 mul_vec = np.multiply(idf_v,mul_vec)
 sum = np.sum(mul_vec)
 return sum


def save_data(data,name):
    from pickle import dump
    output = open(name,"wb")
    dump(data,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()

if __name__=='__main__':
  vocabulary = load_data("words/vocabulary.pkl")
  context_dict = load_data("vectors/context_dict.pkl")
  bm25n_dict = load_data("vectors/normalized_dict.pkl")
  idf_vector = load_data("vectors/idf_vector.pkl")
  dimension = len(vocabulary)
  """ WORD """
  word = "dólar"
  entry = search_entry(word,vocabulary)
  """ Syn. Relation """
  bm25n_vector = bm25n_dict[entry]
  syn = np.multiply(bm25n_vector,idf_vector)
  print("For the word:",word,".We have the following relations")
  print_relation(vocabulary,syn)
  
