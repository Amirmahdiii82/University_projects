import numpy as np
import random
import statistics as st
popSize = 100
generation = 40


# ----- init population --------------------------
def init_pop():
    Population = np.zeros((popSize,2))
    for i in range(popSize):  
        Population[i] = 64*np.random.rand(2)-32
    return Population
# ------------------------------------------------
  

# parent selection: uniform -----------------------------
def parent_selection():
    muRate = 0.5
    crossRate = 0.3
    muPop_size = int( np.ceil(muRate * popSize)) 
    crossPop_size = int (2*np.ceil((crossRate * popSize)/2)) 
    childPop_size = muPop_size + crossPop_size
    matingPoolIndex = random.sample( range(0,popSize),int(childPop_size))     
    return (matingPoolIndex,muPop_size,crossPop_size)
# ------------------------------------------------------
    

# crossover : 1 point ----------------------------------
def Crossover(Population, crossPop_size, matingPoolIndexes):
    chrom_size =  len (Population[0])
    children_cross = np.zeros((crossPop_size,chrom_size))
    i=0
    while i < crossPop_size:
        x= matingPoolIndexes [i]
        y= matingPoolIndexes [i+1]
        Parent1 = Population[x]
        Parent2 = Population[y]
        child1 = (Parent1[0] , Parent2[1])
        child2 = (Parent2[0] , Parent1[1])
        children_cross[i]= child1
        children_cross[i+1]= child2
        i = i + 2
    return children_cross
# -----------------------------------------------------

# ------ mutation -------------------------------
def mutate(Population,muPop_size , matingPoolIndexes):
    chrom_size =  len (Population[0])
    children_mut = np.zeros((muPop_size,chrom_size))
    crossPop_size =   len(matingPoolIndexes) - muPop_size -1
    mu=0
    sigma = 5
    i = crossPop_size
    j= 0
    while i < len(matingPoolIndexes)-1:
        x= matingPoolIndexes [i]
        Parent_single = Population[x]
        Deltax = np.random.normal (mu , sigma)
        randomGenC = np.random.randint(0,len(Parent_single))
        muchild = Parent_single.copy()
        newGen = Parent_single[randomGenC] + Deltax
        muchild[randomGenC] = newGen
        if muchild[randomGenC] > 32:
            muchild[randomGenC] = 32
        elif muchild[randomGenC]< -32:
            muchild[randomGenC] = -32
        children_mut[j] = muchild
        i = i + 1
        j= j + 1
    return children_mut
# -----------------------------------------------------
    
# # survival selection: elitism -----------------------
def survivor_selection(TotalPop,mainPopsize):
    a = 20
    b = 0.2
    c = 2 * np.pi
    TotalpopSize = len(TotalPop)
    fitness = np.zeros(TotalpopSize)
    for i in range(TotalpopSize):
        X = TotalPop[i,0]
        Y = TotalPop[i,1]
        sum_sq_term = -a * np.exp(-b * np.sqrt(X*X + Y*Y) / 2)
        cos_term = -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
        Z = a + np.exp(1) + sum_sq_term + cos_term
        fitness[i] = Z
    
    Total_bestIndexes = np.argsort(fitness)
    Final_bestIndexes = Total_bestIndexes[0:mainPopsize]
    
    newPop = TotalPop[Final_bestIndexes]
    newPopFitness = fitness[Final_bestIndexes]
    return newPop , newPopFitness
#-------------------------------------------------------


# ---------Genetic main loop ---------------------------
Population = init_pop() 
mainPopsize = popSize 
best_fitness_array= np.zeros(generation)
fitn_average_array= np.zeros(generation)

for iteration in range(generation):
      print("generation:", iteration)
      matingPoolIndexes , muPop_size , crossPop_size = parent_selection()
      offspring_cross = Crossover(Population, crossPop_size, matingPoolIndexes)
      offspring_mu = mutate(Population, muPop_size, matingPoolIndexes)
      TotalPop = np.concatenate((Population,offspring_cross,offspring_mu) , 0 )
      newPop , newPopFitness = survivor_selection(TotalPop, mainPopsize)
      bestIndexes = np.argsort(newPopFitness)
      Final_bestIndex = bestIndexes[0]
      best_fitness_array [iteration] = newPopFitness[Final_bestIndex]
      fitn_average_array [iteration] = st.mean(newPopFitness)
      Population = newPop
      
      
# --------------------------------------------------

bestIndexes = np.argsort(newPopFitness)
Final_bestIndex = bestIndexes[0]
bestSolution = newPop[Final_bestIndex]
bestSolution_fitness =  newPopFitness[Final_bestIndex]








