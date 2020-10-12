import numpy as np
import os
from math import log

def IG(file_path, sampletxt, att_no):

# Calculating the entropy of root node

    def entropy_root(data):
        (unique, counts) = np.unique(data, return_counts=True)
        n = len(data)
        ent =0
        for i in counts:
            p = i/n
            ent+= -(p*log(p,2))
        return ent

# calculating the total entropy of child nodes

    def entropy(attr, clas):
        ent = 0
        uniq = np.unique(attr)
        uniq_class = np.unique(clas)
        for i in uniq:
            temp_ent = 0
            temp = np.zeros(len(uniq_class))
            indices = np.where(attr == i)
            n = len(indices[0])
            for j in indices[0]:
                for k in range(len(uniq_class)):
                    if clas[j] == uniq_class[k]:
                        temp[k] += 1
            temp_p = temp/n
            for i in temp_p:
                if i != 0:
                    temp_ent += -(i*log(i,2))
            ent += temp_ent*(n/len(data))
#         print('f')
        return round(ent,3)
    

    def ig(data, attr):
        return round(entropy_root(data_transpose[-1]) - entropy(attr, data_transpose[-1]),3)
    
# Loading the data from the given text file

    temp = np.loadtxt(fname = os.path.join(file_path, sampletxt), delimiter= '\n', dtype= str)
    data_temp = [i.replace('{','').replace('}', '').split(',') for i in temp]
    data = np.asarray([[i for i in j] for j in data_temp])

    data_transpose = np.transpose(data)

    attr = data_transpose[att_no]
    
# Calculating the information gain

    value  = ig(data, attr)
    
#     print('f')
    return value
    
    
file_path = r'C:\Users\kalya\OneDrive - University of Illinois at Chicago\!UIC\!Semesters\3rd Sem\CS 583 Data Mining and Text Mining\Assignements\Assignment 2'
Value = IG(file_path, 'AS2_Sample.txt', 3)
print('IG (' + str(Value) + ')')