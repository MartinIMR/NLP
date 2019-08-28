import nltk
def tokenize(text_string):
  tokens = nltk.word_tokenize(text_string)
  return tokens

def remove_stopwords(tokens):
  from nltk.corpus import stopwords
  stop_words = stopwords.words("spanish")
  content = [w for w in tokens if w not in stop_words]
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
  return clean_tokens

def remove_tags(raw_text):
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(raw_text,"lxml")
  cleaned = soup.get_text()
  return cleaned

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
  file_name = "e960401_mod.htm"
  readed = get_text(file_name) #Getting the text string 
  raw = remove_tags(readed) #Removing the tags
  tokens = tokenize(raw) #Tokenize process 
  print("There are", len(tokens),"tokens.")
  cleaned_tokens = get_clean_tokens(convert_lower_case(tokens))  #Get only words
  print("There are", len(cleaned_tokens)," cleaned tokens.")
  cleaned_tokens = remove_stopwords(cleaned_tokens) #Removal of stopwords
  print("There are", len(cleaned_tokens)," after removing stopwords.")
  print(cleaned_tokens[:200]) 
  #text = nltk.Text(cleaned_tokens) # Convert to type text
  
  
