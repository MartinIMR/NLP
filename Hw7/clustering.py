import nltk
import numpy as np
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans# define the k-means clustering function

def load_data(file_name):
  from pickle import load 
  input = open(file_name,"rb")
  data = load(input)
  input.close()
  return data

def classify_sklearn(X, y): 
  from sklearn.feature_extraction.text import CountVectorizer
  count_vect = CountVectorizer()
  X_counts = count_vect.fit_transform(X)

def file_exist(file):
  import os
  if os.path.isfile(file):
   return True
  else:
   print("El archivo ",file," no existe")
   return False 

def obtain_dataset(folder):
 texts = []
 for i in range(2,4380):
  file = folder+str(i)+".txt"
  if(file_exist(file)):
   text = open(file)
   texts.append(text.read())
   text.close()
 return texts

def k_means(feature_matrix, num_clusters=5):
km = KMeans(n_clusters=num_clusters,max_iter=10000)
km.fit(feature_matrix)
clusters = km.labels_
return km, clusters
# set k = 5, lets say we want 5 clusters from the 100 movies

num_clusters = 5

if __name__ == "__main__":
 folder = "texts/" 
 texts = obtain_dataset(folder)
 #y = load_data("ranks.pkl")
 X = CountVectorizer(texts)
 num_clusters = 5
  
