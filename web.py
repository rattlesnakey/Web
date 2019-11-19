from numpy import *
import numpy as np
x=array([[1,2,0],[2,0,2]])
a,b,c=np.linalg.svd(x)
d=[[0,0,0],[0,0,0]]
d[0][0]=b[0]
d[1][1]=b[1]
print("完全奇异值分解：\n")
print("u:\n")
print(a)
print("sigma:\n")
print(array(d))
print("vt:\n")
print(c)
e,f,g=np.linalg.svd(x,full_matrices=0)
print("紧奇异值分解：\n")
print("u:\n")
print(e)
h=[[0,0],[0,0]]
h[0][0]=f[0]
h[1][1]=f[1]
print("sigma:\n")
print(array(h))
print("vt:\n")
print(g)
print (s)
