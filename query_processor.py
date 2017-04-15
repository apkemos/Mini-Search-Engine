# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 17:33:35 2017

@author: zero
"""


import nltk
from text_processor import get_wordnet_pos
from text_processor import is_stop_word
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet      
from collections import defaultdict        
        
        
def process_query(query, inv_ind):
    """This function gets as input a string which represents the user's 
    query it tokenizes it and lemmatizes it similar to the way the
    inverted index was made"""
    
    tokens = nltk.word_tokenize(query)
    tokens = [token.lower() for token in tokens]
    tagged = nltk.pos_tag(tokens)
    wnl = WordNetLemmatizer()

    new_query = []
    
    for token, tag in tagged:
        if is_stop_word(tag) == True:
            continue
        new_query.append( str(wnl.lemmatize(token, get_wordnet_pos(tag)) ) ) #conver to string fron utf-8        #,   
    
    return retrieve_documents(new_query, inv_ind)
    

 
 
def retrieve_documents(new_query, inv_ind):   
    """This functions gets a lemmatizes query and an inverted index
    as arguments and returns the """
            
    documents = []
    #Get concatenated post list with duplicates of every token matched
    post_list_conc = []
    for token in new_query:
        if token in inv_ind:
            post_list_conc.extend(inv_ind[token])
    
    #Create a defaultdictionary that maps lemmas to weights
    #this way we can add the weights of multiple same doc_ids
    post_dict = defaultdict(int)
    for doc_id , weight in post_list_conc:
        post_dict[doc_id] += weight
     
    #convert to list of tuple (lemma, weight)
    post_dict = post_dict.items()              
    
    #sort based on weight
    sorted_weights = sorted(post_dict, key=lambda tup: tup[1], reverse = True)  
       #     print sorted_weights
       
    documents = [ doc[0] for doc in sorted_weights]
        
    
    return documents