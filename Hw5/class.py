
from nltk.corpus import stopwords
stopwords = st.words()

fd = nltk.FreqDist(words)
vocabulary = sorted(list(fd.))
fd = dictionary(fd)

backgroud_words = []

for voc in vocabu:
  backwo_Words

def e_step(prob_background, prob_topic,
           background_words_probs, topic_words_probs):
  numerator = prob_topic * topic_words_probs
  denominator = numerator + prob_background * background_word_probs
  z_0_probs = np.divide(numerator,denominator)

def m_step(counts,z_0_probs):
  numerator = np.multiply(counts,z_0_probs)
  denominator = np.sum(numerator)
  topic_word_probs = numerator / denominator 
  return topic_word_probs

def comun
