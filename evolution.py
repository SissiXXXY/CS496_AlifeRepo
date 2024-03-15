import math
import random
import xml.etree.ElementTree as ET
import functions

import numpy as np
import mutate

for i in range(1, 11):
    functions.GenerateCreature("object.xml", f"new_creature{i}.xml")
    functions.View(f"new_creature{i}.xml", i, 0)
for r in range(1, 3):
    roundbest = mutate.SelectBest(f"fitness{r-1}.txt", r)
    for j in range(1, 11):
        mutate.MakeCopy(roundbest, f"round{r}_cr{j}.xml")
    for k in range(1, 11):
        funcchoice = random.choice([mutate.MutateWeightMass, mutate.MutateExtendShank])
        funcchoice(f"round{r}_cr{k}.xml")
        functions.View(f"round{r}_cr{k}.xml", k, r)
for p in range(3, 6):
    roundbest = mutate.SelectBest(f"fitness{p-1}.txt", p)
    for j in range(1, 11):
        mutate.MakeCopy(roundbest, f"round{p}_cr{j}.xml")
    for k in range(1, 11):
        funcchoice = random.choice(
            [
                mutate.MutateWeightMass,
                mutate.MutateExtendShank,
                mutate.MutateTail,
                mutate.MutateMass,
            ]
        )
        funcchoice(f"round{p}_cr{k}.xml")
        functions.View(f"round{p}_cr{k}.xml", k, p)

mutate.SelectBest(f"fitness{5}.txt", "Last")
# selectbest = mutate.SelectBest(f"fitness{p}.txt", p)
