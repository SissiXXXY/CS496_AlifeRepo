# CS496_AlifeRepo
Northwestern CS496 Artificial Life Repository
Author:Yao Xiao

Delete all fitness files (e.g. fitness0.txt) before you run


crucial files:
obj.xml
mutate.py
functions.py
evolution.py

Run the file : evolution.py

(For inidividual file run, modify the file name in script.py, run script.py)
(To check all models in rendered view, uncomment "viewer.render()" in View() in functions.py)

First, it will procedually generate 10 randomized creatures based on the initial creature (obj.xml)
These 10 creatures will be saved in new_creature(1-10).xml

The one creature with the highest fitness score will be selected and duplicated for population
Then, population will go over 5 rounds of evolution
Round 1~2: Evolve randomly with two of the mutations
Round 3~5: Evolve randomly with all kinds of mutations

Select the best creature each round for the next population for evolution
The best creature with highest fitness score will be updated in the fitness file
The last round will also be evaluated, eventhough there will be no duplication afterwards

Randomization:
Randomize main body shape, size
Randomize legs shape, size

Fitness Function:
Efficiency of the movement:
Absolute Dist(start to end) / Total Dist Moved

Mutation Functions:
MutateWeightMass: Add a weightmass of random mass deviated from the center of the mass of the main body

MutateExtendShank: Extend two shank parts on the same side with random coefficient

MutateMass: Modify the mass of the mainbody evenly to a random value

MutateTail: Add a tail with random mass and random angle range of the hinge to the mainbody 


