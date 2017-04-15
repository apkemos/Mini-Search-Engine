# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 18:41:17 2017

@author: zero
"""
from __future__ import division

import time

import os
import sys
import math
from os import listdir
from os.path import isfile, join
from collections import Counter, defaultdict
import text_processor
import query_processor
import random
#class InvertedBuilder():
class InvertedIndex( object ):

    
    
    def __init__(self):
        self.inv_ind = {}
        self.IDF_ind = {}
        self.url_dct = defaultdict(str)
        self.file_list = []
        self.N = 0
        
    def get_all_files(self, path_to_coll):
        """Get in a list all txt file names in a directory """
        
        article_files = [f for f in listdir(path_to_coll) if f.endswith(".txt")]
        if 'mapping.txt' in article_files: #get only article files
            article_files.remove('mapping.txt')
            
        self.get_mapping(path_to_coll)    
        self.file_list = article_files
        self.N = len(self.file_list)

    def get_mapping(self, path_to_coll):
        """Creates id to url dictionary from mapping file"""
        with open( path_to_coll + 'mapping.txt' , 'r') as f:
            for line in f:
                print line
                id , url = line.rstrip('\n').split(" ")
                self.url_dct[id] = url
    
    
    def build_IDF_index(self, file_name):
        """This function updates the IDF value of all terms.5
        It takes as input the lemmatized file, finds all unique lemmas
        in the text, and updates the IDF dictionary"""
        
        with open( file_name, 'r' ) as f:
            text = f.read()
            terms = set(text.split())
            for lemma in terms:
                self.IDF_ind[lemma] = self.IDF_ind.get(lemma, 0) + 1 # dct.get(key[, default]) returns dct[key] if it exists, and default if not.
             
            
            
    def build_inverted_index(self, file_name):
        """This function updates the inverted index. It gets as input
        the lemmatized file to be inserted in index finds the frequency of
        each lemma, and inserts a tuple (doc_ID, TF-IDF weight)
        in the lemma's post list"""
        
        doc_id = os.path.splitext(os.path.basename(file_name))[0].replace('-lem', "") #convert name of file to id
        with open( file_name, 'r' ) as f:
            text = f.read()
            terms = Counter(text.split()).most_common()
            for (lemma, freq) in terms:
                idf = self.idf_func(self.N, self.IDF_ind[lemma])
                if lemma in self.inv_ind:
                    self.inv_ind[lemma].append((doc_id, freq*idf))
                else:
                    self.inv_ind[lemma] = [(doc_id, freq*idf)]
                    
            
    
    def idf_func(self, N, N_t):
        """Calculates IDF based on DF N_t of lemma"""
        if N_t != 0:
          return math.log10(N/N_t)
        else:
    		 return 0
    
    def save_index(self, file_name ):
       """Saves the index to specified XML format"""
       
       with open(file_name , 'w+') as f:
            f.write("<inverted_index>\n")
            for lemma, post_list in self.inv_ind.iteritems():
                f.write("<lemma_name=" + lemma +">\n" )
                for id_n_weight in post_list:
                    f.write("<document id=" + str(id_n_weight[0]) +"> " + "<weight=" + str(id_n_weight[1]) + ">\n")
                f.write("</lemma>\n")
            f.write("</>\n</>")
            
    def load_index (self,  file_name):
        """This function gets as input the XML formatted file that the index
          has been saved and upploads it in self.inv_ind"""
          
        import re

        self.inv_ind = defaultdict(list) #init key_vals as list
        docs = set() #Used to count the number of different documents
        with open(file_name , 'r') as f:
               f.readline() #read <inverted_index>
               curr_lemma = ""
               for line in f:
                   if line == '</lemma>\n':                     
                       continue
                   if line == '</>\n': #if end of file break
                       break
                   elif line[1] == 'l': #if new lemma
                       match = re.findall(r'\=(.+?)\>',line) #finds all strings between = and >
                       curr_lemma = match[0]
                       continue
                   else: #append every next (doc_id, weight) in current lemma post list
                       match = re.findall(r'\=(.+?)\>', line) #get doc id and weight as list
                       match[1] = float(match[1])
                       docs.add(match[0]) #add document if not already there
                       id_n_weight = tuple(match) #make it a tupple
                       self.inv_ind[curr_lemma].append(id_n_weight) #all keys have a default already
                       
        self.N = len(docs)            
                   
                   
          
               
               
         
