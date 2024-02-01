## roulette wheel ##
import numpy as np
fitness = 100*np.random.rand(20)

TotalFit = sum(fitness)
size = len(fitness)

# pribability density function and accumulation function
p = np.zeros(size)
a = np.zeros(size)

for i in range(size):
    p[i]= fitness[i]/TotalFit
    if i==0:
        a[0]=p[0]
    else:
        a[i] = a[i-1] + p[i]

        
        
# run roulette wheel
randomPointer = np.random.rand()
j = 0
while randomPointer > a[j]:
    j= j + 1        
    
selectedChrom = j  









  