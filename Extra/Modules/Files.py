def file_exists(file):
 import os
 if os.path.isfile(file):
  return True
 else:
  print("El archivo ",file," no existe")
  return False 

def load_data(file_name):
 from pickle import load 
 input = open(file_name,"rb")
 data = load(input)
 input.close()
 return data

def save_data(data,name):
 from pickle import dump
 output = open(name,"wb")
 dump(data,output,-1)
 output.close()
