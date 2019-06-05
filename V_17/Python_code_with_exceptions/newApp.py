from flask import Flask, jsonify, render_template, flash, request, redirect, url_for
import pandas as pd
from final_try_new_ner import *
from flask_cors import CORS
#import cv2
from timeit import default_timer as timer
import ast
import chardet

app = Flask(__name__)

CORS(app)

def check_encoding_newApp(self):
    test = open(self, 'rb').read()
    result = chardet.detect(test)
    charenc = result['encoding']
    return(charenc)
    

@app.route('/predict', methods=['GET', 'POST'])
def predict():
        print('resss', request.data)
        fileInput = request.data.decode("utf-8")
        fileInput = ast.literal_eval(fileInput)
        start = timer()
        
        dicts_linient = {}
        dicts_medium = {}
        dicts_strict = {}
        print(fileInput)
       
        path_training = 'C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Middleware\\training\\'+  fileInput['trainingDocument']
        count_training = 0
        with open(path_training, encoding=check_encoding_newApp(path_training)) as f:
                for x in f:
                        count_training = count_training + 1
        
        if count_training == 0:
                return jsonify({'training_count': 0  })
        else:
                result = get_documents(fileInput['trainingDocument'], fileInput['testingDocument'])
                if result is True:
                        # For linient model
                        path = 'C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Python_code_with_exceptions\\Uniq_Final_Sentences_Lenient.txt'
                        print("****************** check ***************************")
                        count_linient = 0
                        with open(path, encoding = check_encoding_newApp(path)) as f:
                                for line_linient in f:
                                        dicts_linient[count_linient] = line_linient
                                        count_linient = count_linient + 1

                        # For medium model
                        path_medium = 'C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Python_code_with_exceptions\\Uniq_Final_Sentences_Moderate.txt'
                        
                        count_medium = 0
                        with open(path_medium, encoding = check_encoding_newApp(path_medium)) as f:
                                for line_medium in f:
                                        dicts_medium[count_medium] = line_medium
                                        count_medium = count_medium + 1

                        # For strict model
                        path_strict = 'C:\\Users\\ArgusMLPOC_Admin\\Desktop\\Argus\\Final_demo\\backup\\V_16\\Python_code_with_exceptions\\Uniq_Final_Sentences_Strict.txt'
                        
                        count_strict = 0
                        with open(path_strict, encoding = check_encoding_newApp(path_strict)) as f:
                                for line_strict in f:
                                        dicts_strict[count_strict] = line_strict
                                        count_strict = count_strict + 1
                        #cv2.waitkey(30)
                        duration = timer() - start
                        print(duration)
                        print("#############################  check 2 #######################")
                        output = jsonify({'sentence_linient': dicts_linient, 'count_linient': count_linient, 'sentence_medium': dicts_medium, 'count_medium': count_medium, 'sentence_strict': dicts_strict, 'count_strict': count_strict})
                else:
                        output = jsonify({'message': 'Exception Found'})
        
                return output
                         
