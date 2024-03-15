# CS496_AlifeRepo
Northwestern CS496 Artificial Life Repository

Delete the following files before you run:
fitness.txt fitness0.txt, fitness1.txt, fitness2.txt 
new_creature.xml new_creature(1-5).xml
round1_cr(1-5).xml
round2_cr(1-5).xml

crucial files:
obj.xml
mutate.py
functions.py

Run the file : mutate.py
There will be two rounds of mutation

Firstly, it will automatically randomly generate 5 creatures, each will be under the name "new_creature(1-5).xml"
fitness1.txt will be generated at this part.
fitness1.txt records 5 creatures and their fitness scores at this point

Round1:
Select the best creature and make 5 copies, update the best one to fitness1.txt
For each copy:
    Randomly select from two mutation functions and apply to the copy
Evaluate the fitness score of the 5 copies and write the fitness2.txt

Round2:
Select the best creature and make 5 copies, update the best one to fitness2.txt
For each copy:
    Randomly select from two mutation functions and apply to the copy
Evaluate the fitness score of the 5 copies and write the fitness3.txt