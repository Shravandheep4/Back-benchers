#Basic dependencies
import codecs, glob, os, re, logging, pprint, multiprocessing
import numpy as np

#External libraries
import nltk                           #For generating corpus
import gensim.models.word2vec as w2v  #To generate vectors from word embeddings
import sklearn.manifold               #To reduce the dimensions 
import matplotlib.pyplot as plt       #For visual representation
import pandas as pd                   #To manipulate data
import seaborn as sns                 #To Plot graphs


##Process Data and clean 
nltk.download("punkt")  #pretrained tokenizer
nltk.download("stopwords") #words that are insignificant for training the model

#get the book names, matching txt files
#book_filenames = sorted(glob.glob("*.txt"))
#print(book_filenames)

corpus_raw = u""

#Read characters & words from text files and store it in the raw corpus
subjectname = str(input("Source name: "))
textfile = sorted(glob.glob("Data\\"+subjectname+".txt"))
print(textfile)


for text in textfile:
    print(f"Reading '{text}'")
    with codecs.open(text, "r", "utf-8") as file:
        corpus_raw += file.read()

print(f"Corpus is now {len(corpus_raw)} characters long\n")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
raw_sentences = tokenizer.tokenize(corpus_raw)

cachedStopWords =  nltk.corpus.stopwords.words("english")
#Convert into a list of words
#remove unnecessary symbols 
#Split the sentences into words
def sentence_to_wordlist(raw):
    clean = re.sub("[^a-zA-Z]", " ", raw)
    words = clean.split()
    stem = nltk.PorterStemmer()
    
    for stemming in words:
        stemming = stem.stem(stemming)
        if stemming  in cachedStopWords:
            stemming = ''

    return words


sentences = []

for raw_sentence in raw_sentences:
    if len(raw_sentence) > 0:
        sentences.append(sentence_to_wordlist(raw_sentence))

token_count = sum([len(sentence) for sentence in sentences])
print("The book corpus contains {0:,} tokens".format(token_count))


# 3 main properties that vectors help us with
# DISTANCE, SIMILARITY, RANKING
num_features = 300
min_word_count = 3
num_workers = multiprocessing.cpu_count()
context_size = 7
downsampling = 1e-3
seed = 1

learningmodel = w2v.Word2Vec(
    sg = 1,
    seed = seed,
    workers = num_workers,
    size = num_features,
    min_count = min_word_count,
    window = context_size,
    sample = downsampling
    )
learningmodel.build_vocab(sentences)

print("Vocabulary length: ", len(learningmodel.wv.vocab))

#Training our model
learningmodel.train(sentences, total_examples = token_count, epochs= 50)

filename = str(input("Subject : "))

if not os.path.exists("Training Data\\" + filename):
    location = "Training Data\\" + filename
    os.makedirs(location)

learningmodel.save(os.path.join(location, filename+"_learning_model"))






