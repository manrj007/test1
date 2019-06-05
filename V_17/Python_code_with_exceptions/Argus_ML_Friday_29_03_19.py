# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:45:58 2019

@author: Mohammadsaif.UR
"""



import os
import re
import gensim
from gensim.models import KeyedVectors
import string
import nltk
import csv
import collections
import spacy
import sklearn
import pandas
import numpy
from spacy import displacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from collections import OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
#from nltk.tokenize.treebank import TreebankWordDetokenizer
#treebank = TreebankWordDetokenizer()
os.chdir('C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Python_code_with_exceptions\\')
#filename = 'GoogleNews-vectors-negative300.bin'
#model = KeyedVectors.load_word2vec_format(filename,binary=True)
nlp = spacy.load('en')

#text_loaded = ''
#search_sentence = ''

trainingPath = 'C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Middleware\\training\\'
testingPath = 'C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Middleware\\testing\\'
#text_loaded = open('C:\\Users\\Administrator\\Desktop\\Argus\\updatedpythonintegratedcode\\OCR_Output_Document.txt', encoding='utf-8-sig').read()
#search_sentence = open('C:\\Users\\Administrator\\Desktop\\Argus\\updatedpythonintegratedcode\\Training_Field_Document.txt', encoding='utf-8-sig').read()
Flag = False
#doc1 = 'file-1553096591715.txt'
#doc2 = 'file-1553096592897.txt'
###################### Start of get_documents function ########################
def get_documents(doc1, doc2 ):
    
#    global text_loaded 
    try:
        tempTraining = trainingPath+ doc1
        tempTest = testingPath + doc2   
        print(tempTraining)
        print(tempTest)

#        try:
        text_loaded = open(tempTest, 'r').read()
        text_loaded = text_loaded.replace("\n", "")
        
        search_sentence = open(tempTraining, encoding = 'utf-8').read()
        
#        except:
#        text_loaded = open(tempTest, 'rb').read()
#        search_sentence =  open(tempTraining,'rb').read()

        text_loaded = text_loaded.replace("\n", "").strip()
        text_loaded = text_loaded.replace("\\", "")
        #text_loaded = text_loaded.lower()
        text_loaded = text_loaded.strip()
#        print('textloaded    :   ', text_loaded)
        print('search_sentence    :  ', search_sentence)
        tokens = nlp(text_loaded)
        sent_spacy = []
        for sent in tokens.sents:
            sent = sent.string.strip()
            sent_spacy.append(sent)
        len(sent_spacy)   
        sentences = sent_spacy
#        tokens_sentences = [word_tokenize(t) for t in sentences]
        
        search_sentence_list = search_sentence.splitlines()
        
    ###############################################################################    
        
        
        # Lenient Mode Output
        if (pattern_matching_verb_pos(sentences, search_sentence_list)[0] == [] and 
                pattern_matching_verb_entity(sentences, search_sentence_list)[0] == [] and 
                    bqm_sent(sentences, search_sentence_list) == [] and 
                        vsm_sent(sentences, search_sentence_list)[0] == []):
            Final_Sentences_Lenient = []
        else:
            Final_Sentences_Lenient = [pattern_matching_verb_pos(sentences, search_sentence_list)[0] + 
                                       pattern_matching_verb_entity(sentences, search_sentence_list)[0] +
                                       vsm_sent(sentences, search_sentence_list)[0]]
            
        Uniq_Final_Sentences_Lenient = []
        if Final_Sentences_Lenient == []:
            Uniq_Final_Sentences_Lenient == []
        else:
            Uniq_Final_Sentences_Lenient = list(set(Final_Sentences_Lenient[0]))
        
        # writing Uniq_Final_Sentences_Lenient locally to a text file
        with open('Uniq_Final_Sentences_Lenient.txt', 'w') as f:
            for s in Uniq_Final_Sentences_Lenient:
                f.write(s + '\n')  
                        
        
        
        # Moderate Mode Output 
        if (pattern_matching_verb_pos(sentences, search_sentence_list)[1] == [] and 
                pattern_matching_verb_entity(sentences, search_sentence_list)[1] == [] and 
                    bqm_sent(sentences, search_sentence_list) == [] and 
                        vsm_sent(sentences, search_sentence_list)[1] == []):
            Final_Sentences_Moderate = []
        else:
            Final_Sentences_Moderate = [pattern_matching_verb_pos(sentences, search_sentence_list)[1] + 
                                        pattern_matching_verb_entity(sentences, search_sentence_list)[1] +
                                        vsm_sent(sentences, search_sentence_list)[1]]
            
        Uniq_Final_Sentences_Moderate = []
        if Final_Sentences_Moderate == []:
            Uniq_Final_Sentences_Moderate == []
        else:
            Uniq_Final_Sentences_Moderate = list(set(Final_Sentences_Moderate[0]))
        
        # writing Uniq_Final_Sentences_Moderate locally to a text file
        with open('Uniq_Final_Sentences_Moderate.txt', 'w') as f:
            for s in Uniq_Final_Sentences_Moderate:
                f.write(s + '\n')
    
    
    
        # Strict Mode Output
        if (pattern_matching_verb_pos(sentences, search_sentence_list)[2] == [] and 
                pattern_matching_verb_entity(sentences, search_sentence_list)[2] == [] and 
                    bqm_sent(sentences, search_sentence_list) == [] and 
                        vsm_sent(sentences, search_sentence_list)[2] == []):
            Final_Sentences_Strict = []
        else:    
            Final_Sentences_Strict = [pattern_matching_verb_pos(sentences, search_sentence_list)[2] + 
                                      pattern_matching_verb_entity(sentences, search_sentence_list)[2] + 
                                      vsm_sent(sentences, search_sentence_list)[2]]
        
        Uniq_Final_Sentences_Strict = []
        if Final_Sentences_Strict == []:
            Uniq_Final_Sentences_Strict == []
        else:
            Uniq_Final_Sentences_Strict = list(set(Final_Sentences_Strict[0]))
        
        # writing Uniq_Final_Sentences_Moderate locally to a text file
        with open('Uniq_Final_Sentences_Strict.txt', 'w') as f:
            for s in Uniq_Final_Sentences_Strict:
                f.write(s + '\n')
        
        
        return True
    
    except Exception as e:
        return False



##############################################################################

def words_to_be_searched(self):
    words_to_be_searched_stop_rem = []
    words_to_be_searched = []
    pos = []
    user_input = self
    doc_input = nlp(user_input)
    for word in doc_input:
        y = [word.text, word.tag_]
        pos.append(y)
    #    print(x)
    #    print(word.text, word.tag_, spacy.explain(word.tag_))
        if word.tag_ == 'VBZ' or word.tag_ == 'VBG' or word.tag_ == 'VBP' or word.tag_ == 'VBD' or word.tag_ ==  'VBN' or  word.tag_ ==  'VBZ' or word.tag_ == 'VB':
            words_to_be_searched.append(str(word))
    #print(pos)
    for j in words_to_be_searched:
        if j not in stop_words:
            if j.isalnum():
                words_to_be_searched_stop_rem.append(j)
    return(words_to_be_searched_stop_rem)
 
    
    
    
    
####################### Start of Parts Of Speech Tagging ######################
def pos(self):
    pos = []
    user_input = self
    doc_input = nlp(user_input)
    for word in doc_input:
        y = [word.text, word.tag_]
        pos.append(y)
    return(pos)
    
    
def pattern_bqm(search_sentence_list, bqm_output):
    pos_list = []
    for i in range(len(search_sentence_list)):
        for j in range(len(bqm_output)):
            print("Input" + " " + str(i+1) + ":")
            print(search_sentence_list[i])
            print(" ")
            ps = pos(bqm_output[j])
            words_ss = words_to_be_searched(search_sentence_list[i])
            words_bqm = words_to_be_searched(bqm_output[j])
            words_to_be_searched_stop_rem = [i for i in  words_ss if i in words_bqm]
            for k in range(len(words_to_be_searched_stop_rem)):
                for l in range(len(ps)-1):
                    if words_to_be_searched_stop_rem[k] == ps[l][0]:
                        if l == 0:
                            pattern = [ps[l][1], ps[l+1][1], ps[l+2][1]]
                            a = [bqm_output[j], pattern]
                            pos_list.append(a)
                        elif l == 1:
                            pattern = [ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
                            a = [bqm_output[j], pattern]
                            pos_list.append(a)
                            
                        elif l == len(ps)-2:
                            pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1]]
                            a = [bqm_output[j], pattern]
                            pos_list.append(a)
                            
                        elif l == len(ps)-1:
                            pattern = [ps[l-2][1], pos[l-1][1], ps[l][1]]
                            a = [bqm_output[j], pattern]
                            pos_list.append(a)
                            
                        else:
                            pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
                            a = [bqm_output[j], pattern]
                            pos_list.append(a)
#            for k in range(len(words_to_be_searched_stop_rem)):
#                for l in range(len(ps)):
#                    if l == 0:
#                        if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                            pattern = [ps[l][1], ps[l+1][1], ps[l+2][1]]
#                            a = [bqm_output[j], pattern]
#                            pos_list.append(a)
#                    elif l == 1:
#                        if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                            pattern = [ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
#                            a = [bqm_output[j], pattern]
#                            pos_list.append(a)
#                    elif l == len(ps)-2:
#                        if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                            pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1]]
#                            a = [bqm_output[j], pattern]
#                            pos_list.append(a)
#                    elif l == len(ps)-1:
#                        if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                            pattern = [ps[l-2][1], pos[l-1][1], ps[l][1]]
#                            a = [bqm_output[j], pattern]
#                            pos_list.append(a)
#                    else:
#                        if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                            pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
#                            a = [bqm_output[j], pattern]
#                            pos_list.append(a)         
    return(pos_list)
 
    
def pattern_ss(self):
    pos_list = []
    for i in range(len(self)):
        print("Input" + " " + str(i+1) + ":")
        print(self[i])
        print(" ")
        ps = pos(self[i])
        words_to_be_searched_stop_rem = words_to_be_searched(self[i])
        for k in range(len(words_to_be_searched_stop_rem)):
            for l in range(len(ps)-1):
                if words_to_be_searched_stop_rem[k] == ps[l][0]:
                        if l == 0:
                            pattern = [ps[l][1], ps[l+1][1], ps[l+2][1]]
                            a = [self[i], pattern]
                            pos_list.append(a)
                        elif l == 1:
                            pattern = [ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
                            a = [self[i], pattern]
                            pos_list.append(a)
                            
                        elif l == len(ps)-2:
                            pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1]]
                            a = [bqm_output[j], pattern]
                            pos_list.append(a)
                            
                        elif l == len(ps)-1:
                            pattern = [ps[l-2][1], pos[l-1][1], ps[l][1]]
                            a = [self[i], pattern]
                            pos_list.append(a)
                            
                        else:
                            pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
                            a = [self[i], pattern]
                            pos_list.append(a)
                            
                            
#        for k in range(len(words_to_be_searched_stop_rem)):
#            for l in range(len(ps)):                
#                if l == 0:
#                    if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                        pattern = [ps[l][1], ps[l+1][1], ps[l+2][1]]
#                        a = [self[i], pattern]
#                        pos_list.append(a)
#                elif l == 1:
#                    if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                        pattern = [ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
#                        a = [self[i], pattern]
#                        pos_list.append(a)
#                elif l == len(ps)-2:
#                    if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                        pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1]]
#                        a = [self[i], pattern]
#                        pos_list.append(a)
#                elif l == len(ps)-1:
#                    if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                        pattern = [ps[l-2][1], pos[l-1][1], ps[l][1]]
#                        a = [self[i], pattern]
#                        pos_list.append(a)
#                else:
#                    if words_to_be_searched_stop_rem[k] == ps[l][0]:
#                        pattern = [ps[l-2][1], ps[l-1][1], ps[l][1], ps[l+1][1], ps[l+2][1]]
#                        a = [self[i], pattern]
#                        pos_list.append(a)        
    return(pos_list)
    
def pattern_matching_verb_pos(sentences, search_sentence_list):
#def pattern_matching_verb_pos(tokens_sentences, search_sentence_list):
    bqm_output = bqm_sent(sentences, search_sentence_list)
#    bqm_output = bqm_sent(tokens_sentences, search_sentence_list)
    
    # Strict Approach
    pos_list_ss = pattern_ss(search_sentence_list)
    pos_list_bqm = pattern_bqm(search_sentence_list, bqm_output)
    
    final_output_list_strict = []
    for i in range(len(pos_list_ss)):
        for j in range(len(pos_list_bqm)):
            if pos_list_ss[i][1] == pos_list_bqm[j][1]:
                final_output_list_strict.append(pos_list_bqm[j][0])
    final_output_list_strict = list(set(final_output_list_strict))
    
    
    BQM = [item[0] for item in pos_list_bqm]
    BQM_Strict = final_output_list_strict
    
    df3 = pandas.DataFrame(columns = BQM)
    row1 = [1 for x in df3]
    df3 = df3.append(pandas.Series(row1, index = BQM), ignore_index=True)
    row2 = []
    for val1 in BQM:
        if val1 in BQM_Strict:
            row2.append(1)
        else:
            row2.append(0)
    df3 = df3.append(pandas.Series(row2, index = BQM), ignore_index=True)
    cols = []
    for i in range(len(BQM)):
        c = 'Sent'+ str(i+1)
        cols.append(c)
    df3.columns = cols
    df3.index = ['POS', 'POS_Strict']
    print(" ")
    print(df3)
    POS_Strict_Accuracy = df3.sum(axis=1)[1]/df3.sum(axis=1)[0]
    print("POS_Strict_Accuracy = ", POS_Strict_Accuracy)
    ###########################################################################
    
    # Moderate Approach
    pos_list_ss_moderate = []
    for i in range(len(pos_list_ss)):
        s = [pos_list_ss[i][0], pos_list_ss[i][1][1:4]]
        pos_list_ss_moderate.append(s)
        
    pos_list_bqm_moderate = []
    for i in range(len(pos_list_bqm)):
        s = [pos_list_bqm[i][0], pos_list_bqm[i][1][1:4]]
        pos_list_bqm_moderate.append(s)
        
    final_output_list_moderate = []
    for i in range(len(pos_list_ss_moderate)):
        for j in range(len(pos_list_bqm_moderate)):
            if pos_list_ss_moderate[i][1] == pos_list_bqm_moderate[j][1]:
                final_output_list_moderate.append(pos_list_bqm_moderate[j][0])
    final_output_list_moderate = list(set(final_output_list_moderate))
    
    BQM_Moderate = final_output_list_moderate
    
    df2 = pandas.DataFrame(columns = BQM)
    row1 = [1 for x in df2]
    df2 = df2.append(pandas.Series(row1, index = BQM), ignore_index=True)
    row2 = []
    for val1 in BQM:
        if val1 in BQM_Moderate:
            row2.append(1)
        else:
            row2.append(0)
    df2 = df2.append(pandas.Series(row2, index = BQM), ignore_index=True)
    cols = []
    for i in range(len(BQM)):
        c = 'Sent'+ str(i+1)
        cols.append(c)
    df2.columns = cols
    df2.index = ['POS', 'POS_Moderate']
    print(" ")
    print(df2)
    POS_Moderate_Accuracy = df2.sum(axis=1)[1]/df2.sum(axis=1)[0]
    print("POS_Moderate_Accuracy = ", POS_Moderate_Accuracy)
    ###########################################################################
    
    # Lenient Approach
    pos_list_ss_lenient = []
    for i in range(len(pos_list_ss)):
        s = [pos_list_ss[i][0], pos_list_ss[i][1][2]]
        pos_list_ss_lenient.append(s)
         
    pos_list_bqm_lenient = []
    for i in range(len(pos_list_bqm)):
        s = [pos_list_bqm[i][0], pos_list_bqm[i][1][2]]
        pos_list_bqm_lenient.append(s)
         
    final_output_list_lenient = []
    for i in range(len(pos_list_ss_lenient)):
        for j in range(len(pos_list_bqm_lenient)):
            if pos_list_ss_lenient[i][1] == pos_list_bqm_lenient[j][1]:
                final_output_list_lenient.append(pos_list_bqm_lenient[j][0])
    final_output_list_lenient = list(set(final_output_list_lenient))
    
    BQM_Lenient = final_output_list_lenient
         
    df1 = pandas.DataFrame(columns = BQM)
    row1 = [1 for x in df1]
    df1 = df1.append(pandas.Series(row1, index = BQM), ignore_index=True)
    row2 = []
    for val1 in BQM:
        if val1 in BQM_Lenient:
            row2.append(1)
        else:
            row2.append(0)
    df1 = df1.append(pandas.Series(row2, index = BQM), ignore_index=True)
    cols = []
    for i in range(len(BQM)):
        c = 'Sent'+ str(i+1)
        cols.append(c)
    df1.columns = cols
    df1.index = ['POS', 'POS_Lenient']
    print(" ")
    print(df1)
    POS_Lenient_Accuracy = df1.sum(axis=1)[1]/df1.sum(axis=1)[0]
    print("POS_Lenient_Accuracy = ", POS_Lenient_Accuracy)   
    print(" ")
    ###########################################################################
        
    return(final_output_list_lenient, final_output_list_moderate, final_output_list_strict)            
#################### End of Parts Of Speech Tagging ###########################
    
    
    
    
    
#################### Start of Named Entity Recognition ########################
def pattern_matching_verb_entity(sentences, search_sentence_list):
#def pattern_matching_verb_entity(tokens_sentences, search_sentence_list):
    print(" ")
    print("Pattern Matching Verb With Entity Output")
    print(" ")
    bqm_output = bqm_sent(sentences, search_sentence_list)
    final_sentences_lenient = []
    final_sentences_moderate = []
    final_sentences_strict = []
    for i in range(len(search_sentence_list)):
        print(" ")
        print("Input" + " " + str(i+1) + ":")
        print(search_sentence_list[i])
        print(" ")
        input_entities = []
        user_input = search_sentence_list[i]
        doc_input = nlp(user_input)
        print("Input Entities:    ")
        for j in doc_input.ents:
            if len(j.text) > 1:
                print(j.text, j.start_char, j.end_char, j.label_)
                input_entities.append(j.label_)
        #######################################################################
                
        # Lenient approach
        print(" ")
        print("Entities To Be searched: ", input_entities)
        print(" ")
        print("Entities From BQM Output")
        for sent in bqm_output:
            doc_test = nlp(str(sent))
            for k in doc_test.ents:
                print(k.text, k.start_char, k.end_char, k.label_)
                if k.label_ in input_entities:
                    final_sentences_lenient.append(sent)
        unique_final_sentences_lenient = list(sorted(set(final_sentences_lenient), key = final_sentences_lenient.index))            
        
        df1 = pandas.DataFrame(columns = bqm_output)
        row1 = [1 for x in bqm_output]
        df1 = df1.append(pandas.Series(row1, index = bqm_output), ignore_index=True)
        row2 = []
        for val1 in bqm_output:
            if val1 in final_sentences_lenient:
                row2.append(1)
            else:
                row2.append(0)
        df1 = df1.append(pandas.Series(row2, index = bqm_output), ignore_index=True)
        cols = []
        for i in range(len(bqm_output)):
            c = 'Sent'+ str(i+1)
            cols.append(c)
        df1.columns = cols
        df1.index = ['NER', 'NER_Lenient']
        print(" ")
        print(df1)
        NER_Lenientt_Accuracy = df1.sum(axis=1)[1]/df1.sum(axis=1)[0]
        print("NER_Lenientt_Accuracy = ", NER_Lenientt_Accuracy)
        #######################################################################
        
        # Moderate approach
        print(" ")
        print("Entities To Be searched: ", input_entities)
        print(" ")
        print("Entities From BQM Output")
        for sent in bqm_output:
            doc_test = nlp(str(sent))
            k_moderate = []
            for k in doc_test.ents:
                print(k.text, k.start_char, k.end_char, k.label_)
                k_moderate.append(k.label_)
            k_moderate_new = []
            if set(k_moderate).issubset(input_entities)  == False:
                common_entities = list(set(k_moderate).intersection(input_entities))
                k_moderate_new.append(common_entities) 
            k_moderate_new = [x for x in k_moderate_new if x != []]
            if not k_moderate_new:
                if set(k_moderate_new).issubset(input_entities):
                    final_sentences_moderate.append(sent)
        unique_final_sentences_moderate = list(sorted(set(final_sentences_moderate), key = final_sentences_moderate.index))
        
        df2 = pandas.DataFrame(columns = bqm_output)
        row1 = [1 for x in bqm_output]
        df2 = df2.append(pandas.Series(row1, index = bqm_output), ignore_index=True)
        row2 = []
        for val1 in bqm_output:
            if val1 in final_sentences_moderate:
                row2.append(1)
            else:
                row2.append(0)
        df2 = df2.append(pandas.Series(row2, index = bqm_output), ignore_index=True)
        cols = []
        for i in range(len(bqm_output)):
            c = 'Sent'+ str(i+1)
            cols.append(c)
        df2.columns = cols
        df2.index = ['NER', 'NER_Moderate']
        print(" ")
        print(df2)
        NER_Moderate_Accuracy = df2.sum(axis=1)[1]/df2.sum(axis=1)[0]
        print("NER_Moderate_Accuracy = ", NER_Moderate_Accuracy)
        #######################################################################
        
        # Strict approach
        print(" ")
        print("Entities To Be searched: ", input_entities)
        print(" ")
        print("Entities From BQM Output")
        for sent in bqm_output:
            doc_test = nlp(str(sent))
            k_strict = []
            for k in doc_test.ents:
                print(k.text, k.start_char, k.end_char, k.label_)
                k_strict.append(k.label_)
            if set(k_strict).issubset(input_entities):
                final_sentences_strict.append(sent)
        unique_final_sentences_strict = list(sorted(set(final_sentences_strict), key = final_sentences_strict.index))            
    
        df3 = pandas.DataFrame(columns = bqm_output)
        row1 = [1 for x in bqm_output]
        df3 = df3.append(pandas.Series(row1, index = bqm_output), ignore_index=True)
        row2 = []
        for val1 in bqm_output:
            if val1 in final_sentences_strict:
                row2.append(1)
            else:
                row2.append(0)
        df3 = df3.append(pandas.Series(row2, index = bqm_output), ignore_index=True)
        cols = []
        for i in range(len(bqm_output)):
            c = 'Sent'+ str(i+1)
            cols.append(c)
        df3.columns = cols
        df3.index = ['NER', 'NER_Strict']
        print(" ")
        print(df3)
        NER_Strict_Accuracy = df3.sum(axis=1)[1]/df3.sum(axis=1)[0]
        print("NER_Strict_Accuracy = ", NER_Strict_Accuracy)  
        print(" ")
        #######################################################################
        
    return(unique_final_sentences_lenient, unique_final_sentences_moderate, unique_final_sentences_strict)
###################### End of Named Entity Recognition ########################





############################# Start of Word2Vec ###############################
#def word2vec(tokens_sentences, search_sentence_list):
def word2vec(sentences, search_sentence_list):
    Word2Vec_Without_Cutoff = []
    Word2Vec_Lenient = []
    Word2Vec_Moderate = []
    Word2Vec_Strict = []
    print(" ")
    print("Word2Vec Output")
    print(" ")
    for i in range(len(search_sentence_list)):
        print("Input" + " " + str(i+1) + ":")
        print(search_sentence_list[i])
        print(" ")
        words_to_be_searched = []
        user_input = search_sentence_list[i]
        doc_input = nlp(user_input)
        for word in doc_input:
            print(word.text, word.tag_, spacy.explain(word.tag_))
            if word.tag_ == 'VBZ' or word.tag_ == 'VBG' or word.tag_ == 'VBP' or word.tag_ == 'VBD' or word.tag_ ==  'VBN' or  word.tag_ ==  'VBZ' or word.tag_ == 'VB' :
                words_to_be_searched.append(str(word))
        
        words_to_be_searched_stop_rem_all = []        
        words_to_be_searched_stop_rem_lenient = []
        words_to_be_searched_stop_rem_moderate = []
        words_to_be_searched_stop_rem_strict = []
        
        for j in words_to_be_searched:
            if j not in stop_words:
                if j.isalnum():
                    output_word2vec = model.most_similar(j, topn=10)
                    
                    # extracting without any cutoff
                    for k in range(len(output_word2vec)):
                        words_to_be_searched_stop_rem_all.append(output_word2vec[k][0])
                    
                    # extracting words for lenient approach
                    for k in range(len(output_word2vec)):
                        if output_word2vec[k][1] >= 0.3:
                            words_to_be_searched_stop_rem_lenient.append(output_word2vec[k][0])
                    
                    # extracting words for moderate approach
                    for k in range(len(output_word2vec)):
                        if output_word2vec[k][1] >= 0.5:
                            words_to_be_searched_stop_rem_moderate.append(output_word2vec[k][0])
                            
                    # extracting words for strict approach
                    for k in range(len(output_word2vec)):
                        if output_word2vec[k][1] >= 0.7:
                            words_to_be_searched_stop_rem_strict.append(output_word2vec[k][0])


                    words_to_be_searched_stop_rem_all.append(j)
                    words_to_be_searched_stop_rem_lenient.append(j)
                    words_to_be_searched_stop_rem_moderate.append(j)
                    words_to_be_searched_stop_rem_strict.append(j)
        #######################################################################


       # Without Cutoff Aproach
        print("  ")
        print("Words To Be Searched For Without Cutoff Mode: ", words_to_be_searched_stop_rem_all)
        print("   ")
        print("Output" + " " + str(i+1) + ":")
        for i in range(len(sentences)):
#        for sent in tokens_sentences:
            for word in words_to_be_searched_stop_rem_all:
                if word in word_tokenize(sentences[i]):
#                if word in sent:
                    print(sentences[i])
#                    print(treebank.detokenize(sent))
                    print(" ")
                    Word2Vec_Without_Cutoff.append(sentences[i])
#                    Word2Vec_Without_Cutoff.append(treebank.detokenize(sent))
        #######################################################################
        
        
        # Lenient Aproach
        print("  ")
        print("Words To Be Searched For Lenient Mode: ", words_to_be_searched_stop_rem_lenient)
        print("   ")
        print("Output" + " " + str(i+1) + ":")
        for i in range(len(sentences)):
#        for sent in tokens_sentences:
            for word in words_to_be_searched_stop_rem_lenient:
                if word in word_tokenize(sentences[i]):
#                if word in sent:
                    print(sentences[i])
#                    print(treebank.detokenize(sent))
                    print(" ")
                    Word2Vec_Lenient.append(sentences[i])
#                    Word2Vec_Lenient.append(treebank.detokenize(sent))
         
            
        df1 = pandas.DataFrame(columns = Word2Vec_Without_Cutoff)
        row1 = [1 for x in Word2Vec_Without_Cutoff]
        df1 = df1.append(pandas.Series(row1, index = Word2Vec_Without_Cutoff), ignore_index=True)
        row2 = []
        for val1 in Word2Vec_Without_Cutoff:
            if val1 in Word2Vec_Lenient:
                row2.append(1)
            else:
                row2.append(0)
        df1 = df1.append(pandas.Series(row2, index = Word2Vec_Without_Cutoff), ignore_index=True)
        cols = []
        for l in range(len(Word2Vec_Without_Cutoff)):
            c = 'Sent'+ str(l+1)
            cols.append(c)
        df1.columns = cols
        df1.index = ['Word2Vec_Without_Cutoff', 'Word2Vec_Lenient']
        print(" ")
        print(df1)
        Word2Vec_Lenient_Accuracy = df1.sum(axis=1)[1]/df1.sum(axis=1)[0]
        print("Word2Vec_Lenient_Accuracy = ", Word2Vec_Lenient_Accuracy)
        print(" ")
        #######################################################################
    
    
        # Moderate Aproach
        print("  ")
        print("Words To Be Searched For Moderate Mode: ", words_to_be_searched_stop_rem_moderate)
        print("   ")
        print("Output" + " " + str(i+1) + ":")
        for i in range(len(sentences)):
#        for sent in tokens_sentences:
            for word in words_to_be_searched_stop_rem_moderate:
                if word in word_tokenize(sentences[i]):
#                if word in sent:
                    print(sentences[i])
#                    print(treebank.detokenize(sent))
                    print(" ")
                    Word2Vec_Moderate.append(sentences[i])
#                    Word2Vec_Moderate.append(treebank.detokenize(sent))
                    
                    
        df2 = pandas.DataFrame(columns = Word2Vec_Without_Cutoff)
        row1 = [1 for x in Word2Vec_Without_Cutoff]
        df2 = df2.append(pandas.Series(row1, index = Word2Vec_Without_Cutoff), ignore_index=True)
        row2 = []
        for val1 in Word2Vec_Without_Cutoff:
            if val1 in Word2Vec_Moderate:
                row2.append(1)
            else:
                row2.append(0)
        df2 = df2.append(pandas.Series(row2, index = Word2Vec_Without_Cutoff), ignore_index=True)
        cols = []
        for m in range(len(Word2Vec_Without_Cutoff)):
            c = 'Sent'+ str(m+1)
            cols.append(c)
        df2.columns = cols
        df2.index = ['Word2Vec_Without_Cutoff', 'Word2Vec_Moderate']
        print(" ")
        print(df2)
        Word2Vec_Moderate_Accuracy = df2.sum(axis=1)[1]/df2.sum(axis=1)[0]
        print("Word2Vec_Moderate_Accuracy = ", Word2Vec_Moderate_Accuracy)
        print(" ")
        #######################################################################
    
    
        # Strict Approach
        print("  ")
        print("Words To Be Searched For Strict Mode: ", words_to_be_searched_stop_rem_strict)
        print("   ")
        print("Output" + " " + str(i+1) + ":")
        for i in range(len(sentences[i])):
#        for sent in tokens_sentences:
            for word in words_to_be_searched_stop_rem_strict:
                if word in word_tokenize(sentences[i]):
#                if word in sent:
                    print(sentences[i])
#                    print(treebank.detokenize(sent))
                    print(" ")
                    Word2Vec_Strict.append(sentences[i])
#                    Word2Vec_Strict.append(treebank.detokenize(sent))
                   
                    
        df3 = pandas.DataFrame(columns = Word2Vec_Without_Cutoff)
        row1 = [1 for x in Word2Vec_Without_Cutoff]
        df3 = df3.append(pandas.Series(row1, index = Word2Vec_Without_Cutoff), ignore_index=True)
        row2 = []
        for val1 in Word2Vec_Without_Cutoff:
            if val1 in Word2Vec_Strict:
                row2.append(1)
            else:
                row2.append(0)
        df3 = df3.append(pandas.Series(row2, index = Word2Vec_Without_Cutoff), ignore_index=True)
        cols = []
        for n in range(len(Word2Vec_Without_Cutoff)):
            c = 'Sent'+ str(n+1)
            cols.append(c)
        df3.columns = cols
        df3.index = ['Word2Vec_Without_Cutoff', 'Word2Vec_Strict']
        print(" ")
        print(df3)
        Word2Vec_Strict_Accuracy = df3.sum(axis=1)[1]/df3.sum(axis=1)[0]
        print("Word2Vec_Strict_Accuracy = ", Word2Vec_Strict_Accuracy)
        print(" ")
        #######################################################################
    
    
    print('\n')                    
    print("Word2Vec_Without_Cutoff:")
    print(" ")              
    print('\n\n'.join([str(item) for item in Word2Vec_Without_Cutoff]))
    
    
    print('\n')                    
    print("Word2Vec_Lenient:")
    print(" ")              
    print('\n\n'.join([str(item) for item in Word2Vec_Lenient]))
    
    
    print('\n')                    
    print("Word2Vec_Moderate:")
    print(" ")              
    print('\n\n'.join([str(item) for item in Word2Vec_Moderate]))
    
    
    print('\n')                    
    print("Word2Vec_Strict:")
    print(" ")              
    print('\n\n'.join([str(item) for item in Word2Vec_Strict]))
    ###########################################################################

    print(" ")
    return(Word2Vec_Lenient, Word2Vec_Moderate, Word2Vec_Strict)
############################ End of Word2Vec ##################################   





############################### Start of  VSM #################################
def preprocess_sent(self):
    op = []
    text = self.replace("\\", "")
    text = text.translate(str.maketrans("","", string.punctuation))
    text = re.sub(r'\d+', '', text)
    text = re.sub(' +', ' ', text)
    text = text.strip()
#    text = text.lower()
    tokens = word_tokenize(text)
    words = [j for j in tokens if not j in stop_words]
    cleansed_doc = []
    for k in words:
        if k.isalnum():
           if len(k) > 1:
              cleansed_doc.append(k)
    str_cleansed_doc = ' '.join(cleansed_doc)
    if str_cleansed_doc != '':
        op.append(str_cleansed_doc)
    return(op)                    
                    

def preprocess_searchkeyword(self):
        text = self.replace("\\", "")
        text = text.translate(str.maketrans("","", string.punctuation))
        text = re.sub(r'\d+', '', text)
        text = re.sub(' +', ' ', text)
        text = text.strip()
#        text = text.lower()
        tokens = word_tokenize(text)
        words = [j for j in tokens if not j in stop_words]
        cleansed_doc = []
        for k in words:
            if k.isalnum():
               if len(k) > 1:
                  cleansed_doc.append(k)
        str_cleansed_doc = ' '.join(cleansed_doc)
        return(str_cleansed_doc)
        
        
def vsm_sent(sentences, search_sentence_list):
    Collated_Output_VSM_No_Cutoff = []
    print(" ")
    print("VSM Output")
    print(" ")
    for i in range(len(search_sentence_list)):
        print("Input" + " " + str(i+1) + ":", search_sentence_list[i])
        print("  ")
        words_to_be_searched = []
        words_to_be_searched_stop_rem = []
        user_input = search_sentence_list[i]
        doc_input = nlp(user_input)
        for word in doc_input:
            print(word.text, word.tag_, spacy.explain(word.tag_))
            if word.tag_ == 'VBZ' or word.tag_ == 'VBG' or word.tag_ == 'VBP' or word.tag_ == 'VBD' or word.tag_ ==  'VBN' or  word.tag_ ==  'VBZ' or word.tag_ == 'VB' :
                words_to_be_searched.append(str(word))
        
        for k in words_to_be_searched:
            if k not in stop_words:
                if k.isalnum():
                    words_to_be_searched_stop_rem.append(k)
        print("the words to be searched are   : ", words_to_be_searched_stop_rem)
        print(" ")
        new_sentences = []
        for word in words_to_be_searched_stop_rem:
            print(word + " " + "Result:")
            for sent in sentences:
                if re.search(r"\b%s\b" % re.escape(word.lower()), sent.lower()):
                    new_sentences.append(sent)
                    print(sent)
                    print(" ")
        unique_new_sentences = list(sorted(set(new_sentences), key=new_sentences.index))
        text = [preprocess_searchkeyword(search_sentence_list[i])] + unique_new_sentences
        print(" ")
        print("Cosine List" + " " + str(i+1) + ":")
        print(" ")
        print('\n\n'.join([str(item) for item in text]))
        count_vectorizer = CountVectorizer()
        count_matrix = count_vectorizer.fit_transform(text)
        cm = list(count_matrix)
        cs = []
        for l in range(len(cm)-1):
            c = cosine_similarity(count_matrix[0:1], count_matrix[l+1:l+2])
            c = [l.tolist() for l in c][0]
            c = [text[l+1], round(c[0], 3)]
            cs.append(c)
            cs.sort(key = lambda x:x[1], reverse = True)
        Collated_Output_VSM_No_Cutoff.append(cs)  

    Collated_Output_VSM_No_Cutoff = [x for x in Collated_Output_VSM_No_Cutoff if x != []]
    Collated_Output_VSM_No_Cutoff = [val for sublist in Collated_Output_VSM_No_Cutoff for val in sublist]

    VSM = Collated_Output_VSM_No_Cutoff
    VSM_Without_Cutoff = [item[0] for item in VSM]
    ###########################################################################
    
    # Lenient Approach
    VSM_Lenient = []
    for i in range(len(VSM)):
        if (VSM[i][1] >= 0.3):
            VSM_Lenient.append(VSM[i][0])
    df1 = pandas.DataFrame(columns = VSM_Without_Cutoff)
    row1 = [1 for x in VSM_Without_Cutoff]
    df1 = df1.append(pandas.Series(row1, index = VSM_Without_Cutoff), ignore_index=True)
    row2 = []
    for val1 in VSM_Without_Cutoff:
        if val1 in VSM_Lenient:
            row2.append(1)
        else:
            row2.append(0)
    df1 = df1.append(pandas.Series(row2, index = VSM_Without_Cutoff), ignore_index=True)
    cols = []
    for i in range(len(VSM)):
        c = 'Sent'+ str(i+1)
        cols.append(c)
    df1.columns = cols
    df1.index = ['VSM_Without_Cutoff', 'VSM_Lenient']
    print(" ")
    print(df1)
    VSM_Lenient_Accuracy = df1.sum(axis=1)[1]/df1.sum(axis=1)[0]
    print("VSM_Lenient_Accuracy = ", VSM_Lenient_Accuracy)
    ###########################################################################
    
    # Moderate Approach
    VSM_Moderate = []
    for i in range(len(VSM)):
        if (VSM[i][1] >= 0.5): 
            VSM_Moderate.append(VSM[i][0])

    df2 = pandas.DataFrame(columns = VSM_Without_Cutoff)
    row1 = [1 for x in VSM_Without_Cutoff]
    df2 = df2.append(pandas.Series(row1, index = VSM_Without_Cutoff), ignore_index=True)
    row2 = []
    for val1 in VSM_Without_Cutoff:
        if val1 in VSM_Moderate:
            row2.append(1)
        else:
            row2.append(0)
    df2 = df2.append(pandas.Series(row2, index = VSM_Without_Cutoff), ignore_index=True)
    cols = []
    for i in range(len(VSM)):
        c = 'Sent'+ str(i+1)
        cols.append(c)
    df2.columns = cols
    df2.index = ['VSM_Without_Cutoff', 'VSM_Moderate']
    print(" ")
    print(df2)
    VSM_Moderate_Accuracy = df2.sum(axis=1)[1]/df2.sum(axis=1)[0]
    print("VSM_Moderate_Accuracy = ", VSM_Moderate_Accuracy)
    ###########################################################################
    
    # Strict Approach
    VSM_Strict = []
    for i in range(len(VSM)):
        if (VSM[i][1] >= 0.7):
            VSM_Strict.append(VSM[i][0])
    df3 = pandas.DataFrame(columns = VSM_Without_Cutoff)
    row1 = [1 for x in VSM_Without_Cutoff]
    df3 = df3.append(pandas.Series(row1, index = VSM_Without_Cutoff), ignore_index=True)
    row2 = []
    for val1 in VSM_Without_Cutoff:
        if val1 in VSM_Strict:
            row2.append(1)
        else:
            row2.append(0)
    df3 = df3.append(pandas.Series(row2, index = VSM_Without_Cutoff), ignore_index=True)
    cols = []
    for i in range(len(VSM)):
        c = 'Sent'+ str(i+1)
        cols.append(c)
    df3.columns = cols
    df3.index = ['VSM_Without_Cutoff', 'VSM_Strict']
    print(" ")
    print(df3)
    VSM_Strict_Accuracy = df3.sum(axis=1)[1]/df3.sum(axis=1)[0]
    print("VSM_Strict_Accuracy = ", VSM_Strict_Accuracy)
    print(" ")
    ###########################################################################
    
    return(VSM_Lenient, VSM_Moderate, VSM_Strict)
################################### End of VSM ################################

    
    
    
    
################################ Start of BQM #################################
def bqm_sent(sentences, search_sentence_list):
#def bqm_sent(tokens_sentences, search_sentence_list):
    Collated_Output_BQM = []
    print(" ")
    print("BQM Output")
    print(" ")
    for i in range(len(search_sentence_list)):
        print("Input" + " " + str(i+1) + ":")
        print(search_sentence_list[i])
        print(" ")
        words_to_be_searched = []
        words_to_be_searched_stop_rem = []
        user_input = search_sentence_list[i]
        doc_input = nlp(user_input)
        for word in doc_input:
            print(word.text, word.tag_, spacy.explain(word.tag_))
            if word.tag_ == 'VBZ' or word.tag_ == 'VBG' or word.tag_ == 'VBP' or word.tag_ == 'VBD' or word.tag_ ==  'VBN' or  word.tag_ ==  'VBZ' or word.tag_ == 'VB' :
                words_to_be_searched.append(str(word))
        for j in words_to_be_searched:
            if j not in stop_words:
                if j.isalnum():
                    words_to_be_searched_stop_rem.append(j)
        print("  ")
        print("Words To Be Searched: ",words_to_be_searched_stop_rem)
        print("   ")
        print("Output" + " " + str(i+1) + ":")
        for i in range(len(sentences)):
#        for sent in tokens_sentences:
            for word in words_to_be_searched_stop_rem:
                if str(word).lower() in [x.lower() for x in word_tokenize(sentences[i])]:
#                if str(word).lower() in [x.lower() for x in sent]:
                    print(sentences[i])
#                    print(treebank.detokenize(sent))
                    print(" ")
                    Collated_Output_BQM.append(sentences[i])
#                    Collated_Output_BQM.append(treebank.detokenize(sent))
    print('\n')                    
    print("Collated_Output_BQM:")
    print(" ")              
    print('\n\n'.join([str(item) for item in Collated_Output_BQM]))
    return(Collated_Output_BQM)
################################ End of BQM ###################################
    

    