import numpy as np
import os

def freq_itemsets(file_path, sampletxt, mistxt):
    def get_mis(MIS):
        ms = {}
        sdc =0.1
        mis_rest =0
        for i in MIS:
    #         temp3 = []
            if i[0] == 'SDC':
    #             print(i[1])
                sdc = float(i[1])
            elif i[0] == 'MIS(rest)':
                mis_rest = float(i[1])
            else: 
    #             temp3.append(i[0][4])
    #             temp3.append(float(i[1]))
    #             ms.append(temp3)
                ms[str(int(i[0][4:len(i[0])-1]))] =  float(i[1])
        return ms, mis_rest, sdc
    

    def get_items(data):
        temp6 =[]
        for i in data:
            for j in i:
                temp6.append(str(j))
        return np.unique(temp6)

    
    def all_mis(MIS_temp, items):
        MIS ={}
        for i in items:
            try:
                MIS[i] = MIS_temp[i]
            except:
                MIS[i] = mis_rest
        return MIS
    

    def sort(a, MIS, mis_rest):
        temp5 = {} 
        try: 
            for i in a:
                temp5[i] = MIS[str(i)] 
            l = [i[0] for i in sorted(temp5.items(), key = lambda x: x[1])]
        except:
            for i in a:
                temp5[i[0]] = MIS[i[0]] 
            l = [[i[0]] for i in sorted(temp5.items(), key = lambda x: x[1])]            

        return l
    

    def order(M):
        order ={}
        
        for (i,j) in list(enumerate(M)):
            order[j] = i
            
        return order
    

    def init_pass(M,MIS):
        temp_L = []
        flag = True
        for i in M:
            if count[tuple([i])]/no_trans >= MIS[i] and flag:
                temp_L.append([i])
                min_mis = MIS[i]
                flag = False

            elif not flag:
                if count[tuple([i])]/no_trans >= min_mis:
                    temp_L.append([i])
                    
        return temp_L
    

    def first_counting(M, data_sorted):
        for i in M:
            count[tuple([i])] = 0
        # print(count)
        for i in data_sorted:
            for j in i:
        #         print(j)
                count[tuple([j])] += 1

            
    def F1(count, MIS, L):
        temp_F = []
        for i in L:
        #     print(i)
            if count[tuple(i)]/no_trans >= MIS[i[0]]:
                temp_F.append(i)
                support[tuple(i)] = round(count[tuple(i)]/no_trans,3)
        return temp_F
    

    def level2_candidate(L,sdc, support):
        temp_c =[]
        for i in range(len(L)):
    #         print('\n')
    #         print(L[i])
            j = i+1
            while j < len(L):

    #             print(j)
    #             print(L[j])
                if count[tuple(L[j])]/no_trans >= MIS[L[i][0]] and abs(count[tuple(L[j])]/no_trans - count[tuple(L[i])]/no_trans) <= sdc:
                    temp_c.append(sort([L[i][0], L[j][0]], order, mis_rest))

                j += 1
    #         print(z)
        return temp_c
    

    def support_count(a, data):
        for i in a:
    #         print(i)
            count[tuple(i)] = 0
            for j in data:            
                if all(x in j for x in i):
                    count[tuple(i)] += 1
        return count
    

    def freq_gen(t, data):
        temp_f =[]
        for i in t:
    #         print(i)
            temp_c = 0
            for j in data:
                if all(x in j for x in i):
                    temp_c += 1
            if temp_c/no_trans >= MIS[i[0]]:
    #             print(temp_c/no_trans)
    #             print(MIS[i[0]])
                temp_f.append(i)
                support[tuple(i)] = round(temp_c/no_trans,3)
        return support, temp_f
    

    def MS_candidate(f, sdc):
        temp_c =[]
        length = len(f)
        count = support_count(f, data)
    #     print(count)

        for i in range (0,length):
            element1 = f[i][:-1]
            for j in range (i+1,length):
                element2 = f[j][:-1]
    #             print(element1)
                if element1 == element2 and abs(count[tuple([f[i][len(f[i])-1]])]/no_trans - count[tuple([f[j][len(f[j])-1]])]/no_trans) <= sdc:
                    temp_comb = list(set(f[i] + f[j]))
    #                 print(temp_comb)
    #                 print(z)
                    comb = sort(temp_comb, order, mis_rest)
                    temp_c.append(comb)

                    for k in range(1,len(comb)+1):
    #                     print(comb[:k-1])
    #                     print(comb[k:])
                        s = comb[:k-1] + comb[k:]
    #                     print(s)
                        if comb[0] in s or MIS[comb[1]] == MIS[comb[0]]:
                            if s not in f:
    #                             print('t')
                                temp_c.remove(comb)
                                break
    #                 print(z)
        return temp_c


    temp = np.loadtxt(fname = os.path.join(file_path, sampletxt), delimiter= '\n', dtype= str)
    data_temp = [i.replace('{','').replace('}', '').split(', ') for i in temp]
    data = [[i for i in j] for j in data_temp]
    no_trans = len(data)

    temp2 = np.loadtxt(fname = os.path.join(file_path, mistxt), delimiter= '\n', dtype= str)
    MIS_temp = [i.split(' = ') for i in temp2]

    MIS_temp2, mis_rest, sdc = get_mis(MIS_temp)

    items = get_items(data)

    MIS = all_mis(MIS_temp2, items)

    data_sorted = [sort(i, MIS, mis_rest) for i in data]

    M = sort(items, MIS, mis_rest)

    order = order(M)

    global count
    count ={}
    first_counting(M, data_sorted) 

    temp_L =  init_pass(M,MIS)
    L = sort(temp_L, order, mis_rest)
    
    global support
    support ={}
    F = []
    
    temp_f = F1(count, MIS, L)
    F.append(sort(temp_f, order, mis_rest))

    C = [] 
    if len(temp_f) != 0:                 
        C.append(level2_candidate(L, sdc, support))

        support, temp_f = freq_gen(C[0], data)
        F.append(temp_f)
    k = 1
    while len(temp_f) != 0:

        C.append(MS_candidate(F[k], sdc))
        temp_s, temp_f = freq_gen(C[k], data)
        if len(temp_f) != 0: 
            F.append(temp_f)
            support.update(temp_s)
        k += 1
#     return F

    for i in range(len(F)):
        print('(Length-' + str(i+1) + ' ' + str(len(F[i])))
        for j in F[i]:
            temp = '     ('
            for k in j:
                temp += k
                if k != j[-1]:
                    temp += ' '
            temp += ')'
            print(temp)
        print(')')
        print('\n')


file_path = r'C:\Users\kalya\OneDrive - University of Illinois at Chicago\!UIC\!Semesters\3rd Sem\CS 583 Data Mining and Text Mining\Assignements\Assignment 1'
freq_itemsets(file_path, 'Sample.txt', 'MIS.txt')