if __name__ == '__main__':

    
    cwd = os.getcwd()
    u_input = '0'
    index = InvertedIndex()
    while True:
        print "*"*20
        print 'SELECT ONE OF THE OPTIONS BELLOW'
        print "*"*20
        print '1) Build index'
        print '2) Save index'
        print '3) Load index'
        print '4) Search'
        print '5) Exit'
        print 't) for testing'
        u_input = raw_input()
        if u_input == '5':
            sys.exit()
        elif u_input == '1':
            coll_path = raw_input('Please enter collection path\n')
            if coll_path == '':
                coll_path = cwd + '\\MyCrawler\\MyCrawler\\spiders\\collection\\'
            save_path = cwd + "\\file_base\\" 
            lidir = listdir(coll_path)    
            lem_file = [] #list of name of files, used later in building index
            
            index.get_all_files(coll_path)
         #   print (index.file_list)
            #Process text. Builds 2 files tagged-no stop words, lemmatized
            for i in xrange(0, index.N):
                article_file = coll_path + index.file_list[i]
                article_name = os.path.splitext(os.path.basename(article_file))[0] #remove .txt
                
                tagged_file = save_path + '\\' + article_name + '-tagged.txt'
                tagged_sw_file = save_path + '\\'+ article_name  + '-tagged-sw.txt'    
                lem_file.append(save_path +'\\' + article_name + '-lem.txt')
                
                text_processor.tokenize_text(article_file, tagged_file)
                stop_words =  text_processor.remove_stopwords( tagged_file, tagged_sw_file  )
                os.remove(tagged_file)
                text_processor.lemmmatize_text ( tagged_sw_file, lem_file[i] )
                
                index.build_IDF_index(lem_file[i])
            
            for i in xrange(0, index.N):
                index.build_inverted_index(lem_file[i])
             
            #for debug
            IDF_ind = index.IDF_ind
            inv_ind = index.inv_ind
            URL_TEST =  index.url_dct
            file_list = index.file_list
      
        elif u_input == '2':
            save_name = raw_input('Please enter path and file name to save the index\n')
            if save_name == '':
                save_name = 'save_index.txt' #to be deleted
            index.save_index(save_name)
            print 'Index saved'
        elif u_input == '3':
            load_name = raw_input('Please enter path and file name of index to load\n')
            map_dir = raw_input('Please enter the directory of mapping to url \n') #in case mapping is in another file
            if ( load_name == '' and map_dir == '' ):  
                load_name = 'save_index.txt' # to be deleted
                path = cwd + '\\' + load_name
                map_dir =  cwd + '\\MyCrawler\\MyCrawler\\spiders\\collection\\' 
            if ( os.path.exists(path) == True ):
                index.load_index(path)
                index.get_mapping(map_dir)
                inv_ind = index.inv_ind
                N = index.N
            else:
                print "There is no file with this name in this path"
            print 'Index loaded'
        elif u_input == '4':
            query =  raw_input('Please enter query and file name to save the index\n')
            retrieved = query_processor.process_query(query, index.inv_ind)
            print retrieved
            urls = [index.url_dct[doc] for doc in retrieved]
            if len(urls) == 0:
                print 'No documents found matching your search'
            else:
                for url in urls:
                    print url
        
        elif u_input == 't':
          examples = ['trump', 'minister', 'court' , 'month' , 'year' , 'write' , 'new' ,
                     'global' , 'china', 'europe', 'public', 'people', 'waste', 'vehicle',
                     'policy', 'do', 'hold' , 'executive', 'economic', 'cost', 'scandal',
                     'car', 'company' ]
          all_queries= []
          for i in xrange(0,20):
              one_lemma = random.sample(examples,1)[0]
              all_queries.append( one_lemma)
              
          
          for i in xrange(0,20):
             two_samples = random.sample(examples,2)
             two_lemmas = " ".join(two_samples)
             all_queries.append( two_lemmas)
          
          for i in xrange(0,30):
             three_samples = random.sample(examples,3)
             three_lemmas = " ".join(three_samples)
             all_queries.append( three_lemmas)  
             
          for i in xrange(0,30):
             four_samples = random.sample(examples,4)
             four_lemmas = " ".join(four_samples)
             all_queries.append( four_lemmas)    
        
          print all_queries
          start_time = time.time()
          for query in all_queries:
              print query
              retrieved = query_processor.process_query(query, index.inv_ind)
              print retrieved
              urls = [index.url_dct[doc] for doc in retrieved]
              if len(urls) == 0:
                 print 'No documents found matching your search'
              else:
                for url in urls:
                    print url
          end_time = time.time() - start_time
          avg_time = end_time/100.0 
          print("--- %s seconds ---"  % avg_time) 
  
        
        
        

 
    
    
    
    
    
    
    
    
    
    
    
    
    