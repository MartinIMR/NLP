import nltk
import numpy as np

def load_data(file_name):
  from pickle import load 
  input = open(file_name,"rb")
  data = load(input)
  input.close()
  return data

def obtain_vocabulary(articles):
  text = " ".join(articles)
  tokens = nltk.word_tokenize(text)
  vocabulary = sorted(set(tokens))
  return vocabulary

def obtain_frequencies(articles):
  text = " ".join(articles)
  tokens = nltk.word_tokenize(text)
  frequency = dict(nltk.FreqDist(tokens))
  return frequency

if __name__=='__main__':
  articles = load_data("lemmatized_articles.pkl")
  vocabulary = obtain_vocabulary(articles) #Vocabulary
  fd = obtain_frequencies(articles) #All text frequencies
  """ Create the background distribution vector """
  background_vector = []
  for word in vocabulary:
    background_vector.append(fd[word])
  background_vector = np.array(background_vector) 
  total_count = np.sum(background_vector)
  background_vector = background_vector/total_count

"""
from nltk.corpus import stopwords
stopwords = stopwords.words('spanish')
words = [word for word in words if word not in stopwords]

fd = nltk.FreqDist(words)
vocabulary = sorted(list(fd.keys()))
fd = dict(fd)
print('\n The vocabulary has %d words. ' %len(vocabulary))
#Calculate background frequency for all text
background_word_counts = []
for voc in vocabulary:
    background_word_counts.append(fd[voc])
background_word_counts = np.array(background_word_counts)
s = np.sum(background_word_counts)
background_word_probs = background_word_counts / s


#initialize uniform probabilities for the one topic model

num = 1 / len(vocabulary)
topic_word_probs = np.full(shape = len(vocabulary), fill_value = num)
print('The initial value of uniform probability for topical terms is %f.' %num)

#initialize (uniform) probabilities for the topics
prob_background = 0.5
prob_topic = 0.5

def e_step(prob_background, prob_topic,
           background_word_probs, topic_word_probs):
    #compute probability of the latent cariable z = 0
    numerator = prob_topic * topic_word_probs
    denominator = numerator + prob_background * background_word_probs
    z_0_probs = np.divide(numerator, denominator)
    return z_0_probs

z_0_probs = e_step(prob_background, prob_topic, 
                   background_word_probs, topic_word_probs)

#find  word counts in a document
f = open('article_2_e960401_lemmatized.txt', encoding = 'utf-8')
text = f.read()
f.close()

words = nltk.Text(nltk.word_tokenize(text))

counts = []
for voc in vocabulary:
    count = words.count(voc)
    counts.append(count)
counts = np.array(counts)

def m_step(counts, z_0_probs):
    numerator = np.multiply(counts,z_0_probs)
    denominator = np.sum(numerator) #denominator is a scalar
    topic_word_probs = numerator / denominator
    return topic_word_probs

def compute_document_likelihood(background_word_probs,
                                topic_word_probs, counts,
                                prob_background, prob_topic,
                                num_iterations = 50,
                                print_likelihood = False):
    
    arguments_for_logarithm = background_word_probs * prob_background + \
                                topic_word_probs * prob_topic
                                
    logarithms = np.log(arguments_for_logarithm)
    for i in range (len(logarithms)):
        product = logarithms[i] * counts[i]
        logarithms[i] = product
    document_likelihood = np.sum(logarithms)
    if print_likelihood == True:
        if num_iterations % 20 ==0:
            print('Document likelihood is %f' %document_likelihood)
"""

