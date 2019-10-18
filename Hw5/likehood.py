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

def E_step(prob_back, prob_top,back_vector,topic_vector):
    """ Compute probability for latent variable z = 0 
        in this case for the topic """
    numerator = topic_vector * prob_top
    denominator = numerator + back_vector * prob_back
    z0_vector = np.divide(numerator, denominator) # z0 vector of probability
    return z0_vector

def M_step(counts, z0_probs):
    numerator = np.multiply(counts,z0_probs) #Each word count by z = 0
    denominator = np.sum(numerator) #Sum all values of the numerator (Scalar)
    topic_probs = numerator / denominator # For each element divide 
    return topic_probs

def compute_likelihood(article, vocabulary, back_vector, topic_vector,
                       back_prob,topic_prob, iterations = 50, print_iterations = False):

    words = nltk.Text(nltk.word_tokenize(article))
    counts = []
    """ Count frequency of each word in article """
    for word in vocabulary:
     counts.append(words.count(word))
    counts = np.array(counts) 
    z0 = 0
    for i in range(iterations):
      z0 = E_step(back_prob, topic_prob,back_vector,topic_vector)
      topic_vector = M_step(counts,z0) 
      logarithms = np.log(back_vector * back_prob + \
                                topic_vector * topic_prob)
      product = np.multiply(logarithms, counts)
      document_likelihood = np.sum(logarithms)
      if print_iterations == True:
         print("Document likelihood is:")
         print(document_likelihood)
    return topic_vector

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
  """ Create the topic distribution vector """
  dimension = len(vocabulary)
  topic_vector = np.full(shape = dimension, fill_value = (1/dimension))
  back_prob = 0.5 #Probability of background
  topic_prob = 0.5 #Probabilty of topic
  i = 0
  topics = []
  for article in articles:
    print("For article ",i,":")
    topics.append(compute_likelihood(article, vocabulary, background_vector,
    topic_vector,back_prob,topic_prob,20,True))
  for i in range(len(articles)): 
    print("Article ",i," has topics:")
    print(articles[i][:10])
