import nltk
import numpy as np
from bs4 import BeautifulSoup

def load_data(file_name):
  from pickle import load 
  input = open(file_name,"rb")
  data = load(input)
  input.close()
  return data

def print_relations(entry,relations):
 word = entry[0]
 category = entry[1]
 print("The word:",word," has the following relations")
 for key in relations.keys():
   key_cat = key[1]
   if category == key_cat:
    coseno = relations[key]
    if coseno >= 0.1:
     print(key[0],":",relations[key])

def search_entry(word,vec_dict):
 word_key = ""
 for pair in vec_dict.keys():
   entry = pair[0]
   if word == entry:
    word_key = pair
 return word_key

def cos_sim(word_key,vec_dict):
 dic_rel = {}
 word_vector = vec_dict[word_key]
 for key in vec_dict.keys():
   vector = vec_dict[key]
   coseno = np.dot(word_vector,vector) / \
   ( np.sqrt(np.sum(word_vector**2)) * np.sqrt(np.sum(vector**2)) )
   if coseno > 0:
    dic_rel[key] = coseno
 return dic_rel

def dot_sim(word_key,vec_dict):
 dic_rel = {}
 word_vector = vec_dict[word_key]
 for key in vec_dict.keys():
   vector = vec_dict[key]
   coseno = np.dot(word_vector,vector) / \
   ( np.sqrt(np.sum(word_vector**2)) * np.sqrt(np.sum(vector**2)) )
   if coseno > 0:
    dic_rel[key] = coseno
 return dic_rel


if __name__=='__main__':
  vectors_dict = load_data("vectors.pkl") #Create vector's dictionary
  sought = "haber"
  entry = search_entry(sought,vectors_dict) # Search for pair of the word 
  # Get the relations of the word
  dicsim_coseno = cos_sim(entry,vectors_dict)
  dicsim_dot = dot_sim(entry,vectors_dict)
  print("For the word:",sought," the similar words are:")
  #Function to print the relation of the word
  print_relations(entry,relations)
