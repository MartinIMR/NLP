import nltk
import numpy as np
from bs4 import BeautifulSoup

def load_data(file_name):
  from pickle import load 
  input = open(file_name,"rb")
  data = load(input)
  input.close()
  return data

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

def idf_vector(context_dict):
  context_keys = list(context_dict.keys())
  m = len(context_keys) 
  vector = np.zeros(m, dtype=float)
  for i in range(m):
   vector[i] = m+1
  vector = np.log( (vector + 1) )
  for i in range(m):
    k = 0
    word = context_keys[i]
    for key in context_dict.keys():
     context = context_dict[key]
     if word in context:
      k = k + 1
    vector[i] = vector[i]/k
  return vector

def norm_dict(bm_dic,idf_vec):
  norm_dic = {}
  for key in bm_dic.keys():
    norm_dic[key] = np.multiply(bm_dic[key],idf_vec)
  return norm_dic

def save_data(data,name):
    from pickle import dump
    output = open(name,"wb")
    dump(data,output, -1) #mete bytes en archivo nuestro diccionario de lemmas
    output.close()

if __name__=='__main__':
  """
  vocabulary = load_data("vocabulary.pkl")
  context_dict = load_data("context_dic.pkl")
  #vectors_dict = load_data("bm25_vectors.pkl") #Create vector's dictionary
  #sought = "haber"
  #entry = search_entry(sought,vectors_dict) # Search for pair of the word 
  #Creating idf vector 
  #idf_v = idf_vector(context_dict)
  #save_data(idf_v,"idf_vector.pkl")
  #Loading idf vector
  idf_v = load_data("idf_vector.pkl")
  bm25_dict = load_data("bm25_vectors.pkl")
  word1 = "dólar"
  entry1 = search_entry(word1,vocabulary)
  word2 = "ver"
  entry2 = search_entry(word2,vocabulary)
  vec1 = bm25_dict[entry1]
  vec2 = bm25_dict[entry2]
  simil = okapi_sim(vec1,vec2,idf_v)
  print("Sim between ",word1," and ",word2," is:")
  print(simil)
  """

  vocabulary = load_data("vocabulary.pkl")
  context_dict = load_data("context_dic.pkl")

  """ WORD """
  word = "dólar"
  entry = search_entry(word,vocabulary)
  """ LIST 1:POS and RAW FREQUENCY """
  raw_dict = load_data("count_vectors.pkl") 
  dicsim_coseno = cos_dict(entry,raw_dict)
  list_cos = convert_list(dicsim_coseno)
  print("For the word:",word)
  print("\n")
  print("Coseno similitud:")
  print(list_cos[:200])
  
  """ LIST 2:IDF FREQUENCY """
  print("\n")
  bm_dict = load_data("bm25_vectors.pkl") 
  idf_vec = load_data("idf_vector.pkl") 
  dicsim_okapi = okapi_dict(entry,bm_dict,idf_vec)
  list_bm = convert_list(dicsim_okapi)
  print("BM25 similitud:")
  print(list_bm[:200])
  print("\n")

  """ LIST 3:COS AND IDF """
  print("\n")
  bmnorm_dict = norm_dict(bm_dict,idf_vec)
  dicsim_mix = cos_dict(entry,bmnorm_dict)
  list_nbm = convert_list(dicsim_mix)
  print("COS and BM25 similitud:")
  print(list_nbm[:200])

