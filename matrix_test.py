import numpy as np
import numpy as np
import binascii
from PIL import Image, ImageFilter

def mat():
    
    coords = (3,3)
    enum = lambda x: list(enumerate(x)) # IMPORTANT turns list into list of tuples, each tuple containing (index, value)
    
    A = np.array([[6,2,3],[1,4,7],[5,0,6]])
    print("Original matrix: ")
    print(A)
    
    a = enum(A.flatten())
    print("Flattened matrix with indices: ")
    print(a)
    
    e = [5,4,3,1,0,6,7,2,8]
    
    L = len(e)
    
    enc = lambda x: e[ (x[1]+x[0])%L ]
    b = np.apply_along_axis(enc,1,a)
    B = b.reshape(coords)
    print("Encrypted matrix: ")
    print(B)
    
    b = enum(B.flatten())[::-1]
    print("Flattened encrypted matrix with indices: ")
    print(b)
    
    dec = lambda x: (e.index(x[1])-x[0])%L
    a = np.apply_along_axis(dec,1,b)[::-1]
    A = a.reshape(coords)
    print("Decrypted matrix - same as original: ")
    print(A)
    



if __name__ == "__main__":
    mat()