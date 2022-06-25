import numpy as np
from math import *

e_r = np.array([0,1,0])/np.linalg.norm(np.array([0,1,0]))
print(e_r)
e_Phi = (np.array([1, 0, 0])* e_r)
print(e_Phi)
if e_Phi==0:
    print("aa")