import nltk
def tokenize(text_string):
  tokens = nltk.Text(nltk.word_tokenize(text_string))
  return tokens

def remove_stopwords(text):
  from nltk.corpus import stopwords
  sw = stopwords.words("spanish")
  content = [w for w in text if w not in sw]
  return content

def sort_tokens(tokens):
  tokens.sort()
  ordered_tokens = tokens
  return ordered_tokens

def convert_lower_case(tokens):
  lower_case_tokens = [token.lower() for token in tokens]
  return lower_case_tokens

def get_clean_tokens(tokens):
  import re
  clean_tokens = []
  for token in tokens:
    clean_token = []
    for char in token:
      if re.match("[a-záéíóúñü]",char):
        clean_token.append(char)
    clean_string = "".join(clean_token)
    if clean_string != "":
     clean_tokens.append(clean_string)
  return clea_tokens

def delete_tags(file_string):
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(file_string,"lxml")
  file_string = soup.get_text()
  return file_string

def get_text(fname):
  file = open(fname, "r", encoding="UTF-8")
  file_string = file.read()
  file.close()
  return file_string 

def write_text(text_string,fname):
  file = open(fname,"w",encoding="UTF-8")
  file.write(text_string)
  file.close()

if __name__=='__main__':
  fname="e960401_mod.htm"
  readed = get_text(fname)
  print("There are:",len(tokenize(readed))," before html removal.")
  no_tags = delete_tags(readed)
  print("There are:",len(tokenize(no_tags))," after html removal.")
  tokens = convert_lower_case(tokenize(readed))
  print("There are:",len(tokens)," tokens.")
  ordered = sort_tokens(tokens)
  removed = remove_stopwords(ordered)
  print("There are:",len(removed)," tokens without stopwords")
  write_text(readed,"clear.txt")
