from bs4 import BeautifulSoup as bs
import re

def save_data(data,name):
 from pickle import dump
 output = open(name,"wb")
 dump(data,output,-1)
 output.close()


file = open("senticon.es.xml")
text = file.read()
file.close()
data = bs(text,"lxml")
tags = data.findAll("lemma")
pol_dict = {}
for tag in tags:
  pol_dict[tag.getText()] = float(tag.get("pol"))
save_data(pol_dict,"pols.pkl")
