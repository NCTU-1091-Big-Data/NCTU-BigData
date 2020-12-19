# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 15:51:24 2020

@author: ASUS
"""

import pandas as pd
import numpy as np
import pickle


def inference(data):
    '''
       inference data.
       data : list or np.array. list length must 17.
           i.g [ 19491, 3874, 0.1987584013134267, 0, 0, 23, 54,
           25, 29, 4, 0.0005643630393514956, 0.00010261146170027192, 1, 6, 2,
           18, 1]
    '''
    
    v = np.asarray(data, dtype=float)
    
    col = ['content_length', 'lead_length',
           'lead_length_ratio', 'num_header2_reference', 'num_refTag',
           'num_ref_tag', 'num_page_links', 'num_cite_temp',
           'num_non_cite_templates', 'num_categories', 'num_images_length',
           'num_files_length', 'has_infobox', 'num_lv2_headings',
           'num_lv3_headings', 'website_count', 'word_count']
    
    '''取log
     'content_length','num_header2_reference','num_refTag',
     'num_ref_tag','num_page_links','num_non_cite_templates'
     [0, 3, 4, 5, 6, 8] 
     '''
    num = [0, 3, 4, 5, 6, 8] 
    
    def lg(n):
        if n<0:
            n = 0
        return np.log(n+0.0001)
    
    for c in num:
        v[c] = lg(v[c])
    
    df = pd.DataFrame(v,col).T
    
    
    file_name = "xgb_reg.pkl"
    
    # load
    xgb_model_loaded = pickle.load(open(file_name, "rb"))
    
    y_pred=xgb_model_loaded.predict(df)
    
    
    return y_pred

if __name__ == '__main__': 
    #len=17
    a = [ 19491, 3874, 0.1987584013134267, 0, 0, 23, 54,
       25, 29, 4, 0.0005643630393514956, 0.00010261146170027192, 1, 6, 2,
       18, 1]
    print(inference(a))
    

