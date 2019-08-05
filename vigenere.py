def encrypt(alphanum,message,keyword):
    output=''
    for i in range(len(message)):
        output=output+alphanum[ord(keyword[i])-97][ord(message[i])-97]
    return output
    
    
def decrypt(alphanum,message,keyword):
    output=''
    for i in range(len(message)):
        alpha=alphanum[0]
        row=alphanum[ord(keyword[i])-97]
        for j in range(len(row)):
            if row[j]==message[i]:
                output=output+alpha[j]
    return output

def fixKeyword(message,keyword):
    if len(message)>len(keyword):
        while len(keyword)<=len(message):
            keyword=keyword+keyword
        keyword=keyword[:len(message)]
        
    elif len(message)<len(keyword):
        keyword=keyword[:len(message)]
    return keyword
    
    
def main():
    alpha=[]
    alphanum=[]
    
    for i in range(97,123):
        alpha.append(str(chr(i)))
        
    alphanum.append(alpha)
    for i in range(1,26):
        end=alphanum[i-1][0]
        l=alphanum[i-1][1:]
        l.append(end)
        alphanum.append(l)
    
    message=input('enter plain text: ')
    keyword=input('enter the keyword: ')
    keyword=fixKeyword(message,keyword)
    
    while True:
        inp=input("Type e to encrypt, type d to decrypt: ").lower()
        if inp=='e':
            output=encrypt(alphanum,message,keyword)
            print(output)
            break
        elif inp=='d':
            output=decrypt(alphanum,message,keyword)
            print(output)
            break
        else:
            print('not a valid input')

main()