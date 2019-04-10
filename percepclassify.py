# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 23:14:15 2019

@author: nov28
"""

from __future__ import division
import os
import sys
import numpy as np
import glob

from collections import Counter, defaultdict
import re


def tokenize(sett,f):
    s=[ x for x in sett if x in f]
    #s=[y for y in s if len(y)!=1 if y not in comwords]
    return s


if __name__=='__main__':
    all_files = glob.glob(os.path.join(sys.argv[2], '*/*/*/*.txt'))
    directory=sys.argv[1]
    docname=os.path.split(directory)[1]
    if docname.split(".")[0]=="vanillamodel":
        vnm=open("vanillamodel.txt","r")
        tempt= vnm.readline()
        c1f=vnm.readline()
        class1_features=c1f.split(" ")[:-1]
        tempt=vnm.readline()
        vnwline=vnm.readline()
        wc1vn=eval(vnwline)
        tempt=vnm.readline()
        bc1vn=int(vnm.readline())
        tempt= vnm.readline()
        cl2f=vnm.readline()
        class2_features= cl2f.split(" ")[:-1]
        tempt=vnm.readline()
        vnw2line= vnm.readline()
        wc2vn= eval(vnw2line)
        tempt=vnm.readline()
        bc2vn=int(vnm.readline())
        
    if docname.split(".")[0]=="averagemodel":
        vnm=open("averagemodel.txt","r")
        tempt= vnm.readline()
        c1f=vnm.readline()
        class1_features=c1f.split(" ")[:-1]
        tempt=vnm.readline()
        vnwline=vnm.readline()
        wc1avg=eval(vnwline)
        tempt=vnm.readline()
        bc1avg=float(vnm.readline())
        tempt= vnm.readline()
        cl2f=vnm.readline()
        class2_features= cl2f.split(" ")[:-1]
        tempt=vnm.readline()
        vnw2line= vnm.readline()
        wc2avg= eval(vnw2line)
        tempt=vnm.readline()
        bc2avg=float(vnm.readline())
    
    #loading test data
    pntestlist=[]
    tdtestlist=[]
    
    for f in all_files:
        #remove in vocareum
        flets=list(re.findall(r'\w+', open(f).read().lower()))
        ftokenspn=tokenize(flets,class1_features)
        ftokenstd=tokenize(flets,class2_features)
        
        tempcpn= Counter(ftokenspn)
        tempctd=Counter(ftokenstd)
        #print(itemlist)
        pntestlist.append(tempcpn)
        tdtestlist.append(tempctd)
    
    opfile= open("percepoutput.txt","w+")
    if docname.split(".")[0]=="vanillamodel":
        for item in range(len(all_files)):
            tempdictpn=pntestlist[item]
            b=sum([tempdictpn[w]*wc1vn[w] for w in tempdictpn]) + bc1vn
            if b>0:
                labelb="positive"
            else:
                labelb="negative"
            tempdicttd= tdtestlist[item]
            a=sum([tempdicttd[w]*wc2vn[w] for w in tempdicttd]) + bc2vn
            if a>0:
                labela="truthful"
            else:
                labela="deceptive"
            opfile.write(labela+" "+labelb+" "+all_files[item]+"\n")
        opfile.close()
    
    if docname.split(".")[0]=="averagemodel":
        for item in range(len(all_files)):
            tempdictpn=pntestlist[item]
            b=sum([tempdictpn[w]*wc1avg[w] for w in tempdictpn]) + bc1avg
            if b>0:
                labelb="positive"
            else:
                labelb="negative"
            tempdicttd= tdtestlist[item]
            a=sum([tempdicttd[w]*wc2avg[w] for w in tempdicttd]) + bc2avg
            if a>0:
                labela="truthful"
            else:
                labela="deceptive"
            opfile.write(labela+" "+labelb+" "+all_files[item]+"\n")
        opfile.close()
    
    