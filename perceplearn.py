# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 22:50:09 2019

@author: nov28
"""

from __future__ import division
import os
import sys
import glob
from collections import Counter, defaultdict
import re
import json
from random import shuffle

def tokenize(sett,f):
    s=[ x for x in sett if x in f]
    #s=[y for y in s if len(y)!=1 if y not in comwords]
    return s


if __name__=='__main__':
    all_files=glob.glob(os.path.join(sys.argv[1], '*/*/*/*.txt'))
    p_files=[]
    n_files=[]
    t_files=[]
    d_files=[]
    for f in all_files:
        class1, class2, fold, fname = f.split(os.path.sep)[-4:]
        class1= class1.split('_')[0]
        class2= class2.split('_')[0]
        if class1=="positive" :
            p_files.append(f)
        else:
            n_files.append(f)
        if class2=="truthful":
            t_files.append(f)
        else:
            d_files.append(f)
    
    
    #classifier1 features
    poscom= Counter()
    swp=['a','able','hotel','room','stay','chicago','city','michigan','about','she','with','this','you','our','rooms','across','all','also','am','among','an','and','any','are','as','at','be','because','been','by','dear','else','for','from','had','has','her','hers','him','his','i','in','into','is','it','me','my','of','on','only','or','own','so','that','the','their','there','to','us','was','we']
    
    for pf in p_files:
        #remove in vocareum
        class1, class2, fold, fname = pf.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            flets=list(re.findall(r'\w+', open(pf).read().lower()))
            for t in flets:
                if t in swp or t.isdigit():
                    continue
                else:
                    
                    poscom[t] += 1
    p750=(poscom.most_common(750))
    class1_features=[]
    for p,n in p750:
        class1_features.append(p)
    
    negcom= Counter()
    swn=['a','able','hotel','room','stay','chicago','city','michigan','about','with','this','you','our','rooms','across','all','also','am','among','an','and','any','are','as','at','be','because','been','by','dear','else','for','from','had','has','her','hers','him','his','i','in','into','is','it','me','my','of','on','only','or','own','so','she','that','the','their','there','to','us','was','we']
    
    for nf in n_files:
        #remove in vocareum
        class1, class2, fold, fname = nf.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            flets=list(re.findall(r'\w+', open(nf).read().lower()))
            for t in flets:
                if t in swn or t.isdigit():
                    continue
                else:
                    
                    negcom[t] += 1
        
    n750=(negcom.most_common(750))
    for n,num in n750:
        if n not in class1_features:
            class1_features.append(n)
    #loading train data pos neg
    pnlist=[]
    for pf in p_files:
        #remove in vocareum
        class1, class2, fold, fname = pf.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            itemlist=[]
            flets=list(re.findall(r'\w+', open(pf).read().lower()))
            ftokens=tokenize(flets,class1_features)
            tempc= Counter(ftokens)
            itemlist.append(1)
            itemlist.append(tempc)
            #print(itemlist)
            pnlist.append(itemlist)
    for nf in n_files:
        #remove in vocareum
        class1, class2, fold, fname = nf.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            itemlist=[]
            flets=list(re.findall(r'\w+', open(nf).read().lower()))
            ftokens=tokenize(flets,class1_features)
            tempc= Counter(ftokens)
            itemlist.append(-1)
            itemlist.append(tempc)
            #print(itemlist)
            pnlist.append(itemlist)
    
    posneglists=pnlist[:]
    
    
    
    
    #used for tokenization of deceptive
    decepcom= Counter()
    c2f=[]
    for df in d_files:
        #remove in vocareum
        class1, class2, fold, fname = df.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            flets=list(re.findall(r'\w+', open(df).read().lower()))
            for t in flets:
                if t.isalpha():
                    
                    decepcom[t] += 1
    class2_features=[]
    for d,n in decepcom.most_common(1000):
        class2_features.append(d)
    
    trucom= Counter()
    for tf in t_files:
        #remove in vocareum
        class1, class2, fold, fname = tf.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            flets=list(re.findall(r'\w+', open(tf).read().lower()))
            for t in flets:
                if t.isalpha():
                    trucom[t] += 1
                    
    c2f=class2_features[:]
    t1000=(trucom.most_common(1000))
    for n,num in t1000:
        if n not in class2_features:
            c2f.append(n)
    
    #loading true dec train data
    tdlist=[]
    for tf in t_files:
        #remove in vocareum
        class1, class2, fold, fname = tf.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            itemlist=[]
            flets=list(re.findall(r'\w+', open(tf).read().lower()))
            ftokens=tokenize(flets,c2f)
            tempc= Counter(ftokens)
            itemlist.append(1)
            itemlist.append(tempc)
            #print(itemlist)
            tdlist.append(itemlist)
    
    for df in d_files:
        #remove in vocareum
        class1, class2, fold, fname = df.split(os.path.sep)[-4:]
        if fold=="fold1":
            continue
        else:
            itemlist=[]
            flets=list(re.findall(r'\w+', open(df).read().lower()))
            ftokens=tokenize(flets,c2f)
            tempc= Counter(ftokens)
            itemlist.append(-1)
            itemlist.append(tempc)
            #print(itemlist)
            tdlist.append(itemlist)
        
    
    trudeclists=tdlist[:]
    
    #vanillaaaaaa pos neg train
    
    #training...................
    
    
    weightsc1vn= defaultdict(int)
    bc1vn=0
    
    tnumupdates=0
    
    for epochs in range(50):
        shuffle(posneglists)
        updates=0
        for iopair in posneglists:
            tempdict= iopair[1]
            #print(tempdict)
            y=iopair[0]
            a=sum([tempdict[w]*weightsc1vn[w] for w in tempdict]) + bc1vn
            if a*y <=0:
                tnumupdates+=1
                updates +=1
                for w in tempdict:
                    weightsc1vn[w] += y*tempdict[w]
                bc1vn += y
        #print("updates each epoch: ",updates )
    #print("total no. of updates: ",tnumupdates)
    
    #vanillaaaaaa tru dec train
    
    #training...................
    #from random import shuffle
    
    weightsc2vn= defaultdict(int)
    bc2vn=0
    
    tnumupdates=0
    
    for epochs in range(120):
        shuffle(trudeclists)
        updates=0
        for iopair in trudeclists:
            tempdict= iopair[1]
            #print(tempdict)
            y=iopair[0]
            a=sum([tempdict[w]*weightsc2vn[w] for w in tempdict]) + bc2vn
            if a*y <=0:
                tnumupdates+=1
                updates +=1
                for w in tempdict:
                    weightsc2vn[w] += y*tempdict[w]
                bc2vn += y
        #print("updates each epoch: ",updates )
    #print("total no. of updates: ",tnumupdates)
    
    #avg pos neg train
    #from random import shuffle
    
    weightsc1avg= defaultdict(float)
    bc1avg=0.0
    u1= defaultdict(float)
    beta1=0.0
    c1=1
    totupdates=0
    for epoch in range(50):
        shuffle(posneglists)
        numupdates=0
        for iopair in posneglists:
            tempdict= iopair[1]
            #print(tempdict)
            y=iopair[0]
            a= (sum([tempdict[w]*weightsc1avg[w] for w in tempdict]) + bc1avg)*y
            #print(a)
            if a<=0:
                numupdates+=1
                for w in tempdict:
                    weightsc1avg[w] += y*tempdict[w]
                    u1[w] += y*c1*tempdict[w]
                bc1avg += y
                beta1 += y*c1
            c1 +=1
        #print("entry updates: ",numupdates)
    for w in weightsc1avg:
        weightsc1avg[w] -= u1[w]/c1
    bc1avg -= beta1/c1
    
    
    #avg tru dec train
    
    #from random import shuffle
    
    weightsc2avg= defaultdict(float)
    bc2avg=0.0
    u2= defaultdict(float)
    beta2=0.0
    c2=1
    totupdates=0
    for epoch in range(120):
        shuffle(trudeclists)
        numupdates=0
        for iopair in trudeclists:
            tempdict= iopair[1]
            #print(tempdict)
            y=iopair[0]
            a= (sum([tempdict[w]*weightsc2avg[w] for w in tempdict]) + bc2avg)*y
            #print(a)
            if a<=0:
                numupdates+=1
                for w in tempdict:
                    weightsc2avg[w] += y*tempdict[w]
                    u2[w] += y*c2*tempdict[w]
                bc2avg += y
                beta2 += y*c2
            c2 +=1
        #print("entry updates: ",numupdates)
    for w in weightsc2avg:
        weightsc2avg[w] -= u2[w]/c2
    bc2avg -= beta2/c2
    
    with open('vanillamodel.txt','w+') as output:
        output.write("classifier 1 Positive/Negative classifier features "+"\n")
        for cl in class1_features:
            output.write(str(cl) + " ")
        output.write("\n")
        output.write("weights: "+"\n")
        output.write(json.dumps(weightsc1vn))
        output.write("\n")
        output.write("Bias:"+"\n")
        output.write(str(bc1vn))
        output.write("\n")
        output.write("classifier 2 Truthful/Deceptive classifier features "+"\n")
        for cl in c2f:
            output.write(str(cl) + " ")
        output.write("\n")
        output.write("weights: "+"\n")
        output.write(json.dumps(weightsc2vn))
        output.write("\n")
        output.write("Bias:"+"\n")
        output.write(str(bc2vn))
        output.write("\n")
    output.close()
    
    with open('averagemodel.txt','w+') as output1:
        output1.write("classifier 1 Positive/Negative classifier features "+"\n")
        for cl in class1_features:
            output1.write(str(cl) + " ")
        output1.write("\n")
        output1.write("weights: "+"\n")
        output1.write(json.dumps(weightsc1avg))
        output1.write("\n")
        output1.write("Bias:"+"\n")
        
        output1.write(str(bc1avg))
        output1.write("\n")
        output1.write("classifier 2 Truthful/Deceptive classifier features "+"\n")
        for cl in c2f:
            output1.write(str(cl) + " ")
        output1.write("\n")
        output1.write("weights: "+"\n")
        output1.write(json.dumps(weightsc2avg))
        output1.write("\n")
        output1.write("Bias:"+"\n")
        output1.write(str(bc2avg))
        output1.write("\n")
    output1.close()
        
    
    
    
    
