# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 20:16:31 2017

@author: zero
"""
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
from collections import defaultdict

  
def tokenize_text( article_file, tagged_file ): 
    """This function tokenizes the text contained in file
    article_file and outputs it in tagged_file in format
    (token) (tag)\n"""      
    
    with open(article_file, 'r') as f:
            article = f.read()
            tokens = nltk.word_tokenize(article)
            tokens = [token.lower() for token in tokens]
            tagged = nltk.pos_tag(tokens)
    
    
    with open(tagged_file, 'w+') as f:
                f.write( '\n'.join('%s %s' %tag_tuple for tag_tuple in tagged) )
                #
    f.closed


def remove_stopwords( tagged_file, tagged_sw_file ):
    """This function removes the lines in a file with format
    (token) (tag)\n where the tag is contained in a list of stop_words
    and saves the result in the file tagged_sw_file with the same format"""
    
#    stop_words = [] #mot necessary, for test purposes to see which words are being removed
    with open( tagged_file, 'r') as tf, open (tagged_sw_file, 'w') as tswf:
        for line in tf:
            tok_n_tag = line.rstrip('\n').split(" ")
            token = tok_n_tag[0]
            tag = tok_n_tag[1]
            if is_stop_word(tag) == True :
#                stop_words.append(token)
                continue
            else:
                tswf.write( token + ' ' + tag + '\n' )
#    return stop_words
 
    
def is_stop_word(tag):
    """This function takes a tag as input and returns True 
    if it is contained ina  stop words list"""
    
    stop_words_tags = [ 'CD', 'CC' , 'DT' ,  'EX', 'IN', 'LS', 'MD',
                    'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO',
                    'UH', 'WDT', 'WP', 'WP$', 'WRB', '.', ',' ,'(', ')', ':',
                      '>' , '<' , '\"\"', '\'', '\'\'']
    if tag in stop_words_tags:
        return True
    else: 
        return False
 
    

def lemmmatize_text( tagged_sw_file, lem_file ):
    """This function takes a file in format (token) (tag)\n and
    gets the lemma of the token using wordnet and the tag.
    It saves all the resulted lemma in lem_file 
    seperated by space to get the lemmatized document """   
    wnl = WordNetLemmatizer()
     
    with open ( tagged_sw_file, 'r') as tswf, open( lem_file, 'w') as lf:
        for line in tswf: 
          tok_n_tag = line.rstrip('\n').split(" ")
          token = tok_n_tag[0]
          tag = tok_n_tag[1]

          tag_lem = str( wnl.lemmatize(token, get_wordnet_pos(tag)))          
          lf.write(tag_lem + ' ')
      
         




def get_wordnet_pos(treebank_tag):
    """This function gets as input a POS tag from nltk tokenizer
    and returns the wordnet equivalent to use in the lemmatization"""
    
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN