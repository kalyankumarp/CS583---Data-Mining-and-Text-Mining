import numpy as np
import os
import matplotlib.pyplot as mp

def EM_assignment3(file_path, sampletxt):
    
# Predicting the classes based on the given probabilities
    def predicted_class(data, threshold):
        data_t = np.transpose(data)
        temp  = []
        temp2 = []
        temp3 = []
        for i in data_t[0]:
            if i>=threshold:
                temp.append('A')
            else:
                temp.append('B')
        for j in data_t[1]:
            if j == 1.0:
                temp3.append('A')
            else:
                temp3.append('B')  

        temp2.append(data_t[0])
        temp2.append(temp3)
        temp2.append(temp)

        return np.asarray(temp2)

    def evaluation_metrics(data_t, threshold):
        data = predicted_class(data_t, threshold)

    # CONFUSION Matrix 
        actual_Classes = data[-2]    
        predicted_Classes = data[-1] 
        class_uniq = np.unique(actual_Classes)
    #     print(class_uniq)
        n = len(class_uniq)
        conf = np.zeros((n,n))

        for i in range(len(class_uniq)):
            for j in range(len(class_uniq)):
                conf[i, j] = np.sum((actual_Classes == class_uniq[i]) & (predicted_Classes == class_uniq[j]))

# The rows are actual and columns are predicted
# The first row is positive and second one is of negative class. The same for columns            

    # Evaluation Metrics
        EM = {}
        EM['accuracy'] = round(sum(np.diagonal(conf))/len(data[0]),3)
        EM['prec_positive'] = round(conf[0][0]/sum(conf[:,0]),3)
        temp_rec = round(conf[0][0]/sum(conf[0,:]),3)
        temp_func = lambda temp: 0 if bool(np.isnan(temp))  else temp
        EM['rec_positive'] = temp_func(temp_rec)

        EM['F1_positive'] = temp_func(round((2*EM['prec_positive']*EM['rec_positive'])/(EM['prec_positive']+EM['rec_positive']),3))
        EM['TPR'] = EM['rec_positive']
        EM['sensitivity'] = EM['rec_positive']
        EM['TNR'] = temp_func(round(conf[1][1]/sum(conf[1,:]),3))
        EM['specificity'] = EM['TNR']
        EM['FPR'] = temp_func(round(1 - EM['TNR'],3))
        return EM, conf

    def ROC(data):
        data_np = np.asarray(data)
        ind=np.argsort(data_np[:,-2])
        data_sorted=data_np[ind][:,1:]
        a = []
        for i in range(len(data_sorted)):
            thres = data_sorted[i][0]
            EM_temp = evaluation_metrics(data_sorted, thres)[0]
            b =[EM_temp['FPR'], EM_temp['TPR']]
            a.append(b) 
        return np.transpose(a)

    
    def auc(a):

# Using Trapeziodal principle to find the area under the roc curve

        area = 0
        for i in range(len(a[0])-1):
            area += abs((a[0][i+1] - a[0][i])*(a[1][i+1] + a[1][i]))/2
        return round(area,3)
    
# Loading the data from the given text file    

    temp = np.loadtxt(fname = os.path.join(file_path, sampletxt), delimiter= '\n', dtype= str)
    data_temp = [i.replace('{','').replace('}', '').split(', ') for i in temp]
    data = [[float(i) for i in j] for j in data_temp]

    # data2= predicted_class(data, 0.5)
    EM, conf = evaluation_metrics(np.asarray(data)[:,1:], 0.5)

    a = ROC(data)
    
    print('(')
    print('(Accuracy ' + str(EM['accuracy']) + ')')
    print('(Precision ' + str(EM['prec_positive']) + ')')
    print('(Recall ' + str(EM['rec_positive']) + ')')
    print('(F1 ' + str(EM['F1_positive']) + ')')
    print('(TPR ' + str(EM['TPR']) + ')')
    print('(FPR ' + str(EM['FPR']) + ')')
    print('(Specificity ' + str(EM['specificity']) + ')')
    print('(Sensitivity ' + str(EM['sensitivity']) + ')')
    print('(AUC ' + str(auc(a)) + ')')
    print(')')

file_path = r'C:\Users\kalya\OneDrive - University of Illinois at Chicago\!UIC\!Semesters\3rd Sem\CS 583 Data Mining and Text Mining\Assignements\Assignment 3'
EM_assignment3(file_path, 'AS3_Sample2.txt')
