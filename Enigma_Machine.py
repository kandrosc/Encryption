#!/usr/bin/env python3

import sys
import os
usage="Usage: Enigma_Machine.py Input e/d f/t\nInput:The text or file to be encrypted/decrypted\ne/d:Type '0' to encrypt the file/text or '1' to decrypt the file/text\nf/t:Type '0' to encrypt/decrypt the input or '1' to instead read input as a file name and encrypt/decrypt the selected file"
filename=""


def shift(num,sList):
    if num>0:
        for i in range(num):
            safe=sList[len(sList)-1]
            for j in range(len(sList)-1,0,-1):
                sList[j]=sList[j-1]
            sList[0]=safe
            
    elif num<0:
        for i in range(-num):
            safe=sList[0]
            for j in range(len(sList)-1):
                sList[j]=sList[j+1]
            sList[len(sList)-1]=safe
    else:
        pass
    return sList

#Plugboard
def plugboard(char):
    with open("Enigma_Pattern.txt","r") as eng:
        file=eng.read()    
    lines=file.splitlines()
    p=lines[1].split(" ")
    check=True
    
    for i in range(len(p)):
        if len(p[i])!=2:
            check=False
        else:
            for j in range(2):
                if ord(p[i][j])<32 or ord(p[i][j])>126:
                    check=False
    
    if check==True:
        for i in range(len(p)):
            if char==p[i][0]:
                char=p[i][1]
            elif char==p[i][1]:
                char=p[i][0]
    return char



def encrypt():
    #Setup
    with open("Enigma_Pattern.txt","r") as eng:
        file=eng.read()
    lines=file.splitlines()
    c=list(message)
    tempList=list(lines[0])
    q=0

    n=lines[0].split(" ")
    for i in range(len(lines)-2):
        q=q+1
    
    #Determines starting position for each rotor
    for i in range(q):
        d=list(lines[2+i])
        d=shift(int(n[i+1]),d)
        lines[2+i]=d
        
    res=""
    #First Cycle
    for i in range(len(message)):   
        for e in range(q-1):
            k=list(lines[2])
            l=list(lines[3+e])
            c[i]=plugboard(c[i]) 
            for j in range(len(k)):
                if c[i]==k[j]:
                    c[i]=l[j]
                    break           
            for s in range(q):
                lines[2+s]=shift(int(n[q+s+1]),lines[2+s])
        res=res+c[i]
    
    #Addition/Substitution
    s=[None]*len(res)
    for i in range(len(res)):
        s[i]=ord(res[i])
    res=""
    for i in range(len(s)):
        if int(n[0])>=0:
            if s[i]>=32 and s[i]<=(126-int(n[0])):
                s[i]=s[i]+int(n[0])
            elif s[i]>(126-int(n[0])) and s[i]<=126:
                s[i]=s[i]-(95-int(n[0]))
        elif int(n[0])<0:
            if s[i]<=126 and s[i]>=(32-int(n[0])):
                s[i]=s[i]+int(n[0])
            elif s[i]<(32-int(n[0])) and s[i]>=32:
                s[i]=s[i]+(95+int(n[0]))
        res=res+str(chr(s[i]))
        
    enc=""
    #Second Cycle
    b=list(res)
    for i in range(len(res)):   
        for e in range(q-1):
            k=list(lines[len(lines)-1])
            l=list(lines[len(lines)-2-e])
            b[i]=plugboard(b[i]) 
            for j in range(len(k)):
                if b[i]==k[j]:
                    b[i]=l[j]
                    break           
            for s in range(q):
                lines[2+s]=shift(int(n[q+s+1]),lines[2+s])
        enc=enc+b[i]
        
    enc=""
    for i in range(len(b)):
        enc=enc+b[i]
        
    if sys.argv[3]=="1":
        output=open("encrypted_"+filename,"w")
        output.write(enc)
        output.close()
    else:
        print(enc) 













def decrypt():
    #Setup
    with open("Enigma_Pattern.txt","r") as eng:
        file=eng.read()
    lines=file.splitlines()
    c=list(message)
    tempList=list(lines[0])
    q=0

    n=lines[0].split(" ")
    for i in range(len(lines)-2):
        q=q+1
    
    #Determines starting positions for each rotor
    for i in range(q):
        d=list(lines[2+i])
        d=shift(int(n[q+i+1])*(len(message)*(q*2-2)-1)+int(n[i+1]),d)
        lines[2+i]=d
    
    #First cycle
    res=""
    for i in range(len(message)-1,-1,-1):    
        for e in range(q-1):
            k=list(lines[2+e])
            l=list(lines[len(lines)-1])
            for j in range(len(k)):
                if c[i]==k[j]:
                    c[i]=l[j]                   
                    break              
            for s in range(q):
                lines[2+s]=shift(int(n[q+s+1])*-1,lines[2+s])
            c[i]=plugboard(c[i])
        res=res+c[i]
    res=res[::-1]
            
    #Addition/Substitution
    s=[None]*len(res)
    v=int(n[0])*-1
    for i in range(len(res)):
        s[i]=ord(res[i])
    res=""
    for i in range(len(s)):
        if v>=0:
            if s[i]>=32 and s[i]<=(126-v):
                s[i]=s[i]+v
            elif s[i]>(126-v) and s[i]<=126:
                s[i]=s[i]-(95-v)
        elif v<0:
            if s[i]<=126 and s[i]>=(32-v):
                s[i]=s[i]+v
            elif s[i]<32-v and s[i]>=32:
                s[i]=s[i]+95+v
        res=res+str(chr(s[i]))
        
    dec=""
    #Second cycle
    b=list(res)
    for i in range(len(res)-1,-1,-1):   
        for e in range(q-1):
            k=list(lines[len(lines)-1-e])
            l=list(lines[2])
            for j in range(len(k)):
                if b[i]==k[j]:
                    b[i]=l[j]                   
                    break            
            for s in range(q):
                lines[2+s]=shift(int(n[q+s+1])*-1,lines[2+s])
            b[i]=plugboard(b[i]) 
        dec=dec+b[i]
        
    b=list(dec)    
    dec=""
    for i in range(len(b)):
        dec=dec+b[i]
    dec=dec[::-1]
    
    if sys.argv[3]=="1":
        output=open("decrypted_"+filename,"w")
        output.write(dec)
        output.close()
    else:   
        print(dec)
    
    
    
    
if __name__=="__main__":
    message=sys.argv[1]
    if sys.argv[3]=="0" or len(sys.argv)<4:
        pass
    
    elif sys.argv[3]=="1":
        if not (os.path.isfile(message)):
            raise FileNotFoundError(message)
        else:
            with open(message,"r") as file:
                filename=message
                message=file.read()
    elif len(sys.argv)<1 or len(sys.argv)<2 or len(sys.argv)<3:
        print(usage)
        
    if sys.argv[2]=="0":
            encrypt()
    elif sys.argv[2]=="1":
            decrypt()
    else:
        print(usage)    