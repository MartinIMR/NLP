import nltk
import string
import re
from bs4 import BeautifulSoup

def file_exist(file):
  import os
  if os.path.isfile(file):
   return True
  else:
   print("El archivo ",file," no existe")
   return False 

def obtain_reviews(folder):
  from nltk.corpus import stopwords
  sw = stopwords.words("spanish")
  for i in range(2,4380): #Open each document 2-4380
    print("Processing review ",i)
    file = folder+str(i)+".review.pos"
    if file_exist(file):
     review = open(file,encoding="Latin-1")
     lines = review.readlines()
     review.close()
     texto = []
     for line in lines:
       line = line.split()
       if((len(line) != 0) and (line[1] not in sw) and (line[1] not in string.punctuation)):
        texto.append(line[1])
     clean_text = []
     for word in texto:
       cleaned = re.sub("[^(a-záéíóúñü)]","",word) #Leave only simple words
       if(cleaned != ""):
         clean_text.append(cleaned)      
     texto = " ".join(clean_text)
     text_file = open("texts/"+str(i)+".txt","w")
     text_file.write(texto)
     text_file.close()

def obtain_ranks(folder):
  ranks = []
  for i in range(2,4380):
    file = folder + str(i)+".xml"
    if file_exist(file):
      xml = open(file,encoding="Latin-1")
      review = xml.read()
      xml.close()
      soup = BeautifulSoup(review,"lxml")
      review = soup.find_all("review")
      review = review[0]
      rank = review.get("rank")
      ranks.append(int(rank))
  return ranks

def save_data(data,name):
    from pickle import dump
    output = open(name,"wb")
    dump(data,output,-1)
    output.close()


if __name__ == "__main__":
 folder = "corpusCine/" 
 #obtain_reviews(folder)
 ranks = obtain_ranks(folder)
 print(ranks[:10]) 
 save_data(ranks,"ranks.pkl")
